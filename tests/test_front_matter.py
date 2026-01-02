"""Test content front matter validation.

Tests:
- Check all markdown files have valid front matter
- Verify required fields (date, title, etc.) exist
- Check for YAML syntax errors
"""

from pathlib import Path
from typing import Dict, List

import pytest

from .utils import extract_markdown_front_matter


def get_required_front_matter_by_section(file_path: Path) -> List[str]:
    """Get required front matter fields based on file location."""
    if "blog" in str(file_path):
        return ["title", "date"]
    elif "docs" in str(file_path):
        return ["title"]
    elif file_path.name == "_index.md":
        return ["title"]
    else:
        return []


def test_all_markdown_files_have_front_matter(all_content_files: List[Path]) -> None:
    """Test that all markdown files have front matter."""
    missing_front_matter = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read(100) # Only check the start
        
        # Handle UTF-8 BOM if present
        if content.startswith('\ufeff'):
            content = content[1:]

        if not content.strip().startswith("---"):
            missing_front_matter.append(str(md_file.relative_to(md_file.parent.parent.parent)))

    if missing_front_matter:
        print(f"\n❌ Found {len(missing_front_matter)} files without front matter:")
        for file_path in sorted(missing_front_matter)[:20]:
            print(f"    - {file_path}")
        if len(missing_front_matter) > 20:
            print(f"    ... and {len(missing_front_matter) - 20} more")

        pytest.fail(f"{len(missing_front_matter)} files missing front matter")


def test_front_matter_valid_yaml(all_content_files: List[Path]) -> None:
    """Test that front matter is valid YAML."""
    invalid_yaml = []

    for md_file in all_content_files[:100]:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if content.startswith("---") and not isinstance(front_matter, dict):
            invalid_yaml.append(str(md_file.relative_to(md_file.parent.parent)))

    if invalid_yaml:
        print(f"\n❌ Found {len(invalid_yaml)} files with invalid YAML front matter:")
        for file_path in invalid_yaml:
            print(f"    - {file_path}")

        pytest.fail("Found invalid YAML front matter")


def test_blog_posts_have_date(all_content_files: List[Path]) -> None:
    """Test that blog posts have date field."""
    blog_files = [f for f in all_content_files if "blog" in str(f)]

    missing_date = []

    for md_file in blog_files:
        if md_file.name == "_index.md":
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "date" not in front_matter:
            missing_date.append(str(md_file.relative_to(md_file.parent.parent)))

    if missing_date:
        print(f"\n❌ Found {len(missing_date)} blog posts without date:")
        for file_path in missing_date[:20]:
            print(f"    - {file_path}")
        if len(missing_date) > 20:
            print(f"    ... and {len(missing_date) - 20} more")

        pytest.fail("Blog posts should have date field")


def test_all_files_have_title(all_content_files: List[Path]) -> None:
    """Test that all markdown files have title field."""
    missing_title = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "title" not in front_matter:
            missing_title.append(str(md_file.relative_to(md_file.parent.parent.parent)))

    if missing_title:
        print(f"\n❌ Found {len(missing_title)} files without title:")
        for file_path in sorted(missing_title)[:20]:
            print(f"    - {file_path}")
        if len(missing_title) > 20:
            print(f"    ... and {len(missing_title) - 20} more")

        pytest.fail("Markdown files should have title field")


def test_date_format_valid(all_content_files: List[Path]) -> None:
    """Test that date fields are in valid format."""
    import re

    date_pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\+|-)\d{2}:\d{2})?$"
    )

    invalid_dates = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "date" in front_matter:
            date_str = str(front_matter["date"])

            if not date_pattern.match(date_str):
                invalid_dates.append(
                    (str(md_file.relative_to(md_file.parent.parent)), date_str)
                )

    if invalid_dates:
        print(f"\n❌ Found {len(invalid_dates)} files with invalid date format:")
        for file_path, date_str in invalid_dates[:20]:
            print(f"    - {file_path}: {date_str}")
        if len(invalid_dates) > 20:
            print(f"    ... and {len(invalid_dates) - 20} more")

        pytest.fail("Date fields should be in ISO 8601 format (YYYY-MM-DD)")


