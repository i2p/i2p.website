---
title: "Bringen Sie Ihre I2P-Kenntnisse mit verschlüsselten LeaseSets auf das nächste Niveau"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "Es heißt, dass I2P den Schwerpunkt auf Hidden Services (versteckte Dienste) legt; wir untersuchen eine mögliche Interpretation davon."
categories: ["general"]
API_Translate: wahr
---

## Bringen Sie Ihre I2P-Kenntnisse mit verschlüsselten LeaseSets auf das nächste Niveau

Es wurde in der Vergangenheit gesagt, dass I2P die Unterstützung für versteckte Dienste betont, was in vielerlei Hinsicht zutrifft. Allerdings bedeutet das für Nutzer, Entwickler und Administratoren versteckter Dienste nicht immer dasselbe. Verschlüsselte LeaseSets und ihre Anwendungsfälle bieten einen einzigartigen, praktischen Einblick darin, wie I2P versteckte Dienste vielseitiger und einfacher zu verwalten macht und wie I2P auf dem Konzept der versteckten Dienste aufbaut, um für potenziell interessante Anwendungsfälle Sicherheitsvorteile zu bieten.

## Was ist ein LeaseSet?

Wenn Sie einen versteckten Dienst erstellen, veröffentlichen Sie etwas, das "LeaseSet" genannt wird, in der I2P NetDB. Das "LeaseSet" ist, einfach ausgedrückt, das, was andere I2P-Nutzer benötigen, um zu entdecken, "wo" sich Ihr versteckter Dienst im I2P-Netzwerk befindet. Es enthält "Leases", die tunnels identifizieren, über die Ihr versteckter Dienst erreicht werden kann, sowie den öffentlichen Schlüssel Ihrer Destination, mit dem Clients Nachrichten verschlüsseln. Diese Art von verstecktem Dienst ist für jeden erreichbar, der die Adresse hat, was derzeit wahrscheinlich der häufigste Anwendungsfall ist.

Manchmal möchten Sie jedoch nicht, dass Ihre versteckten Dienste für jedermann zugänglich sind. Manche Leute nutzen versteckte Dienste, um auf einen SSH-Server auf einem Heim-PC zuzugreifen oder um ein Netzwerk aus IoT-Geräten zusammenzukoppeln. In solchen Fällen ist es nicht notwendig und kann sogar kontraproduktiv sein, Ihren versteckten Dienst für alle im I2P-Netzwerk zugänglich zu machen. Hier kommen "Encrypted LeaseSets" (verschlüsselte leaseSets) ins Spiel.

## Verschlüsselte LeaseSets: SEHR versteckte Dienste

Verschlüsselte LeaseSets sind LeaseSets, die in verschlüsselter Form in der NetDB veröffentlicht werden, wobei keine der Leases oder öffentlichen Schlüssel sichtbar sind, es sei denn, der Client besitzt die Schlüssel, die erforderlich sind, um das darin enthaltene LeaseSet zu entschlüsseln. Nur Clients, mit denen Sie Schlüssel teilen (für PSK Encrypted LeaseSets), oder die ihre Schlüssel mit Ihnen teilen (für DH Encrypted LeaseSets), werden die Destination sehen können und sonst niemand.

I2P unterstützt mehrere Strategien für verschlüsselte LeaseSets. Um die richtige Wahl zu treffen, sollte man die wichtigsten Merkmale jeder Strategie verstehen. Wenn ein verschlüsseltes LeaseSet die "Pre-Shared Key(PSK)"-Strategie (vorab geteilter Schlüssel) verwendet, generiert der Server einen Schlüssel (oder mehrere), den der Serverbetreiber anschließend mit jedem Client teilt. Dieser Austausch muss selbstverständlich out-of-band (außerhalb des eigentlichen Kanals) erfolgen, zum Beispiel über einen Austausch auf IRC. Diese Variante verschlüsselter LeaseSets ist so ähnlich, als würde man sich mit einem Passwort bei einem WLAN anmelden. Nur meldet man sich hier bei einem versteckten Dienst an.

Wenn ein Encrypted LeaseSet eine Diffie-Hellman-(DH)-Strategie verwendet, werden die Schlüssel stattdessen auf dem Client erzeugt. Wenn sich ein Diffie-Hellman-Client mit einer Destination (Zieladresse) verbindet, die ein Encrypted LeaseSet verwendet, muss er zunächst seine Schlüssel mit dem Serverbetreiber austauschen. Der Serverbetreiber entscheidet dann, ob der DH-Client autorisiert wird. Diese Version von Encrypted LeaseSets ist ähnlich wie SSH mit einer `authorized_keys`-Datei. Mit dem Unterschied, dass Sie sich bei einem Hidden Service (versteckter Dienst) anmelden.

