---
title: "Melhorias no Transporte IPv6"
number: "158"
author: "zzz, original"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Fechado"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
---

## Nota
Implantação e teste de rede em andamento.
Sujeito a revisões menores.


## Visão Geral

Esta proposta é para implementar melhorias nos transportes SSU e NTCP2 para IPv6.


## Motivação

À medida que o IPv6 cresce ao redor do mundo e configurações apenas IPv6 (especialmente em dispositivos móveis) se tornam mais comuns,
precisamos melhorar nosso suporte ao IPv6 e remover as suposições de que
todos os roteadores são compatíveis com IPv4.

### Verificação de Conectividade

Ao selecionar pares para túneis, ou selecionar caminhos OBEP/IBGW para rotear mensagens,
é útil calcular se o roteador A pode se conectar ao roteador B.
Em geral, isso significa determinar se A tem capacidade de saída para um tipo de endereço e transporte (IPv4/v6)
que corresponda a um dos endereços de entrada anunciados de B.

No entanto, em muitos casos, não conhecemos as capacidades de A e temos que fazer suposições.
Se A estiver oculto ou protegido por firewall, os endereços não são publicados e não temos conhecimento direto -
portanto, presumimos que ele é compatível com IPv4 e não é compatível com IPv6.
A solução é adicionar duas novas "capacidades" ou capacidades ao Router Info para indicar capacidade de saída para IPv4 e IPv6.

### Introduzidores IPv6

Nossas especificações [SSU](/en/docs/transport/ssu/) e [SSU-SPEC](/en/docs/spec/ssu/) contêm erros e inconsistências sobre se
introduzidores IPv6 são suportados para introduções IPv4.
De qualquer forma, isso nunca foi implementado no Java I2P nem no i2pd.
Isso precisa ser corrigido.

### Introduções IPv6

Nossas especificações [SSU](/en/docs/transport/ssu/) e [SSU-SPEC](/en/docs/spec/ssu/) deixam claro que
introduções IPv6 não são suportadas.
Isso foi com a suposição de que o IPv6 nunca é protegido por firewall.
Isso claramente não é verdade, e precisamos melhorar o suporte para roteadores IPv6 com firewall.

### Diagramas de Introdução

Legenda: ----- é IPv4, ====== é IPv6

Apenas IPv4 atual:

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


Introdução IPv4, introduzidor IPv6

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

Introdução IPv6, introduzidor IPv6

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

Introdução IPv6, introduzidor IPv4

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Design

Há três mudanças a serem implementadas.

- Adicionar capacidades "4" e "6" às capacidades do Endereço do Roteador para indicar suporte de saída IPv4 e IPv6.
- Adicionar suporte para introduções IPv4 via introduzidores IPv6.
- Adicionar suporte para introduções IPv6 via introduzidores IPv4 e IPv6.

## Especificação

### Capacidades 4/6

