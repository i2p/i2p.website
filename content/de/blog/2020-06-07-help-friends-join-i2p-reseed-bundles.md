---
title: "Helfen Sie Ihren Freunden, I2P beizutreten, indem Sie Reseed-Bündel teilen"
date: 2020-06-07
author: "idk"
description: "Reseed-Bundles erstellen, austauschen und verwenden"
categories: ["reseed"]
---

Die meisten neuen I2P router treten dem Netzwerk durch Bootstrapping mit Hilfe eines Reseed-Dienstes bei. Allerdings sind Reseed-Dienste zentralisiert und vergleichsweise leicht zu blockieren, wenn man die Betonung auf dezentralisierte und nicht blockierbare Verbindungen im restlichen I2P-Netzwerk berücksichtigt. Wenn ein neuer I2P router nicht in der Lage ist zu bootstrappen, kann möglicherweise ein vorhandener I2P router verwendet werden, um ein funktionsfähiges "Reseed bundle" zu erzeugen und ohne einen Reseed-Dienst zu bootstrappen.

Es ist möglich, dass ein Benutzer mit einer funktionierenden I2P-Verbindung einem blockierten router beim Beitritt zum Netzwerk hilft, indem er eine Reseed-Datei erzeugt und sie über einen geheimen oder nicht blockierten Kanal übermittelt. Tatsächlich ist in vielen Fällen ein bereits verbundener I2P router von Reseed-Blockierung überhaupt nicht betroffen, sodass **funktionierende I2P routers zur Verfügung zu haben bedeutet, dass bestehende I2P routers neuen I2P routers helfen können, indem sie ihnen einen versteckten Weg zum Bootstrapping bereitstellen**.

## Erstellen eines Reseed-Bundles

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Reseed (Initialbefüllung der netDb) aus einer Datei durchführen

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
