# I2P Website Tests

This directory contains comprehensive unit tests for the I2P website.

## Test Suites

### 1. Configuration Validation (`test_config_validation.py`)
- Validates `hugo.toml` TOML syntax
- Validates `data/downloads.yaml` structure and format
- Validates all `i18n/*.toml` files
- Checks version numbers, SHA256 hashes, and required fields

### 2. i18n Consistency (`test_i18n_consistency.py`)
- Verifies all languages have the same translation keys as English
- Reports missing translations per language
- Checks translation coverage percentage
- Validates critical translations

### 3. Link Validation (`test_links.py`)
- Validates internal links in generated HTML
- Validates internal links in markdown files
- Checks for broken anchor links
- Validates image references

### 4. Download Link Verification (`test_downloads.py`)
- Validates URL formats for all download links
- Verifies HTTPS/HTTP/I2P/Tor link protocols
- Checks version consistency
- Validates SHA256 hash formats

### 5. HTML Output Validation (`test_html_output.py`)
- Verifies RSS feeds exist for all languages
- Verifies JSON search indices exist
- Validates HTML structure
- Checks for duplicate element IDs

### 6. Static Asset Validation (`test_static_assets.py`)
- Validates image references in markdown and HTML
- Checks for broken image links
- Validates SVG files
- Reports duplicate filenames

### 7. Front Matter Validation (`test_front_matter.py`)
- Checks all markdown files have valid front matter
- Verifies required fields (date, title, etc.)
- Validates date formats
- Checks categories/tags are lists

## Running Tests

### Prerequisites
- Python 3.11+
- Hugo 0.147.8 or later
- Test dependencies (install with `pip install -r requirements.txt`)

### Quick Test (no Hugo build)
```bash
python -m pytest tests/test_config_validation.py tests/test_downloads.py -v
```

### Full Test Suite (includes Hugo build)
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
python -m pytest tests/test_i18n_consistency.py -v
```

### Run with verbose output
```bash
python -m pytest tests/ -vv --tb=short
```

### Run tests in parallel (faster)
```bash
python -m pytest tests/ -n auto
```

## CI/CD Integration

Tests are automatically run on GitHub Actions when:
- Code is pushed to `main` branch
- Pull requests are created/opened to `main`

Tests will block merges if any test fails.

## Test Failures

If tests fail, you'll see:
- Which test failed
- The assertion that failed
- Detailed error message

Common failure types:
- Missing translation keys
- Broken links
- Invalid configuration values
- Missing required files

## Adding New Tests

1. Create a new test file in `tests/`
2. Import fixtures from `conftest.py`
3. Follow existing test naming conventions (`test_` prefix)
4. Use descriptive test names
5. Add clear error messages

## Notes

- Some tests require Hugo to build the site first (slower)
- Link checking tests can be resource-intensive
- Tests are designed to catch errors before deployment
- Tests use temporary directories for Hugo builds
