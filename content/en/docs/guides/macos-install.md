---
title: "Installing I2P on macOS (The Long Way)"
description: "Step-by-step guide to manually installing I2P and its dependencies on macOS"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## What You'll Need

- A Mac running macOS 10.14 (Mojave) or later
- Administrator access to install applications
- About 15-20 minutes of time
- Internet connection for downloading installers

## Overview

This installation process has four main steps:

1. **Install Java** - Download and install Oracle Java Runtime Environment
2. **Install I2P** - Download and run the I2P installer
3. **Configure I2P App** - Set up the launcher and add to your dock
4. **Configure I2P Bandwidth** - Run the setup wizard to optimize your connection

## Part One: Install Java

I2P requires Java to run. If you already have Java 8 or later installed, you can [skip to Part Two](#part-two-download-and-install-i2p).

### Step 1: Download Java

Visit the [Oracle Java download page](https://www.oracle.com/java/technologies/downloads/) and download the macOS installer for Java 8 or later.

![Download Oracle Java for macOS](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

Locate the downloaded `.dmg` file in your Downloads folder and double-click to open it.

![Open the Java installer](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS may display a security prompt because the installer is from an identified developer. Click **Open** to proceed.

![Give the installer permission to proceed](/images/guides/macos-install/2-jre.png)

### Step 4: Install Java

Click **Install** to begin the Java installation process.

![Start installing Java](/images/guides/macos-install/3-jre.png)

### Step 5: Wait for Installation

The installer will copy files and configure Java on your system. This usually takes 1-2 minutes.

![Wait for the installer to complete](/images/guides/macos-install/4-jre.png)

### Step 6: Installation Complete

When you see the success message, Java is installed! Click **Close** to finish.

![Java installation complete](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Now that Java is installed, you can install the I2P router.

### Step 1: Download I2P

Visit the [Downloads page](/downloads/) and download the **I2P for Unix/Linux/BSD/Solaris** installer (the `.jar` file).

![Download I2P installer](/images/guides/macos-install/0-i2p.png)

### Step 2: Run the Installer

Double-click the downloaded `i2pinstall_X.X.X.jar` file. The installer will launch and ask you to select your preferred language.

![Select your language](/images/guides/macos-install/1-i2p.png)

### Step 3: Welcome Screen

Read the welcome message and click **Next** to continue.

![Installer introduction](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

The installer will display an important notice about updates. I2P updates are **end-to-end signed** and verified, even though this installer itself is unsigned. Click **Next**.

![Important notice about updates](/images/guides/macos-install/3-i2p.png)

### Step 5: License Agreement

Read the I2P license agreement (BSD-style license). Click **Next** to accept.

![License agreement](/images/guides/macos-install/4-i2p.png)

### Step 6: Select Installation Directory

Choose where to install I2P. The default location (`/Applications/i2p`) is recommended. Click **Next**.

![Select installation directory](/images/guides/macos-install/5-i2p.png)

### Step 7: Select Components

Leave all components selected for a complete installation. Click **Next**.

![Select components to install](/images/guides/macos-install/6-i2p.png)

### Step 8: Start Installation

Review your choices and click **Next** to begin installing I2P.

![Start the installation](/images/guides/macos-install/7-i2p.png)

### Step 9: Installing Files

The installer will copy I2P files to your system. This takes about 1-2 minutes.

![Installation in progress](/images/guides/macos-install/8-i2p.png)

### Step 10: Generate Launch Scripts

The installer creates launch scripts for starting I2P.

![Generating launch scripts](/images/guides/macos-install/9-i2p.png)

### Step 11: Installation Shortcuts

The installer offers to create desktop shortcuts and menu entries. Make your selections and click **Next**.

![Create shortcuts](/images/guides/macos-install/10-i2p.png)

### Step 12: Installation Complete

Success! I2P is now installed. Click **Done** to finish.

![Installation complete](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Now let's make I2P easy to launch by adding it to your Applications folder and Dock.

### Step 1: Open Applications Folder

Open Finder and navigate to your **Applications** folder.

![Open the Applications folder](/images/guides/macos-install/0-conf.png)

### Step 2: Find I2P Launcher

Look for the **I2P** folder or the **Start I2P Router** application inside `/Applications/i2p/`.

![Find the I2P launcher](/images/guides/macos-install/1-conf.png)

### Step 3: Add to Dock

Drag the **Start I2P Router** application to your Dock for easy access. You can also create an alias on your desktop.

![Add I2P to your Dock](/images/guides/macos-install/2-conf.png)

**Tip**: Right-click the I2P icon in the Dock and select **Options → Keep in Dock** to make it permanent.

## Part Four: Configure I2P Bandwidth

When you first launch I2P, you'll run through a setup wizard to configure your bandwidth settings. This helps optimize I2P's performance for your connection.

### Step 1: Launch I2P

Click the I2P icon in your Dock (or double-click the launcher). Your default web browser will open to the I2P Router Console.

![I2P Router Console welcome screen](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

The setup wizard will greet you. Click **Next** to begin configuring I2P.

![Setup wizard introduction](/images/guides/macos-install/1-wiz.png)

### Step 3: Language and Theme

Select your preferred **interface language** and choose between **light** or **dark** theme. Click **Next**.

![Select language and theme](/images/guides/macos-install/2-wiz.png)

### Step 4: Bandwidth Test Information

The wizard will explain the bandwidth test. This test connects to the **M-Lab** service to measure your internet speed. Click **Next** to proceed.

![Bandwidth test explanation](/images/guides/macos-install/3-wiz.png)

### Step 5: Run Bandwidth Test

Click **Run Test** to measure your upload and download speeds. The test takes about 30-60 seconds.

![Running the bandwidth test](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Review your test results. I2P will recommend bandwidth settings based on your connection speed.

![Bandwidth test results](/images/guides/macos-install/5-wiz.png)

### Step 7: Configure Bandwidth Sharing

Choose how much bandwidth you want to share with the I2P network:

- **Automatic** (Recommended): I2P manages bandwidth based on your usage
- **Limited**: Set specific upload/download limits
- **Unlimited**: Share as much as possible (for fast connections)

Click **Next** to save your settings.

![Configure bandwidth sharing](/images/guides/macos-install/6-wiz.png)

### Step 8: Configuration Complete

Your I2P router is now configured and running! The router console will show your connection status and allow you to browse I2P sites.

## Getting Started with I2P

Now that I2P is installed and configured, you can:

1. **Browse I2P sites**: Visit the [I2P homepage](http://127.0.0.1:7657/home) to see links to popular I2P services
2. **Configure your browser**: Set up a [browser profile](/docs/guides/browser-config) to access `.i2p` sites
3. **Explore services**: Check out I2P email, forums, file sharing, and more
4. **Monitor your router**: The [console](http://127.0.0.1:7657/console) shows your network status and statistics

### Useful Links

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Configuration**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Address Book**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Bandwidth Settings**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

If you want to change your bandwidth settings or re-configure I2P later, you can re-run the welcome wizard from the Router Console:

1. Go to [I2P Setup Wizard](http://127.0.0.1:7657/welcome)
2. Follow the wizard steps again

## Troubleshooting

### I2P Won't Start

- **Check Java**: Make sure Java is installed by running `java -version` in Terminal
- **Check permissions**: Ensure the I2P folder has the correct permissions
- **Check logs**: Look at `~/.i2p/wrapper.log` for error messages

### Browser Can't Access I2P Sites

- Make sure I2P is running (check the Router Console)
- Configure your browser's proxy settings to use HTTP proxy `127.0.0.1:4444`
- Wait 5-10 minutes after starting for I2P to integrate into the network

### Slow Performance

- Run the bandwidth test again and adjust your settings
- Make sure you're sharing some bandwidth with the network
- Check your connection status in the Router Console

## Uninstalling I2P

To remove I2P from your Mac:

1. Quit the I2P router if it's running
2. Delete the `/Applications/i2p` folder
3. Delete the `~/.i2p` folder (your I2P configuration and data)
4. Remove the I2P icon from your Dock

## Next Steps

- **Join the community**: Visit [i2pforum.net](http://i2pforum.net) or check out I2P on Reddit
- **Learn more**: Read the [I2P documentation](/en/docs) to understand how the network works
- **Get involved**: Consider [contributing to I2P](/en/get-involved) development or running infrastructure

Congratulations! You're now part of the I2P network. Welcome to the invisible internet!

---

