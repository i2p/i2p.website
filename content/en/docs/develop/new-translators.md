---
title: "New Translator's Guide"
description: "How to contribute translations to the I2P website and router console using Transifex or manual methods"
slug: "new-translators"
lastUpdated: "2025-10"
aliases:
  - "/en/get-involved/guides/new-translators/"
  - "/get-involved/guides/new-translators/"
type: docs
---

Want to help make I2P accessible to more people around the world? Translation is one of the most valuable contributions you can make to the project. This guide will walk you through translating the router console.

## Translation Methods

There are two ways to contribute translations:

### Method 1: Transifex (Recommended)

**This is the easiest way to translate I2P.** Transifex provides a web-based interface that makes translation simple and accessible.

1. Sign up at [Transifex](https://www.transifex.com/otf/I2P/)
2. Request to join the I2P translation team
3. Start translating directly in your browser

No technical knowledge required - just sign up and start translating!

### Method 2: Manual Translation

For translators who prefer working with git and local files, or for languages not yet set up on Transifex.

**Requirements:**
- Familiarity with git version control
- Text editor or translation tool (POEdit recommended)
- Command-line tools: git, gettext

**Setup:**
1. Join [#i2p-dev on IRC](/contact/#irc) and introduce yourself
2. Update translation status on the wiki (ask in IRC for access)
3. Clone the appropriate repository (see sections below)

---

## Router Console Translation

The router console is the web interface you see when running I2P. Translating it helps users who aren't comfortable with English.

### Using Transifex (Recommended)

1. Go to [I2P on Transifex](https://www.transifex.com/otf/I2P/)
2. Select the router console project
3. Choose your language
4. Start translating

### Manual Router Console Translation

**Prerequisites:**
- Same as website translation (git, gettext)
- GPG key (for commit access)
- Signed developer agreement

**Clone the main I2P repository:**
```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```

**Files to translate:**

The router console has approximately 15 files that need translation:

1. **Core interface files:**
   - `apps/routerconsole/locale/messages_*.po` - Main console messages
   - `apps/routerconsole/locale-news/messages_*.po` - News messages

2. **Proxy files:**
   - `apps/i2ptunnel/locale/messages_*.po` - Tunnel configuration interface

3. **Application locales:**
   - `apps/susidns/locale/messages_*.po` - Address book interface
   - `apps/susimail/locale/messages_*.po` - Email interface
   - Other app-specific locale directories

4. **Documentation files:**
   - `installer/resources/readme/readme_*.html` - Installation readme
   - Help files in various apps

**Translation workflow:**
```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```

**Submit your work:**
- Create merge request on [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- Or share files with the development team on IRC

---

## Translation Tools

### POEdit (Highly Recommended)

[POEdit](https://poedit.net/) is a specialized editor for .po translation files.

**Features:**
- Visual interface for translation work
- Shows translation context
- Automatic validation
- Available for Windows, macOS, and Linux

### Text Editors

You can also use any text editor:
- VS Code (with i18n extensions)
- Sublime Text
- vim/emacs (for terminal users)

### Quality Checks

Before submitting:
1. **Check for formatting:** Ensure placeholders like `%s` and `{0}` remain unchanged
2. **Test your translations:** Install and run I2P to see how they look
3. **Consistency:** Keep terminology consistent across files
4. **Length:** Some strings have space constraints in the UI

---

## Tips for Translators

### General Guidelines

- **Stay consistent:** Use the same translations for common terms throughout
- **Keep formatting:** Preserve HTML tags, placeholders (`%s`, `{0}`), and line breaks
- **Context matters:** Read the source English carefully to understand context
- **Ask questions:** Use IRC or forums if something is unclear

### Common I2P Terms

Some terms should remain in English or be transliterated carefully:

- **I2P** - Keep as is
- **eepsite** - I2P website (may require explanation in your language)
- **tunnel** - Connection path (avoid Tor terminology like "circuit")
- **netDb** - Network database
- **floodfill** - Type of router
- **destination** - I2P address endpoint

### Testing Your Translations

1. Build I2P with your translations
2. Change language in router console settings
3. Navigate through all pages to check:
   - Text fits in UI elements
   - No garbled characters (encoding issues)
   - Translations make sense in context

---

## Frequently Asked Questions

### Why is the translation process so complex?

The process uses version control (git) and standard translation tools (.po files) because:

1. **Accountability:** Track who changed what and when
2. **Quality:** Review changes before they go live
3. **Consistency:** Maintain proper file formatting and structure
4. **Scalability:** Manage translations across multiple languages efficiently
5. **Collaboration:** Multiple translators can work on the same language

### Do I need programming skills?

**No!** If you use Transifex, you only need:
- Fluency in both English and your target language
- A web browser
- Basic computer skills

For manual translation, you'll need basic command-line knowledge, but no coding is required.

### How long does it take?

- **Router console:** Approximately 15-20 hours for all files
- **Maintenance:** A few hours per month to update new strings

### Can multiple people work on one language?

Yes! Coordination is key:
- Use Transifex for automatic coordination
- For manual work, communicate in #i2p-dev IRC channel
- Divide work by sections or files

### What if my language isn't listed?

Request it on Transifex or contact the team on IRC. The development team can set up a new language quickly.

### How do I test my translations before submitting?

- Build I2P from source with your translations
- Install and run it locally
- Change language in console settings

---

## Getting Help

### IRC Support

Join [#i2p-dev on IRC](/contact/#irc) for:
- Technical help with translation tools
- Questions about I2P terminology
- Coordination with other translators
- Direct support from developers

### Forums

- Translation discussions on [I2P Forums](http://i2pforum.net/)
- Inside I2P: Translation forum on zzz.i2p (requires I2P router)

### Documentation

- [Transifex Documentation](https://docs.transifex.com/)
- [POEdit Documentation](https://poedit.net/support)
- [gettext Manual](https://www.gnu.org/software/gettext/manual/)

---

## Recognition

All translators are credited in:
- The I2P router console (About page)
- Website credits page
- Git commit history
- Release announcements

Your work directly helps people around the world use I2P safely and privately. Thank you for contributing!

---

## Next Steps

Ready to start translating?

1. **Choose your method:**
   - Quick start: [Sign up on Transifex](https://www.transifex.com/otf/I2P/)
   - Manual approach: Join [#i2p-dev on IRC](/contact/#irc)

2. **Start small:** Translate a few strings to get familiar with the process

3. **Ask for help:** Don't hesitate to reach out on IRC or forums

**Thank you for helping make I2P accessible to everyone!**
