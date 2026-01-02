# I2P Website

The official website for the Invisible Internet Project (I2P), built with [Hugo](https://gohugo.io/).

## Quick Start

```bash
# Clone the repository
git clone https://github.com/i2p/i2p.www.git
cd i2p.www

# Install Hugo (v0.147.8+ required)
# macOS: brew install hugo
# Linux: snap install hugo

# Run development server
hugo server -D

# Build for production
hugo --minify
```

## Project Structure

```
i2p.www/
├── assets/css/          # Main stylesheet (main.css)
├── content/             # Markdown content by language
│   ├── en/              # English (source language)
│   ├── de/              # German
│   ├── es/              # Spanish
│   ├── fr/              # French
│   └── ...              # 13 languages total
├── data/                # Data files (downloads.yaml, etc.)
├── i18n/                # UI translation strings
├── layouts/             # Hugo templates
├── scripts/             # Utility scripts
│   ├── i2p_tools.sh     # Interactive tool menu
│   ├── tools/           # Content management tools
│   └── translate/       # Translation automation
├── static/              # Static assets (images, fonts, etc.)
└── tests/               # Python test suite
```

## Supported Languages

| Code | Language | Status |
|------|----------|--------|
| en | English | Source |
| de | Deutsch | Translated |
| es | Español | Translated |
| fr | Français | Translated |
| ru | Русский | Translated |
| zh | 中文 | Translated |
| ko | 한국어 | Translated |
| ar | العربية | Translated |
| pt | Português | Translated |
| vi | Tiếng Việt | Translated |
| hi | हिन्दी | Translated |
| cs | Čeština | Translated |
| tr | Türkçe | Translated |

## Tools

### Interactive Menu

Run the interactive tools menu:

```bash
./scripts/i2p_tools.sh
```

This provides a menu-driven interface for common tasks:

```
╔════════════════════════════════════════╗
║       I2P Website Tools                ║
╚════════════════════════════════════════╝

What would you like to do?

  1) Update Site Banner
  2) Add Research Paper
  3) Add Media/Press Entry
  4) Exit
```

### Individual Tools

#### Update Site Banner

Updates the notification banner shown at the top of all pages:

```bash
./scripts/tools/update_banner.sh
```

The banner configuration is stored in `hugo.toml` and content in `i18n/*.toml` files.

#### Add Research Paper

Adds a new research paper to the papers section:

```bash
./scripts/tools/add_paper.sh
```

Prompts for paper details (title, authors, year, abstract, PDF URL) and creates entries in all language files.

#### Add Media/Press Entry

Adds a new media mention or press coverage:

```bash
./scripts/tools/add_media.sh
```

### Translation Scripts

Located in `scripts/translate/`:

- `translate_claude_batch.py` - Batch translation using Claude API
- `translate_openai_batch.py` - Batch translation using OpenAI API
- `translate_openai_realtime.py` - Real-time translation using OpenAI
- `ci_translate.sh` - CI/CD translation automation

## Development

### Prerequisites

- Hugo Extended v0.147.8+
- Python 3.11+ (for tests)
- Node.js (optional, for some optimizations)

### Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_links.py

# Run with verbose output
pytest tests/ -v
```

### Test Coverage

- **Config validation** - Hugo configuration integrity
- **Downloads** - Download links and checksums
- **Front matter** - Markdown metadata validation
- **HTML output** - Generated HTML structure
- **i18n consistency** - Translation key completeness
- **Links** - Internal and external link validation
- **Static assets** - Asset file integrity
- **Accessibility** - Basic a11y checks
- **Build performance** - Size and page count metrics
- **Translation completeness** - Cross-language content parity

### Local Development Server

```bash
# Start with drafts enabled
hugo server -D

# Start with specific port
hugo server -p 1314

# Start with live reload disabled
hugo server --disableLiveReload
```

## Deployment

### CI/CD Pipeline

The site uses GitHub Actions for CI/CD:

1. **Build** - Hugo builds the site with minification
2. **Test** - Python test suite validates output
3. **Optimize** - SVG optimization and WebP conversion
4. **Deploy** - Cloudflare Pages deployment

### Manual Build

```bash
# Production build
hugo --minify --gc

# Output is in public/
```

## Configuration

### Site Settings (`hugo.toml`)

Key configuration options:

```toml
# Banner settings
[params.banner]
  enabled = true
  dismissible = true
  id = "banner-3"  # Auto-incremented by i2p_tools.sh

# Poll settings
[params.poll]
  enabled = true
  pollId = "2"
```

> **Note:** Do not manually edit banner or poll settings. Use `./scripts/i2p_tools.sh` which automatically handles ID increments and updates all language files.

### Download Data (`data/downloads.yaml`)

Contains all download links, versions, and checksums for I2P releases.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes
6. Push to the branch (`git push origin feature/my-feature`)
7. Open a Pull Request

### Content Guidelines

- **Only create/edit files in `content/en/`** - English is the source language
- Translations are **automatically generated** by the CI/CD pipeline when new English content is detected
- The pipeline will translate new content and commit it to the repository automatically
- Never manually create or edit files in other language directories (`content/de/`, `content/fr/`, etc.)
- Use frontmatter for metadata (title, description, date)
- Images go in `static/images/`

## License

This project is part of the I2P Project. See [LICENSE](LICENSE) for details.

## Links

- [I2P Website](https://geti2p.net)
- [I2P Documentation](https://geti2p.net/docs)
- [I2P Forum](https://i2pforum.net)
- [Report Issues](https://github.com/i2p/i2p.www/issues)
