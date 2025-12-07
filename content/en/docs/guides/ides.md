---
title: "Using an IDE with I2P"
description: "Set up Eclipse and NetBeans for developing I2P with Gradle and bundled project files"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p>
The main I2P development branch (<code>i2p.i2p</code>) has been set up to enable developers to easily set up two of the commonly-used IDEs for Java development: Eclipse and NetBeans.
</p>

<h2>Eclipse</h2>

<p>
The main I2P development branches (<code>i2p.i2p</code> and branches from it) contain <code>build.gradle</code> to enable the branch to be easily set up in Eclipse.
</p>

<ol>
<li>
Make sure you have a recent version of Eclipse. Anything newer than 2017 should do.
</li>
<li>
Check out the I2P branch into some directory (e.g. <code>$HOME/dev/i2p.i2p</code>).
</li>
<li>
Select "File → Import..." and then under "Gradle" select "Existing Gradle Project".
</li>
<li>
For "Project root directory:" choose the directory that the I2P branch was checked out to.
</li>
<li>
In the "Import Options" dialog, select "Gradle Wrapper" and press Continue.
</li>
<li>
In the "Import Preview" dialog you can review the project structure. Multiple projects should appear under "i2p.i2p". Press "Finish".
</li>
<li>
Done! Your workspace should now contain all projects within the I2P branch, and their build dependencies should be correctly set up.
</li>
</ol>

<h2>NetBeans</h2>

<p>
The main I2P development branches (<code>i2p.i2p</code> and branches from it) contain NetBeans project files.
</p>

<!-- Keep content minimal and close to original; will update later. -->
