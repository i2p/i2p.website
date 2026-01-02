---
title: "Novo Modelo de Proposta de Criptografia"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
toc: true
---

## Visão Geral

Este documento descreve questões importantes a serem consideradas ao propor
uma substituição ou adição à nossa criptografia assimétrica ElGamal.

Este é um documento informativo.


## Motivação

O ElGamal é antigo e lento, e existem melhores alternativas.
No entanto, há várias questões que devem ser abordadas antes de podermos adicionar ou mudar para qualquer novo algoritmo.
Este documento destaca essas questões não resolvidas.


## Pesquisa de Fundo

Qualquer pessoa que proponha novas criptografias deve primeiro estar familiarizada com os seguintes documentos:

- [Proposta 111 NTCP2](/pt/proposals/111-ntcp-2/)
- [Proposta 123 LS2](/pt/proposals/123-new-netdb-entries/)
- [Proposta 136 tipos de assinatura experimentais](/pt/proposals/136-experimental-sigtypes/)
- [Proposta 137 tipos de assinatura opcionais](/pt/proposals/137-optional-sigtypes/)
- Discussões para cada uma das propostas acima, vinculadas no interior
- [prioridades de proposta de 2018](http://zzz.i2p/topics/2494)
- [proposta ECIES](http://zzz.i2p/topics/2418)
- [visão geral de novas criptografias assimétricas](http://zzz.i2p/topics/1768)
- [Visão geral de criptografias de baixo nível](/pt/docs/specs/common-structures/)


## Usos de Criptografia Assimétrica

Como revisão, usamos ElGamal para:

1) Mensagens de Construção de Túnel (a chave está em RouterIdentity)

2) Criptografia entre roteadores de netdb e outras mensagens I2NP (a chave está em RouterIdentity)

3) Criptografia de ponta a ponta do Cliente ElGamal+AES/SessionTag (a chave está em LeaseSet, a chave de Destino não é usada)

4) Efêmero DH para NTCP e SSU


## Design

Qualquer proposta para substituir ElGamal por outra coisa deve fornecer os seguintes detalhes.


## Especificação

Qualquer proposta para nova criptografia assimétrica deve especificar completamente as seguintes coisas.


### 1. Geral

Responda às seguintes perguntas em sua proposta. Note que pode ser necessário um proposta separada das especificidades no ponto 2) abaixo, pois pode conflitar com as propostas existentes 111, 123, 136, 137, ou outras.

- Para quais dos casos acima 1-4 você propõe usar a nova criptografia?
- Se for para 1) ou 2) (roteador), onde a chave pública será colocada, no RouterIdentity ou nas propriedades do RouterInfo? Você pretende usar o tipo de criptografia no certificado de chave? Especifique completamente. Justifique sua decisão de qualquer maneira.
- Se for para 3) (cliente), você pretende armazenar a chave pública no destino e usar o tipo de criptografia no certificado de chave (como na proposta ECIES), ou armazená-la no LS2 (como na proposta 123), ou algo mais? Especifique completamente e justifique sua decisão.
- Para todos os usos, como o suporte será anunciado? Se for para 3), ele será colocado no LS2 ou em outro lugar? Se for para 1) e 2), é semelhante às propostas 136 e/ou 137? Especifique completamente e justifique suas decisões. Provavelmente precisará de uma proposta separada para isso.
- Especifique completamente como e por que isso é compatível retroativamente e especifique completamente um plano de migração.
- Quais propostas não implementadas são pré-requisitos para sua proposta?


### 2. Tipo específico de criptografia

Responda às seguintes perguntas em sua proposta:

- Informações gerais sobre criptografia, curvas/parâmetros específicos, justifique completamente sua escolha. Forneça links para especificações e outras informações.
- Resultados de testes de velocidade comparados ao ElG e outras alternativas, se aplicável. Inclua encriptação, decriptação e geração de chaves.
- Disponibilidade de bibliotecas em C++ e Java (tanto OpenJDK, BouncyCastle, quanto terceiros)
  Para terceiros ou não-Java, forneça links e licenças
- Número(s) proposto(s) para tipo de criptografia (faixa experimental ou não)


## Notas


