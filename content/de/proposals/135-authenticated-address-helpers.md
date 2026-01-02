---
title: "Authentifizierte Address Helpers"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Offen"
thread: "http://zzz.i2p/topics/2241"
toc: true
---

## Übersicht

Dieser Vorschlag fügt eine Authentifizierungsmechanismus zu Address Helper-URLs hinzu.


## Motivation

Address Helper-URLs sind von Natur aus unsicher. Jeder kann einen Address Helper 
Parameter in einen Link einfügen, sogar für ein Bild, und kann jede beliebige 
Destination in den "i2paddresshelper"-URL-Parameter einfügen. Abhängig von der 
HTTP-Proxy-Implementierung des Benutzers kann diese Hostname/Destination-Zuordnung, 
falls sie sich nicht bereits im Adressbuch befindet, akzeptiert werden, entweder 
mit oder ohne eine Zwischenseite, die der Benutzer akzeptieren muss.


## Design

Vertrauenswürdige Jump-Server und Adressbuch-Registrierungsdienste würden neue 
Address Helper-Links bereitstellen, die Authentifizierungsparameter hinzufügen. 
Die beiden neuen Parameter wären eine Base-64-Signatur und ein "signed-by"-String.

Diese Dienste würden ein öffentliches Schlüsselzertifikat generieren und bereitstellen. 
Dieses Zertifikat wäre zum Herunterladen und zur Aufnahme in HTTP-Proxy-Software verfügbar. 
Benutzer und Softwareentwickler würden entscheiden, ob sie solchen Diensten vertrauen, 
indem sie das Zertifikat einbeziehen.

Beim Auftreffen auf einen Address Helper-Link würde der HTTP-Proxy nach den zusätzlichen 
Authentifizierungsparametern suchen und versuchen, die Signatur zu überprüfen. Bei 
erfolgter Überprüfung würde der Proxy wie zuvor fortfahren, entweder indem er den neuen 
Eintrag akzeptiert oder eine Zwischenseite für den Benutzer anzeigt. Bei fehlerhafter 
Überprüfung könnte der Proxy den Address Helper ablehnen oder dem Benutzer zusätzliche 
Informationen anzeigen.

Falls keine Authentifizierungsparameter vorhanden sind, kann der HTTP-Proxy die Anfrage 
annehmen, ablehnen oder dem Benutzer Informationen präsentieren.

Jump-Dienste würden wie üblich vertraut, jedoch mit dem zusätzlichen Authentifizierungsschritt. 
Address Helper-Links auf anderen Seiten müssten geändert werden.


## Sicherheitsimplikationen

Dieser Vorschlag erhöht die Sicherheit durch Hinzufügung von Authentifizierung durch 
vertrauenswürdige Registrierungs-/Jump-Dienste.


## Spezifikation

Noch zu bestimmen.

Die beiden neuen Parameter könnten i2paddresshelpersig und i2paddresshelpersigner sein?

Akzeptierte Signaturtypen noch zu bestimmen. Wahrscheinlich nicht RSA, da die Base-64-Signaturen 
sehr lang wären.

Signaturalgorithmus: Noch zu bestimmen. Vielleicht nur hostname=b64dest (gleich wie Vorschlag 112 für 
die Registrierungs-Authentifizierung)

Möglicher dritter neuer Parameter: Der Registrierungs-Authentifizierungsstring (der Teil nach dem "#!"), 
der für zusätzliche Überprüfung durch den HTTP-Proxy verwendet werden soll. Jeder "#" im String müsste 
als "&#35;" oder "&num;" escaped sein oder durch ein anderes spezifiziertes (noch zu bestimmendes) 
URL-sicheres Zeichen ersetzt werden.


## Migration

Alte HTTP-Proxys, die die neuen Authentifizierungsparameter nicht unterstützen, würden sie ignorieren 
und an den Webserver weiterleiten, was harmlos sein sollte.

Neue HTTP-Proxys, die optional Authentifizierungsparameter unterstützen, würden auch mit alten 
Address Helper-Links, die sie nicht enthalten, gut funktionieren.

Neue HTTP-Proxys, die Authentifizierungsparameter erfordern, würden alte Address Helper-Links, die 
sie nicht enthalten, nicht zulassen.

Die Richtlinien einer Proxy-Implementierung könnten sich im Laufe eines Migrationszeitraums 
weiterentwickeln.

## Probleme

Ein Webseitenbetreiber könnte keinen Address Helper für seine eigene Seite generieren, da er die 
Signatur eines vertrauenswürdigen Jump-Servers benötigt. Er müsste sie auf dem vertrauenswürdigen 
Server registrieren und die authentifizierte Helper-URL von diesem Server erhalten. Gibt es eine 
Möglichkeit, dass eine Seite eine selbstauthentifizierte Address Helper-URL generiert?

Alternativ könnte der Proxy den Referer für eine Address Helper-Anfrage überprüfen. Wäre der Referer 
vorhanden, enthielte einen b32 und würde der b32 mit der Destination des Helpers übereinstimmen, 
könnte dies als Selbstreferenz erlaubt werden. Andernfalls könnte angenommen werden, dass es sich 
um eine Anfrage eines Dritten handelt, und abgelehnt werden.
