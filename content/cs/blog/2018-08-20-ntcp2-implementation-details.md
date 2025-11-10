---
title: "Podrobnosti implementace NTCP2"
date: 2018-08-20
author: "villain"
description: "Podrobnosti implementace nového transportního protokolu I2P a technické specifikace"
categories: ["development"]
---

Transportní protokoly I2P byly původně vyvinuty zhruba před 15 lety. Tehdy byl hlavním cílem skrýt přenášená data, nikoli skrýt, že se protokol vůbec používá. Nikdo vážně neuvažoval o ochraně proti DPI (hluboká inspekce paketů) a cenzuře protokolů. Časy se mění a přestože původní transportní protokoly stále poskytují silné zabezpečení, objevil se požadavek na nový transportní protokol. NTCP2 je navržen tak, aby odolal současným cenzurním hrozbám. Především analýze délky paketů pomocí DPI. Nový protokol navíc využívá nejnovější poznatky v kryptografii. NTCP2 je založen na [Noise Protocol Framework](https://noiseprotocol.org/noise.html), s SHA256 jako hashovací funkcí a x25519 jako výměnou klíčů Diffie-Hellman (DH) na eliptické křivce.

Úplná specifikace protokolu NTCP2 je [k dispozici zde](/docs/specs/ntcp2/).

## Nová kryptografie

NTCP2 vyžaduje přidání následujících kryptografických algoritmů do implementace I2P:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

Ve srovnání s naším původním protokolem NTCP používá NTCP2 x25519 místo ElGamal pro funkci DH, AEAD/Chaha20/Poly1305 místo AES-256-CBC/Adler32 a používá SipHash pro maskování informace o délce paketu. Funkce derivace klíče použitá v NTCP2 je složitější a nyní používá mnoho volání HMAC-SHA256.

*Poznámka k implementaci i2pd (C++): Všechny výše zmíněné algoritmy, s výjimkou SipHash, jsou implementovány v OpenSSL 1.1.0. SipHash bude přidán do nadcházejícího vydání OpenSSL 1.1.1. Pro zajištění kompatibility s OpenSSL 1.0.2, které je používáno ve většině současných systémů, hlavní vývojář projektu i2pd [Jeff Becker](https://github.com/majestrate) přispěl samostatnými implementacemi chybějících kryptografických algoritmů.*

## Změny v RouterInfo

NTCP2 vyžaduje mít třetí klíč (x25519) navíc k dosavadním dvěma klíčům (šifrovacímu a podpisovému). Nazývá se statický klíč a musí být přidán k libovolné adrese v RouterInfo jako parametr "s". Je vyžadován jak u NTCP2 iniciátora (Alice), tak u responderu (Bob). Pokud NTCP2 podporuje více než jedna adresa, například IPv4 a IPv6, musí být parametr "s" u všech stejný. U adresy Alice je dovoleno mít pouze parametr "s" bez nastavených "host" a "port". Dále je vyžadován parametr "v", který je v současnosti vždy nastaven na "2".

Adresa NTCP2 může být deklarována buď jako samostatná adresa NTCP2, nebo jako starší typ adresy NTCP s dodatečnými parametry; v takovém případě bude přijímat jak připojení NTCP, tak NTCP2. Implementace Java I2P používá druhý přístup, i2pd (implementace v C++) používá první.

Pokud uzel přijímá spojení NTCP2, musí zveřejnit své RouterInfo s parametrem "i", který se používá jako inicializační vektor (IV) pro veřejný šifrovací klíč, když tento uzel navazuje nová spojení.

## Navázání spojení

Pro navázání spojení musí obě strany vygenerovat páry efemérních klíčů x25519. Na základě těchto klíčů a „statických“ klíčů odvozují sadu klíčů pro přenos dat. Obě strany musí ověřit, že druhá strana skutečně vlastní soukromý klíč odpovídající tomuto statickému klíči a že tento statický klíč je shodný s tím, který je v RouterInfo.

K navázání spojení se odesílají tři zprávy:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Společný klíč x25519, nazývaný «input key material», se vypočítá pro každou zprávu, poté se klíč pro šifrování zprávy vygeneruje funkcí MixKey. Hodnota ck (chaining key – řetězový klíč) se uchovává po dobu výměny zpráv. Tato hodnota se použije jako konečný vstup při generování klíčů pro přenos dat.

Funkce MixKey vypadá přibližně takto v implementaci I2P v C++:

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
**SessionRequest** message is made of a public x25519 Alice key (32 bytes), a block of data encrypted with AEAD/Chacha20/Poly1305 (16 bytes), a hash (16 bytes) and some random data in the end (padding). Padding length is defined in the encrypted block of data. Encrypted block also contains length of the second part of the **SessionConfirmed** message. A block of data is encrypted and signed with a key derived from Alice's ephemeral key and Bob's static key. Initial ck value for MixKey function is set to SHA256 (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Protože 32 bajtů veřejného klíče x25519 může být detekováno pomocí DPI, je šifrováno algoritmem AES-256-CBC s použitím hashe Bobovy adresy jako klíče a parametru "i" z RouterInfo jako inicializačního vektoru (IV).

Zpráva **SessionCreated** má stejnou strukturu jako **SessionRequest**, pouze klíč je vypočten na základě efemérních klíčů obou stran. IV (inicializační vektor) vytvořený po zašifrování/dešifrování veřejného klíče ze zprávy **SessionRequest** se použije jako IV pro šifrování/dešifrování efemérního veřejného klíče.

Zpráva **SessionConfirmed** má 2 části: veřejný statický klíč a Alicin RouterInfo (informace o routeru). Rozdíl oproti předchozím zprávám je v tom, že efemérní veřejný klíč je šifrován pomocí AEAD/Chaha20/Poly1305 se stejným klíčem jako **SessionCreated**. To vede ke zvětšení první části zprávy ze 32 na 48 bajtů. Druhá část je také šifrována pomocí AEAD/Chaha20/Poly1305, ale s použitím nového klíče, vypočteného z Bobova efemérního klíče a Aličina statického klíče. Část RouterInfo lze také doplnit náhodnou datovou výplní, ale není to nutné, protože RouterInfo má obvykle různou délku.

## Generování klíčů pro přenos dat

If every hash and key verification has succeeded, a common ck value must be present after the last MixKey operation on both sides. This value is used to generate two sets of keys <k, sipk, sipiv> for each side of a connection. "k" is a AEAD/Chaha20/Poly1305 key, "sipk" is a SipHash key, "sipiv" is an initial value for SipHash IV, that is changed after each use.

Kód použitý ke generování klíčů vypadá takto v implementaci I2P v jazyce C++:

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
*Poznámka k implementaci i2pd (C++): Prvních 16 bajtů pole "sipkeys" tvoří klíč pro SipHash, posledních 8 bajtů tvoří IV (inicializační vektor). SipHash vyžaduje dva klíče po 8 bajtech, ale i2pd je zpracovává jako jediný klíč o délce 16 bajtů.*

## Přenášení dat

Data jsou přenášena v rámcích, každý rámec má 3 části:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

Maximální velikost dat přenesených v jednom rámci je 65519 bajtů.

Délka zprávy je zamaskována aplikací funkce XOR s prvními dvěma bajty aktuálního SipHash IV (inicializační vektor).

Šifrovaná část dat obsahuje bloky dat. Každému bloku předchází 3bajtová hlavička, která určuje typ bloku a jeho délku. Obvykle se přenášejí bloky typu I2NP, což jsou zprávy I2NP se změněnou hlavičkou. Jeden rámec NTCP2 může přenášet více bloků I2NP.

Dalším důležitým typem datového bloku je náhodný datový blok. Doporučuje se přidat náhodný datový blok do každého rámce NTCP2. Lze přidat pouze jeden náhodný datový blok a musí být poslední.

To jsou další datové bloky používané v aktuální implementaci NTCP2:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Shrnutí

Nový transportní protokol I2P NTCP2 poskytuje účinnou odolnost proti cenzuře založené na DPI. Zároveň snižuje zátěž CPU díky rychlejší, moderní kryptografii, kterou používá. Díky tomu je pravděpodobnější, že I2P poběží i na méně výkonných zařízeních, jako jsou chytré telefony a domácí routery. Obě hlavní implementace I2P mají plnou podporu pro NTCP2 a zpřístupňují NTCP2 k použití počínaje verzí 0.9.36 (Java) a 2.20 (i2pd, C++).
