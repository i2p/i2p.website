---
title: "Developer Guidelines and Coding Style"
description: "End-to-end guidelines for contributing to I2P: workflow, release cycle, coding style, logging, licensing, and issue handling"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
  - "/en/get-involved/guides/dev-guidelines/"
  - "/get-involved/guides/dev-guidelines/"
  - "/en//get-involved/guides/dev-guidelines"
type: docs
---

Read the [New Developers Guide](/docs/develop/new-developers/) first.

## Basic Guidelines and Coding Style

Most of the following should be common sense for anybody who has worked on open source or in a commercial programming environment. The following applies mostly to the main development branch i2p.i2p. Guidelines for other branches, plugins, and external apps may be substantially different; check with the appropriate developer for guidance.

### Community

- Please don't just write code. If you can, participate in other development activities, including: development discussions and support on IRC and i2pforum.i2p; testing; bug reporting and responses; documentation; code reviews; etc.
- Active devs should be available periodically on IRC `#i2p-dev`. Be aware of the current release cycle. Adhere to release milestones such as feature freeze, tag freeze, and the check-in deadline for a release.

### Release Cycle

The normal release cycle is 10–16 weeks, four releases a year. Following are the approximate deadlines within a typical 13‑week cycle. Actual deadlines for each release are set by the release manager after consultation with the full team.

- 1–2 days after previous release: Check-ins to trunk are allowed.
- 2–3 weeks after previous release: Deadline to propagate major changes from other branches to trunk.
- 4–5 weeks before release: Deadline to request new home page links.
- 3–4 weeks before release: Feature freeze. Deadline for major new features.
- 2–3 weeks before release: Hold project meeting to review new home page link requests, if any.
- 10–14 days before release: String freeze. No more changes to translated (tagged) strings. Push strings to Transifex, announce translation deadline on Transifex.
- 10–14 days before release: Feature deadline. Bug fixes only after this time. No more features, refactoring or cleanup.
- 3–4 days before release: Translation deadline. Pull translations from Transifex and check in.
- 3–4 days before release: Check-in deadline. No check-ins after this time without the permission of the release builder.
- Hours before release: Code review deadline.

### Git

- Have a basic understanding of distributed source control systems, even if you haven't used git before. Ask for help if you need it. Once pushed, check-ins are forever; there is no undo. Please be careful. If you have not used git before, start with baby steps. Check in some small changes and see how it goes.
- Test your changes before checking them in. If you prefer the check-in‑before‑test development model, use your own development branch in your own account, and create an MR once the work is done. Do not break the build. Do not cause regressions. In case you do (it happens), please do not vanish for a long period after you push your change.
- If your change is non-trivial, or you want people to test it and need good test reports to know whether your change was tested or not, add a check-in comment to `history.txt` and increment the build revision in `RouterVersion.java`.
- Do not check in major changes into the main i2p.i2p branch late in the release cycle. If a project will take you more than a couple days, create your own branch in git, in your own account, and do the development there so you do not block releases.
- For big changes (generally speaking, more than 100 lines, or touching more than three files), check it into a new branch on your own GitLab account, create an MR, and assign a reviewer. Assign the MR to yourself. Merge the MR yourself once the reviewer approves it.
- Do not create WIP branches in the main I2P_Developers account (except for i2p.www). WIP belongs in your own account. When the work is done, create an MR. The only branches in the main account should be for true forks, like a point release.
- Do development in a transparent fashion and with the community in mind. Check in often. Check in or merge into the main branch as frequently as possible, given the guidelines above. If you are working on some big project in your own branch/account, let people know so they may follow along and review/test/comment.

### Coding Style

