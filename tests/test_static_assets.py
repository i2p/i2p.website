import pytest
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

def get_all_files(root: Path):
    return [p for p in root.glob("**/*") if p.is_file()]

def test_image_references_in_markdown(all_content_files, project_root):
    """
    Validate image references in Markdown files: ![alt](src) and <img src="...">
    """
    broken_images = []
    
    # Regex for markdown image: ![alt](url "title")
    md_img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    # Regex for HTML img tag: <img src="url">
    html_img_pattern = re.compile(r'<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    
    for md_file in all_content_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
            
        refs = []
        for match in md_img_pattern.finditer(content):
            refs.append(match.group(1).split()[0]) # Split to remove title part
            
        for match in html_img_pattern.finditer(content):
            refs.append(match.group(1))
            
        for ref in refs:
            # Clean ref
            ref = ref.strip()
            
            if ref.startswith(("http", "data:")):
                continue
            
            # Resolve ref
            target = None
            if ref.startswith("/"):
                # Ignore legacy/router console links
                if "configservice.jsp" in ref:
                    continue
                # Absolute from site root -> static/ or content/
                # Check static first
                static_target = project_root / "static" / ref.lstrip("/")
                if static_target.exists():
                    continue
                
                # Check content (less common for absolute paths unless using bundles)
                content_target = project_root / "content" / ref.lstrip("/")
                if content_target.exists():
                    continue

                broken_images.append(f"{md_file.relative_to(project_root)} -> {ref}")
            else:
                # Relative to md file
                target = (md_file.parent / ref).resolve()
                if not target.exists():
                    broken_images.append(f"{md_file.relative_to(project_root)} -> {ref}")

    if broken_images:
        pytest.fail(f"Found {len(broken_images)} broken image references in Markdown:\n" + "\n".join(broken_images[:20]))

def test_svg_validation(all_static_files):
    """
    Validate that SVG files are valid XML.
    """
    invalid_svgs = []
    
    for file_path in all_static_files:
        if file_path.suffix.lower() == ".svg":
            try:
                ET.parse(file_path)
            except ET.ParseError as e:
                invalid_svgs.append(f"{file_path.name}: {e}")
            except Exception as e:
                # Some SVGs might have encoding issues or other problems
                invalid_svgs.append(f"{file_path.name}: {e}")

    if invalid_svgs:
        pytest.fail(f"Found {len(invalid_svgs)} invalid SVG files:\n" + "\n".join(invalid_svgs[:20]))

def test_duplicate_filenames(all_static_files):
    """
    Report duplicate filenames in static directory.
    Duplicates might be intentional, but checking for them helps avoid confusion.
    This test currently warns/prints rather than fails, unless strictly required.
    """
    name_map = defaultdict(list)
    for p in all_static_files:
        name_map[p.name].append(p)
        
    duplicates = {name: paths for name, paths in name_map.items() if len(paths) > 1}
    
    if duplicates:
        print(f"\nFound {len(duplicates)} duplicate filenames in static content:")
        count = 0
        for name, paths in duplicates.items():
            # Filter out intentional duplicates if pattern matches?
            # For now just list them.
            paths_str = ", ".join([str(p.parent.name) + "/" + p.name for p in paths])
            print(f"  {name}: {paths_str}")
            count += 1
            if count > 10:
                print("  ... and more")
                break
        # Decide if this should fail test. Usually duplications are bad practice but not fatal.
        # User asked to "Reports duplicate filenames", so printing is likely enough.
        # assert not duplicates # Uncomment to enforce uniqueness
