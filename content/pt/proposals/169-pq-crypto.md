---
title: "Protocolos Criptográficos Pós-Quânticos"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "Abrir"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### Status

| Protocolo / Funcionalidade | Status |
|--------------------|--------|
| Ratchet | Completo no Java I2P e i2pd |
| NTCP2 | Beta Q1 2026 |
| SSU2 | Implementação começando em breve, Beta Q23 2026 |
| MLDSA SigTypes | Baixa prioridade, provavelmente 2027+ |
## Visão Geral

Embora a pesquisa e a competição por criptografia pós-quântica (PQ) adequada tenham prosseguido por uma década, as escolhas não se tornaram claras até recentemente.

Começamos a analisar as implicações da criptografia PQ em 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Os padrões TLS adicionaram suporte para criptografia híbrida nos últimos dois anos e agora é usada para uma parcela significativa do tráfego criptografado na internet devido ao suporte no Chrome e Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

O NIST finalizou e publicou recentemente os algoritmos recomendados para criptografia pós-quântica [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Várias bibliotecas de criptografia comuns agora suportam os padrões NIST ou lançarão suporte em um futuro próximo.

Tanto a [Cloudflare](https://blog.cloudflare.com/pq-2024/) quanto o [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recomendam que a migração comece imediatamente. Veja também o FAQ PQ de 2022 da NSA [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). O I2P deve ser líder em segurança e criptografia. Agora é hora de implementar os algoritmos recomendados. Usando nosso sistema flexível de tipos de criptografia e tipos de assinatura, adicionaremos tipos para criptografia híbrida, e para assinaturas PQ e híbridas.

## Objetivos

- Selecionar algoritmos resistentes a PQ
- Adicionar algoritmos somente PQ e híbridos aos protocolos I2P onde apropriado
- Definir múltiplas variantes
- Selecionar as melhores variantes após implementação, testes, análise e pesquisa
- Adicionar suporte incrementalmente e com compatibilidade regressiva

## Não-Objetivos

- Não altere os protocolos de criptografia unidirecional (Noise N)
- Não abandone o SHA256, não está ameaçado a curto prazo pela computação quântica
- Não selecione as variantes preferidas finais neste momento

## Modelo de Ameaças

- Routers no OBEP ou IBGW, possivelmente em conluio,
  armazenando mensagens garlic para descriptografia posterior (forward secrecy)
- Observadores da rede
  armazenando mensagens de transporte para descriptografia posterior (forward secrecy)
- Participantes da rede falsificando assinaturas para RI, LS, streaming, datagramas,
  ou outras estruturas

## Protocolos Afetados

Modificaremos os seguintes protocolos, aproximadamente em ordem de desenvolvimento. O lançamento geral provavelmente será do final de 2025 até meados de 2027. Consulte a seção Prioridades e Lançamento abaixo para detalhes.

| Protocolo / Funcionalidade | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet e LS | Aprovado 2025-06; beta 2025-08; lançamento 2025-11 |
| Hybrid MLKEM NTCP2 | Testado na rede ao vivo, Aprovado 2026-02; meta beta 2026-05; meta lançamento 2026-08 |
| Hybrid MLKEM SSU2 | Aprovado 2026-02; meta beta 2026-08; meta lançamento 2026-11 |
| MLDSA SigTypes 12-14 | Proposta é estável mas pode não ser finalizada até 2027 |
| MLDSA Dests | Testado na rede ao vivo, requer atualização da rede para suporte floodfill |
| Hybrid SigTypes 15-17 | Preliminar |
| Hybrid Dests | |
## Design

Iremos suportar os padrões NIST FIPS 203 e 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) que são baseados em, mas NÃO compatíveis com, CRYSTALS-Kyber e CRYSTALS-Dilithium (versões 3.1, 3 e anteriores).

### Troca de Chaves

Iremos suportar troca de chaves híbrida nos seguintes protocolos:

| Proto   | Tipo Noise | Suporta apenas PQ? | Suporta Híbrido? |
|---------|------------|-------------------|------------------|
| NTCP2   | XK         | não               | sim              |
| SSU2    | XK         | não               | sim              |
| Ratchet | IK         | não               | sim              |
| TBM     | N          | não               | não              |
| NetDB   | N          | não               | não              |
PQ KEM fornece apenas chaves efêmeras e não suporta diretamente handshakes de chave estática como Noise XK e IK.

O Noise N não usa uma troca de chaves bidirecional e, portanto, não é adequado para criptografia híbrida.

Portanto, ofereceremos suporte apenas à criptografia híbrida, para NTCP2, SSU2 e Ratchet. Definiremos as três variantes ML-KEM como em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), totalizando 3 novos tipos de criptografia. Os tipos híbridos serão definidos apenas em combinação com X25519.

Os novos tipos de criptografia são:

| Tipo | Código |
|------|--------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
O overhead será substancial. Os tamanhos típicos das mensagens 1 e 2 (para XK e IK) estão atualmente em torno de 100 bytes (antes de qualquer payload adicional). Isso aumentará de 8x a 15x dependendo do algoritmo.

### Assinaturas

Suportaremos assinaturas PQ e híbridas nas seguintes estruturas:

Então iremos suportar tanto assinaturas apenas PQ quanto híbridas. Definiremos as três variantes ML-DSA como em [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), três variantes híbridas com Ed25519, e três variantes apenas PQ com prehash somente para arquivos SU3, totalizando 9 novos tipos de assinatura. Tipos híbridos serão definidos apenas em combinação com Ed25519. Usaremos o ML-DSA padrão, NÃO as variantes pre-hash (HashML-DSA), exceto para arquivos SU3.

