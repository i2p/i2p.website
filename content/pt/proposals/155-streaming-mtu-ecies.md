---
title: "MTU em Streaming para Destinos ECIES"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Closed"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Nota
Implantação e teste de rede em andamento.
Sujeito a pequenas revisões.


## Visão Geral


### Resumo

O ECIES reduz a sobrecarga de mensagens de sessão existente (ES) em cerca de 90 bytes.
Portanto, podemos aumentar o MTU em cerca de 90 bytes para conexões ECIES.
Veja the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

Sem aumentar o MTU, em muitos casos as economias de sobrecarga não são realmente 'economizadas',
já que as mensagens serão preenchidas para usar duas mensagens de túnel completas de qualquer forma.

Esta proposta não requer qualquer alteração às especificações.
É postada como uma proposta apenas para facilitar a discussão e a construção de consenso
do valor recomendado e dos detalhes de implementação.


### Objetivos

- Aumentar o MTU negociado
- Maximizar o uso de mensagens de túnel de 1 KB
- Não alterar o protocolo de streaming


## Design

Use a opção existente MAX_PACKET_SIZE_INCLUDED e a negociação de MTU.
O streaming continua a usar o mínimo do MTU enviado e recebido.
O padrão permanece 1730 para todas as conexões, independentemente das chaves usadas.

As implementações são encorajadas a incluir a opção MAX_PACKET_SIZE_INCLUDED em todos os pacotes SYN, em ambas as direções,
embora isso não seja um requisito.

Se um destino for apenas ECIES, use o valor mais alto (tanto como Alice ou Bob).
Se um destino for de chave dupla, o comportamento pode variar:

Se o cliente de chave dupla estiver fora do roteador (em uma aplicação externa),
ele pode não "saber" a chave sendo usada no outro extremo, e Alice pode solicitar
um valor mais alto no SYN, enquanto os dados máximos no SYN permanecem 1730.

Se o cliente de chave dupla estiver dentro do roteador, a informação de que chave
está sendo usada pode ou não ser conhecida pelo cliente.
O conjunto de aluguel pode não ter sido buscado ainda, ou as interfaces de API internas
podem não disponibilizar facilmente essa informação para o cliente.
Se a informação estiver disponível, Alice pode usar o valor mais alto;
caso contrário, Alice deve usar o valor padrão de 1730 até ser negociado.

Um cliente de chave dupla como Bob pode enviar o valor mais alto em resposta,
mesmo que nenhum valor ou um valor de 1730 tenha sido recebido de Alice;
no entanto, não há provisão para negociar para cima em streaming,
então o MTU deve permanecer em 1730.


Conforme observado em the [Streaming API documentation](/docs/api/streaming/),
os dados nos pacotes SYN enviados de Alice para Bob podem exceder o MTU de Bob.
Esta é uma fraqueza no protocolo de streaming.
Portanto, os clientes de chave dupla devem limitar os dados nos pacotes SYN enviados
a 1730 bytes, enquanto enviam uma opção de MTU mais alta.
Uma vez que o MTU mais alto é recebido de Bob, Alice pode aumentar o tamanho máximo
de carga útil enviado.


### Análise