- Coding style throughout most of the code is 4 spaces for indentation. Do not use tabs. Do not reformat code. If your IDE or editor wants to reformat everything, get control of it. In some places, the coding style is different. Use common sense. Emulate the style in the file you are modifying.
- All new public and package-private classes and methods require Javadocs. Add `@since` release-number. Javadocs for new private methods are desirable.
- For any Javadocs added, there must not be any doclint errors or warnings. Run `ant javadoc` with Oracle Java 14 or higher to check. All params must have `@param` lines, all non-void methods must have `@return` lines, all exceptions declared thrown must have `@throws` lines, and no HTML errors.
- Classes in `core/` (i2p.jar) and portions of i2ptunnel are part of our official API. There are several out-of-tree plugins and other applications that rely on this API. Be careful not to make any changes that break compatibility. Don't add methods to the API unless they are of general utility. Javadocs for API methods should be clear and complete. If you add or change the API, also update the documentation on the website (i2p.www branch).
- Tag strings for translation where appropriate, which is true for all UI strings. Don't change existing tagged strings unless really necessary, as it will break existing translations. Do not add or change tagged strings after the tag freeze in the release cycle so that translators have a chance to update before the release.
- Use generics and concurrent classes where possible. I2P is a highly multi-threaded application.
- Be familiar with common Java pitfalls that are caught by FindBugs/SpotBugs. Run `ant findbugs` to learn more.
- Java 8 is required to build and run I2P as of release 0.9.47. Do not use Java 7 or 8 classes or methods in embedded subsystems: addressbook, core, i2ptunnel.jar (non‑UI), mstreaming, router, routerconsole (news only), streaming. These subsystems are used by Android and embedded applications that require only Java 6. All classes must be available in Android API 14. Java 7 language features are acceptable in these subsystems if supported by the current version of the Android SDK and they compile to Java 6‑compatible code.
- Try‑with‑resources cannot be used in embedded subsystems as it requires `java.lang.AutoCloseable` in the runtime, and this is not available until Android API 19 (KitKat 4.4).
- The `java.nio.file` package cannot be used in embedded subsystems as it is not available until Android API 26 (Oreo 8).
- Other than the above limitations, Java 8 classes, methods, and constructs may be used in the following subsystems only: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty‑i2p.jar, jsonrpc, routerconsole (except news), SAM, susidns, susimail, systray.
- Plugin authors may require any minimum Java version via the `plugin.config` file.
- Explicitly convert between primitive types and classes; don't rely on autoboxing/unboxing.
- Don't use `URL`. Use `URI`.
- Don't catch `Exception`. Catch `RuntimeException` and checked exceptions individually.
- Don't use `String.getBytes()` without a UTF‑8 charset argument. You may also use `DataHelper.getUTF8()` or `DataHelper.getASCII()`.
- Always specify a UTF‑8 charset when reading or writing files. The `DataHelper` utilities may be helpful.
- Always specify a locale (for example `Locale.US`) when using `String.toLowerCase()` or `String.toUpperCase()`. Do not use `String.equalsIgnoreCase()`, as a locale cannot be specified.
- Don't use `String.split()`. Use `DataHelper.split()`.
- Don't add code to format dates and times. Use `DataHelper.formatDate()` and `DataHelper.formatTime()`.
- Ensure that `InputStream`s and `OutputStream`s are closed in finally blocks.
- Use `{}` for all `for` and `while` blocks, even if only one line. If you use `{}` for either the `if`, `else`, or `if-else` block, use it for all blocks. Put `} else {` on a single line.
- Specify fields as `final` wherever possible.
- Don't store `I2PAppContext`, `RouterContext`, `Log`, or any other references to router or context items in static fields.
- Don't start threads in constructors. Use `I2PAppThread` instead of `Thread`.

### Logging

The following guidelines apply to the router, webapps, and all plugins.

- For any messages not displayed at the default log level (WARN, INFO, and DEBUG), unless the message is a static string (no concatenation), always use `log.shouldWarn()`, `log.shouldInfo()`, or `log.shouldDebug()` before the log call to avoid unnecessary object churn.
- Log messages that may be displayed at the default log level (ERROR, CRIT, and `logAlways()`) should be brief, clear, and understandable to a non‑technical user. This includes exception reason text that may also be displayed. Consider translating if the error is likely to happen (for example, on form submission errors). Otherwise, translation is not necessary, but it may be helpful to search for and reuse a string that is already tagged for translation elsewhere.
- Log messages not displayed at the default log level (WARN, INFO, and DEBUG) are intended for developer use, and do not have the above requirements. However, WARN messages are available in the Android log tab, and may be of assistance to users debugging issues, so use some care with WARN messages as well.
- INFO and DEBUG log messages should be used sparingly, especially in hot code paths. While useful during development, consider removing them or commenting them out after testing is complete.
- Do not log to stdout or stderr (wrapper log).

### Licenses

- Only check in code that you wrote yourself. Before checking in any code or library JARs from other sources, justify why it is necessary, verify the license is compatible, and obtain approval from the release manager.
- If you do obtain approval to add external code or JARs, and binaries are available in any Debian or Ubuntu package, you must implement build and packaging options to use the external package instead. Checklist of files to modify: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- For any images checked in from external sources, it is your responsibility to first verify the license is compatible. Include the license and source information in the check-in comment.

### Bugs

- Managing issues is everybody's job; please help. Monitor [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) for issues you can help with. Comment on, fix, and close issues if you can.
- New developers should start by fixing issues. When you have a fix, attach your patch to the issue and add the keyword `review-needed`. Do not close the issue until it's been successfully reviewed and you've checked your changes in. Once you've done this smoothly for a couple of tickets, you may follow the normal procedure above.
- Close an issue when you think you've fixed it. We don't have a test department to verify and close tickets. If you aren’t sure you fixed it, close it and add a note saying "I think I fixed it, please test and reopen if it's still broken". Add a comment with the dev build number or revision and set the milestone to the next release.