| Tipo | Suporta apenas PQ? | Suporta Híbrido? |
|------|-------------------|------------------|
| RouterInfo | sim | sim |
| LeaseSet | sim | sim |
| Streaming SYN/SYNACK/Close | sim | sim |
| Repliable Datagrams | sim | sim |
| Datagram2 (prop. 163) | sim | sim |
| I2CP create session msg | sim | sim |
| Arquivos SU3 | sim | sim |
| Certificados X.509 | sim | sim |
| Java keystores | sim | sim |
Usaremos a variante de assinatura "hedged" ou randomizada, não a variante "determinística", conforme definido na seção 3.4 do [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Isso garante que cada assinatura seja diferente, mesmo quando aplicada aos mesmos dados, e fornece proteção adicional contra ataques de canal lateral. Veja a seção de notas de implementação abaixo para detalhes adicionais sobre as escolhas do algoritmo, incluindo codificação e contexto.

Os novos tipos de assinatura são:

Certificados X.509 e outras codificações DER utilizarão as estruturas compostas e OIDs definidos no [rascunho do IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Tipo | Código |
|------|--------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
O overhead será substancial. Os tamanhos típicos de destino Ed25519 e identidade de router são 391 bytes. Estes aumentarão de 3,5x a 6,8x dependendo do algoritmo. As assinaturas Ed25519 são de 64 bytes. Estas aumentarão de 38x a 76x dependendo do algoritmo. RouterInfo assinados típicos, leaseSet, datagramas respondíveis e mensagens de streaming assinadas têm cerca de 1KB. Estes aumentarão de 3x a 8x dependendo do algoritmo.

Como os novos tipos de identidade de destino e router não conterão preenchimento, eles não serão compressíveis. Os tamanhos de destinos e identidades de router que são compactados com gzip em trânsito aumentarão de 12x a 38x dependendo do algoritmo.

Para Destinations, os novos tipos de assinatura são suportados com todos os tipos de criptografia no leaseSet. Defina o tipo de criptografia no certificado de chave como NONE (255).

### Combinações Legais

Para RouterIdentities, o tipo de criptografia ElGamal está depreciado. Os novos tipos de assinatura são suportados apenas com criptografia X25519 (tipo 4). Os novos tipos de criptografia serão indicados nos RouterAddresses. O tipo de criptografia no certificado de chave continuará sendo tipo 4.

Os vetores de teste para SHA3-256, SHAKE128 e SHAKE256 estão disponíveis no [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### Nova Criptografia Necessária

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anteriormente CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Usado apenas para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 e SHAKE256 (extensões XOF para SHA3-128 e SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Note que a biblioteca Java bouncycastle suporta todos os itens acima. O suporte da biblioteca C++ está no OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Não ofereceremos suporte ao [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), é muito muito mais lento e maior que o ML-DSA. Não ofereceremos suporte ao próximo FIPS206 (Falcon), ainda não foi padronizado. Não ofereceremos suporte ao NTRU ou outros candidatos PQ que não foram padronizados pelo NIST.

### Alternativas

Existe alguma pesquisa [paper](https://eprint.iacr.org/2020/379.pdf) sobre adaptar o Wireguard (IK) para criptografia PQ pura, mas há várias questões em aberto nesse paper. Posteriormente, essa abordagem foi implementada como Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) para Wireguard PQ.

### Rosenpass

O Rosenpass usa um handshake similar ao Noise KK com chaves estáticas pré-compartilhadas Classic McEliece 460896 (500 KB cada) e chaves efêmeras Kyber-512 (essencialmente MLKEM-512). Como os textos cifrados Classic McEliece têm apenas 188 bytes, e as chaves públicas e textos cifrados Kyber-512 são razoáveis, ambas as mensagens de handshake cabem em um MTU UDP padrão. A chave compartilhada de saída (osk) do handshake PQ KK é usada como a chave pré-compartilhada de entrada (psk) para o handshake IK padrão do Wireguard. Então há dois handshakes completos no total, um PQ puro e um X25519 puro.

Não podemos fazer nada disso para substituir nossos handshakes XK e IK porque:

Há muitas informações valiosas no whitepaper, e iremos revisá-lo em busca de ideias e inspiração. TODO.

- Não podemos fazer KK, Bob não tem a chave estática da Alice
- Chaves estáticas de 500KB são grandes demais
- Não queremos uma viagem de ida e volta extra

Atualize as seções e tabelas no documento de estruturas comuns [/docs/specs/common-structures/](/docs/specs/common-structures/) da seguinte forma:

## Especificação

### Estruturas Comuns

Os novos tipos de Chave Pública são:

#### Problemas

Chaves públicas híbridas são a chave X25519. Chaves públicas KEM são a chave PQ efêmera enviada de Alice para Bob. A codificação e ordem de bytes são definidas em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Tipo | Comprimento da Chave Pública | Desde | Uso |
|------|-------------------------------|-------|-----|
| MLKEM512_X25519 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM512 | 800 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM768 | 1184 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM1024 | 1568 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM512_CT | 768 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| NONE | 0 | 0.9.xx | Ver proposta 169, apenas para destinations com tipos de assinatura PQ, não para RIs ou Leasesets |
As chaves MLKEM*_CT não são realmente chaves públicas, elas são o "texto cifrado" enviado de Bob para Alice no handshake Noise. Elas são listadas aqui por completude.

Os novos tipos de Chave Privada são:

#### PrivateKey

As chaves privadas híbridas são as chaves X25519. As chaves privadas KEM são apenas para Alice. A codificação KEM e a ordem dos bytes são definidas em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Tipo | Comprimento da Chave Privada | Desde | Uso |
|------|------------------------------|-------|-----|
| MLKEM512_X25519 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM512 | 1632 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM768 | 2400 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
| MLKEM1024 | 3168 | 0.9.xx | Ver proposta 169, apenas para handshakes, não para Leasesets, RIs ou Destinations |
Os novos tipos de Chave Pública de Assinatura são:

#### SigningPublicKey

Chaves públicas de assinatura híbridas são a chave Ed25519 seguida pela chave PQ, como no [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). A codificação e ordem de bytes são definidas no [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Comprimento (bytes) | Desde | Uso |
|------|---------------------|-------|-----|
| MLDSA44 | 1312 | 0.9.xx | Ver proposta 169 |
| MLDSA65 | 1952 | 0.9.xx | Ver proposta 169 |
| MLDSA87 | 2592 | 0.9.xx | Ver proposta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Ver proposta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Ver proposta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Ver proposta 169 |
| MLDSA44ph | 1344 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb |
| MLDSA65ph | 1984 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb |
| MLDSA87ph | 2624 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb |
Os novos tipos de Chave Privada de Assinatura são:

#### SigningPrivateKey

As chaves privadas de assinatura híbridas são a chave Ed25519 seguida pela chave PQ, conforme descrito no [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). A codificação e ordem de bytes são definidas no [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Comprimento (bytes) | Desde | Uso |
|------|---------------------|-------|-----|
| MLDSA44 | 2560 | 0.9.xx | Ver proposta 169 |
| MLDSA65 | 4032 | 0.9.xx | Ver proposta 169 |
| MLDSA87 | 4896 | 0.9.xx | Ver proposta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Ver proposta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Ver proposta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Ver proposta 169 |
| MLDSA44ph | 2592 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb. Ver proposta 169 |
| MLDSA65ph | 4064 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb. Ver proposta 169 |
| MLDSA87ph | 4928 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb. Ver proposta 169 |
Os novos tipos de assinatura são:

As assinaturas híbridas são a assinatura Ed25519 seguida pela assinatura PQ, como no [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). As assinaturas híbridas são verificadas verificando ambas as assinaturas, e falhando se qualquer uma falhar. A codificação e ordem de bytes são definidas no [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### Assinatura

Os novos tipos de Chave Pública de Assinatura são:

| Tipo | Comprimento (bytes) | Desde | Uso |
|------|---------------------|-------|-----|
| MLDSA44 | 2420 | 0.9.xx | Ver proposta 169 |
| MLDSA65 | 3309 | 0.9.xx | Ver proposta 169 |
| MLDSA87 | 4627 | 0.9.xx | Ver proposta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Ver proposta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Ver proposta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Ver proposta 169 |
| MLDSA44ph | 2484 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb. Ver proposta 169 |
| MLDSA65ph | 3373 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb. Ver proposta 169 |
| MLDSA87ph | 4691 | 0.9.xx | Apenas para arquivos SU3, não para estruturas netDb. Ver proposta 169 |
Os novos tipos de Chave Pública Criptográfica são:

#### Certificados de Chave

Chaves públicas de assinatura híbridas são a chave Ed25519 seguida pela chave PQ, como no [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). A codificação e ordem de bytes são definidas no [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Código do Tipo | Comprimento Total da Chave Pública | Desde | Uso |
|------|----------------|-------------------------------------|-------|-----|
| MLDSA44 | 12 | 1312 | 0.9.xx | Ver proposta 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | Ver proposta 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | Ver proposta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Ver proposta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Ver proposta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Ver proposta 169 |
| MLDSA44ph | 18 | n/d | 0.9.xx | Apenas para arquivos SU3 |
| MLDSA65ph | 19 | n/d | 0.9.xx | Apenas para arquivos SU3 |
| MLDSA87ph | 20 | n/d | 0.9.xx | Apenas para arquivos SU3 |
Para destinos com tipos de assinatura Hybrid ou PQ, use NONE (tipo 255) para o tipo de criptografia, mas não há chave criptográfica, e toda a seção principal de 384 bytes é para a chave de assinatura.

| Tipo | Código do Tipo | Comprimento Total da Chave Pública | Desde | Uso |
|------|----------------|-------------------------------------|-------|-----|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Ver proposta 169, apenas para Leasesets, não para RIs ou Destinations |
| NONE | 255 | 0 | 0.9.xx | Ver proposta 169 |
Tipos de chave híbrida NUNCA são incluídos em certificados de chave; apenas em leaseSets.

Sem preenchimento. O comprimento total é 7 + comprimento total da chave. O comprimento do certificado da chave é 4 + comprimento excessivo da chave.

#### Tamanhos de destino

Aqui estão os comprimentos para os novos tipos de Destination. O tipo Enc para todos é NONE (tipo 255) e o comprimento da chave de criptografia é tratado como 0. Toda a seção de 384 bytes é usada para a primeira parte da chave pública de assinatura. NOTA: Isso é diferente da especificação para os tipos de assinatura ECDSA_SHA512_P521 e RSA, onde mantivemos a chave ElGamal de 256 bytes no destination mesmo que não fosse usada.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

Exemplo de fluxo de bytes de destino de 1319 bytes para MLDSA44:

Exemplo de fluxo de bytes de identidade do router de 1351 bytes para MLDSA44:

| Tipo | Código do Tipo | Comprimento Total da Chave Pública | Principal | Excesso | Comprimento Total do Dest |
|------|----------------|-------------------------------------|-----------|---------|---------------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### Tamanhos de RouterIdent

Aqui estão os comprimentos para os novos tipos de Destination. O tipo de criptografia para todos é X25519 (tipo 4). Toda a seção de 352 bytes após a chave pública X25519 é usada para a primeira parte da chave pública de assinatura. Sem preenchimento. O comprimento total é 39 + comprimento total da chave. O comprimento do certificado da chave é 4 + comprimento excedente da chave.

Os handshakes usam padrões de handshake do [Noise Protocol](https://noiseprotocol.org/noise.html).

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Tipo | Código do Tipo | Comprimento Total da Chave Pública | Principal | Excesso | Comprimento Total do RouterIdent |
|------|----------------|-------------------------------------|-----------|---------|----------------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

As seguintes modificações ao XK e IK para sigilo futuro híbrido (hfs) são especificadas conforme a [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) seção 5:

O padrão e1 é definido como segue, conforme especificado na seção 4 da [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

#### KDF para split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Identificadores Noise

O padrão ekem1 é definido como segue, conforme especificado na [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) seção 4:

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) Novo formato de sessão (com vinculação)

Esta seção se aplica tanto aos protocolos IK quanto XK.

### Padrões de Handshake

O handshake híbrido é definido na [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). A primeira mensagem, de Alice para Bob, contém e1, a chave de encapsulamento, antes da carga útil da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() nela (como Alice) ou DecryptAndHash() (como Bob). Em seguida, processe a carga útil da mensagem como de costume.

O seguinte mapeamento de letras é usado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem
- e1 = chave PQ efêmera de uso único, enviada de Alice para Bob
- ekem1 = o texto cifrado KEM, enviado de Bob para Alice

Definimos as seguintes funções correspondentes aos blocos fundamentais criptográficos utilizados conforme definido em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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
(encap_key, decap_key) = PQ_KEYGEN()

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
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

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
### KDF do Handshake Noise

#### 1b) Novo formato de sessão (com vinculação)

- Devemos parar de enviar dados ratchet 0-RTT (além do LS)?
- Devemos mudar o ratchet de IK para XK se não enviarmos dados 0-RTT?

#### Visão Geral

kem_shared_key = DECAPS(ciphertext, decap_key)

Note que tanto a encap_key quanto o ciphertext são criptografados dentro de blocos ChaCha/Poly nas mensagens 1 e 2 do handshake Noise. Eles serão descriptografados como parte do processo de handshake.

A segunda mensagem, de Bob para Alice, contém ekem1, o texto cifrado, antes da carga útil da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() nela (como Bob) ou DecryptAndHash() (como Alice). Em seguida, calcule a kem_shared_key e chame MixKey(kem_shared_key). Então processe a carga útil da mensagem normalmente.

#### Operações ML-KEM Definidas

Para XK: Após o padrão de mensagem 'es' e antes da carga útil, adicione:

OU

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

Para IK: Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicione:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

Para XK: Após o padrão de mensagem 'es' e antes da carga útil, adicione:

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

OU

A kem_shared_key é misturada na chaining key com MixHash(). Veja abaixo para detalhes.

#### KDF da Alice para Mensagem 1

Para XK: Após o padrão de mensagem 'ee' e antes do payload, adicione:

OU

Para IK: Após o padrão de mensagem 'ee' e antes do padrão de mensagem 'se', adicionar:

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
#### Bob KDF para Mensagem 1

Para XK: Após o padrão de mensagem 'ee' e antes do payload, adicione:

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
#### Bob KDF para Mensagem 2

Atualize a especificação ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) da seguinte forma:

OU

Formato criptografado:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF da Alice para Mensagem 2

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF para Mensagem 3 (apenas XK)

inalterado

#### Identificadores Noise

inalterado

### Ratchet

Mudanças: O ratchet atual tem uma carga útil vazia para a primeira seção ChaCha, e a carga útil na segunda seção. Com ML-KEM, agora existem três seções. A primeira seção contém o texto cifrado PQ criptografado. A segunda seção tem uma carga útil vazia. A terceira seção contém a carga útil.

#### Cabeçalho Longo

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Cabeçalho Curto

Alterações: O ratchet atual continha a chave estática na primeira seção ChaCha, e o payload na segunda seção. Com ML-KEM, agora há três seções. A primeira seção contém a chave pública PQ criptografada. A segunda seção contém a chave estática. A terceira seção contém o payload.

Formato descriptografado:

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

| Tipo | Código do Tipo | Comprimento X | Comprimento Msg 1 | Comprimento Msg 1 Cif | Comprimento Msg 1 Dec | Comprimento chave PQ | Comprimento pl |
|------|----------------|---------------|-------------------|----------------------|---------------------|------------------|----------------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Note que a carga útil deve conter um bloco DateTime, então o tamanho mínimo da carga útil é 7. Os tamanhos mínimos da mensagem 1 podem ser calculados de acordo.

#### 1g) Formato de Resposta de Nova Sessão

Mudanças: O NTCP2 atual contém apenas as opções na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

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

| Tipo | Código do Tipo | Comp Y | Comp Msg 2 | Comp Msg 2 Cript | Comp Msg 2 Decr | Comp PQ CT | comp opt |
|------|----------------|--------|------------|------------------|------------------|------------|----------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Note que embora a mensagem 2 normalmente tenha uma carga útil diferente de zero, a especificação do ratchet [/docs/specs/ecies/](/docs/specs/ecies/) não a exige, portanto o tamanho mínimo da carga útil é 0. Os tamanhos mínimos da mensagem 2 podem ser calculados de acordo.

### NTCP2

Atualize a especificação NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) da seguinte forma:

#### Identificadores Noise

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Conteúdo bruto:

Para que NTCP2 PQ e não-PQ possam ser suportados no mesmo endereço e porta do router, usamos o bit mais significativo do valor X (chave pública efêmera X25519) para marcar que é uma conexão PQ. Este bit sempre permanece desmarcado para conexões não-PQ.

Nota: o campo de versão no bloco de opções da mensagem 1 deve ser definido como 2, mesmo para conexões PQ.

Para Bob, após a des-ofuscação AES de X, teste X[31] & 0x80. Se o bit estiver definido, limpe-o com X[31] &= 0x7f, e descriptografe via Noise como uma conexão PQ. Se o bit estiver limpo, descriptografe via Noise como uma conexão não-PQ normalmente.

Para PQ NTCP2 anunciado em um endereço de router e porta diferentes, isso não é necessário.

Para informações adicionais, consulte a seção Endereços Publicados abaixo.

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
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
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão tipo 4, e o suporte será indicado nos endereços do router.

Tamanhos:

| Tipo | Código do Tipo | Tamanho X | Tamanho Msg 1 | Tamanho Msg 1 Enc | Tamanho Msg 1 Dec | Tamanho chave PQ | Tamanho opt |
|------|----------------|-----------|---------------|-------------------|-------------------|------------------|-------------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

#### 2) SessionCreated

Conteúdo bruto:

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Tamanhos:

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

| Tipo | Código do tipo | Comprimento Y | Comprimento Msg 2 | Comprimento Msg 2 Enc | Comprimento Msg 2 Dec | Comprimento PQ CT | Comprimento opt |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

#### 3) SessionConfirmed

Inalterado

#### Função de Derivação de Chave (KDF) (para fase de dados)

Inalterado

#### Endereços Publicados

Em todos os casos, use o nome do transporte NTCP2 como de costume.

Use o mesmo endereço/porta que o não-PQ, não-firewalled. Apenas uma variante PQ é suportada. No endereço do router, publique v=2 (como de costume) e o novo parâmetro pq=[3|4|5] para indicar MLKEM 512/768/1024. Alice define o MSB da chave efêmera (key[31] & 0x80) na solicitação de sessão para indicar que esta é uma conexão híbrida. Veja acima. Routers mais antigos ignorarão o parâmetro pq e conectarão como não-pq, como de costume.

Endereços com firewall (nenhum IP publicado): No endereço do router, publique v=2 (como de costume). Não há necessidade de publicar um parâmetro pq.

Alice pode se conectar a um Bob PQ usando a variante PQ que Bob publica, independentemente de Alice anunciar suporte pq em suas informações de router, ou se ela anuncia a mesma variante.

Na especificação atual, as mensagens 1 e 2 são definidas para ter uma quantidade "razoável" de preenchimento, com uma faixa de 0-31 bytes recomendada, e nenhum máximo especificado.

#### Preenchimento Máximo

Até a API 0.9.68 (versão 2.11.0), o Java I2P implementava um máximo de 256 bytes de padding para conexões não-PQ, no entanto isso não estava previamente documentado. A partir da API 0.9.69 (versão 2.12.0), o Java I2P implementa o mesmo padding máximo para conexões não-PQ como para MLKEM-512. Veja a tabela abaixo.

Use o tamanho de mensagem definido como o padding máximo, ou seja, o padding máximo dobrará o tamanho da mensagem para conexões PQ, conforme segue:

Use o tamanho de mensagem definido como o preenchimento máximo, ou seja, o preenchimento máximo dobrará o tamanho da mensagem para conexões PQ, da seguinte forma:

| Preenchimento Máximo da Mensagem | não-PQ (até 0.9.68) | não-PQ (a partir de 0.9.69) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|----------------------------------|----------------------|------------------------------|-----------|-----------|------------|
| Session Request  |   256   |   880   |    880   |     1264   |    1648  |
| Session Created  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

Note que MLKEM-1024 NÃO é suportado para SSU2, pois as chaves são muito grandes para caber em um datagrama padrão de 1500 bytes.

#### Identificadores Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

O cabeçalho longo tem 32 bytes. É usado antes de uma sessão ser criada, para Token Request, SessionRequest, SessionCreated e Retry. Também é usado para mensagens Peer Test e Hole Punch fora de sessão.

#### Tamanho da Nova Sessão

Nas mensagens seguintes, defina o campo ver (versão) no cabeçalho longo para 3 ou 4, para indicar MLKEM-512 ou MLKEM-768.

Nas mensagens seguintes, defina o campo ver (version) no cabeçalho longo para 2, como de costume, mesmo se MLKEM-512 ou MLKEM-768 for suportado. As implementações também podem definir o valor para 3 ou 4, se a outra extremidade suportar, mas isso não é necessário. As implementações devem aceitar qualquer valor 2-4.

- (0) Solicitação de Sessão
- (1) Sessão Criada
- (9) Tentar Novamente
- (10) Solicitação de Token
- (11) Perfuração de Hole

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

- (7) Teste de Peer (mensagens fora de sessão 5-7)

Tamanhos, não incluindo overhead do IP:

- Solicitação de Relay
- Resposta de Relay
- Introdução de Relay
- Teste de Peer

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

inalterado

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

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Ofuscação

inalterado

#### SessionRequest (Tipo 0)

Mudança KDF para Proteção contra Spoofing: Para abordar os problemas levantados na Proposta 165 [Prop165]_, mas com uma solução diferente, modificamos o KDF para Session Request. Isso é apenas para sessões PQ. O KDF para sessões não-PQ permanece inalterado.

Conteúdo bruto:

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

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
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
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
MTU mínimo para MLKEM768_X25519: 1318 para IPv4 e 1338 para IPv6. Veja abaixo.

| Tipo | Código do Tipo | Tamanho X | Tamanho Msg 1 | Tamanho Msg 1 Criptografada | Tamanho Msg 1 Descriptografada | Tamanho chave PQ | Tamanho pl |
|------|----------------|-----------|---------------|-------------------------------|----------------------------------|------------------|------------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | muito grande | | | | |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

Mudanças: O SSU2 atual contém apenas os dados do bloco na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

#### SessionCreated (Tipo 1)

Conteúdo bruto:

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Tamanhos:

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
Tamanhos, não incluindo sobrecarga IP:

| Tipo | Código do Tipo | Comprimento de Y | Comprimento da Msg 2 | Comprimento Codificado da Msg 2 | Comprimento Decodificado da Msg 2 | Comprimento do CT PQ | Comprimento do pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | muito grande | | | | |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

Mudanças: O SSU2 atual contém apenas os dados do bloco na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Assinaturas PQ: Blocos de relay, blocos de Peer Test e mensagens de Peer Test contêm todas assinaturas. Infelizmente, as assinaturas PQ são maiores que o MTU. Não existe atualmente um mecanismo para fragmentar blocos de Relay ou Peer Test ou mensagens através de múltiplos pacotes UDP. O protocolo deve ser estendido para suportar fragmentação. Isso será feito numa proposta separada a ser determinada. Até que isso seja completado, Relay e Peer Test não serão suportados.

#### SessionConfirmed (Tipo 2)

inalterado

#### KDF para fase de dados

inalterado

#### Retransmissão e Teste de Pares

Os seguintes blocos contêm campos de versão. Eles permanecerão na versão 2 (para compatibilidade com um Bob não-PQ), e não mudarão para a versão 3/4 para PQ.

- SAMv3
- Bittorrent
- Diretrizes para desenvolvedores
- Nomenclatura / catálogo de endereços / servidores de redirecionamento
- Outros documentos

Em todos os casos, use o nome do transporte SSU2 como de costume. MLKEM-1024 não é suportado.

#### Endereços Publicados

Use o mesmo endereço/porta que não-PQ, não-firewalled. Uma ou ambas as variantes PQ são suportadas. No endereço do router, publique v=2 (como usual) e o novo parâmetro pq=[3|4|3,4|4,3] para indicar MLKEM 512/768/ambos. Routers com MTU menor que o mínimo especificado abaixo não devem publicar um parâmetro "pq" contendo "4". Publique 4,3 para indicar uma preferência por MLKEM-768 ou 3,4 para indicar uma preferência por MLKEM-512. A versão real fica a critério do iniciador, e a preferência pode não ser honrada. Routers com MTU menor que o mínimo especificado abaixo não devem conectar usando MLKEM768. Routers mais antigos irão ignorar o parâmetro pq e conectar não-pq como usual.

Tenha cuidado para não exceder o MTU com MLKEM768. O MTU mínimo para MLKEM768_X25519 é 1318 para IPv4 e 1338 para IPv6 (assumindo um payload mínimo de 10 bytes com um bloco DateTime e um bloco Padding ou RelayTagRequest). O MTU mínimo para SSU2 em geral é 1280, então nem todos os peers podem usar MLKEM768. Não publique ou use MLKEM768 se o MTU real for menor que o mínimo, seja localmente ou como anunciado pelo peer. Tenha cuidado para não incluir tamanho de padding de forma que a mensagem 1 ou 2 excederia o MTU local ou remoto.

Endereços com firewall (nenhum IP publicado): No endereço do router, publique v=2 (como de costume). O parâmetro pq DEVE ser publicado em endereços com firewall, para suportar relay.

Alice pode conectar-se a um Bob PQ usando a variante PQ que Bob publica, independentemente de Alice anunciar ou não o suporte PQ em suas informações de router, ou se ela anuncia a mesma variante.

Na especificação atual, as mensagens 1 e 2 são definidas para ter uma quantidade "razoável" de preenchimento, com uma faixa de 0-31 bytes recomendada, e nenhum máximo especificado.

#### MTU

TODO: Existe uma maneira mais eficiente de definir assinatura/verificação para evitar copiar a assinatura?

### Streaming

TODO

### Arquivos SU3

A seção 8.1 do [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) não permite HashML-DSA em certificados X.509 e não atribui OIDs para HashML-DSA, devido a complexidades de implementação e segurança reduzida.

Para assinaturas apenas PQ de arquivos SU3, use os OIDs definidos no [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) das variantes não-prehash para os certificados. Não definimos assinaturas híbridas de arquivos SU3, porque podemos ter que fazer hash dos arquivos duas vezes (embora HashML-DSA e X2559 usem a mesma função hash SHA512). Além disso, concatenar duas chaves e assinaturas em um certificado X.509 seria completamente fora do padrão.

Note que não permitimos assinatura Ed25519 de arquivos SU3, e embora tenhamos definido assinatura Ed25519ph, nunca concordamos com um OID para ela, ou a usamos.

Os tipos de assinatura normais são proibidos para arquivos SU3; use as variantes ph (prehash).

O novo tamanho máximo de Destination será 2599 (3468 em base 64).

### Outras Especificações

O novo tamanho máximo de Destination será 2599 (3468 em base 64).

Aumento de tamanho (bytes):

- Se a mensagem 1 for menor que 919 bytes, é o protocolo ratchet atual.
- Se a mensagem 1 for maior ou igual a 919 bytes, provavelmente é MLKEM512_X25519.
  Tente MLKEM512_X25519 primeiro e, se falhar, tente o protocolo ratchet atual.

## Análise de Sobrecarga

### Troca de Chaves

Velocidade:

| Tipo | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Velocidades conforme relatado pela [Cloudflare](https://blog.cloudflare.com/pq-2024/):

Resultados preliminares de testes em Java:

| Tipo | Velocidade relativa |
|------|---------------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2,25x mais rápido |
| MLKEM768 | 1,5x mais rápido |
| MLKEM1024 | 1x (mesmo) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4,9x DH = 22% mais lento |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5,3x DH = 32% mais lento |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% mais lento |
Tamanho:

| Tipo | DH/encaps Relativo | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x mais rápido | 22x mais rápido | 17x mais rápido |
| MLKEM768 | 17x mais rápido | 14x mais rápido | 9x mais rápido |
| MLKEM1024 | 12x mais rápido | 10x mais rápido | 6x mais rápido |
### Assinaturas

#### Tamanhos

Velocidade:

| Tipo | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (cada msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Velocidades

Resultados preliminares de testes em Java:

| Tipo | Sinal de velocidade relativa | verificar |
|------|------------------------------|-----------|
| EdDSA_SHA512_Ed25519 | linha de base | linha de base |
| MLDSA44 | 5x mais lento | 2x mais rápido |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Tamanho:

| Tipo | Sinal de velocidade relativa | verificar | keygen |
|------|------------------------------|-----------|--------|
| EdDSA_SHA512_Ed25519 | linha de base | linha de base | linha de base |
| MLDSA44 | 4,6x mais lento | 1,7x mais rápido | 2,6x mais rápido |
| MLDSA65 | 8,1x mais lento | igual | 1,5x mais rápido |
| MLDSA87 | 11,1x mais lento | 1,5x mais lento | igual |
## Análise de Segurança

As categorias de segurança NIST são resumidas no slide 10 da [apresentação NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Critérios preliminares: Nossa categoria mínima de segurança NIST deve ser 2 para protocolos híbridos e 3 para PQ-only.

| Categoria | Tão Seguro Quanto |
|-----------|-------------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Categorias de segurança NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Esta proposta define tanto tipos de assinatura híbridos quanto apenas PQ. O híbrido MLDSA44 é preferível ao MLDSA65 apenas PQ. Os tamanhos de chaves e assinaturas para MLDSA65 e MLDSA87 são provavelmente grandes demais para nós, pelo menos no início.

| Algoritmo | Categoria de Segurança |
|-----------|------------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Assinaturas

Categorias de segurança NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

Embora vamos definir e implementar 3 tipos de criptografia e 9 tipos de assinatura, planejamos medir o desempenho durante o desenvolvimento e analisar ainda mais os efeitos do aumento dos tamanhos das estruturas. Também continuaremos a pesquisar e monitorar desenvolvimentos em outros projetos e protocolos.

| Algoritmo | Categoria de Segurança |
|-----------|------------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Preferências de Tipo

Após desenvolvimento e testes, iremos definir um tipo preferido ou padrão para cada caso de uso. A seleção exigirá fazer compromissos entre largura de banda, CPU e nível de segurança estimado. Nem todos os tipos podem ser adequados ou permitidos para todos os casos de uso.

As preferências preliminares são as seguintes, sujeitas a alterações:

Encryption: MLKEM768_X25519

Assinaturas: MLDSA44_EdDSA_SHA512_Ed25519

As restrições preliminares são as seguintes, sujeitas a alterações:

Assinaturas: MLDSA87 e variante híbrida provavelmente muito grandes; MLDSA65 e variante híbrida podem ser muito grandes

As bibliotecas Bouncycastle, BoringSSL e WolfSSL agora suportam MLKEM e MLDSA. O suporte do OpenSSL estará em sua versão 3.5 lançada em 8 de abril de 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Notas de Implementação

### Suporte de Biblioteca

A biblioteca Noise do southernstorm.com adaptada pelo Java I2P continha suporte preliminar para handshakes híbridos, mas removemos por não estar sendo usado; teremos que adicioná-lo de volta e atualizá-lo para corresponder à [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

Usaremos a variante de assinatura "hedged" ou randomizada, não a variante "determinística", conforme definido na seção 3.4 do [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Isso garante que cada assinatura seja diferente, mesmo quando sobre os mesmos dados, e fornece proteção adicional contra ataques de canal lateral. Embora o [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) especifique que a variante "hedged" é o padrão, isso pode ou não ser verdade em várias bibliotecas. Os implementadores devem garantir que a variante "hedged" seja usada para assinatura.

### Variantes de Assinatura

Utilizamos o processo de assinatura normal (chamado Pure ML-DSA Signature Generation) que codifica a mensagem internamente como 0x00 || len(ctx) || ctx || message, onde ctx é algum valor opcional de tamanho 0x00..0xFF. Não estamos usando nenhum contexto opcional. len(ctx) == 0. Este processo é definido no [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 step 10 e Algorithm 3 step 5. Note que alguns vetores de teste publicados podem requerer a configuração de um modo onde a mensagem não é codificada.

O aumento do tamanho resultará em muito mais fragmentação de tunnel para armazenamentos NetDB, handshakes de streaming e outras mensagens. Verifique mudanças de desempenho e confiabilidade.

### Confiabilidade

Encontre e verifique qualquer código que limite o tamanho em bytes das informações do router e leasesets.

### Tamanhos das Estruturas

Revisar e possivelmente reduzir o máximo de LS/RI armazenados na RAM ou no disco, para limitar o aumento de armazenamento. Aumentar os requisitos mínimos de largura de banda para floodfills?

### NetDB

A classificação/detecção automática de múltiplos protocolos nos mesmos tunnels deve ser possível baseada numa verificação de comprimento da mensagem 1 (New Session Message). Usando MLKEM512_X25519 como exemplo, o comprimento da mensagem 1 é 816 bytes maior que o protocolo ratchet atual, e o tamanho mínimo da mensagem 1 (com apenas um payload DateTime incluído) é 919 bytes. A maioria dos tamanhos de mensagem 1 com ratchet atual tem um payload menor que 816 bytes, então podem ser classificadas como ratchet não-híbrido. Mensagens grandes são provavelmente POSTs que são raras.

### Ratchet

#### Tunnels Compartilhados

Portanto, a estratégia recomendada é:

Isso deve nos permitir suportar eficientemente o ratchet padrão e o ratchet híbrido no mesmo destino, assim como anteriormente suportávamos ElGamal e ratchet no mesmo destino. Portanto, podemos migrar para o protocolo híbrido MLKEM muito mais rapidamente do que se não pudéssemos suportar protocolos duplos para o mesmo destino, porque podemos adicionar suporte MLKEM a destinos existentes.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

As combinações suportadas obrigatórias são:

As seguintes combinações podem ser complexas e NÃO são obrigatórias de serem suportadas, mas podem ser, dependendo da implementação:

- Mais de um MLKEM
- ElG + um ou mais MLKEM
- X25519 + um ou mais MLKEM
- ElG + X25519 + um ou mais MLKEM

Pode ser que não tentemos suportar múltiplos algoritmos MLKEM (por exemplo, MLKEM512_X25519 e MLKEM_768_X25519) no mesmo destino. Escolha apenas um; no entanto, isso depende de selecionarmos uma variante MLKEM preferida, para que os túneis de cliente HTTP possam usar uma. Dependente da implementação.

- Seleção de Noise Hash - manter SHA256 ou atualizar?
  SHA256 deve ser bom por mais 20-30 anos, não ameaçado por PQ,
  Veja [apresentação NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) e [apresentação NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Se SHA256 for quebrado, temos problemas piores (netdb).
- NTCP2 porta separada, endereço de router separado
- SSU2 relay / teste de peer
- Campo de versão SSU2
- Versão de endereço de router SSU2

Nós PODEMOS tentar suportar três algoritmos (por exemplo X25519, MLKEM512_X25519, e MLKEM769_X25519) no mesmo destino. A classificação e estratégia de repetição podem ser muito complexas. A configuração e interface de configuração podem ser muito complexas. Dependente da implementação.

Provavelmente NÃO tentaremos suportar algoritmos ElGamal e híbridos no mesmo destino. ElGamal está obsoleto, e ElGamal + híbrido apenas (sem X25519) não faz muito sentido. Além disso, as Mensagens de Nova Sessão ElGamal e Híbridas são ambas grandes, então as estratégias de classificação muitas vezes teriam que tentar ambas as descriptografias, o que seria ineficiente. Dependente da implementação.

Os clientes podem usar as mesmas chaves estáticas X25519 ou chaves diferentes para os protocolos X25519 e híbrido nos mesmos tunnels, dependendo da implementação.

A especificação ECIES permite Garlic Messages no payload da New Session Message, o que possibilita a entrega 0-RTT do pacote de streaming inicial, geralmente um HTTP GET, juntamente com o leaseset do cliente. No entanto, o payload da New Session Message não possui forward secrecy. Como esta proposta está enfatizando forward secrecy aprimorada para ratchet, as implementações podem ou devem adiar a inclusão do payload de streaming, ou da mensagem de streaming completa, até a primeira Existing Session Message. Isso seria às custas da entrega 0-RTT. As estratégias também podem depender do tipo de tráfego ou tipo de tunnel, ou de GET vs. POST, por exemplo. Dependente da implementação.

#### Forward Secrecy

MLKEM, MLDSA, ou ambos no mesmo destino, aumentará drasticamente o tamanho da Nova Mensagem de Sessão, conforme descrito acima. Isso pode diminuir significativamente a confiabilidade da entrega da Nova Mensagem de Sessão através de tunnels, onde elas devem ser fragmentadas em múltiplas mensagens de tunnel de 1024 bytes. O sucesso da entrega é proporcional ao número exponencial de fragmentos. As implementações podem usar várias estratégias para limitar o tamanho da mensagem, às custas da entrega 0-RTT. Dependente da implementação.

#### Tamanho da Nova Sessão

Definimos o MSB da chave efêmera (key[31] & 0x80) na solicitação de sessão para indicar que esta é uma conexão híbrida. Isso nos permite executar tanto NTCP padrão quanto NTCP híbrido na mesma porta. Apenas uma variante híbrida seria suportada e anunciada no endereço do router. Por exemplo, v=2,3 ou v=2,4 ou v=2,5.

### NTCP2

Como Alice, para uma conexão PQ, antes da ofuscação, defina X[31] |= 0x80. Isso torna X uma chave pública X25519 inválida. Após a ofuscação, AES-CBC irá randomizá-la. O MSB de X será aleatório após a ofuscação.

#### Ofuscação

Como Bob, teste se (X[31] & 0x80) != 0 após a des-ofuscação. Se for o caso, é uma conexão PQ.

A versão mínima do router necessária para NTCP2-PQ está por definir.

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão tipo 4, e o suporte será indicado nos endereços do router.

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

### SSU2

Usamos o campo de versão no cabeçalho longo e o definimos como 3 para MLKEM512 e 4 para MLKEM768. v=2,3,4 no endereço seria suficiente.

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão como tipo 4, e o suporte será indicado nos endereços do router.

## Compatibilidade do Router

### Nomes de Transporte

Em todos os casos, use os nomes de transporte NTCP2 e SSU2 como de costume.

### Tipos de Criptografia do Router

Não recomendado. Use apenas os novos transportes listados acima que correspondem ao tipo de router. Routers mais antigos não conseguem conectar, construir tunnels através, ou enviar mensagens netDb para. Levaria vários ciclos de lançamento para depurar e garantir suporte antes de habilitar por padrão. Pode estender a implementação por um ano ou mais em relação às alternativas abaixo.

#### Routers Tipo 5/6/7

Recomendado. Como PQ não afeta a chave estática X25519 ou protocolos de handshake N, poderíamos deixar os routers como tipo 4, e apenas anunciar novos transportes. Routers mais antigos ainda poderiam conectar, construir tunnels através, ou enviar mensagens netDb para.

#### Routers Tipo 4

MLKEM-768 é recomendado para Ratchet, NTCP2 e SSU2, como o melhor equilíbrio entre segurança e comprimento de chave.

#### Recomendações

Routers mais antigos verificam RIs e, portanto, não conseguem conectar, construir túneis ou enviar mensagens netDb. Levaria vários ciclos de lançamento para depurar e garantir suporte antes de ativar por padrão. Seriam os mesmos problemas do lançamento do tipo de criptografia 5/6/7; pode estender o lançamento por um ano ou mais em relação à alternativa de lançamento do tipo de criptografia tipo 4 listada acima.

### Tipos de Assinatura do Router

#### Routers Tipo 12-17

Nenhuma alternativa.

Estas podem estar presentes no LS com chaves X25519 tipo 4 mais antigas. Routers mais antigos irão ignorar chaves desconhecidas.

### Tipos de Criptografia LS

#### Chaves LS Tipo 5-7

Os destinos podem suportar múltiplos tipos de chave, mas apenas fazendo tentativas de descriptografia da mensagem 1 com cada chave. A sobrecarga pode ser mitigada mantendo contagens de descriptografias bem-sucedidas para cada chave, e tentando primeiro a chave mais usada. O Java I2P usa esta estratégia para ElGamal+X25519 no mesmo destino.

Os routers verificam as assinaturas do leaseSet e, portanto, não conseguem conectar ou receber leaseSets para destinos do tipo 12-17. Seriam necessários vários ciclos de lançamento para depurar e garantir suporte antes de habilitar por padrão.

### Tipos de Assin. de Destino

#### Destinos Tipo 12-17

Nenhuma alternativa.

Estas podem estar presentes no LS com chaves X25519 tipo 4 mais antigas. Routers mais antigos irão ignorar chaves desconhecidas.

## Prioridades e Implementação

Os dados mais valiosos são o tráfego fim-a-fim, criptografado com ratchet. Como um observador externo entre os saltos do tunnel, isso é criptografado duas vezes mais, com criptografia de tunnel e criptografia de transporte. Como um observador externo entre OBEP e IBGW, é criptografado apenas uma vez mais, com criptografia de transporte. Como participante OBEP ou IBGW, ratchet é a única criptografia. No entanto, como os tunnels são unidirecionais, capturar ambas as mensagens no handshake ratchet exigiria routers em conluio, a menos que os tunnels fossem construídos com o OBEP e IBGW no mesmo router.

O modelo de ameaça PQ de quebrar as chaves de autenticação em um período razoável de tempo (digamos alguns meses) e então se passar pela autenticação ou descriptografar em quase tempo real, está muito mais distante? E é quando gostaríamos de migrar para chaves estáticas PQC.

Portanto, o modelo de ameaça PQ mais antigo é OBEP/IBGW armazenando tráfego para descriptografia posterior. Devemos implementar hybrid ratchet primeiro.

Ratchet é a prioridade mais alta. Transportes são os próximos. Assinaturas são a prioridade mais baixa.

O lançamento de assinaturas também será um ano ou mais tarde do que o lançamento de criptografia, porque nenhuma compatibilidade com versões anteriores é possível. Além disso, a adoção do MLDSA na indústria será padronizada pelo CA/Browser Forum e pelas Autoridades Certificadoras. As CAs precisam primeiro de suporte a módulo de segurança de hardware (HSM), que atualmente não está disponível [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Esperamos que o CA/Browser Forum conduza as decisões sobre escolhas específicas de parâmetros, incluindo se deve apoiar ou exigir assinaturas compostas [rascunho IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

Deveríamos conseguir simplesmente tentar um-depois-do-outro, como fizemos com X25519, para ser provado.

O trabalho sobre o suporte à assinatura MLDSA no I2P está suspenso até o final de 2027 ou 2028, aguardando a definição por órgãos de padrões quanto aos algoritmos, possivelmente com redução no tamanho das chaves e/ou assinaturas, além da adoção pela indústria. Veja [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) e [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Além disso, a adoção do MLDSA pela indústria será padronizada pelo IETF, CA/Browser Forum e Autoridades Certificadoras. As ACs precisam, em primeiro lugar, de suporte em módulos de segurança de hardware (HSM), o que atualmente não está disponível [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Espera-se que o IETF e o CA/Browser Forum conduzam as decisões sobre escolhas específicas de parâmetros, incluindo se devem apoiar ou exigir assinaturas compostas [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Marco | Objetivo |
|-------|----------|
| Ratchet beta | Final de 2025 |
| Selecionar melhor tipo de criptografia | Início de 2026 |
| NTCP2 beta | Início de 2026 |
| SSU2 beta | Meio de 2026 |
| Ratchet produção | Meio de 2026 |
| Ratchet padrão | Final de 2026 |
| Signature beta | Final de 2026 |
| NTCP2 produção | Final de 2026 |
| SSU2 produção | Início de 2027 |
| Selecionar melhor tipo de assinatura | Início de 2027 |
| NTCP2 padrão | Início de 2027 |
| SSU2 padrão | Meio de 2027 |
| Signature produção | Meio de 2027 |
## Migração

Devemos ser capazes de simplesmente tentar um e depois o outro, como fizemos com o X25519, para ser comprovado.

Deveríamos ser capazes de simplesmente tentar um e depois o outro, como fizemos com o X25519, para ser comprovado.

## Problemas

O SHA256 deve ser seguro por mais 20-30 anos, sem ameaça do pós-quântico (PQ), veja a [apresentação do NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) e a [apresentação do NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Se o SHA256 for quebrado, teremos problemas maiores (netDb).

## Referências

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
