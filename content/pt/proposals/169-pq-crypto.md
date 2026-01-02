---
title: "Protocolos Criptográficos Pós-Quânticos"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Aberto"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Visão Geral

Embora a pesquisa e competição por criptografia pós-quântica (PQ) adequada tenham estado em andamento por uma década, as escolhas não se tornaram claras até recentemente.

Começamos a analisar as implicações da criptografia PQ em 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Os padrões TLS adicionaram suporte para criptografia híbrida nos últimos dois anos e agora é usado para uma porção significativa do tráfego criptografado na internet devido ao suporte no Chrome e Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

O NIST finalizou e publicou recentemente os algoritmos recomendados para criptografia pós-quântica [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Várias bibliotecas de criptografia comuns agora suportam os padrões NIST ou irão lançar suporte em um futuro próximo.

Tanto [Cloudflare](https://blog.cloudflare.com/pq-2024/) quanto [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recomendam que a migração comece imediatamente. Veja também o FAQ PQ da NSA de 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). O I2P deve ser líder em segurança e criptografia. Agora é o momento de implementar os algoritmos recomendados. Usando nosso sistema flexível de tipos de criptografia e tipos de assinatura, adicionaremos tipos para criptografia híbrida, e para assinaturas PQ e híbridas.

## Objetivos

- Selecionar algoritmos resistentes ao PQ
- Adicionar algoritmos apenas PQ e híbridos aos protocolos I2P onde apropriado
- Definir múltiplas variantes
- Selecionar as melhores variantes após implementação, testes, análise e pesquisa
- Adicionar suporte incrementalmente e com compatibilidade retroativa

## Não-Objetivos

- Não altere protocolos de criptografia unidirecional (Noise N)
- Não abandone o SHA256, não ameaçado a curto prazo por PQ
- Não selecione as variantes preferidas finais neste momento

## Modelo de Ameaças

- Routers no OBEP ou IBGW, possivelmente em conluio,
  armazenando mensagens garlic para descriptografia posterior (forward secrecy)
- Observadores de rede
  armazenando mensagens de transporte para descriptografia posterior (forward secrecy)
- Participantes da rede falsificando assinaturas para RI, LS, streaming, datagramas,
  ou outras estruturas

## Protocolos Afetados

Modificaremos os seguintes protocolos, aproximadamente na ordem de desenvolvimento. A implementação geral provavelmente será do final de 2025 até meados de 2027. Consulte a seção Prioridades e Implementação abaixo para detalhes.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Design

Daremos suporte aos padrões NIST FIPS 203 e 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) que são baseados em, mas NÃO compatíveis com, CRYSTALS-Kyber e CRYSTALS-Dilithium (versões 3.1, 3 e anteriores).

### Key Exchange

Ofereceremos suporte ao intercâmbio híbrido de chaves nos seguintes protocolos:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM fornece apenas chaves efêmeras e não suporta diretamente handshakes de chave estática como Noise XK e IK.

Noise N não usa uma troca de chaves bidirecional e, portanto, não é adequado para criptografia híbrida.

Portanto, suportaremos apenas criptografia híbrida, para NTCP2, SSU2 e Ratchet. Definiremos as três variantes ML-KEM como em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), para um total de 3 novos tipos de criptografia. Os tipos híbridos serão definidos apenas em combinação com X25519.

Os novos tipos de criptografia são:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
O overhead será substancial. Os tamanhos típicos de mensagem 1 e 2 (para XK e IK) atualmente são de cerca de 100 bytes (antes de qualquer payload adicional). Isso aumentará de 8x a 15x dependendo do algoritmo.

### Signatures

Apoiaremos assinaturas PQ e híbridas nas seguintes estruturas:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Portanto, suportaremos tanto assinaturas apenas PQ quanto híbridas. Definiremos as três variantes ML-DSA conforme em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), três variantes híbridas com Ed25519, e três variantes apenas PQ com prehash apenas para arquivos SU3, totalizando 9 novos tipos de assinatura. Tipos híbridos serão definidos apenas em combinação com Ed25519. Usaremos o ML-DSA padrão, NÃO as variantes pre-hash (HashML-DSA), exceto para arquivos SU3.

Usaremos a variante de assinatura "hedged" ou randomizada, não a variante "determinística", conforme definido em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) seção 3.4. Isso garante que cada assinatura seja diferente, mesmo quando sobre os mesmos dados, e fornece proteção adicional contra ataques de canal lateral. Consulte a seção de notas de implementação abaixo para detalhes adicionais sobre as escolhas de algoritmo, incluindo codificação e contexto.