def test_draft_flag_consistency(all_content_files: List[Path]) -> None:
    """Test that draft flag is boolean if present."""
    non_boolean_draft = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "draft" in front_matter:
            draft = front_matter["draft"]

            if not isinstance(draft, bool):
                non_boolean_draft.append(
                    (str(md_file.relative_to(md_file.parent.parent)), str(draft))
                )

    if non_boolean_draft:
        print(f"\n⚠️  Found {len(non_boolean_draft)} files with non-boolean draft flag:")
        for file_path, value in non_boolean_draft[:20]:
            print(f"    - {file_path}: {value}")
        if len(non_boolean_draft) > 20:
            print(f"    ... and {len(non_boolean_draft) - 20} more")


def test_description_field(all_content_files: List[Path]) -> None:
    """Test that files have description field for SEO."""
    files_without_description = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "description" not in front_matter or not front_matter["description"]:
            files_without_description.append(
                str(md_file.relative_to(md_file.parent.parent))
            )

    if files_without_description:
        print(f"\n⚠️  Found {len(files_without_description)} files without description:")
        for file_path in files_without_description[:20]:
            print(f"    - {file_path}")
        if len(files_without_description) > 20:
            print(f"    ... and {len(files_without_description) - 20} more")


def test_categories_field_valid(all_content_files: List[Path]) -> None:
    """Test that categories field is a list/array if present."""
    invalid_categories = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "categories" in front_matter:
            categories = front_matter["categories"]

            if not isinstance(categories, list):
                invalid_categories.append(
                    (
                        str(md_file.relative_to(md_file.parent.parent)),
                        type(categories).__name__,
                    )
                )

    if invalid_categories:
        print(
            f"\n❌ Found {len(invalid_categories)} files with invalid categories field:"
        )
        for file_path, type_name in invalid_categories[:20]:
            print(f"    - {file_path}: {type_name} (should be list)")
        if len(invalid_categories) > 20:
            print(f"    ... and {len(invalid_categories) - 20} more")

        pytest.fail("Categories field should be a list/array")


def test_tags_field_valid(all_content_files: List[Path]) -> None:
    """Test that tags field is a list/array if present."""
    invalid_tags = []

    for md_file in all_content_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        if "tags" in front_matter:
            tags = front_matter["tags"]

            if not isinstance(tags, list):
                invalid_tags.append(
                    (
                        str(md_file.relative_to(md_file.parent.parent)),
                        type(tags).__name__,
                    )
                )

    if invalid_tags:
        print(f"\n❌ Found {len(invalid_tags)} files with invalid tags field:")
        for file_path, type_name in invalid_tags[:20]:
            print(f"    - {file_path}: {type_name} (should be list)")
        if len(invalid_tags) > 20:
            print(f"    ... and {len(invalid_tags) - 20} more")

        pytest.fail("Tags field should be a list/array")


def test_front_matter_no_empty_fields(all_content_files: List[Path]) -> None:
    """Test that front matter fields don't have empty string values."""
    empty_fields = []

    for md_file in all_content_files[:50]:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        front_matter = extract_markdown_front_matter(content)

        if not isinstance(front_matter, dict):
            continue

        for key, value in front_matter.items():
            if isinstance(value, str) and value.strip() == "":
                empty_fields.append(
                    (str(md_file.relative_to(md_file.parent.parent)), key)
                )

    if empty_fields:
        print(f"\n⚠️  Found {len(empty_fields)} empty front matter fields:")
        for file_path, key in empty_fields[:20]:
            print(f"    - {file_path}: {key}")
        if len(empty_fields) > 20:
            print(f"    ... and {len(empty_fields) - 20} more")