Isso foi originalmente implementado sem uma proposta formal, mas é necessário para
introduções IPv6, por isso incluímos aqui.
Veja também [CAPS](http://zzz.i2p/topics/3050).

Duas novas capacidades "4" e "6" são definidas.
Essas novas capacidades serão adicionadas à propriedade "caps" no Endereço do Roteador, não nas capacidades do Router Info.
Atualmente, não temos uma propriedade "caps" definida para NTCP2.
Um endereço SSU com introduzidores é, por definição, ipv4 agora. Não suportamos introdução ipv6 de forma alguma.
No entanto, esta proposta é compatível com introduções IPv6. Veja abaixo.

Além disso, um roteador pode suportar conectividade via uma rede de sobreposição como I2P-over-Yggdrasil,
mas não deseja publicar um endereço, ou esse endereço não tem um formato padrão IPv4 ou IPv6.
Este novo sistema de capacidade deve ser suficientemente flexível para suportar essas redes também.

Definimos as seguintes alterações:

NTCP2: Adicionar propriedade "caps"

SSU: Adicionar suporte para um Endereço do Roteador sem um host ou introduzidores, para indicar suporte de saída
para IPv4, IPv6, ou ambos.

Ambos os transportes: Definir os seguintes valores de capacidades:

- "4": Suporte IPv4
- "6": Suporte IPv6

Vários valores podem ser suportados em um único endereço. Veja abaixo.
Pelo menos uma dessas capacidades é obrigatória se nenhum valor "host" estiver incluído no Endereço do Roteador.
No máximo, uma dessas capacidades é opcional se um valor "host" estiver incluído no Endereço do Roteador.
Capacidades de transporte adicionais podem ser definidas no futuro para indicar suporte a redes de sobreposição ou outra conectividade.

#### Casos de uso e exemplos

SSU:

SSU com host: 4/6 opcional, nunca mais de um.
Exemplo: SSU caps="4" host="1.2.3.4" key=... port="1234"

SSU somente de saída para um, outro é publicado: Apenas Capacidades, 4/6.
Exemplo: SSU caps="6"

SSU com introduzidores: nunca combinados. 4 ou 6 é necessário.
Exemplo: SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... key=...

SSU oculto: Apenas Capacidades, 4, 6, ou 46. Vários são permitidos.
Não há necessidade de dois endereços, um com 4 e outro com 6.
Exemplo: SSU caps="46"

NTCP2:

NTCP2 com host: 4/6 opcional, nunca mais de um.
Exemplo: NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

NTCP2 somente de saída para um, outro é publicado: Capacidades, s, v apenas, 4/6/y, vários são permitidos.
Exemplo: NTCP2 caps="6" i=... s=... v="2"

NTCP2 oculto: Capacidades, s, v apenas 4/6, vários são permitidos. Não há necessidade de dois endereços, um com 4 e outro com 6.
Exemplo: NTCP2 caps="46" i=... s=... v="2"

### Introduzidores IPv6 para IPv4

As seguintes alterações são necessárias para corrigir erros e inconsistências nas especificações.
Também descrevemos isso como "parte 1" da proposta.

#### Alterações na Especificação

[SSU](/en/docs/transport/ssu/) atualmente diz (notas de IPv6):

IPv6 é suportado desde a versão 0.9.8. Endereços de retransmissão publicados podem ser IPv4 ou IPv6, e a comunicação Alice-Bob pode ser via IPv4 ou IPv6.

Adicione o seguinte:

Enquanto a especificação foi alterada a partir da versão 0.9.8, a comunicação Alice-Bob via IPv6 não foi realmente suportada até a versão 0.9.50.
Versões anteriores de roteadores Java publicaram erroneamente a capacidade 'C' para endereços IPv6,
mesmo que eles não atuassem realmente como um introduzidor via IPv6.
Portanto, roteadores devem confiar apenas na capacidade 'C' em um endereço IPv6 se a versão do roteador for 0.9.50 ou superior.

[SSU-SPEC](/en/docs/spec/ssu/) atualmente diz (Solicitação de Retransmissão):

O endereço IP só é incluído se for diferente do endereço de origem e porta do pacote.
Na implementação atual, o comprimento do IP é sempre 0 e a porta é sempre 0,
e o receptor deve usar o endereço de origem e porta do pacote.
Esta mensagem pode ser enviada via IPv4 ou IPv6. Se IPv6, Alice deve incluir seu endereço IPv4 e porta.

Adicione o seguinte:

O IP e a porta devem ser incluídos para introduzir um endereço IPv4 ao enviar esta mensagem via IPv6.
Isso é suportado a partir da versão 0.9.50.

### Introduções IPv6

Todas as três mensagens de retransmissão SSU (RelayRequest, RelayResponse, e RelayIntro) contêm campos de comprimento IP
para indicar o comprimento do endereço IP (Alice, Bob, ou Charlie) a seguir.

Portanto, nenhuma mudança no formato das mensagens é necessária.
Apenas mudanças textuais nas especificações, indicando que endereços IP de 16 bytes são permitidos.

As seguintes alterações são necessárias nas especificações.
Também descrevemos isso como "parte 2" da proposta.

#### Alterações na Especificação

[SSU](/en/docs/transport/ssu/) atualmente diz (notas de IPv6):

A comunicação Bob-Charlie e Alice-Charlie é via IPv4 apenas.

[SSU-SPEC](/en/docs/spec/ssu/) atualmente diz (Solicitação de Retransmissão):

Não há planos para implementar retransmissão para IPv6.

Alterar para:

Retransmissão para IPv6 é suportada a partir da versão 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) atualmente diz (Resposta de Retransmissão):

O endereço IP de Charlie deve ser IPv4, pois é o endereço que Alice enviará a solicitação de sessão após o furo.
Não há planos para implementar retransmissão para IPv6.

Alterar para:

O endereço IP de Charlie pode ser IPv4 ou, a partir da versão 0.9.xx, IPv6.
Esse é o endereço para o qual Alice enviará a solicitação de sessão após o furo.
Retransmissão para IPv6 é suportada a partir da versão 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) atualmente diz (Introdução à Retransmissão):

O endereço IP de Alice é sempre 4 bytes na implementação atual, porque Alice está tentando se conectar a Charlie via IPv4.
Esta mensagem deve ser enviada através de uma conexão IPv4 estabelecida,
pois essa é a única forma que Bob conhece o endereço IPv4 de Charlie para retornar a Alice na Resposta de Retransmissão.

Alterar para:

Para IPv4, o endereço IP de Alice é sempre 4 bytes, porque Alice está tentando se conectar a Charlie via IPv4.
A partir da versão 0.9.xx, o IPv6 é suportado, e o endereço IP de Alice pode ter 16 bytes.

Para IPv4, esta mensagem deve ser enviada através de uma conexão IPv4 estabelecida,
pois essa é a única forma que Bob conhece o endereço IPv4 de Charlie para retornar a Alice na Resposta de Retransmissão.
A partir da versão 0.9.xx, o IPv6 é suportado, e esta mensagem pode ser enviada por uma conexão IPv6 estabelecida.

Também adicionar:

A partir da versão 0.9.xx, qualquer endereço SSU publicado com introduzidores deve conter "4" ou "6" na opção "caps".

## Migração

Todos os roteadores antigos devem ignorar a propriedade caps no NTCP2 e caracteres de capacidade desconhecidos na propriedade caps do SSU.

Qualquer endereço SSU com introduzidores que não contenha uma capacidade "4" ou "6" é assumido como sendo para introdução IPv4.
