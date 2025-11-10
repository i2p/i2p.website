---
title: "Translation Guide"
description: "Help make I2P accessible to users worldwide by translating the router console and website"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Overview

Help make I2P accessible to users around the world by translating the I2P router console and website into your language. Translation is an ongoing process, and contributions of any size are valuable.

## Translation Platform

We use **Transifex** for all I2P translations. This is the easiest and recommended method for both new and experienced translators.

### Getting Started with Transifex

1. **Create an account** at [Transifex](https://www.transifex.com/)
2. **Join the I2P project**: [I2P on Transifex](https://explore.transifex.com/otf/I2P/)
3. **Request to join** your language team (or request a new language if not listed)
4. **Start translating** once approved

### Why Transifex?

- **User-friendly interface** - No technical knowledge required
- **Translation memory** - Suggests translations based on previous work
- **Collaboration** - Work with other translators in your language
- **Quality control** - Review process ensures accuracy
- **Automatic updates** - Changes sync with the development team

## What to Translate

### Router Console (Priority)

The I2P router console is the primary interface users interact with when running I2P. Translating it has the most immediate impact on user experience.

**Key areas to translate:**

- **Main interface** - Navigation, menus, buttons, status messages
- **Configuration pages** - Settings descriptions and options
- **Help documentation** - Built-in help files and tooltips
- **News and updates** - Initial news feed shown to users
- **Error messages** - User-facing error and warning messages
- **Proxy configurations** - HTTP, SOCKS, and tunnel setup pages

All router console translations are managed through Transifex in `.po` (gettext) format.

## Translation Guidelines

### Style and Tone

- **Clear and concise** - I2P deals with technical concepts; keep translations simple
- **Consistent terminology** - Use the same terms throughout (check translation memory)
- **Formal vs. informal** - Follow conventions for your language
- **Preserve formatting** - Keep placeholders like `{0}`, `%s`, `<b>tags</b>` intact

### Technical Considerations

- **Encoding** - Always use UTF-8 encoding
- **Placeholders** - Do not translate variable placeholders (`{0}`, `{1}`, `%s`, etc.)
- **HTML/Markdown** - Preserve HTML tags and Markdown formatting
- **Links** - Keep URLs unchanged unless there's a localized version
- **Abbreviations** - Consider whether to translate or keep original (e.g., "KB/s", "HTTP")

### Testing Your Translations

If you have access to an I2P router:

1. Download the latest translation files from Transifex
2. Place them in your I2P installation
3. Restart the router console
4. Review the translations in context
5. Report any issues or improvements needed

## Getting Help

### Community Support

- **IRC Channel**: `#i2p-dev` on I2P IRC or OFTC
- **Forum**: I2P development forums
- **Transifex Comments**: Ask questions directly on translation strings

### Common Questions

**Q: How often should I translate?**
Translate at your own pace. Even translating a few strings helps. The project is ongoing.

**Q: What if my language isn't listed?**
Request a new language on Transifex. If there's demand, the team will add it.

**Q: Can I translate alone or need a team?**
You can start alone. As more translators join your language, you can collaborate.

**Q: How do I know what needs translation?**
Transifex shows completion percentages and highlights untranslated strings.

**Q: What if I disagree with an existing translation?**
Suggest improvements in Transifex. Reviewers will evaluate changes.

## Advanced: Manual Translation (Optional)

For experienced translators who want direct access to source files:

### Requirements

- **Git** - Version control system
- **POEdit** or text editor - For editing `.po` files
- **Basic command line** knowledge

### Process

1. **Clone the repository**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Find translation files**:
   - Router console: `apps/routerconsole/locale/`
   - Look for `messages_xx.po` (where `xx` is your language code)

3. **Edit translations**:
   - Use POEdit or a text editor
   - Save with UTF-8 encoding

4. **Test locally** (if you have I2P installed)

5. **Submit changes**:
   - Create a merge request on [I2P Git](https://i2pgit.org/)
   - Or share your `.po` file with the development team

**Note**: Most translators should use Transifex. Manual translation is only for those comfortable with Git and development workflows.

## Thank You

Every translation helps make I2P more accessible to users worldwide. Whether you translate a few strings or entire sections, your contribution makes a real difference in helping people protect their privacy online.

**Ready to start?** [Join I2P on Transifex →](https://explore.transifex.com/otf/I2P/)
