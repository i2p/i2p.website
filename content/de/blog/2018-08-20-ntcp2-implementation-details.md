---
title: "NTCP2-Implementierungsdetails"
date: 2018-08-20
author: "villain"
description: "Implementierungsdetails und technische Spezifikationen des neuen I2P-Transportprotokolls"
categories: ["development"]
---

Die Transportprotokolle von I2P wurden ursprünglich vor etwa 15 Jahren entwickelt. Damals bestand das Hauptziel darin, die übertragenen Daten zu verbergen, nicht die Tatsache, dass man das Protokoll selbst verwendete. Niemand dachte ernsthaft über Schutzmaßnahmen gegen DPI (Deep Packet Inspection) und Zensur von Protokollen nach. Die Zeiten ändern sich, und obwohl die ursprünglichen Transportprotokolle weiterhin starke Sicherheit bieten, gab es eine Nachfrage nach einem neuen Transportprotokoll. NTCP2 ist so konzipiert, dass es aktuellen Zensurbedrohungen standhält. Vor allem der DPI-Analyse von Paketlängen. Außerdem verwendet das neue Protokoll die modernsten Entwicklungen der Kryptografie. NTCP2 basiert auf dem [Noise Protocol Framework](https://noiseprotocol.org/noise.html), mit SHA256 als Hashfunktion und x25519 für einen Diffie-Hellman-(DH)-Schlüsselaustausch über elliptische Kurven.

Die vollständige Spezifikation des NTCP2-Protokolls ist [hier zu finden](/docs/specs/ntcp2/).

## Neue Kryptografie

NTCP2 erfordert das Hinzufügen der folgenden kryptografischen Algorithmen zu einer I2P-Implementierung:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

Im Vergleich zu unserem ursprünglichen Protokoll NTCP verwendet NTCP2 x25519 statt ElGamal für die DH-Funktion, AEAD/Chaha20/Poly1305 statt AES-256-CBC/Adler32 und verwendet SipHash zur Verschleierung der Längeninformation des Pakets. Die in NTCP2 verwendete Schlüsselableitungsfunktion ist komplexer und verwendet nun viele HMAC-SHA256-Aufrufe.

*Hinweis zur i2pd-Implementierung (C++): Alle oben genannten Algorithmen, mit Ausnahme von SipHash, sind in OpenSSL 1.1.0 implementiert. SipHash wird in der kommenden Version OpenSSL 1.1.1 hinzugefügt. Zur Kompatibilität mit OpenSSL 1.0.2, das in den meisten aktuellen Systemen verwendet wird, hat der i2pd-Kernentwickler [Jeff Becker](https://github.com/majestrate) eigenständige Implementierungen der fehlenden kryptografischen Algorithmen beigesteuert.*

## RouterInfo-Änderungen

NTCP2 erfordert neben den beiden vorhandenen Schlüsseln (Verschlüsselungs- und Signaturschlüssel) einen dritten Schlüssel (x25519). Er wird statischer Schlüssel genannt und muss zu jeder RouterInfo-Adresse als "s"-Parameter hinzugefügt werden. Er ist sowohl für den NTCP2-Initiator (Alice) als auch den NTCP2-Responder (Bob) erforderlich. Wenn mehr als eine Adresse NTCP2 unterstützt, beispielsweise IPv4 und IPv6, muss "s" für alle identisch sein. Die Adresse von Alice darf ausschließlich den "s"-Parameter enthalten, ohne dass "host" und "port" gesetzt sind. Außerdem ist ein "v"-Parameter erforderlich, der derzeit immer auf "2" gesetzt ist.

Eine NTCP2-Adresse kann entweder als separate NTCP2-Adresse deklariert werden oder als NTCP-Adresse im alten Stil mit zusätzlichen Parametern, wobei sie in diesem Fall sowohl NTCP- als auch NTCP2-Verbindungen akzeptiert. Die Java-I2P-Implementierung verwendet den zweiten Ansatz, i2pd (C++-Implementierung) verwendet den ersten.

Wenn ein Knoten NTCP2-Verbindungen akzeptiert, muss er seine RouterInfo mit dem Parameter "i" veröffentlichen, der als Initialisierungsvektor (IV) für den öffentlichen Verschlüsselungsschlüssel verwendet wird, wenn dieser Knoten neue Verbindungen aufbaut.

## Herstellen einer Verbindung

Um eine Verbindung herzustellen, müssen beide Seiten ephemere x25519-Schlüsselpaare erzeugen. Basierend auf diesen Schlüsseln und auf "statischen" Schlüsseln leiten sie einen Satz von Schlüsseln für die Datenübertragung ab. Beide Parteien müssen prüfen, dass die Gegenseite tatsächlich über einen privaten Schlüssel zu diesem statischen Schlüssel verfügt und dass dieser statische Schlüssel derselbe ist wie in RouterInfo.

Es werden drei Nachrichten gesendet, um eine Verbindung herzustellen:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Ein gemeinsamer x25519-Schlüssel, genannt «input key material» (Eingabeschlüsselmaterial), wird für jede Nachricht berechnet, woraufhin der Schlüssel zur Nachrichtenverschlüsselung mithilfe der MixKey-Funktion erzeugt wird. Ein Wert ck (chaining key, Verkettungsschlüssel) wird während des Nachrichtenaustauschs beibehalten. Dieser Wert wird als abschließende Eingabe verwendet, wenn Schlüssel für die Datenübertragung erzeugt werden.

Die Funktion MixKey sieht in der C++-Implementierung von I2P ungefähr so aus:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
Die **SessionRequest**-Nachricht besteht aus einem öffentlichen x25519-Schlüssel von Alice (32 Byte), einem mit AEAD/Chacha20/Poly1305 verschlüsselten Datenblock (16 Byte), einem Hash (16 Byte) sowie am Ende einigen Zufallsdaten (Padding). Die Länge des Paddings ist im verschlüsselten Datenblock definiert. Der verschlüsselte Block enthält außerdem die Länge des zweiten Teils der **SessionConfirmed**-Nachricht. Der Datenblock wird mit einem Schlüssel verschlüsselt und signiert, der aus Alices ephemerem Schlüssel und Bobs statischem Schlüssel abgeleitet wird. Der anfängliche ck-Wert für die MixKey-Funktion ist auf SHA256 gesetzt (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Da die 32 Bytes des öffentlichen x25519-Schlüssels durch DPI erkannt werden können, wird er mit dem AES-256-CBC-Algorithmus verschlüsselt, wobei der Hash von Bobs Adresse als Schlüssel und der Parameter "i" aus der RouterInfo als Initialisierungsvektor (IV) verwendet wird.

Die **SessionCreated**-Nachricht hat die gleiche Struktur wie **SessionRequest**, außer dass der Schlüssel auf Grundlage der ephemeren Schlüssel beider Seiten berechnet wird. Die IV, die nach dem Ver- bzw. Entschlüsseln des öffentlichen Schlüssels aus der **SessionRequest**-Nachricht erzeugt wird, wird als IV zum Ver- bzw. Entschlüsseln des ephemeren öffentlichen Schlüssels verwendet.

Die Nachricht **SessionConfirmed** hat 2 Teile: einen öffentlichen statischen Schlüssel und die RouterInfo von Alice. Der Unterschied gegenüber den vorherigen Nachrichten ist, dass der ephemere öffentliche Schlüssel mit AEAD/Chaha20/Poly1305 unter Verwendung desselben Schlüssels wie bei **SessionCreated** verschlüsselt wird. Das führt dazu, dass der erste Teil der Nachricht von 32 auf 48 Bytes anwächst. Der zweite Teil wird ebenfalls mit AEAD/Chaha20/Poly1305 verschlüsselt, jedoch mit einem neuen Schlüssel, der aus Bobs ephemerem Schlüssel und Alices statischem Schlüssel berechnet wird. Der RouterInfo-Teil kann außerdem mit zufälligem Daten-Padding aufgefüllt werden, ist jedoch nicht erforderlich, da RouterInfo üblicherweise variable Länge hat.

## Erzeugung von Datenübertragungsschlüsseln

Wenn jede Hash- und Schlüsselüberprüfung erfolgreich war, muss nach der letzten MixKey-Operation auf beiden Seiten ein gemeinsamer ck-Wert vorhanden sein. Dieser Wert wird verwendet, um für jede Seite einer Verbindung zwei Sätze von Schlüsseln <k, sipk, sipiv> zu erzeugen. "k" ist ein AEAD/Chaha20/Poly1305-Schlüssel, "sipk" ist ein SipHash-Schlüssel, "sipiv" ist ein Initialwert für den SipHash IV (Initialisierungsvektor), der nach jeder Verwendung geändert wird.

Der zur Generierung von Schlüsseln verwendete Code sieht in der C++-Implementierung von I2P so aus:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) Implementierungshinweis: Die ersten 16 Bytes des Arrays "sipkeys" bilden einen SipHash-Schlüssel, die letzten 8 Bytes bilden den IV (Initialisierungsvektor). SipHash erfordert zwei 8-Byte-Schlüssel, aber i2pd behandelt sie als einen einzigen 16-Byte-Schlüssel.*

## Data Transferring

Daten werden in Frames übertragen, jedes davon besteht aus drei Teilen:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

Die maximale Länge der in einem Frame übertragenen Daten beträgt 65519 Bytes.

Die Nachrichtenlänge wird verschleiert, indem die XOR-Funktion mit den ersten beiden Bytes des aktuellen SipHash-IVs angewendet wird.

Der verschlüsselte Datenabschnitt enthält Datenblöcke. Jedem Block wird ein 3-Byte-Header vorangestellt, der Blocktyp und Blocklänge definiert. In der Regel werden I2NP-Typ-Blöcke übertragen; dabei handelt es sich um I2NP-Nachrichten mit verändertem Header. Ein NTCP2-Frame kann mehrere I2NP-Blöcke übertragen.

Der andere wichtige Datenblocktyp ist ein zufälliger Datenblock. Es wird empfohlen, jedem NTCP2-Frame einen zufälligen Datenblock hinzuzufügen. Es kann nur ein zufälliger Datenblock hinzugefügt werden, und er muss der letzte Block sein.

Dies sind weitere Datenblöcke, die in der aktuellen NTCP2-Implementierung verwendet werden:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Zusammenfassung

Das neue I2P-Transportprotokoll NTCP2 bietet wirksamen Schutz vor DPI-Zensur. Es führt außerdem zu geringerer CPU-Last aufgrund der verwendeten schnelleren, modernen Kryptografie. Damit ist es wahrscheinlicher, dass I2P auf leistungsschwachen Geräten wie Smartphones und Heimroutern läuft. Beide großen I2P-Implementierungen unterstützen NTCP2 vollständig und stellen NTCP2 ab Version 0.9.36 (Java) bzw. 2.20 (i2pd, C++) zur Verfügung.
