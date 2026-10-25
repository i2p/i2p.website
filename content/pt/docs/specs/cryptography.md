---
title: "Especificação de Criptografia de Baixo Nível"
description: "Detalhes de baixo nível dos algoritmos criptográficos utilizados no I2P"
slug: "cryptography"
aliases:
  - "/pt/how_cryptography"
  - "/pt/how_cryptography/"
category: "Design"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Visão Geral

> **Nota:** Este documento está em sua maioria obsoleto. Consulte os seguintes documentos para as especificações atuais: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Esta página especifica os detalhes de baixo nível da criptografia no I2P.

Existem vários algoritmos criptográficos em uso no I2P. No design original do I2P, havia apenas um de cada tipo - um algoritmo simétrico, um algoritmo assimétrico, um algoritmo de assinatura e um algoritmo de hash. Não havia provisão para adicionar mais algoritmos ou migrar para outros com mais segurança.

Nos últimos anos, adicionamos uma estrutura para suportar múltiplas primitivas e combinações de forma retrocompatível. Numerosos algoritmos de assinatura, com comprimentos variados de chave e assinatura, são definidos por "tipos de assinatura". Esquemas de criptografia ponta a ponta, usando uma combinação de criptografia assimétrica e simétrica, e com comprimentos de chave variados, são definidos por "tipos de criptografia".

Vários protocolos e estruturas de dados no I2P incluem campos para especificar o tipo de assinatura e/ou tipo de criptografia. Esses campos, juntamente com as definições de tipo, definem os comprimentos de chave e assinatura e as primitivas criptográficas necessárias para utilizá-los. As definições dos tipos de assinatura e criptografia estão na [especificação de Estruturas Comuns](/docs/specs/common-structures).

Os protocolos I2P originais NTCP, SSU e ElGamal/AES+SessionTags usam uma combinação de criptografia assimétrica ElGamal e criptografia simétrica AES. Os protocolos mais recentes NTCP2 e ECIES-X25519-AEAD-Ratchet usam uma combinação de troca de chaves X25519 e criptografia simétrica ChaCha20/Poly1305.

- ECIES-X25519-AEAD-Ratchet substituiu ElGamal/AES+SessionTags.
- NTCP2 substituiu NTCP.
- SSU2 substituiu SSU.
- Criação de tunnel X25519 substituiu a criação de tunnel ElGamal.

## Criptografia Assimétrica

O algoritmo de criptografia assimétrica original no I2P é ElGamal. O algoritmo mais recente, usado em vários lugares, é a troca de chaves ECIES X25519 DH.

Estamos no processo de migrar todo o uso de ElGamal para X25519.

NTCP (com ElGamal) foi migrado para NTCP2 (com X25519). ElGamal/AES+SessionTag está sendo migrado para ECIES-X25519-AEAD-Ratchet.

### X25519

Para detalhes do uso de X25519, veja [NTCP2](/docs/specs/ntcp2) e [ECIES](/docs/specs/ecies).

### ElGamal

ElGamal é usado em vários lugares no I2P:

- Para criptografar mensagens TunnelBuild de router para router
- Para criptografia ponta a ponta (destino para destino) como parte do ElGamal/AES+SessionTag usando a chave de criptografia no LeaseSet
- Para criptografia de alguns armazenamentos e consultas do netDb enviados para routers floodfill como parte do ElGamal/AES+SessionTag (destino para router ou router para router).

