---
title: "Git über I2P für Benutzer"
date: 2020-03-06
author: "idk"
description: "Git über I2P"
categories: ["development"]
---

Anleitung zum Einrichten des Git-Zugriffs über einen I2P Tunnel. Dieser Tunnel dient als Zugriffspunkt auf einen einzelnen Git-Dienst in I2P. Er ist Teil der übergreifenden Bemühungen, I2P von monotone auf Git umzustellen.

## Vor allem anderen: Machen Sie sich mit den Möglichkeiten vertraut, die der Dienst der Öffentlichkeit bietet

Je nachdem, wie der Git-Dienst konfiguriert ist, werden eventuell nicht alle Dienste unter derselben Adresse angeboten. Im Fall von git.idk.i2p gibt es eine öffentliche HTTP-URL und eine SSH-URL, die Sie in Ihrem Git-SSH-Client konfigurieren. Beide können für Push und Pull verwendet werden, SSH wird jedoch empfohlen.

## Zuerst: Richte ein Konto bei einem Git-Dienst ein

Um Ihre Repositories auf einem Remote-Git-Dienst anzulegen, registrieren Sie sich dort für ein Benutzerkonto. Natürlich ist es auch möglich, Repositories lokal anzulegen und sie zu einem Remote-Git-Dienst zu pushen, aber die meisten erfordern ein Konto und dass Sie auf dem Server einen Platz für das Repository anlegen.

## Zweitens: Erstellen Sie ein Projekt zum Testen

To make sure the setup process works, it helps to make a repository to test with from the server. Browse to the i2p-hackers/i2p.i2p repository and fork it to your account.

## Drittens: Richten Sie Ihren git client tunnel ein

Um Lese-/Schreibzugriff auf einen Server zu haben, müssen Sie einen tunnel für Ihren SSH-Client einrichten. Wenn Sie nur HTTP/S-Klonen mit Lesezugriff benötigen, können Sie das alles überspringen und einfach die Umgebungsvariable http_proxy verwenden, um git so zu konfigurieren, dass es den vorkonfigurierten I2P HTTP Proxy verwendet. Zum Beispiel:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Für SSH-Zugriff starten Sie den "New Tunnel Wizard" unter http://127.0.0.1:7657/i2ptunnelmgr und richten Sie einen Client tunnel ein, der auf die SSH-Base32-Adresse des Git-Dienstes zeigt.

## Fourth: Attempt a clone

Jetzt, da dein tunnel vollständig eingerichtet ist, kannst du versuchen, per SSH zu klonen:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Es kann vorkommen, dass ein Fehler auftritt, bei dem die Gegenstelle die Verbindung unerwartet trennt. Leider unterstützt git weiterhin kein wiederaufnehmbares Klonen. Bis es das tut, gibt es ein paar recht einfache Möglichkeiten, damit umzugehen. Die erste und einfachste besteht darin, zu versuchen, in geringer Tiefe zu klonen (shallow clone):

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Sobald Sie einen flachen Klon durchgeführt haben, können Sie den Rest wiederaufnehmbar abrufen, indem Sie in das Repository-Verzeichnis wechseln und Folgendes ausführen:

```
git fetch --unshallow
```
An diesem Punkt hast du noch nicht alle deine Branches. Du kannst sie erhalten, indem du Folgendes ausführst:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Empfohlener Arbeitsablauf für Entwickler

Versionsverwaltung funktioniert am besten, wenn Sie sie richtig einsetzen! Wir empfehlen nachdrücklich einen Fork-First-Feature-Branch-Workflow:

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```