Durch die Verschlüsselung Ihres LeaseSet machen Sie es nicht nur Unbefugten unmöglich, sich mit Ihrer Destination (Zieladresse) zu verbinden, sondern auch unbefugten Besuchern, überhaupt die tatsächliche Destination des I2P Hidden Service herauszufinden. Manche Leser haben wahrscheinlich bereits einen Anwendungsfall für ihr eigenes verschlüsseltes LeaseSet in Betracht gezogen.

## Verwendung verschlüsselter LeaseSets für den sicheren Zugriff auf die Router-Konsole

Als Faustregel gilt: Je detailliertere Informationen ein Dienst über Ihr Gerät abrufen kann, desto gefährlicher ist es, diesen Dienst dem Internet – oder gar einem Hidden-Service-Netzwerk wie I2P – auszusetzen. Wenn Sie einen solchen Dienst dennoch bereitstellen möchten, müssen Sie ihn mit etwas wie einem Passwort schützen; im Fall von I2P könnte eine weitaus gründlichere und sicherere Option ein verschlüsseltes LeaseSet sein.

**Bevor Sie fortfahren, lesen und verstehen Sie bitte, dass Sie die Sicherheit Ihres I2P router kompromittieren, wenn Sie das folgende Verfahren ohne ein Encrypted LeaseSet durchführen. Konfigurieren Sie keinen Zugriff auf Ihre router console über I2P ohne ein Encrypted LeaseSet. Geben Sie außerdem die PSKs für Ihr Encrypted LeaseSet nicht an Geräte weiter, die nicht unter Ihrer Kontrolle stehen.**

Ein solcher Dienst, der sich für die Freigabe über I2P eignet, jedoch NUR mit einem Encrypted LeaseSet, ist die I2P router console selbst. Das Freigeben der I2P router console auf einem Rechner in I2P mit einem Encrypted LeaseSet ermöglicht es einem anderen Rechner mit einem Browser, die entfernte I2P-Instanz zu administrieren. Ich finde das nützlich, um meine regulären I2P-Dienste aus der Ferne zu überwachen. Es könnte auch dazu verwendet werden, einen Server zu überwachen, der langfristig einen Torrent seedet, um auf I2PSnark zuzugreifen.

Auch wenn die Erklärung länger dauert, lässt sich ein verschlüsseltes LeaseSet über die Hidden Services Manager UI einfach einrichten.

## Auf dem "Server"

Beginnen Sie, indem Sie den Hidden Services Manager unter http://127.0.0.1:7657/i2ptunnelmgr öffnen, und scrollen Sie bis zum Ende des Abschnitts mit der Bezeichnung "I2P Hidden Services." Erstellen Sie einen neuen versteckten Dienst mit dem Host "127.0.0.1" und dem Port "7657" mit diesen "Tunnel Cryptography Options" und speichern Sie den versteckten Dienst.

Wählen Sie dann auf der Hauptseite von Hidden Services Manager Ihren neuen tunnel aus. Die Tunnel Cryptography Options sollten jetzt Ihren ersten Pre-Shared Key enthalten. Notieren Sie sich diesen für den nächsten Schritt, zusammen mit der Encrypted Base32 Address für Ihren tunnel.

## Auf dem "Client"

Wechseln Sie nun zum Computer des Clients, der sich mit dem versteckten Dienst verbinden wird, und rufen Sie die Keyring Configuration unter http://127.0.0.1:7657/configkeyring auf, um die Schlüssel von zuvor hinzuzufügen. Fügen Sie zunächst die Base32 vom Server in das Feld mit der Beschriftung: "Full destination, name, Base32, or hash." ein. Als Nächstes fügen Sie den Pre-Shared Key (vorab geteilter Schlüssel) vom Server in das Feld "Encryption Key" ein. Klicken Sie auf Speichern, und Sie sind bereit, den versteckten Dienst sicher mit einem verschlüsselten LeaseSet zu besuchen.

## Jetzt sind Sie bereit, I2P per Fernzugriff zu administrieren

Wie Sie sehen, bietet I2P Administratoren versteckter Dienste einzigartige Möglichkeiten, mit denen sie ihre I2P-Verbindungen von überall auf der Welt sicher verwalten können. Andere Encrypted LeaseSets (verschlüsselte LeaseSets), die ich aus demselben Grund auf demselben Gerät vorhalte, verweisen auf den SSH-Server, die Portainer-Instanz, die ich zur Verwaltung meiner Service-Container nutze, und meine persönliche NextCloud-Instanz. Mit I2P ist wirklich privates, stets erreichbares Selbsthosting ein erreichbares Ziel; tatsächlich halte ich dies für einen Bereich, für den wir aufgrund von Encrypted LeaseSets besonders geeignet sind. Mit ihnen könnte I2P zum Schlüssel für die Absicherung selbstgehosteter Hausautomatisierung werden oder einfach zum Rückgrat eines neuen, privateren Peer-to-Peer-Webs.
