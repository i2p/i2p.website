---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Open"
thread: "http://zzz.i2p/topics/2418"
---

## Motivação

O ECIES-P256 é muito mais rápido que o ElGamal. Já existem alguns eepsites i2pd com o tipo de criptografia ECIES-P256 e o Java deve ser capaz de se comunicar com eles e vice-versa. O i2pd suporta desde a versão 2.16.0 (0.9.32 Java).

## Visão Geral

Esta proposta introduz o novo tipo de criptografia ECIES-P256 que pode aparecer na parte do certificado de identidade, ou como um tipo de chave de criptografia separado no LeaseSet2.
Pode ser usado em RouterInfo, LeaseSet1 e LeaseSet2.

### Localizações das Chaves ElGamal

Como revisão,
Chaves públicas ElGamal de 256 bytes podem ser encontradas nas seguintes estruturas de dados.
Consulte a especificação de estruturas comuns.

- Em uma Identidade de Roteador
  Esta é a chave de criptografia do roteador.

- Em um Destino
  A chave pública do destino foi usada para a antiga criptografia i2cp-para-i2cp
  que foi desativada na versão 0.6, atualmente está sem uso exceto para
  o IV para criptografia LeaseSet, que está obsoleto.
  A chave pública no LeaseSet é usada em seu lugar.

- Em um LeaseSet
  Esta é a chave de criptografia do destino.

Nos 3 acima, a chave pública ECIES ainda ocupa 256 bytes, embora o comprimento real da chave seja de 64 bytes.
O restante deve ser preenchido com preenchimento aleatório.

- Em um LS2
  Esta é a chave de criptografia do destino. O tamanho da chave é de 64 bytes.

### Tipos de Criptografia em Certificados de Chave

ECIES-P256 usa o tipo de criptografia 1.
Os tipos de criptografia 2 e 3 devem ser reservados para ECIES-P284 e ECIES-P521.

### Usos de Criptografia Assimétrica

Esta proposta descreve a substituição do ElGamal para:

1) Mensagens de Construção de Túnel (a chave está em RouterIdentity). O bloco ElGamal é de 512 bytes
  
2) Criptografia de Extremidade a Extremidade do Cliente ElGamal+AES/SessionTag (a chave está em LeaseSet, a chave do Destino está sem uso). O bloco ElGamal é de 514 bytes

3) Criptografia de roteador para roteador de netdb e outras mensagens I2NP. O bloco ElGamal é de 514 bytes

### Objetivos

- Compatível com versões anteriores
- Sem alterações para estrutura de dados existente
- Muito mais eficiente em termos de CPU do que o ElGamal

### Não-Objetivos

- RouterInfo e LeaseSet1 não podem publicar ElGamal e ECIES-P256 juntos

### Justificativa

O motor ElGamal/AES+SessionTag sempre fica preso na falta de tags, o que produz uma degradação dramática de desempenho nas comunicações I2P.
A construção de túneis é a operação mais pesada porque o originador deve executar a criptografia ElGamal 3 vezes para cada solicitação de construção de túnel.

## Primitivas Criptográficas Necessárias

1) Geração de chave e DH da curva EC P256

2) AES-CBC-256

3) SHA256

## Proposta Detalhada

Um destino com ECIES-P256 se publica com o tipo de criptografia 1 no certificado.
Os primeiros 64 bytes dos 256 na identidade devem ser interpretados como a chave pública ECIES e o restante deve ser ignorado.
A chave de criptografia separada do LeaseSet é baseada no tipo de chave da identidade.

### Bloco ECIES para ElGamal/AES+SessionTags
O bloco ECIES substitui o bloco ElGamal para ElGamal/AES+SessionTags. O comprimento é de 514 bytes.
Consiste em duas partes de 257 bytes cada.
A primeira parte começa com zero e, em seguida, a chave pública efêmera P256 de 64 bytes, o restante de 192 bytes é preenchimento aleatório.
A segunda parte começa com zero e, em seguida, AES-CBC-256 criptografado com os mesmos 256 bytes de conteúdo que no ElGamal.

### Bloco ECIES para registro de construção de túnel
O registro de construção de túnel é o mesmo, mas sem zeros iniciais nos blocos.
Um túnel pode ser através de qualquer combinação de tipos de criptografia de roteadores e é feito por registro.
O originador do túnel criptografa os registros dependendo do tipo de criptografia publicado pelo participante do túnel, o participante do túnel decifra com base no próprio tipo de criptografia.

### Chave AES-CBC-256
Esta é a calculação de chaves compartilhadas ECDH onde o KDF é o SHA256 sobre a coordenada x.
Considere Alice como a criptografadora e Bob como o decifrador.
Suponha que k seja a chave privada P256 efêmera escolhida aleatoriamente por Alice e P seja a chave pública de Bob.
S é o segredo compartilhado S(Sx, Sy)
Alice calcula S por "acordo" k com P, por exemplo, S = k*P.

Suponha que K seja a chave pública efêmera de Alice e p seja a chave privada de Bob.
Bob pega K do primeiro bloco da mensagem recebida e calcula S = p*K

A chave de criptografia AES é SHA256(Sx) e o iv é Sy.
