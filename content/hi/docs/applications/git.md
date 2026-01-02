---
title: "I2P पर Git"
description: "I2P-होस्टेड सेवाओं जैसे i2pgit.org से Git क्लाइंट्स को कनेक्ट करना"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

I2P के अंदर repositories को clone और push करने के लिए वही Git commands का उपयोग होता है जिन्हें आप पहले से जानते हैं—आपका client बस TCP/IP के बजाय I2P tunnels के माध्यम से connect करता है। यह गाइड एक account सेट करने, tunnels को configure करने, और धीमे links से निपटने की प्रक्रिया को समझाती है।

> **त्वरित शुरुआत:** केवल-पढ़ने की पहुंच HTTP proxy के माध्यम से काम करती है: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`। SSH read/write पहुंच के लिए नीचे दिए गए चरणों का पालन करें।

## 1. एक खाता बनाएं

एक I2P Git सेवा चुनें और पंजीकरण करें:

- I2P के अंदर: `http://git.idk.i2p`
- Clearnet मिरर: `https://i2pgit.org`

पंजीकरण के लिए मैन्युअल अनुमोदन की आवश्यकता हो सकती है; निर्देशों के लिए लैंडिंग पेज देखें। एक बार अनुमोदित होने के बाद, एक repository को fork करें या बनाएं ताकि आपके पास परीक्षण करने के लिए कुछ हो।

## 2. एक I2PTunnel क्लाइंट (SSH) को कॉन्फ़िगर करें

1. router console → **I2PTunnel** खोलें और एक नया **Client** tunnel जोड़ें।
2. सेवा का destination (Base32 या Base64) दर्ज करें। `git.idk.i2p` के लिए आपको प्रोजेक्ट होम पेज पर HTTP और SSH दोनों destinations मिलेंगे।
3. एक local port चुनें (उदाहरण के लिए `localhost:7442`)।
4. यदि आप tunnel का बार-बार उपयोग करने की योजना बना रहे हैं तो autostart सक्षम करें।

UI नई tunnel की पुष्टि करेगा और इसकी स्थिति दिखाएगा। जब यह चल रहा हो, तो SSH क्लाइंट चुने गए पोर्ट पर `127.0.0.1` से कनेक्ट हो सकते हैं।

## 3. SSH के माध्यम से Clone करें

`GIT_SSH_COMMAND` या SSH config stanza के साथ tunnel port का उपयोग करें:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
यदि पहला प्रयास विफल हो जाता है (tunnels धीमी हो सकती हैं), तो shallow clone का प्रयास करें:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
सभी ब्रांचेस को fetch करने के लिए Git को कॉन्फ़िगर करें:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### प्रदर्शन सुझाव

- लचीलापन बढ़ाने के लिए tunnel editor में एक या दो बैकअप tunnels जोड़ें।
- परीक्षण या कम जोखिम वाले repos के लिए आप tunnel की लंबाई को 1 hop तक कम कर सकते हैं, लेकिन गुमनामी के व्यापार-बंद से सावधान रहें।
- `GIT_SSH_COMMAND` को अपने environment में रखें या `~/.ssh/config` में एक entry जोड़ें:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
फिर `git clone git@git.i2p:namespace/project.git` का उपयोग करके clone करें।

## 4. वर्कफ़्लो सुझाव

GitLab/GitHub पर सामान्य fork-and-branch workflow अपनाएं:

1. एक upstream remote सेट करें: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. अपनी `master` को सिंक में रखें: `git pull upstream master`
3. परिवर्तनों के लिए feature branches बनाएं: `git checkout -b feature/new-thing`
4. branches को अपने fork में push करें: `git push origin feature/new-thing`
5. एक merge request सबमिट करें, फिर अपने fork की master को upstream से fast-forward करें।

## 5. गोपनीयता अनुस्मारक

- Git आपके स्थानीय समयक्षेत्र में commit timestamps को संग्रहीत करता है। UTC timestamps को मजबूर करने के लिए:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
जब गोपनीयता महत्वपूर्ण हो तो `git commit` के बजाय `git utccommit` का उपयोग करें।

- यदि गुमनामी एक चिंता का विषय है तो commit संदेशों या repository मेटाडेटा में clearnet URLs या IPs एम्बेड करने से बचें।

## 6. समस्या निवारण

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
उन्नत परिदृश्यों के लिए (बाहरी repos को mirror करना, bundles को seed करना), साथी गाइड देखें: [Git bundle workflows](/docs/applications/git-bundle/) और [Hosting GitLab over I2P](/docs/guides/gitlab/)।