Como descrito em the [ECIES specification](/docs/specs/ecies/#overhead), a sobrecarga do ElGamal para mensagens de sessão existentes é
151 bytes, e a sobrecarga do Ratchet é 69 bytes.
Portanto, podemos aumentar o MTU para conexões ratchet em (151 - 69) = 82 bytes,
de 1730 para 1812.


## Especificação

Adicione as seguintes mudanças e esclarecimentos à seção de Seleção e Negociação de MTU de the [Streaming API documentation](/docs/api/streaming/).
Sem alterações em the [Streaming specification](/docs/specs/streaming/).


O valor padrão da opção i2p.streaming.maxMessageSize permanece 1730 para todas as conexões, independentemente das chaves usadas.
Os clientes devem usar o mínimo do MTU enviado e recebido, como de costume.

Existem quatro constantes e variáveis de MTU relacionadas:

- DEFAULT_MTU: 1730, inalterado, para todas as conexões
- i2cp.streaming.maxMessageSize: padrão 1730 ou 1812, pode ser alterado por configuração
- ALICE_SYN_MAX_DATA: O máximo de dados que Alice pode incluir em um pacote SYN
- negotiated_mtu: O mínimo do MTU de Alice e Bob, a ser usado como o tamanho máximo de dados
  no SYN ACK de Bob para Alice e em todos os pacotes subsequentes enviados em ambas as direções


Existem cinco casos a considerar:


### 1) Alice apenas ElGamal
Sem alteração, 1730 MTU em todos os pacotes.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize padrão: 1730
- Alice pode enviar MAX_PACKET_SIZE_INCLUDED no SYN, não é necessário a menos que != 1730


### 2) Alice apenas ECIES
1812 MTU em todos os pacotes.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize padrão: 1812
- Alice deve enviar MAX_PACKET_SIZE_INCLUDED no SYN


### 3) Alice Chave Dupla e sabe que Bob é ElGamal
1730 MTU em todos os pacotes.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize padrão: 1812
- Alice pode enviar MAX_PACKET_SIZE_INCLUDED no SYN, não é necessário a menos que != 1730


### 4) Alice Chave Dupla e sabe que Bob é ECIES
1812 MTU em todos os pacotes.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize padrão: 1812
- Alice deve enviar MAX_PACKET_SIZE_INCLUDED no SYN


### 5) Alice Chave Dupla e chave de Bob é desconhecida
Envie 1812 como MAX_PACKET_SIZE_INCLUDED no pacote SYN, mas limite os dados do pacote SYN a 1730.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize padrão: 1812
- Alice deve enviar MAX_PACKET_SIZE_INCLUDED no SYN


### Para todos os casos

Alice e Bob calculam
negotiated_mtu, o mínimo do MTU de Alice e Bob, a ser usado como o tamanho máximo de dados
no SYN ACK de Bob para Alice, e em todos os pacotes subsequentes enviados em ambas as direções.


## Justificação

Veja the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) por que o valor atual é 1730.
Veja the [ECIES specification](/docs/specs/ecies/#overhead) por que a sobrecarga do ECIES é 82 bytes a menos que o ElGamal.


## Notas de Implementação

Se o streaming está criando mensagens de tamanho ideal, é muito importante que
a camada ECIES-Ratchet não preencha além desse tamanho.

O tamanho ideal da Mensagem de Alho para caber em duas mensagens de túnel,
incluindo o cabeçalho I2NP de 16 bytes da Mensagem de Alho, 4 bytes do Comprimento da Mensagem de Alho,
etiqueta ES de 8 bytes e MAC de 16 bytes, é de 1956 bytes.

Um algoritmo de preenchimento recomendado no ECIES é o seguinte:

- Se o comprimento total da Mensagem de Alho for de 1954-1956 bytes,
  não adicione um bloco de preenchimento (sem espaço)
- Se o comprimento total da Mensagem de Alho for de 1938-1953 bytes,
  adicione um bloco de preenchimento para preencher exatamente 1956 bytes.
- Caso contrário, preencha como de costume, por exemplo, com uma quantidade aleatória de 0-15 bytes.

Estratégias semelhantes poderiam ser usadas no tamanho ideal de uma mensagem de um túnel (964)
e três mensagens de túnel (2952), embora esses tamanhos devessem ser raros na prática.


## Problemas

O valor 1812 é preliminar. Para ser confirmado e possivelmente ajustado.


## Migração

Sem problemas de compatibilidade retroativa.
Esta é uma opção existente e a negociação de MTU já faz parte da especificação.

Destinos ECIES mais antigos suportarão 1730.
Qualquer cliente que receber um valor mais alto responderá com 1730, e o outro extremo
negociará para baixo, como de costume.