Os novos tipos de assinatura são:

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
Certificados X.509 e outras codificações DER usarão as estruturas compostas e OIDs definidos em [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

O overhead será substancial. Os tamanhos típicos de destino Ed25519 e identidade de router são 391 bytes. Estes aumentarão de 3,5x a 6,8x dependendo do algoritmo. As assinaturas Ed25519 são de 64 bytes. Estas aumentarão de 38x a 76x dependendo do algoritmo. RouterInfo assinado típico, LeaseSet, datagramas respondíveis e mensagens de streaming assinadas são cerca de 1KB. Estes aumentarão de 3x a 8x dependendo do algoritmo.

Como os novos tipos de identidade de destino e router não conterão preenchimento, eles não serão compressíveis. Os tamanhos de destinos e identidades de router que são comprimidos com gzip durante o trânsito aumentarão de 12x a 38x, dependendo do algoritmo.

### Legal Combinations

Para Destinations, os novos tipos de assinatura são suportados com todos os tipos de criptografia no leaseset. Defina o tipo de criptografia no certificado de chave como NONE (255).

Para RouterIdentities, o tipo de criptografia ElGamal está obsoleto. Os novos tipos de assinatura são suportados apenas com criptografia X25519 (tipo 4). Os novos tipos de criptografia serão indicados nos RouterAddresses. O tipo de criptografia no certificado de chave continuará sendo tipo 4.

### New Crypto Required

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anteriormente CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Usado apenas para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 e SHAKE256 (extensões XOF para SHA3-128 e SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Vetores de teste para SHA3-256, SHAKE128, e SHAKE256 estão em [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Note que a biblioteca Java bouncycastle suporta todos os itens acima. O suporte da biblioteca C++ está no OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

Não ofereceremos suporte para [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), é muito mais lento e maior que ML-DSA. Não ofereceremos suporte para o próximo FIPS206 (Falcon), ainda não foi padronizado. Não ofereceremos suporte para NTRU ou outros candidatos PQ que não foram padronizados pelo NIST.

### Rosenpass

Existe alguma pesquisa [paper](https://eprint.iacr.org/2020/379.pdf) sobre adaptar o Wireguard (IK) para criptografia PQ pura, mas há várias questões em aberto nesse artigo. Posteriormente, essa abordagem foi implementada como Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) para Wireguard PQ.

O Rosenpass usa um handshake similar ao Noise KK com chaves estáticas pré-compartilhadas Classic McEliece 460896 (500 KB cada) e chaves efêmeras Kyber-512 (essencialmente MLKEM-512). Como os textos cifrados Classic McEliece têm apenas 188 bytes, e as chaves públicas e textos cifrados Kyber-512 são razoáveis, ambas as mensagens de handshake cabem em uma MTU UDP padrão. A chave compartilhada de saída (osk) do handshake PQ KK é usada como a chave pré-compartilhada de entrada (psk) para o handshake Wireguard IK padrão. Então há dois handshakes completos no total, um PQ puro e um X25519 puro.

Não podemos fazer nada disso para substituir nossos handshakes XK e IK porque:

- Não podemos fazer KK, Bob não tem a chave estática de Alice
- Chaves estáticas de 500KB são grandes demais
- Não queremos uma viagem de ida e volta extra

Há muitas informações boas no whitepaper, e nós iremos analisá-lo para obter ideias e inspiração. TODO.

## Specification

### Troca de Chaves

Atualize as seções e tabelas no documento de estruturas comuns [/docs/specs/common-structures/](/docs/specs/common-structures/) da seguinte forma:

### Assinaturas

Os novos tipos de Chave Pública são:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
As chaves públicas híbridas são a chave X25519. As chaves públicas KEM são a chave PQ efêmera enviada de Alice para Bob. A codificação e a ordem de bytes são definidas em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

As chaves MLKEM*_CT não são realmente chaves públicas, elas são o "ciphertext" enviado de Bob para Alice no handshake Noise. Elas são listadas aqui para completude.

### Combinações Legais

Os novos tipos de Chave Privada são:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Chaves privadas híbridas são as chaves X25519. Chaves privadas KEM são apenas para Alice. A codificação KEM e a ordem de bytes são definidas em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Nova Criptografia Necessária

Os novos tipos de Chaves Públicas de Assinatura são:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
As chaves públicas de assinatura híbrida são a chave Ed25519 seguida pela chave PQ, conforme em [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). A codificação e ordem de bytes são definidas em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Alternativas

Os novos tipos de Chave Privada de Assinatura são:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
As chaves privadas de assinatura híbridas são a chave Ed25519 seguida pela chave PQ, como em [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). A codificação e ordem dos bytes são definidas em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Os novos tipos de Signature são:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
As assinaturas híbridas são a assinatura Ed25519 seguida pela assinatura PQ, como em [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). As assinaturas híbridas são verificadas verificando ambas as assinaturas, e falhando se qualquer uma delas falhar. A codificação e ordem de bytes são definidas em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Os novos tipos de Signing Public Key são:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Os novos tipos de Chave Pública Crypto são:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Os tipos de chave híbrida NUNCA são incluídos em certificados de chave; apenas em leasesets.

Para destinos com tipos de assinatura Hybrid ou PQ, use NONE (tipo 255) para o tipo de criptografia, mas não há chave criptográfica, e toda a seção principal de 384 bytes é para a chave de assinatura.

### Estruturas Comuns

Aqui estão os comprimentos para os novos tipos de Destination. O tipo Enc para todos é NONE (tipo 255) e o comprimento da chave de criptografia é tratado como 0. Toda a seção de 384 bytes é usada para a primeira parte da chave pública de assinatura. NOTA: Isso é diferente da especificação para os tipos de assinatura ECDSA_SHA512_P521 e RSA, onde mantivemos a chave ElGamal de 256 bytes no destination mesmo ela não sendo usada.

Sem padding. O comprimento total é 7 + comprimento total da chave. O comprimento do certificado de chave é 4 + comprimento excedente da chave.

Exemplo de fluxo de bytes de destino de 1319 bytes para MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Aqui estão os comprimentos para os novos tipos de Destination. O tipo Enc para todos é X25519 (tipo 4). Toda a seção de 352 bytes após a chave pública X25519 é usada para a primeira parte da chave pública de assinatura. Sem padding. O comprimento total é 39 + comprimento total da chave. O comprimento do certificado da chave é 4 + comprimento excessivo da chave.

Exemplo de fluxo de bytes de identidade de router de 1351 bytes para MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### ChavePrivada

Os handshakes usam padrões de handshake do [Noise Protocol](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é usado:

- e = chave efêmera única
- s = chave estática
- p = payload da mensagem
- e1 = chave PQ efêmera única, enviada de Alice para Bob
- ekem1 = o texto cifrado KEM, enviado de Bob para Alice

As seguintes modificações para XK e IK para sigilo direto híbrido (hfs) são conforme especificado em [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) seção 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
O padrão e1 é definido da seguinte forma, conforme especificado na seção 4 de [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
O padrão ekem1 é definido como segue, conforme especificado na seção 4 de [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### SigningPublicKey

#### Issues

- Devemos mudar a função hash do handshake? Veja [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 não é vulnerável a PQ, mas se queremos atualizar
  nossa função hash, agora é o momento, enquanto estamos mudando outras coisas.
  A proposta atual do IETF SSH [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) é usar MLKEM768
  com SHA256, e MLKEM1024 com SHA384. Esta proposta inclui
  uma discussão sobre as considerações de segurança.
- Devemos parar de enviar dados de ratchet 0-RTT (além do leaseSet)?
- Devemos mudar o ratchet de IK para XK se não enviarmos dados 0-RTT?

#### Overview

Esta seção aplica-se tanto aos protocolos IK quanto XK.

O handshake híbrido é definido em [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). A primeira mensagem, de Alice para Bob, contém e1, a chave de encapsulamento, antes da carga útil da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() nela (como Alice) ou DecryptAndHash() (como Bob). Em seguida, processe a carga útil da mensagem como de costume.

A segunda mensagem, de Bob para Alice, contém ekem1, o texto cifrado, antes da carga útil da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() nela (como Bob) ou DecryptAndHash() (como Alice). Em seguida, calcule a kem_shared_key e chame MixKey(kem_shared_key). Depois, processe a carga útil da mensagem normalmente.

#### Defined ML-KEM Operations

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos utilizados conforme definido em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Observe que tanto a encap_key quanto o ciphertext são criptografados dentro de blocos ChaCha/Poly nas mensagens 1 e 2 do handshake Noise. Eles serão descriptografados como parte do processo de handshake.

A kem_shared_key é misturada na chave de encadeamento com MixHash(). Veja abaixo para detalhes.

#### Alice KDF for Message 1

Para XK: Após o padrão de mensagem 'es' e antes do payload, adicione:

OU

Para IK: Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicionar:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 1

Para XK: Após o padrão de mensagem 'es' e antes da carga útil, adicione:

OU

Para IK: Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicione:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 2

Para XK: Após o padrão de mensagem 'ee' e antes do payload, adicionar:

OU

Para IK: Após o padrão de mensagem 'ee' e antes do padrão de mensagem 'se', adicione:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### Alice KDF for Message 2

Após o padrão de mensagem 'ee' (e antes do padrão de mensagem 'ss' para IK), adicione:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### KDF for Message 3 (XK only)

inalterado

#### KDF for split()

inalterado

### SigningPrivateKey

Atualize a especificação ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) da seguinte forma:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Alterações: O ratchet atual continha a chave estática na primeira seção ChaCha, e o payload na segunda seção. Com ML-KEM, agora existem três seções. A primeira seção contém a chave pública PQ criptografada. A segunda seção contém a chave estática. A terceira seção contém o payload.

Formato criptografado:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Formato descriptografado:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamanhos:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Note que o payload deve conter um bloco DateTime, portanto o tamanho mínimo do payload é 7. Os tamanhos mínimos da mensagem 1 podem ser calculados adequadamente.

#### 1g) New Session Reply format

Alterações: O ratchet atual tem um payload vazio para a primeira seção ChaCha, e o payload na segunda seção. Com ML-KEM, agora há três seções. A primeira seção contém o texto cifrado PQ encriptado. A segunda seção tem um payload vazio. A terceira seção contém o payload.

Formato criptografado:

```
+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Formato descriptografado:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamanhos:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Note que embora a mensagem 2 normalmente tenha um payload diferente de zero, a especificação ratchet [/docs/specs/ecies/](/docs/specs/ecies/) não o exige, então o tamanho mínimo do payload é 0. Os tamanhos mínimos da mensagem 2 podem ser calculados adequadamente.

### Assinatura

Atualize a especificação NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) da seguinte forma:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Alterações: O NTCP2 atual contém apenas as opções na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamanhos:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão do tipo 4, e o suporte será indicado nos endereços do router.

#### 2) SessionCreated

Alterações: O NTCP2 atual contém apenas as opções na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamanhos:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão tipo 4, e o suporte será indicado nos endereços do router.

#### 3) SessionConfirmed

Inalterado

#### Key Derivation Function (KDF) (for data phase)

Inalterado

### Certificados de Chave

Atualize a especificação SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) da seguinte forma:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

O cabeçalho longo tem 32 bytes. É usado antes de uma sessão ser criada, para Token Request, SessionRequest, SessionCreated e Retry. Também é usado para mensagens Peer Test e Hole Punch fora de sessão.

TODO: Poderíamos usar internamente o campo de versão e usar 3 para MLKEM512 e 4 para MLKEM768. Fazemos isso apenas para os tipos 0 e 1 ou para todos os 6 tipos?

Antes da criptografia do cabeçalho:

```

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

inalterado

#### SessionRequest (Type 0)

Mudanças: O SSU2 atual contém apenas os dados do bloco na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Tamanhos, não incluindo overhead de IP:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

MTU mínimo para MLKEM768_X25519: Cerca de 1316 para IPv4 e 1336 para IPv6.

#### SessionCreated (Type 1)

Alterações: O SSU2 atual contém apenas os dados do bloco na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Tamanhos, não incluindo overhead de IP:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão tipo 4, e o suporte será indicado nos endereços do router.

MTU mínimo para MLKEM768_X25519: Aproximadamente 1316 para IPv4 e 1336 para IPv6.

#### SessionConfirmed (Type 2)

inalterado

#### KDF for data phase

inalterado

#### Problemas

Blocos Relay, blocos Peer Test e mensagens Peer Test contêm todas assinaturas. Infelizmente, assinaturas PQ são maiores que o MTU. Não existe atualmente nenhum mecanismo para fragmentar blocos Relay ou Peer Test ou mensagens através de múltiplos pacotes UDP. O protocolo deve ser estendido para suportar fragmentação. Isso será feito em uma proposta separada a ser determinada. Até que isso seja concluído, Relay e Peer Test não serão suportados.

#### Visão Geral

Poderíamos usar internamente o campo de versão e usar 3 para MLKEM512 e 4 para MLKEM768.

Para as mensagens 1 e 2, MLKEM768 aumentaria os tamanhos de pacote além do MTU mínimo de 1280. Provavelmente simplesmente não seria suportado para essa conexão se o MTU fosse muito baixo.

Para as mensagens 1 e 2, MLKEM1024 aumentaria o tamanho dos pacotes além do MTU máximo de 1500. Isso exigiria fragmentar as mensagens 1 e 2, e seria uma grande complicação. Provavelmente não faremos isso.

Relay e Peer Test: Veja acima

### Tamanhos de destino

TODO: Existe uma forma mais eficiente de definir assinatura/verificação para evitar copiar a assinatura?

### Tamanhos de RouterIdent

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) seção 8.1 proíbe HashML-DSA em certificados X.509 e não atribui OIDs para HashML-DSA, devido a complexidades de implementação e segurança reduzida.

Para assinaturas somente PQ de arquivos SU3, use os OIDs definidos em [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) das variantes não-prehash para os certificados. Não definimos assinaturas híbridas de arquivos SU3, porque talvez tenhamos que fazer hash dos arquivos duas vezes (embora HashML-DSA e X2559 usem a mesma função hash SHA512). Além disso, concatenar duas chaves e assinaturas em um certificado X.509 seria completamente fora do padrão.

Note que não permitimos assinatura Ed25519 de arquivos SU3, e embora tenhamos definido assinatura Ed25519ph, nunca concordamos com um OID para isso, ou o utilizamos.

Os tipos de assinatura normais são proibidos para arquivos SU3; use as variantes ph (prehash).

### Padrões de Handshake

O novo tamanho máximo do Destination será 2599 (3468 em base 64).

Atualizar outros documentos que fornecem orientação sobre tamanhos de Destination, incluindo:

- SAMv3
- Bittorrent
- Diretrizes para desenvolvedores
- Nomenclatura / catálogo de endereços / servidores de redirecionamento
- Outros documentos

## Overhead Analysis

### KDF do Handshake Noise

Aumento de tamanho (bytes):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Velocidade:

Velocidades conforme reportado por [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Resultados preliminares de teste em Java:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Tamanho:

Tamanhos típicos de chave, assinatura, RIdent, Dest ou aumentos de tamanho (Ed25519 incluído para referência) assumindo tipo de criptografia X25519 para RIs. Tamanho adicionado para um Router Info, LeaseSet, datagramas respondíveis, e cada um dos dois pacotes streaming (SYN e SYN ACK) listados. Destinations e Leasesets atuais contêm preenchimento repetido e são compressíveis em trânsito. Novos tipos não contêm preenchimento e não serão compressíveis, resultando em um aumento de tamanho muito maior em trânsito. Veja a seção de design acima.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Velocidade:

Velocidades conforme reportado por [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Resultados preliminares de teste em Java:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

As categorias de segurança NIST estão resumidas no [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10. Critérios preliminares: Nossa categoria mínima de segurança NIST deve ser 2 para protocolos híbridos e 3 para PQ-only.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Todos estes são protocolos híbridos. Provavelmente é preciso preferir MLKEM768; MLKEM512 não é seguro o suficiente.

Categorias de segurança NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Esta proposta define tipos de assinatura tanto híbridos quanto somente PQ. MLDSA44 híbrido é preferível ao MLDSA65 somente PQ. Os tamanhos de chaves e assinaturas para MLDSA65 e MLDSA87 são provavelmente muito grandes para nós, pelo menos inicialmente.

Categorias de segurança NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Embora vamos definir e implementar 3 tipos de criptografia e 9 tipos de assinatura, planejamos medir o desempenho durante o desenvolvimento e analisar ainda mais os efeitos do aumento dos tamanhos das estruturas. Também continuaremos a pesquisar e monitorar desenvolvimentos em outros projetos e protocolos.

Após um ano ou mais de desenvolvimento, tentaremos definir um tipo preferido ou padrão para cada caso de uso. A seleção exigirá fazer compensações entre largura de banda, CPU e nível de segurança estimado. Nem todos os tipos podem ser adequados ou permitidos para todos os casos de uso.

As preferências preliminares são as seguintes, sujeitas a alterações:

Criptografia: MLKEM768_X25519

Assinaturas: MLDSA44_EdDSA_SHA512_Ed25519

As restrições preliminares são as seguintes, sujeitas a alterações:

Criptografia: MLKEM1024_X25519 não permitido para SSU2

Assinaturas: MLDSA87 e variante híbrida provavelmente muito grandes; MLDSA65 e variante híbrida podem ser muito grandes

## Implementation Notes

### Library Support

As bibliotecas Bouncycastle, BoringSSL e WolfSSL agora suportam MLKEM e MLDSA. O suporte do OpenSSL estará no lançamento 3.5 em 8 de abril de 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

A biblioteca Noise do southernstorm.com adaptada pelo Java I2P continha suporte preliminar para handshakes híbridos, mas nós o removemos por não estar sendo usado; teremos que adicioná-lo de volta e atualizá-lo para corresponder a [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

Utilizaremos a variante de assinatura "hedged" ou randomizada, não a variante "determinística", conforme definido em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) seção 3.4. Isso garante que cada assinatura seja diferente, mesmo quando sobre os mesmos dados, e fornece proteção adicional contra ataques de canal lateral. Embora [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) especifique que a variante "hedged" é o padrão, isso pode ou não ser verdadeiro em várias bibliotecas. Os implementadores devem garantir que a variante "hedged" seja usada para assinatura.

Usamos o processo de assinatura normal (chamado Pure ML-DSA Signature Generation) que codifica a mensagem internamente como 0x00 || len(ctx) || ctx || message, onde ctx é algum valor opcional de tamanho 0x00..0xFF. Não estamos usando nenhum contexto opcional. len(ctx) == 0. Este processo é definido em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algoritmo 2 passo 10 e Algoritmo 3 passo 5. Note que alguns vetores de teste publicados podem exigir a definição de um modo onde a mensagem não é codificada.

### Reliability

O aumento do tamanho resultará em muito mais fragmentação de túnel para armazenamentos NetDB, handshakes de streaming e outras mensagens. Verifique mudanças de desempenho e confiabilidade.

### Structure Sizes

Encontre e verifique qualquer código que limite o tamanho em bytes de router infos e leaseSets.

### NetDB

Revisar e possivelmente reduzir o máximo de LS/RI armazenados na RAM ou no disco, para limitar o aumento de armazenamento. Aumentar os requisitos mínimos de largura de banda para floodfills?

### Ratchet

#### Operações ML-KEM Definidas

A auto-classificação/detecção de múltiplos protocolos nos mesmos tunnels deve ser possível baseada numa verificação de comprimento da mensagem 1 (New Session Message). Usando MLKEM512_X25519 como exemplo, o comprimento da mensagem 1 é 816 bytes maior que o protocolo ratchet atual, e o tamanho mínimo da mensagem 1 (com apenas um payload DateTime incluído) é 919 bytes. A maioria dos tamanhos de mensagem 1 com o ratchet atual tem um payload inferior a 816 bytes, então podem ser classificados como ratchet não-híbrido. Mensagens grandes são provavelmente POSTs que são raros.

Portanto, a estratégia recomendada é:

- Se a mensagem 1 tiver menos de 919 bytes, é o protocolo ratchet atual.
- Se a mensagem 1 tiver 919 bytes ou mais, provavelmente é MLKEM512_X25519.
  Tente MLKEM512_X25519 primeiro e, se falhar, tente o protocolo ratchet atual.

Isso deve nos permitir suportar eficientemente ratchet padrão e ratchet híbrido no mesmo destino, assim como anteriormente suportávamos ElGamal e ratchet no mesmo destino. Portanto, podemos migrar para o protocolo híbrido MLKEM muito mais rapidamente do que se não pudéssemos suportar protocolos duplos para o mesmo destino, porque podemos adicionar suporte MLKEM a destinos existentes.

As combinações suportadas obrigatórias são:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

As seguintes combinações podem ser complexas, e NÃO são obrigatórias de serem suportadas, mas podem ser, dependendo da implementação:

- Mais de um MLKEM
- ElG + um ou mais MLKEM
- X25519 + um ou mais MLKEM
- ElG + X25519 + um ou mais MLKEM

Podemos não tentar suportar múltiplos algoritmos MLKEM (por exemplo, MLKEM512_X25519 e MLKEM_768_X25519) no mesmo destino. Escolha apenas um; no entanto, isso depende de selecionarmos uma variante MLKEM preferida, para que os túneis de cliente HTTP possam usar uma. Dependente da implementação.

Nós PODEMOS tentar suportar três algoritmos (por exemplo X25519, MLKEM512_X25519, e MLKEM769_X25519) no mesmo destino. A classificação e estratégia de repetição podem ser muito complexas. A configuração e interface de configuração podem ser muito complexas. Dependente da implementação.

Provavelmente NÃO tentaremos suportar algoritmos ElGamal e híbridos no mesmo destino. ElGamal é obsoleto, e ElGamal + híbrido apenas (sem X25519) não faz muito sentido. Além disso, as Mensagens de Nova Sessão ElGamal e Híbrida são ambas grandes, então as estratégias de classificação frequentemente teriam que tentar ambas as descriptografias, o que seria ineficiente. Dependente da implementação.

Os clientes podem usar as mesmas chaves estáticas X25519 ou chaves diferentes para os protocolos X25519 e híbrido nos mesmos túneis, dependendo da implementação.

#### Alice KDF para Mensagem 1

A especificação ECIES permite Garlic Messages no payload da New Session Message, o que possibilita a entrega 0-RTT do pacote de streaming inicial, geralmente um HTTP GET, juntamente com o leaseset do cliente. No entanto, o payload da New Session Message não possui forward secrecy. Como esta proposta está enfatizando forward secrecy aprimorada para ratchet, as implementações podem ou devem adiar a inclusão do payload de streaming, ou da mensagem de streaming completa, até a primeira Existing Session Message. Isso seria às custas da entrega 0-RTT. As estratégias também podem depender do tipo de tráfego ou tipo de túnel, ou de GET vs. POST, por exemplo. Dependente da implementação.

#### Bob KDF para Mensagem 1

MLKEM, MLDSA, ou ambos no mesmo destino, aumentarão drasticamente o tamanho da New Session Message, como descrito acima. Isso pode diminuir significativamente a confiabilidade da entrega da New Session Message através de tunnels, onde elas devem ser fragmentadas em múltiplas mensagens de tunnel de 1024 bytes. O sucesso da entrega é proporcional ao número exponencial de fragmentos. As implementações podem usar várias estratégias para limitar o tamanho da mensagem, às custas da entrega 0-RTT. Dependente da implementação.

### Ratchet

Podemos definir o MSB da chave efêmera (key[31] & 0x80) na solicitação de sessão para indicar que esta é uma conexão híbrida. Isso nos permitiria executar tanto NTCP padrão quanto NTCP híbrido na mesma porta. Apenas uma variante híbrida seria suportada e anunciada no endereço do router. Por exemplo, v=2,3 ou v=2,4 ou v=2,5.

Se não fizermos isso, precisamos de um endereço/porta de transporte diferente e um novo nome de protocolo como "NTCP1PQ1".

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão tipo 4, e o suporte será indicado nos endereços do router.

TODO

### SSU2

PODE precisar de endereço/porta de transporte diferentes, mas esperamos que não, temos um cabeçalho com flags para a mensagem 1. Poderíamos usar internamente o campo de versão e usar 3 para MLKEM512 e 4 para MLKEM768. Talvez apenas v=2,3,4 no endereço seria suficiente. Mas precisamos de identificadores para ambos os novos algoritmos: 3a, 3b?

Verifique e confirme que o SSU2 pode lidar com o RI fragmentado em múltiplos pacotes (6-8?). O i2pd atualmente suporta apenas 2 fragmentos no máximo?

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

TODO

## Router Compatibility

### Transport Names

Provavelmente não precisaremos de novos nomes de transporte, se conseguirmos executar tanto o padrão quanto o híbrido na mesma porta, com flags de versão.

Se precisarmos de novos nomes de transporte, eles seriam:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Note que o SSU2 não consegue suportar MLKEM1024, é muito grande.

### Router Enc. Types

Temos várias alternativas a considerar:

#### Bob KDF para Mensagem 2

Não recomendado. Use apenas os novos transportes listados acima que correspondem ao tipo de router. Routers mais antigos não conseguem conectar, construir tunnels através de, ou enviar mensagens netDb para. Levaria vários ciclos de lançamento para debugar e garantir suporte antes de habilitar por padrão. Pode estender o rollout por um ano ou mais em relação às alternativas abaixo.

#### KDF da Alice para Mensagem 2

Recomendado. Como o PQ não afeta a chave estática X25519 ou os protocolos de handshake N, poderíamos deixar os routers como tipo 4, e apenas anunciar novos transportes. Routers mais antigos ainda poderiam se conectar, construir túneis através deles, ou enviar mensagens netDb para eles.

#### KDF para Mensagem 3 (apenas XK)

Roteadores Tipo 4 podem anunciar endereços tanto NTCP2 quanto NTCP2PQ*. Estes podem usar a mesma chave estática e outros parâmetros, ou não. Provavelmente precisarão estar em portas diferentes; seria muito difícil suportar ambos os protocolos NTCP2 e NTCP2PQ* na mesma porta, já que não há cabeçalho ou enquadramento que permitiria ao Bob classificar e enquadrar a mensagem Session Request recebida.

Portas e endereços separados serão difíceis para o Java, mas simples para o i2pd.

#### KDF para split()

Routers tipo 4 poderiam anunciar endereços tanto SSU2 quanto SSU2PQ*. Com flags de cabeçalho adicionais, Bob poderia identificar o tipo de transporte de entrada na primeira mensagem. Portanto, poderíamos suportar tanto SSU2 quanto SSUPQ* na mesma porta.

Estes poderiam ser publicados como endereços separados (como o i2pd fez em transições anteriores) ou no mesmo endereço com um parâmetro indicando suporte PQ (como o Java i2p fez em transições anteriores).

Se no mesmo endereço, ou na mesma porta em endereços diferentes, estes usariam a mesma chave estática e outros parâmetros. Se em endereços diferentes com portas diferentes, estes poderiam usar a mesma chave estática e outros parâmetros, ou não.

Portas e endereços separados serão difíceis para o Java, mas diretos para o i2pd.

#### Recommendations

TODO

### NTCP2

#### Identificadores Noise

Routers mais antigos verificam RIs e, portanto, não conseguem se conectar, construir túneis através de, ou enviar mensagens netDb para. Levaria vários ciclos de lançamento para depurar e garantir suporte antes de habilitar por padrão. Seriam os mesmos problemas do rollout de enc. type 5/6/7; poderia estender o rollout por um ano ou mais sobre a alternativa de rollout de enc. type 4 listada acima.

Sem alternativas.

### LS Enc. Types

#### 1b) Novo formato de sessão (com binding)

Estes podem estar presentes no LS com chaves X25519 do tipo 4 mais antigas. Routers mais antigos irão ignorar chaves desconhecidas.

Os destinos podem suportar múltiplos tipos de chave, mas apenas fazendo descriptografias de teste da mensagem 1 com cada chave. A sobrecarga pode ser mitigada mantendo contadores de descriptografias bem-sucedidas para cada chave, e tentando a chave mais usada primeiro. O Java I2P usa esta estratégia para ElGamal+X25519 no mesmo destino.

### Dest. Sig. Types

#### 1g) Formato de Resposta de Nova Sessão

Routers verificam assinaturas de leaseSet e, portanto, não conseguem conectar ou receber leaseSets para destinos tipo 12-17. Levaria vários ciclos de lançamento para depurar e garantir o suporte antes de habilitar por padrão.

Nenhuma alternativa.

## Especificação

Os dados mais valiosos são o tráfego de ponta a ponta, criptografado com ratchet. Como um observador externo entre saltos de tunnel, isso está criptografado duas vezes mais, com criptografia de tunnel e criptografia de transporte. Como um observador externo entre OBEP e IBGW, está criptografado apenas uma vez mais, com criptografia de transporte. Como um participante OBEP ou IBGW, o ratchet é a única criptografia. No entanto, como os tunnels são unidirecionais, capturar ambas as mensagens no handshake ratchet exigiria roteadores em conluio, a menos que os tunnels fossem construídos com o OBEP e IBGW no mesmo roteador.

O modelo de ameaça PQ mais preocupante atualmente é armazenar tráfego hoje, para descriptografia daqui a muitos e muitos anos (sigilo progressivo). Uma abordagem híbrida protegeria contra isso.

O modelo de ameaça PQ de quebrar as chaves de autenticação em um período de tempo razoável (digamos alguns meses) e então personificar a autenticação ou descriptografar em quase tempo real, está muito mais distante? E é quando gostaríamos de migrar para chaves estáticas PQC.

Então, o modelo de ameaça PQ mais antigo é o OBEP/IBGW armazenando tráfego para descriptografia posterior. Devemos implementar ratchet híbrido primeiro.

Ratchet é a prioridade mais alta. Transportes são os próximos. Assinaturas são a prioridade mais baixa.

O lançamento de assinaturas também será um ano ou mais tarde do que o lançamento de criptografia, porque não é possível compatibilidade com versões anteriores. Além disso, a adoção do MLDSA na indústria será padronizada pelo CA/Browser Forum e pelas Autoridades Certificadoras. As CAs precisam primeiro do suporte de módulo de segurança de hardware (HSM), que não está disponível atualmente [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Esperamos que o CA/Browser Forum conduza as decisões sobre escolhas específicas de parâmetros, incluindo se deve apoiar ou exigir assinaturas compostas [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Se não conseguirmos suportar tanto os protocolos ratchet antigos quanto os novos nos mesmos tunnels, a migração será muito mais difícil.

Devemos ser capazes de simplesmente tentar um-depois-do-outro, como fizemos com X25519, para ser comprovado.

## Issues

- Seleção de Hash Noise - manter SHA256 ou atualizar?
  SHA256 deve ser bom por mais 20-30 anos, não ameaçado por PQ,
  Ver [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) e [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Se SHA256 for quebrado, temos problemas piores (netDb).
- NTCP2 porta separada, endereço de router separado
- SSU2 relay / teste de peer
- Campo de versão SSU2
- Versão de endereço de router SSU2
