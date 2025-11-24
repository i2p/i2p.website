---
title: "Protocolos de Criptografia Pós-Quântica"
number: "169"
author: "zzz, original, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Aberto"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Visão Geral

Enquanto a pesquisa e a competição por uma criptografia pós-quântica (PQ) adequada estão em andamento há uma década, as escolhas não se tornaram claras até recentemente.

Começamos a analisar as implicações da cripto PQ em 2022 [FORUM](http://zzz.i2p/topics/3294).

Padrões TLS adicionaram suporte a criptografia híbrida nos últimos dois anos e agora é usado para uma parte significativa do tráfego criptografado na internet devido ao suporte no Chrome e Firefox [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST recentemente finalizou e publicou os algoritmos recomendados para criptografia pós-quântica [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Várias bibliotecas de criptografia comuns agora suportam os padrões NIST ou lançarão suporte em um futuro próximo.

Tanto [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) quanto [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recomendam que a migração comece imediatamente. Veja também o FAQ da NSA PQ de 2022 [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P deve ser um líder em segurança e criptografia. Agora é a hora de implementar os algoritmos recomendados. Usando nosso sistema flexível de tipos de criptografia e tipos de assinatura, adicionaremos tipos para criptografia híbrida e para assinaturas PQ e híbridas.


## Objetivos

- Selecionar algoritmos resistentes a PQ
- Adicionar apenas algoritmos PQ e híbridos aos protocolos I2P onde apropriado
- Definir múltiplas variantes
- Selecionar as melhores variantes após implementação, teste, análise e pesquisa
- Adicionar suporte incrementalmente e com compatibilidade retroativa


## Não-Objetivos

- Não alterar protocolos de criptografia unidirecional (Noise N)
- Não se afastar do SHA256, que não é ameaçado a curto prazo pelo PQ
- Não selecionar as variantes finais preferidas neste momento


## Modelo de Ameaça

- Roteadores no OBEP ou IBGW, possivelmente conluiados, armazenando mensagens de alho para decifração posterior (sigilo a termo)
- Observadores de rede armazenando mensagens de transporte para decifração posterior (sigilo a termo)
- Participantes da rede forjando assinaturas para RI, LS, streaming, datagramas ou outras estruturas


## Protocolos Afetados

Alteraremos os seguintes protocolos, aproximadamente na ordem de desenvolvimento. A implementação geral ocorrerá provavelmente do final de 2025 até meados de 2027. Veja a seção de Prioridades e Implementação abaixo para detalhes.


| Protocolo / Recurso | Status |
| ------------------- | ------ |
| Híbrido MLKEM Ratchet e LS | Aprova |
| Híbrido MLKEM NTCP2 | Alguns |
| Híbrido MLKEM SSU2 | Alguns |
| Tipos de Assinatura MLDSA 12-14 | Propos |
| Destinos MLDSA | Testa |
| Tipos de Assinatura Híbrida 15-17 | relimi |
| Destinos Híbridos |  |




## Design

Suportaremos os padrões NIST FIPS 203 e 204 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) que são baseados, mas NÃO compatíveis, com CRYSTALS-Kyber e CRYSTALS-Dilithium (versões 3.1, 3 e anteriores).



### Troca de Chaves

Suportaremos troca de chaves híbridas nos seguintes protocolos:

| Proto | Tipo Noise | Suporta apenas P | Suporta Híbrid |
| ----- | ---------- | ---------------- | -------------- |
| NTCP2 | XK | não | sim |
| SSU2 | XK | não | sim |
| Ratchet | IK | não | sim |
| TBM | N | não | não |
| NetDB | N | não | não |


PQ KEM fornece apenas chaves efêmeras e não suporta diretamente
handshakes de chave estática como Noise XK e IK.

Noise N não utiliza uma troca de chaves bidirecional e portanto não é adequado
para criptografia híbrida.

Assim, suportaremos apenas criptografia híbrida para NTCP2, SSU2, e Ratchet.
Definiremos as três variantes ML-KEM conforme [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf),
para um total de 3 novos tipos de criptografia.
Tipos híbridos só serão definidos em combinação com X25519.

Os novos tipos de criptografia são:

| Tipo | Códi |
| ---- | ---- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |


A sobrecarga será substancial. Os tamanhos típicos das mensagens 1 e 2 (para XK e IK)
são atualmente em torno de 100 bytes (antes de qualquer carga adicional).
Isso aumentará de 8x a 15x dependendo do algoritmo.


### Assinaturas

Suportaremos assinaturas PQ e híbridas nas seguintes estruturas:

| Tipo | Suporta apenas P | Suporta Híbrid |
| ---- | ---------------- | -------------- |
| RouterInfo | sim | sim |
| LeaseSet | sim | sim |
| Streaming SYN/SYNACK/Close | sim | sim |
| Datagramas Repliações | sim | sim |
| Datagram2 (prop. 163) | sim | sim |
| Mensagem de criação de ses | o I2CP sim | sim |
| Arquivos SU3 | sim | sim |
| Certificados X.509 | sim | sim |
| Java keystores | sim | sim |



Assim, vamos suportar tanto assinaturas apenas PQ quanto híbridas.
Definiremos as três variantes ML-DSA conforme [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf),
três variantes híbridas com Ed25519,
e três variantes apenas PQ com prehash apenas para arquivos SU3,
para um total de 9 novos tipos de assinatura.
Os tipos híbridos só serão definidos em combinação com Ed25519.
Usaremos o ML-DSA padrão, NÃO as variantes de pré-hash (HashML-DSA),
exceto para arquivos SU3.

Usaremos a variante de assinatura "hedged" ou aleatória,
não a variante "determinística", conforme definido em [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) seção 3.4.
Isso garante que cada assinatura seja diferente, mesmo quando sobre os mesmos dados,
e fornece proteção adicional contra ataques de canal lateral.
Veja a seção de notas de implementação abaixo para detalhes adicionais
sobre as escolhas de algoritmo, incluindo codificação e contexto.


Os novos tipos de assinatura são:

| Tipo | Códi |
| ---- | ---- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |


Certificados X.509 e outras codificações DER usarão as
estruturas compostas e OIDs definidos em [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).

A sobrecarga será substancial. Os tamanhos típicos para destinos e identidades de roteador Ed25519
são 391 bytes.
Esses tamanhos aumentarão de 3,5x a 6,8x dependendo do algoritmo.
Assinaturas Ed25519 são 64 bytes.
Esses tamanhos aumentarão de 38x a 76x dependendo do algoritmo.
Os tamanhos típicos para RouterInfo assinado, LeaseSet, datagramas repliáveis, e mensagens de streaming assinadas são cerca de 1KB.
Esses tamanhos aumentarão de 3x a 8x dependendo do algoritmo.

Como os novos tipos de destino e identidade de roteador não conterão preenchimento,
eles não serão compressíveis. Os tamanhos de destinos e identidades de roteador
que são compactados em trânsito aumentarão de 12x - 38x dependendo do algoritmo.



### Combinações Legais

Para Destinations, os novos tipos de assinatura são suportados com todos os tipos de criptografia
no leaseset. Defina o tipo de criptografia no certificado de chave como NONE (255).

Para RouterIdentities, o tipo de criptografia ElGamal está obsoleto.
Os novos tipos de assinatura são suportados apenas com criptografia X25519 (tipo 4).
Os novos tipos de criptografia serão indicados nos RouterAddresses.
O tipo de criptografia no certificado de chave continuará a ser o tipo 4.



### Cripto Nova Necessária

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anteriormente CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS202]_ Usado apenas para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS202]_
- SHAKE128 e SHAKE256 (extensões XOF para SHA3-128 e SHA3-256) [FIPS202]_

Vetores de teste para SHA3-256, SHAKE128, e SHAKE256 estão em [NIST-VECTORS]_.

Observe que a biblioteca Java Bouncycastle suporta todos os itens acima.
O suporte da biblioteca C++ está no OpenSSL 3.5 [OPENSSL]_.


### Alternativas

Não suportaremos [FIPS205]_ (Sphincs+), pois é muito mais lento e maior que ML-DSA.
Não suportaremos o próximo FIPS206 (Falcon), pois ainda não está padronizado.
Não suportaremos NTRU ou outros candidatos PQ que não foram padronizados pelo NIST.


Rosenpass
`````````

Existe alguma pesquisa [PQ-WIREGUARD]_ sobre adaptação do Wireguard (IK)
para cripto puramente PQ, mas existem várias questões abertas nesse artigo.
Mais tarde, essa abordagem foi implementada como Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_
para Wireguard PQ.

Rosenpass usa um handshake semelhante ao Noise KK com chaves estáticas Classic McEliece 460896 pré-compartilhadas
(500 KB cada) e chaves efêmeras Kyber-512 (essencialmente MLKEM-512).
Como os textos cifrados Classic McEliece têm apenas 188 bytes, e as chaves públicas e textos cifrados Kyber-512
são razoáveis, ambas as mensagens de handshake cabem em um MTU padrão de UDP.
A chave compartilhada de saída (osk) do handshake PQ KK é usada como a chave pré-compartilhada de entrada (psk)
para o handshake padrão Wireguard IK.
Portanto, existem dois handshakes completos no total, um puramente PQ e um puramente X25519.

Não podemos fazer nada disso para substituir nossos handshakes XK e IK porque:

- Não podemos fazer KK, Bob não tem a chave estática de Alice
- Chaves estáticas de 500KB são grandes demais
- Não queremos uma rodada extra de ida e volta

Há muita informação boa no whitepaper,
e vamos revisá-la para ideias e inspiração. TODO.



## Especificação

### Estruturas Comuns

Atualizar as seções e tabelas no documento de estruturas comuns [COMMON](https://geti2p.net/spec/common-structures) como segue:


PublicKey
````````````````

Os novos tipos de Chave Pública são:

| Tipo | Comprimento da Ch | ve Púb | ca De |
| ---- | ----------------- | ------ | ----- |
| MLKEM512_X25519 | 32 | 0.9.xx | Veja |
| MLKEM768_X25519 | 32 | 0.9.xx | Veja |
| MLKEM1024_X25519 | 32 | 0.9.xx | Veja |
| MLKEM512 | 800 | 0.9.xx | Veja |
| MLKEM768 | 1184 | 0.9.xx | Veja |
| MLKEM1024 | 1568 | 0.9.xx | Veja |
| MLKEM512_CT | 768 | 0.9.xx | Veja |
| MLKEM768_CT | 1088 | 0.9.xx | Veja |
| MLKEM1024_CT | 1568 | 0.9.xx | Veja |
| NONE | 0 | 0.9.xx | Veja |


Chaves públicas híbridas são a chave X25519.
Chaves públicas KEM são a chave PQ efêmera enviada de Alice para Bob.
A codificação e a ordem de bytes são definidas em [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Chaves MLKEM*_CT não são realmente chaves públicas, elas são o "texto cifrado" enviado de Bob para Alice no handshake Noise.
Elas estão listadas aqui para completar.



PrivateKey
````````````````

Os novos tipos de Chave Privada são:

| Tipo | Comprimento da Cha | e Priv | a Des |
| ---- | ------------------ | ------ | ----- |
| MLKEM512_X25519 | 32 | 0.9.xx | Veja |
| MLKEM768_X25519 | 32 | 0.9.xx | Veja |
| MLKEM1024_X25519 | 32 | 0.9.xx | Veja |
| MLKEM512 | 1632 | 0.9.xx | Veja |
| MLKEM768 | 2400 | 0.9.xx | Veja |
| MLKEM1024 | 3168 | 0.9.xx | Veja |


Chaves privadas híbridas são as chaves X25519.
As chaves privadas KEM são apenas para Alice.
A codificação e a ordem de bytes da KEM são definidas em [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).




SigningPublicKey
````````````````

Os novos tipos de Chave Pública de Assinatura são:

| Tipo | Comprimento (b | es)  D | de |
| ---- | -------------- | ------ | --- |
| MLDSA44 | 1312 | 0.9.xx | Veja |
| MLDSA65 | 1952 | 0.9.xx | Veja |
| MLDSA87 | 2592 | 0.9.xx | Veja |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Veja |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Veja |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Veja |
| MLDSA44ph | 1344 | 0.9.xx | Apena |
| MLDSA65ph | 1984 | 0.9.xx | Apena |
| MLDSA87ph | 2624 | 0.9.xx | Apena |


Chaves públicas de assinatura híbridas são a chave Ed25519 seguida pela chave PQ, conforme em [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
A codificação e a ordem de bytes são definidas em [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).


SigningPrivateKey
`````````````````

Os novos tipos de Chave Privada de Assinatura são:

| Tipo | Comprimento (b | es)  D | de |
| ---- | -------------- | ------ | --- |
| MLDSA44 | 2560 | 0.9.xx | Veja |
| MLDSA65 | 4032 | 0.9.xx | Veja |
| MLDSA87 | 4896 | 0.9.xx | Veja |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Veja |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Veja |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Veja |
| MLDSA44ph | 2592 | 0.9.xx | Apena |
| MLDSA65ph | 4064 | 0.9.xx | Apena |
| MLDSA87ph | 4928 | 0.9.xx | Apena |


Chaves privadas de assinatura híbridas são a chave Ed25519 seguida pela chave PQ, conforme em [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
A codificação e a ordem de bytes são definidas em [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).


Signature
``````````

Os novos tipos de Assinatura são:

| Tipo | Comprimento (b | es)  D | de |
| ---- | -------------- | ------ | --- |
| MLDSA44 | 2420 | 0.9.xx | Veja |
| MLDSA65 | 3309 | 0.9.xx | Veja |
| MLDSA87 | 4627 | 0.9.xx | Veja |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Veja |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Veja |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Veja |
| MLDSA44ph | 2484 | 0.9.xx | Apena |
| MLDSA65ph | 3373 | 0.9.xx | Apena |
| MLDSA87ph | 4691 | 0.9.xx | Apena |


Assinaturas híbridas são a assinatura Ed25519 seguida pela assinatura PQ, conforme em [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Assinaturas híbridas são verificadas verificando ambas as assinaturas, e falhando
se qualquer uma delas falhar.
A codificação e a ordem de bytes são definidas em [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).



Certificados de Chave
``````````````````````

Os novos tipos de Chave Pública de Assinatura são:

| Tipo | Código Tipo | Comprimento Total da Ch | e Públ | a  De |
| ---- | ----------- | ----------------------- | ------ | ----- |
| MLDSA44 | 12 | 1312 | 0.9.xx | Veja |
| MLDSA65 | 13 | 1952 | 0.9.xx | Veja |
| MLDSA87 | 14 | 2592 | 0.9.xx | Veja |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Veja |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Veja |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Veja |
| MLDSA44ph | 18 | n/a | 0.9.xx | Apena |
| MLDSA65ph | 19 | n/a | 0.9.xx | Apena |
| MLDSA87ph | 20 | n/a | 0.9.xx | Apena |




Os novos tipos de Chave Pública Cripto são:

| Tipo | Código Tipo | Comprimento Total da Ch | ve Púb | ca De |
| ---- | ----------- | ----------------------- | ------ | ----- |
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Veja |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Veja |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Veja |
| NONE | 255 | 0 | 0.9.xx | Veja |



Tipos de chave híbrida NUNCA são incluídos em certificados de chave; apenas em leasesets.

Para destinos com tipos de assinatura híbrida ou PQ,
use NONE (tipo 255) para o tipo de criptografia,
mas não há chave de criptografia, e a
seção principal de 384 bytes é para a chave de assinatura.


Tamanhos de Destination
```````````````````````

Aqui estão os comprimentos para os novos tipos de Destination.
Tipo de criptografia para todos é NONE (tipo 255) e o comprimento da chave de criptografia é tratado como 0.
A seção inteira de 384 bytes é usada para a primeira parte da chave pública de assinatura.
NOTA: Isso é diferente da especificação para os tipos de assinatura ECDSA_SHA512_P521
e RSA, onde mantivemos a chave ElGamal de 256 bytes no destino mesmo que não fosse usada.

Sem preenchimento.
O comprimento total é 7 + comprimento total da chave.
O comprimento do certificado de chave é 4 + comprimento excedente da chave.

Exemplo de fluxo de bytes de destino de 1319 bytes para MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]



| Tipo | Código Tipo | Comprimento Total da Ch | e Públ | a  Pri | ipal |
| ---- | ----------- | ----------------------- | ------ | ------ | ---- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |




Tamanhos de RouterIdent
```````````````````````

Aqui estão os comprimentos para os novos tipos de Destination.
Tipo de criptografia para todos é X25519 (tipo 4).
A seção inteira de 352 bytes após a chave pública X28819 é usada para a primeira parte da chave pública de assinatura.
Sem preenchimento.
O comprimento total é 39 + comprimento total da chave.
O comprimento do certificado de chave é 4 + comprimento excedente da chave.

Exemplo de fluxo de bytes de identidade de roteador de 1351 bytes para MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]



| Tipo | Código Tipo | Comprimento Total da Ch | e Públ | a  Pri | ipal |
| ---- | ----------- | ----------------------- | ------ | ------ | ---- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |




### Padrões de Handshake

Handshakes usam padrões de handshake [Noise]_.

A seguinte correspondência de letras é usada:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem
- e1 = chave efêmera PQ de uso único, enviada de Alice para Bob
- ekem1 = o texto cifrado KEM, enviado de Bob para Alice

As seguintes modificações para XK e IK para sigilo híbrido (hfs) são como especificado em [Noise-Hybrid]_ seção 5:

```dataspec

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

O padrão e1 é definido como segue, conforme especificado na seção 4 de [Noise-Hybrid]_ :

```dataspec

Para Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  Para Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)


```


O padrão ekem1 é definido como segue, conforme especificado na seção 4 de [Noise-Hybrid]_ :

```dataspec

Para Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  Para Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)


```




### Função de Derivação de Chave de Handshake (KDF)

Problemas
````````

- Devemos mudar a função hash do handshake? Veja [Escolha do Hash]_.
  SHA256 não é vulnerável ao PQ, mas se quisermos atualizar
  nossa função hash, agora é a hora, enquanto estamos mudando outras coisas.
  A proposta atual da IETF para SSH [SSH-HYBRID]_ é usar MLKEM768
  com SHA256, e MLKEM1024 com SHA384. Essa proposta inclui
  uma discussão das considerações de segurança.
- Devemos parar de enviar dados de aumento de chave de 0-RTT (exceto o LS)?
- Devemos mudar o aumento de chave de IK para XK se não enviarmos dados de 0-RTT?


Visão Geral
````````

Esta seção se aplica aos protocolos IK e XK.

O handshake híbrido é definido em [Noise-Hybrid]_.
A primeira mensagem, de Alice para Bob, contém e1, a chave de encapsulamento, antes da carga útil da mensagem.
Isso é tratado como uma chave estática adicional; chama-se EncryptAndHash() sobre ela (como Alice)
ou DecryptAndHash() (como Bob).
Então processa-se a carga útil da mensagem normalmente.

A segunda mensagem, de Bob para Alice, contém ekem1, o texto cifrado, antes da carga útil da mensagem.
Isso é tratado como uma chave estática adicional; chama-se EncryptAndHash() sobre ela (como Bob)
ou DecryptAndHash() (como Alice).
Em seguida, calcula-se a chave compartilhada kem_shared_key e chama-se MixKey(kem_shared_key).
Então processa-se a carga útil da mensagem normalmente.


Operações Definidas do ML-KEM
`````````````````````````````

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos usados
conforme definido em [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()
    Alice cria as chaves de encapsulamento e decapsulamento
    A chave de encapsulamento é enviada na mensagem 1.
    Os tamanhos de encap_key e decap_key variam com base na variante ML-KEM.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob calcula o texto cifrado e a chave compartilhada,
    usando o texto cifrado recebido na mensagem 1.
    O texto cifrado é enviado na mensagem 2.
    O tamanho do texto cifrado varia com base na variante ML-KEM.
    A chave compartilhada kem_shared_key tem sempre 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)
    Alice calcula a chave compartilhada,
    usando o texto cifrado recebido na mensagem 2.
    A chave compartilhada kem_shared_key tem sempre 32 bytes.

Observe que tanto a encap_key quanto o texto cifrado são criptografados dentro dos blocos ChaCha/Poly
nas mensagens de handshake 1 e 2.
Eles serão decodificados como parte do processo de handshake.

A chave compartilhada kem_shared_key é misturada na chave de encadeamento com MixHash().
Veja abaixo para detalhes.


KDF para Mensagem 1 de Alice
```````````````````````````

Para XK: Após o padrão de mensagem 'es' e antes da carga útil, adicione:

OU

Para IK: Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicione:

```text
Este é o padrão de mensagem "e1":
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  Fim do padrão de mensagem "e1".

  NOTA: Para a próxima seção (carga útil para XK ou chave estática para IK),
  os dados de chave e a chave de encadeamento permanecem os mesmos,
  e n agora é igual a 1 (em vez de 0 para não híbrido).

```


KDF para Mensagem 1 de Bob
```````````````````````````

Para XK: Após o padrão de mensagem 'es' e antes da carga útil, adicione:

OU

Para IK: Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicione:

```text
Este é o padrão de mensagem "e1":

  // DecryptAndHash(encap_key_section)
  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  Fim do padrão de mensagem "e1".

  NOTA: Para a próxima seção (carga útil para XK ou chave estática para IK),
  os dados de chave e a chave de encadeamento permanecem os mesmos,
  e n agora é igual a 1 (em vez de 0 para não híbrido).

```


KDF para Mensagem 2 de Bob
```````````````````````````

Para XK: Após o padrão de mensagem 'ee' e antes da carga útil, adicione:

OU

Para IK: Após o padrão de mensagem 'ee' e antes do padrão de mensagem 'se', adicione:

```text
Este é o padrão de mensagem "ekem1":

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Fim do padrão de mensagem "ekem1".

```


KDF para Mensagem 2 de Alice
```````````````````````````

Após o padrão de mensagem 'ee' (e antes do padrão de mensagem 'ss' para IK), adicione:

```text
Este é o padrão de mensagem "ekem1":

  // DecryptAndHash(kem_ciphertext_section)
  // Parâmetros AEAD
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

  Fim do padrão de mensagem "ekem1".

```


KDF para Mensagem 3 (apenas XK)
```````````````````````````````
inalterado


KDF para split()
`````````````````
inalterado



### Ratchet

Atualizar a especificação ECIES-Ratchet [ECIES](https://geti2p.net/spec/ecies) como segue:


Identificadores Noise
`````````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"



1b) Novo formato de sessão (com vinculação)
``````````````````````````````````````````

Alterações: O ratchet atual continha a chave estática na primeira seção ChaCha,
e a carga útil na segunda seção.
Com o ML-KEM, agora há três seções.
A primeira contém a chave pública PQ criptografada.
A segunda contém a chave estática.
A terceira contém a carga útil.


Formato criptografado:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nova Sessão Chave Pública Efêmera   |
  +             32 bytes                  +
  |     Codificado com Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Chave encap ML-KEM          +
  |       Dados criptografados ChaCha20   |
  +      (veja a tabela abaixo para comprimento) +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação da Mensagem Poly1305 |
  +    (MAC) para Seção encap_key        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Chave Estática X25519       +
  |       Dados criptografados ChaCha20   |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação da Mensagem Poly1305 |
  +    (MAC) para Seção de Chave Estática       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Carga Útil        +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação da Mensagem Poly1305 |
  +    (MAC) para Seção de Carga Útil     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+


```

Formato decodificado:

```dataspec
Parte 1 da Carga Útil:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +           chave encap do ML-KEM       +
  |                                       |
  +      (veja a tabela abaixo para comprimento)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Parte 2 da Carga Útil:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Chave Estática X25519           +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Parte 3 da Carga Útil:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Carga Útil        +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamanhos:

| Tipo | Código Ti | X l | Comp Ms | 1  Comp Enc M | 1  Comp Dec | g 1  Compr | ento da |
| ---- | --------- | --- | ------- | ------------- | ----------- | ---------- | ------- |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |


Note que a carga útil deve conter um bloco DateTime, então o tamanho mínimo da carga útil é 7.
Os tamanhos mínimos da mensagem 1 podem ser calculados de acordo.



1g) Novo formato de resposta de sessão
````````````````````````````````````

Alterações: O ratchet atual tem uma carga útil vazia para a primeira seção ChaCha,
e a carga útil na segunda seção.
Com o ML-KEM, há agora três seções.
A primeira seção contém o texto cifrado PQ criptografado.
A segunda seção tem uma carga útil vazia.
A terceira seção contém a carga útil.


Formato criptografado:

```dataspec
+----+----+----+----+----+----+----+----+
  |       Marcador de Sessão 8 bytes      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Chave Pública Efêmera          +
  |                                       |
  +            32 bytes                   +
  |     Codificado com Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | Texto cifrado ChaCha20 do ML-KEM      |
  +      (veja a tabela abaixo para comprimento)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação da Mensagem Poly1305 |
  +  (MAC) para Seção de texto cifrado    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação da Mensagem Poly1305 |
  +  (MAC) para Seção de chave (sem dados)       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Carga Útil        +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação da Mensagem Poly1305 |
  +    (MAC) para Seção de Carga Útil     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+


```

Formato decodificado:

```dataspec
Parte 1 da Carga Útil:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Texto cifrado do ML-KEM         +
  |                                       |
  +      (veja a tabela abaixo para comprimento)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Parte 2 da Carga Útil:

  vazia

  Parte 3 da Carga Útil:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Carga Útil        +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamanhos:

| Tipo | Código Ti | Y l | Comp Ms | 2  Comp Enc M | 2  Comp Dec | g 2  Compr | ento CT |
| ---- | --------- | --- | ------- | ------------- | ----------- | ---------- | ------- |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |


Note que enquanto a mensagem 2 normalmente terá uma carga útil não nula,
a especificação do ratchet [ECIES](https://geti2p.net/spec/ecies) não a exige, então o tamanho mínimo da carga útil é 0.
Os tamanhos mínimos da mensagem 2 podem ser calculados de acordo.



### NTCP2

Atualizar a especificação NTCP2 [NTCP2](https://geti2p.net/spec/ntcp2) como segue:


Identificadores Noise
`````````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


1) Solicitação de Sessão
````````````````````````

Alterações: O NTCP2 atual contém apenas as opções na seção ChaCha.
Com o ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.


Conteúdos brutos:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        ofuscado com RH_B           +
  |      Chave AES-CBC-256 criptografada X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Quadro ChaChaPoly (MLKEM)           |
  +      (veja a tabela abaixo para comprimento)     +
  |   k definido no KDF para mensagem 1      |
  +   n = 0                               +
  |   veja KDF para dados associados         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | Quadro ChaChaPoly (opções)          |
  +         32 bytes                      +
  |   k definido no KDF para mensagem 1      |
  +   n = 0                               +
  |   veja KDF para dados associados         |
  +----+----+----+----+----+----+----+----+
  |     preenchimento autenticado não criptografado        |
  ~         comprimento definido no bloco de opções            ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Igual a antes exceto para adicionar um segundo Quadro ChaChaPoly


```

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           chave encap do ML-KEM       |
  +      (veja a tabela abaixo para comprimento)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               opções                  |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     preenchimento autenticado não criptografado        |
  +         comprimento definido no bloco de opções            +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+



```

Tamanhos:

| Tipo | Código Ti | Com | com X  C | pr Msg 1  Com | Enc Msg 1  C | pr Dec Msg | Compr |
| ---- | --------- | --- | -------- | ------------- | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |


Nota: Os códigos dos tipos são apenas para uso interno. Os roteadores permanecerão tipo 4,
e o suporte será indicado nos endereços do roteador.


2) Sessão Criada
``````````````````

Alterações: O NTCP2 atual contém apenas as opções na seção ChaCha.
Com o ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.


Conteúdos brutos:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        ofuscado com RH_B           +
  |     Chave AES-CBC-256 criptografada Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Quadro ChaChaPoly (MLKEM)           |
  +     Dados criptografados e autenticados    +
  -      (veja a tabela abaixo para comprimento)     -
  +   k definido no KDF para mensagem 2      +
  |   n = 0; veja KDF para dados associados  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Quadro ChaChaPoly (opções)           |
  +     Dados criptografados e autenticados    +
  -           32 bytes                    -
  +   k definido no KDF para mensagem 2      +
  |   n = 0; veja KDF para dados associados  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     preenchimento autenticado não criptografado        |
  +         comprimento definido no bloco de opções            +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Igual a antes exceto para adicionar um segundo Quadro ChaChaPoly

```

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Texto cifrado do ML-KEM     |
  +      (veja a tabela abaixo para comprimento)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               opções                  |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     preenchimento autenticado não criptografado        |
  +         comprimento definido no bloco de opções            +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamanhos:

| Tipo | Código Ti | Com | com Y  C | pr Msg 2  Com | Enc Msg 2  C | pr Dec Msg | Compr |
| ---- | --------- | --- | -------- | ------------- | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |


Nota: Os códigos dos tipos são apenas para uso interno. Os roteadores permanecerão tipo 4,
e o suporte será indicado nos endereços do roteador.



3) Sessão Confirmada
```````````````````

Inalterado


Função de Derivação de Chave (KDF) (para fase de dados)
``````````````````````````````````````````````

Inalterado




### SSU2

Atualizar a especificação SSU2 [SSU2](https://geti2p.net/spec/ssu2) como segue:


Identificadores Noise
`````````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


Cabeçalho Longo
```````````````
O cabeçalho longo tem 32 bytes. É usado antes de uma sessão ser criada, para Solicitação de Token, Sessão Criada, e Tentativa.
Também é usado para Teste de Usuário fora da sessão e mensagens de Perfuração de Buraco.

TODO: Poderíamos usar internamente o campo de versão e usar 3 para MLKEM512 e 4 para MLKEM768.
Apenas fazemos isso para tipos 0 e 1 ou para todos os 6 tipos?


Antes de criptografar o cabeçalho:

```dataspec

+----+----+----+----+----+----+----+----+
  |      ID de Conexão de Destino         |
  +----+----+----+----+----+----+----+----+
  |   Número de Pacote   |tipo| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        ID de Conexão de Origem        |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  ID de Conexão de Destino :: 8 bytes, inteiro não assinado em big endian

  Número de Pacote :: 4 bytes, inteiro não assinado em big endian

  tipo :: O tipo de mensagem = 0, 1, 7, 9, 10, ou 11

  ver :: A versão do protocolo, igual a 2
         TODO Poderíamos usar internamente o campo de versão e usar 3 para MLKEM512 e 4 para MLKEM768.

  id :: 1 byte, o ID da rede (atualmente 2, exceto para redes de teste)

  flag :: 1 byte, não utilizado, definido como 0 para compatibilidade futura

  ID de Conexão de Origem :: 8 bytes, inteiro não assinado em big endian

  Token :: 8 bytes, inteiro não assinado em big endian

```


Cabeçalho Curto
```````````````
inalterado


Solicitação de Sessão (Tipo 0)
`````````````````````````

Alterações: O SSU2 atual contém apenas os dados do bloco na seção ChaCha.
Com o ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.


Conteúdos brutos:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Bytes 0-15 do Cabeçalho Longo, ChaCha20     |
  +  criptografado com a chave de introdução de Bob        +
  |    Veja o KDF para Criptografia de Cabeçalho          |
  +----+----+----+----+----+----+----+----+
  |  Bytes 16-31 do Cabeçalho Longo, ChaCha20    |
  +  criptografado com a introdução de Bob n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, criptografado com ChaCha20           +
  |       com introdução de Bob n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | Dados criptografados com ChaCha20 (MLKEM)     |
  +          (comprimento varia)              +
  |  k definido no KDF para Solicitação de Sessão |
  +  n = 0                                +
  |  veja KDF para dados associados          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | Dados criptografados com ChaCha20 (carga útil)   |
  +          (comprimento varia)              +
  |  k definido no KDF para Solicitação de Sessão |
  +  n = 0                                +
  |  veja KDF para dados associados          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        MAC Poly1305 (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |      ID de Conexão de Destino         |
  +----+----+----+----+----+----+----+----+
  |   Número de Pacote   |tipo| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        ID de Conexão de Origem        |
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
  |           chave encap do ML-KEM       |
  +      (veja a tabela abaixo para comprimento)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Carga útil de noise (dados do bloco)        |
  +          (comprimento varia)              +
  |     veja abaixo para blocos permitidos      |
  +----+----+----+----+----+----+----+----+


```

Tamanhos, sem incluir overhead de IP:

| Tipo | Código Ti | Com | com X  C | pr Msg 1  Com | Enc Msg 1  C | pr Dec Msg | Compr |
| ---- | --------- | --- | -------- | ------------- | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | muito gra | e |  |  |  |


Nota: Os códigos dos tipos são apenas para uso interno. Os roteadores permanecerão tipo 4,
e o suporte será indicado nos endereços do roteador.

MTU mínimo para MLKEM768_X25519:
Cerca de 1316 para IPv4 e 1336 para IPv6.



Sessão Criada (Tipo 1)
``````````````````````
Alterações: O SSU2 atual contém apenas os dados do bloco na seção ChaCha.
Com o ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.


Conteúdos brutos:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Bytes 0-15 do Cabeçalho Longo, ChaCha20     |
  +  criptografado com a chave de introdução de Bob e    +
  | derivada de chave, veja KDF para Criptografia de Cabeçalho |
  +----+----+----+----+----+----+----+----+
  |  Bytes 16-31 do Cabeçalho Longo, ChaCha20    |
  +  criptografado com chave derivada n=0       +
  |  Veja o KDF para Criptografia de Cabeçalho            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, criptografado com ChaCha20           +
  |       com chave derivada n=0            |
  +              (32 bytes)               +
  |       Veja o KDF para Criptografia de Cabeçalho       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Dados do ChaCha20 (MLKEM)               |
  +     Dados criptografados e autenticados    +
  |  comprimento varia                        |
  +  k definido no KDF para Sessão Criada     +
  |  n = 0; veja KDF para dados associados    |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Dados do ChaCha20 (carga útil)             |
  +     Dados criptografados e autenticados    +
  |  comprimento varia                        |
  +  k definido no KDF para Sessão Criada     +
  |  n = 0; veja KDF para dados associados    |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        MAC Poly1305 (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |      ID de Conexão de Destino         |
  +----+----+----+----+----+----+----+----+
  |   Número de Pacote   |tipo| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        ID de Conexão de Origem        |
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
  |           Texto cifrado do ML-KEM      |
  +      (veja a tabela abaixo para comprimento)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Carga útil de noise (dados do bloco)        |
  +          (comprimento varia)              +
  |      veja abaixo para blocos permitidos     |
  +----+----+----+----+----+----+----+----+

```

Tamanhos, sem incluir overhead de IP:

| Tipo | Código Ti | Com | com Y  C | pr Msg 2  Com | Enc Msg 2  C | pr Dec Msg | Compr |
| ---- | --------- | --- | -------- | ------------- | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | muito gra | e |  |  |  |


Nota: Os códigos dos tipos são apenas para uso interno. Os roteadores permanecerão tipo 4,
e o suporte será indicado nos endereços do roteador.

MTU mínimo para MLKEM768_X25519:
Cerca de 1316 para IPv4 e 1336 para IPv6.


Sessão Confirmada (Tipo 2)
`````````````````````````
inalterado



KDF para fase de dados
```````````````````````
inalterado



Retransmissão e Teste de Usuário
````````````````````

Blocos de Retransmissão, blocos de Teste de Usuário, e mensagens de Teste de Usuário contêm assinaturas.
Infelizmente, as assinaturas PQ são maiores que o MTU.
Não há mecanismo atual para fragmentar blocos ou mensagens de Retransmissão ou de Teste de Usuário
em múltiplos pacotes UDP.
O protocolo deve ser estendido para suportar fragmentação.
Isso será feito em uma proposta separada, a ser definida (TBD).
Até que isso seja completado, retransmissão e teste de usuário não serão suportados.


Problemas
``````

Poderíamos usar internamente o campo de versão e usar 3 para MLKEM512 e 4 para MLKEM768.

Para as mensagens 1 e 2, MLKEM768 aumentaria os tamanhos dos pacotes além do MTU mínimo de 1280.
Provavelmente não suportaríamos para essa conexão se o MTU fosse muito baixo.

Para as mensagens 1 e 2, o MLKEM1024 aumentaria os tamanhos dos pac