Utilizamos números primos comuns para criptografia e descriptografia ElGamal de 2048 bits, conforme especificado pelo IETF [RFC-3526](http://tools.ietf.org/html/rfc3526). Atualmente, apenas usamos ElGamal para criptografar o IV e a chave de sessão em um único bloco, seguido pela carga útil criptografada AES usando essa chave e IV.

O ElGamal não criptografado contém:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
O H(data) é o SHA256 dos dados que são criptografados no bloco ElGamal, e é precedido por um byte aleatório diferente de zero. Este byte é realmente aleatório a partir da versão 0.9.28; antes disso era sempre 0xFF. Ele poderia possivelmente ser usado para flags no futuro. Os dados criptografados no bloco podem ter até 222 bytes de comprimento. Como os dados criptografados podem conter um número substancial de zeros se o texto claro for menor que 222 bytes, é recomendado que as camadas superiores preencham o texto claro até 222 bytes com dados aleatórios. Comprimento total: tipicamente 255 bytes.

O ElGamal criptografado contém:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
Cada parte criptografada é precedida por zeros até um tamanho de exatamente 257 bytes. Comprimento total: 514 bytes. No uso típico, as camadas superiores preenchem os dados de texto claro até 222 bytes, resultando em um bloco não criptografado de 255 bytes. Isso é codificado como duas partes criptografadas de 256 bytes, e há um único byte de preenchimento zero antes de cada parte nesta camada.

Veja o código ElGamal [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

O número primo compartilhado é o primo Oakley para chaves de 2048 bits [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
ou como um valor hexadecimal:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
Usando 2 como gerador.

#### Expoente Curto {#exponent}

Embora o tamanho padrão do expoente seja 2048 bits (256 bytes) e a I2P PrivateKey seja de 256 bytes completos, em alguns casos usamos o tamanho curto do expoente de 226 bits (28,25 bytes). Isso deve ser seguro para uso com os primos Oakley [vanOorschot1996] [BENCHMARKS].

Além disso, [Koshiba2004] aparentemente suporta isso, de acordo com este tópico do sci.crypt [SCI.CRYPT]. O restante da PrivateKey é preenchido com zeros.

Antes da versão 0.9.8, todos os routers utilizavam o expoente curto. A partir da versão 0.9.8, routers x86 de 64 bits utilizam um expoente completo de 2048 bits. Todos os routers agora usam o expoente completo, exceto um pequeno número de routers em hardware muito lento, que continuam a usar o expoente curto devido a preocupações sobre a carga do processador. A transição para um expoente mais longo para essas plataformas é um tópico para estudo adicional.

#### Obsolescência

A vulnerabilidade da rede a um ataque ElGamal e o impacto da transição para um comprimento de bits maior devem ser estudados. Pode ser bastante difícil tornar qualquer mudança compatível com versões anteriores.

## Criptografia Simétrica

O algoritmo de criptografia simétrica original no I2P é AES. O algoritmo mais recente, usado em vários lugares, é Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

Estamos no processo de migrar todo o uso de AES para ChaCha20/Poly1305.

NTCP (com AES) foi migrado para NTCP2 (com ChaCha20/Poly1305). ElGamal/AES+SessionTag está sendo migrado para ECIES-X25519-AEAD-Ratchet.

### ChaCha20/Poly1305

Para os detalhes do uso de ChaCha20/Poly1305 veja [NTCP2](/docs/specs/ntcp2) e [ECIES](/docs/specs/ecies).

### AES

AES é usado para criptografia simétrica, em vários casos:

- Para criptografia de transporte SSU (veja seção "Transports") após troca de chaves DH
- Para criptografia ponta-a-ponta (destino-para-destino) como parte do ElGamal/AES+SessionTag
- Para criptografia de alguns armazenamentos e consultas netDb enviados para roteadores floodfill como parte do ElGamal/AES+SessionTag (destino-para-router ou router-para-router).
- Para criptografia de mensagens periódicas de teste de tunnel enviadas do router para ele mesmo, através de seus próprios tunnels.

Usamos AES com chaves de 256 bits e blocos de 128 bits no modo CBC. O padding usado é especificado no IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, seção 8.1 (para tipo de bloco 02)). Neste caso, o padding consiste em octetos gerados pseudoaleatoriamente para coincidir com blocos de 16 bytes. Especificamente, veja o código CBC [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) e a implementação Cryptix AES [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), bem como o padding, encontrado na função ElGamalAESEngine.getPadding [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### Obsolescência

A vulnerabilidade da rede a um ataque AES e o impacto da transição para um comprimento de bits maior deve ser estudado. Pode ser bastante difícil tornar qualquer mudança compatível com versões anteriores.

## Assinaturas {#sig}

Vários algoritmos de assinatura, com diferentes comprimentos de chave e assinatura, são definidos pelos tipos de assinatura. É relativamente fácil adicionar mais tipos de assinatura.

EdDSA-SHA512-Ed25519 é o algoritmo de assinatura padrão atual. DSA, que era o algoritmo original antes de adicionarmos suporte para tipos de assinatura, ainda está em uso na rede.

### DSA

As assinaturas são geradas e verificadas com [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) de 1024 bits (L=1024, N=160), conforme implementado em [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java). DSA foi escolhido porque é muito mais rápido para assinaturas do que ElGamal.

#### SEED

160 bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Contador

```
33
```
#### Número primo DSA (p)

1024 bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### Quociente DSA (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### Gerador DSA (g)

1024 bit:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
A SigningPublicKey tem 1024 bits. A SigningPrivateKey tem 160 bits.

#### Obsolescência

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) recomenda um mínimo de (L=2048, N=224) para uso além de 2010. Isso pode ser mitigado em certa medida pelo "cryptoperiod", ou tempo de vida de uma determinada chave.

O número primo foi escolhido em 2003, e a pessoa que escolheu o número (TheCrypto) atualmente não é mais um desenvolvedor I2P. Como tal, não sabemos se o primo escolhido é um 'primo forte'. Se um primo maior for escolhido para propósitos futuros, este deve ser um primo forte, e documentaremos o processo de construção.

## Novos Algoritmos de Assinatura

A partir da versão 0.9.12, o router suporta algoritmos de assinatura adicionais que são mais seguros que DSA de 1024 bits. O primeiro uso foi para Destinations; o suporte para Router Identities foi adicionado na versão 0.9.16. Destinations existentes não podem ser migrados de assinaturas antigas para novas; no entanto, há suporte para um único tunnel com múltiplos Destinations, e isso fornece uma maneira de mudar para tipos de assinatura mais novos. O tipo de assinatura é codificado no Destination e Router Identity, de forma que novos algoritmos de assinatura ou curvas podem ser adicionados a qualquer momento.

Os tipos de assinatura atualmente suportados são os seguintes:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (não amplamente usado)
- ECDSA-SHA512-P521 (não amplamente usado)
- EdDSA-SHA512-Ed25519 (padrão a partir da versão 0.9.15)
- RedDSA-SHA512-Ed25519 (a partir da versão 0.9.39)

Tipos de assinatura adicionais são usados apenas na camada de aplicação, principalmente para assinar e verificar arquivos su3. Estes tipos de assinatura são os seguintes:

- RSA-SHA256-2048 (não amplamente usado)
- RSA-SHA384-3072 (não amplamente usado)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (desde a versão 0.9.25; não amplamente usado)

### ECDSA

ECDSA usa as curvas padrão NIST e hashes SHA-2 padrão.

Migramos novos destinos para ECDSA-SHA256-P256 no período de lançamento 0.9.16 - 0.9.19. O uso para Router Identities é suportado a partir da versão 0.9.16 e a migração de routers existentes aconteceu em 2015.

### RSA

RSA padrão PKCS#1 v1.5 (RFC 2313) com o expoente público F4 = 65537.

RSA é agora usado para assinar todo o conteúdo confiável fora da banda, incluindo atualizações de router, ressemeadura, plugins e notícias. As assinaturas são incorporadas no formato "su3" [UPDATES]. Chaves de 4096 bits são recomendadas e usadas por todos os signatários conhecidos. RSA não é usado, nem planejado para uso, em quaisquer Destinations na rede ou Router Identities.

### EdDSA 25519

EdDSA padrão usando curva 25519 e hashes SHA-2 padrão de 512 bits.

Suportado a partir da versão 0.9.15.

Destinations e Router Identities foram migrados no final de 2015.

### RedDSA 25519

EdDSA padrão usando curva 25519 e hashes SHA-2 padrão de 512 bits, mas com chaves privadas diferentes e modificações menores na assinatura. Para leaseSets criptografados. Consulte [EncryptedLeaseSet](/docs/specs/encryptedleaseset) e [Red25519](/docs/specs/red25519) para detalhes.

Suportado a partir da versão 0.9.39.

## Hashes

Hashes são usados em algoritmos de assinatura e como chaves no DHT da rede.

Algoritmos de assinatura mais antigos usam SHA1 e SHA256. Algoritmos de assinatura mais recentes usam SHA512. O DHT usa SHA256.

### SHA256

Os hashes DHT dentro do I2P são SHA256 padrão.

#### Obsolescência

A vulnerabilidade da rede a um ataque SHA-256 e o impacto da transição para um hash mais longo deve ser estudado. Pode ser bastante difícil tornar qualquer mudança compatível com versões anteriores.

## Transportes

Na camada de protocolo mais baixa, a comunicação ponto-a-ponto entre routers é protegida pela segurança da camada de transporte.

Conexões NTCP2 usam X25519 Diffie-Hellman e criptografia autenticada ChaCha20/Poly1305.

Os transportes SSU e NTCP obsoleto usam troca de chaves Diffie-Hellman de 256 bytes (2048 bits) usando o mesmo primo compartilhado e gerador especificado acima para ElGamal, seguido por criptografia simétrica AES conforme descrito acima.

SSU está planejado para ser migrado para SSU2 (com X25519 e ChaCha20/Poly1305).

Todos os transportes fornecem sigilo perfeito para frente [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) nos links de transporte.

### Conexões NTCP2 {#tcp}

As conexões NTCP2 usam X25519 Diffie-Hellman e criptografia autenticada ChaCha20/Poly1305, e o framework do protocolo Noise [Noise](https://noiseprotocol.org/noise.html).

Veja a especificação NTCP2 [NTCP2](/docs/specs/ntcp2) para detalhes e referências.

### Conexões UDP {#udp}

SSU (o transporte UDP) criptografa cada pacote com AES256/CBC com um IV explícito e MAC (HMAC-MD5-128) após concordar com uma chave de sessão efêmera através de uma troca Diffie-Hellman de 2048 bits, autenticação estação-a-estação com a chave DSA do outro router, além de cada mensagem de rede ter seu próprio hash para verificação de integridade local.

Consulte a especificação SSU para detalhes.

AVISO - O HMAC-MD5-128 do I2P usado no SSU é aparentemente não-padrão. Aparentemente, uma versão inicial do SSU usava HMAC-SHA256, e depois foi alterado para MD5-128 por razões de desempenho, mas deixou o tamanho do buffer de 32 bytes intacto. Veja HMACGenerator.java e as notas de status de 2005-07-05 para detalhes.

### Conexões NTCP

NTCP não é mais usado, foi substituído pelo NTCP2.

As conexões NTCP eram negociadas com uma implementação Diffie-Hellman de 2048 bits, usando a identidade do router para prosseguir com um acordo station to station, seguido por alguns campos específicos do protocolo criptografados, com todos os dados subsequentes criptografados com AES (como descrito acima). A razão principal para fazer a negociação DH em vez de usar ElGamalAES+SessionTag é que ela fornece 'sigilo futuro (perfeito)' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy), enquanto ElGamalAES+SessionTag não fornece.

## Referências

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Benchmarks do Crypto++, originalmente em http://www.eskimo.com/~weidai/benchmarks.html (agora inativo), recuperado de http://www.archive.org/, datado de 23 de abril de 2008.
- [Common](/docs/specs/common-structures) - Especificação de Estruturas Comuns
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
