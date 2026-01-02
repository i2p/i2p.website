---
title: "Git über I2P"
description: "Git-Clients mit I2P-gehosteten Diensten wie i2pgit.org verbinden"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Das Klonen und Pushen von Repositories innerhalb von I2P verwendet dieselben Git-Befehle, die Sie bereits kennen – Ihr Client verbindet sich einfach über I2P-Tunnel anstatt über TCP/IP. Diese Anleitung führt Sie durch die Einrichtung eines Kontos, die Konfiguration von Tunnels und den Umgang mit langsamen Verbindungen.

> **Schnellstart:** Schreibgeschützter Zugriff funktioniert über den HTTP-Proxy: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Folgen Sie den Schritten unten für SSH-Lese-/Schreibzugriff.

## 1. Konto erstellen

Wähle einen I2P-Git-Dienst aus und registriere dich:

- Innerhalb von I2P: `http://git.idk.i2p`
- Clearnet-Spiegel: `https://i2pgit.org`

Die Registrierung erfordert möglicherweise eine manuelle Genehmigung; prüfen Sie die Landing-Page für Anweisungen. Nach der Genehmigung forken oder erstellen Sie ein Repository, damit Sie etwas zum Testen haben.

## 2. Konfigurieren Sie einen I2PTunnel-Client (SSH)

1. Öffnen Sie die Router-Konsole → **I2PTunnel** und fügen Sie einen neuen **Client** tunnel hinzu.
2. Geben Sie das Ziel (destination) des Dienstes ein (Base32 oder Base64). Für `git.idk.i2p` finden Sie sowohl HTTP- als auch SSH-Ziele auf der Projekt-Startseite.
3. Wählen Sie einen lokalen Port (zum Beispiel `localhost:7442`).
4. Aktivieren Sie Autostart, wenn Sie den tunnel häufig nutzen möchten.

Die Benutzeroberfläche wird den neuen Tunnel bestätigen und seinen Status anzeigen. Wenn er läuft, können SSH-Clients sich mit `127.0.0.1` auf dem gewählten Port verbinden.

## 3. Über SSH klonen

Verwenden Sie den Tunnel-Port mit `GIT_SSH_COMMAND` oder einem SSH-Konfigurationseintrag:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Wenn der erste Versuch fehlschlägt (Tunnel können langsam sein), versuchen Sie einen flachen Klon:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Konfiguriere Git, um alle Branches abzurufen:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Leistungstipps

- Fügen Sie im Tunnel-Editor einen oder zwei Backup-Tunnel hinzu, um die Ausfallsicherheit zu verbessern.
- Für Tests oder Repositories mit geringem Risiko können Sie die Tunnel-Länge auf 1 Hop reduzieren, beachten Sie jedoch den Kompromiss bei der Anonymität.
- Behalten Sie `GIT_SSH_COMMAND` in Ihrer Umgebung bei oder fügen Sie einen Eintrag zu `~/.ssh/config` hinzu:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Dann klonen Sie mit `git clone git@git.i2p:namespace/project.git`.

## 4. Workflow-Vorschläge

Verwenden Sie einen Fork-and-Branch-Workflow, wie er auf GitLab/GitHub üblich ist:

1. Setzen Sie ein Upstream-Remote: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Halten Sie Ihren `master` synchron: `git pull upstream master`
3. Erstellen Sie Feature-Branches für Änderungen: `git checkout -b feature/new-thing`
4. Pushen Sie Branches zu Ihrem Fork: `git push origin feature/new-thing`
5. Reichen Sie einen Merge-Request ein und aktualisieren Sie dann den Master Ihres Forks per Fast-Forward vom Upstream.

## 5. Datenschutz-Hinweise

- Git speichert Commit-Zeitstempel in deiner lokalen Zeitzone. Um UTC-Zeitstempel zu erzwingen:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Verwenden Sie `git utccommit` anstelle von `git commit`, wenn Datenschutz wichtig ist.

- Vermeiden Sie das Einbetten von Clearnet-URLs oder IPs in Commit-Nachrichten oder Repository-Metadaten, wenn Anonymität ein Anliegen ist.

## 6. Fehlerbehebung

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
Für fortgeschrittene Szenarien (Spiegeln externer Repositories, Seeding von Bundles) siehe die ergänzenden Anleitungen: [Git-Bundle-Workflows](/docs/applications/git-bundle/) und [GitLab über I2P hosten](/docs/guides/gitlab/).
