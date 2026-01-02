---
title: "Atualizações de Streaming"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Fechado"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Visão Geral

Os roteadores Java I2P e i2pd antigos que utilizam API antes da versão 0.9.58 (lançada em março de 2023)
são vulneráveis a um ataque de repetição de pacote SYN em streaming.
Este é um problema de design do protocolo, não um bug de implementação.

Os pacotes SYN são assinados, mas a assinatura do pacote SYN inicial enviado de Alice para Bob
não está vinculada à identidade de Bob, então Bob pode armazenar e repetir esse pacote,
enviando-o para alguma vítima Charlie. Charlie irá pensar que o pacote veio de
Alice e responderá a ela. Na maioria dos casos, isso é inofensivo, mas
o pacote SYN pode conter dados iniciais (como um GET ou POST) que
Charlie processará imediatamente.

## Design

A correção é Alice incluir o hash de destino de Bob nos dados assinados do SYN.
Bob verifica na recepção se esse hash corresponde ao seu hash.

Qualquer vítima potencial de ataque Charlie
verifica estes dados e rejeita o SYN se ele não corresponder ao seu hash.

Ao utilizar o campo de opção NACKs no SYN para armazenar o hash,
a mudança é compatível com versões anteriores, porque não se espera que os NACKs sejam incluídos
no pacote SYN e atualmente são ignorados.

Todas as opções estão cobertas pela assinatura, como de costume, então Bob não pode
re-escrever o hash.

Se Alice e Charlie são com API 0.9.58 ou mais recente, qualquer tentativa de repetição por Bob será rejeitada.

## Especificação

Atualize a [especificação Streaming](/docs/specs/streaming/) para adicionar a seguinte seção:

### Prevenção de repetição

Para evitar que Bob use um ataque de repetição armazenando um pacote SYNCHRONIZE válido assinado
recebido de Alice e mais tarde o enviando para uma vítima Charlie,
Alice deve incluir o hash de destino de Bob no pacote SYNCHRONIZE como se segue:

.. raw:: html

  {% highlight lang='dataspec' %}
Definir o campo de contagem de NACK como 8
  Definir o campo NACKs com o hash de destino de 32 bytes de Bob

{% endhighlight %}

Após a recepção de um SYNCHRONIZE, se o campo de contagem de NACK for 8,
Bob deve interpretar o campo NACKs como um hash de destino de 32 bytes,
e deve verificar se corresponde ao seu hash de destino.
Ele também deve verificar a assinatura do pacote como de costume,
pois isso cobre todo o pacote, incluindo os campos de contagem de NACK e NACKs.
Se a contagem de NACK for 8 e o campo NACKs não corresponder,
Bob deve descartar o pacote.

Isso é necessário para as versões 0.9.58 e superiores.
Isso é compatível com versões anteriores,
porque não se espera NACKs em um pacote SYNCHRONIZE.
Os destinos não sabem e não podem saber qual versão o outro lado está executando.

Nenhuma mudança é necessária para o pacote SYNCHRONIZE ACK enviado de Bob para Alice;
não inclua NACKs nesse pacote.

## Análise de Segurança

Este problema está presente no protocolo de streaming desde que foi criado em 2004.
Foi descoberto internamente pelos desenvolvedores do I2P.
Não temos evidências de que o problema tenha sido explorado.
A chance real de sucesso da exploração pode variar amplamente dependendo
do protocolo de camada de aplicação e do serviço.
Aplicações peer-to-peer provavelmente são mais propensas a serem afetadas
do que aplicações cliente/servidor.

## Compatibilidade

Sem problemas. Todas as implementações conhecidas atualmente ignoram o campo NACKs no pacote SYN.
E mesmo que não o ignorassem, e tentassem interpretá-lo
como NACKs para 8 mensagens diferentes, essas mensagens não estariam pendentes
durante o handshake SYNCHRONIZE e os NACKs não fariam sentido.

## Migração

As implementações podem adicionar suporte a qualquer momento, não é necessária coordenação.
Os roteadores Java I2P e i2pd implementaram isso na API 0.9.58 (lançada em março de 2023).

