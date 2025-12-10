---
title: "Poll Test Page"
date: 2025-01-27
draft: false
---

# Poll Modal Test Page

This is a test page for the CSS-only poll modal implementation.

## Test the Poll Modal

Click the link below to open the poll modal (Poll ID: 2):

**[Open Poll Modal](#poll)**

## How it works

- The modal uses CSS `:target` pseudo-class (no JavaScript for modal logic)
- The poll widget is server-rendered HTML loaded in an iframe
- Voting is handled via form POST (no JavaScript required)
- Network detection (I2P/Tor/clearnet) is handled by a minimal script that only sets the iframe URL

## Testing Checklist

- [ ] Click the link above - modal should open
- [ ] Click the X button or click outside modal - modal should close
- [ ] Try voting - form should submit and show results
- [ ] Check that results display correctly after voting
- [ ] Verify cookie is set to prevent duplicate votes

