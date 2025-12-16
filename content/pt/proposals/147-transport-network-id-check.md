---
title: "Verificação de ID de Rede de Transporte"
number: "147"
author: "zzz"
created: "2019-02-28"
lastupdated: "2019-08-13"
status: "Closed"
thread: "http://zzz.i2p/topics/2687"
target: "0.9.42"
implementedin: "0.9.42"
toc: true
---

## Visão Geral

NTCP2 (proposta 111) não rejeita conexões de diferentes IDs de rede
na fase de Solicitação de Sessão.
A conexão deve atualmente ser rejeitada na fase de Sessão Confirmada,
quando Bob verifica o RI de Alice.

Da mesma forma, SSU não rejeita conexões de diferentes IDs de rede
na fase de Solicitação de Sessão.
A conexão deve atualmente ser rejeitada após a fase de Sessão Confirmada,
quando Bob verifica o RI de Alice.

Esta proposta altera a fase de Solicitação de Sessão de ambos os transportes para incorporar o
ID de rede, de uma forma compatível com versões anteriores.


## Motivação

Conexões de redes erradas devem ser rejeitadas, e o
peer deve ser colocado na lista negra, o mais rapidamente possível.


## Objetivos

- Prevenir a contaminação cruzada de redes de teste e redes bifurcadas

- Adicionar ID de rede ao handshake do NTCP2 e do SSU

- Para o NTCP2,
  o receptor (conexão de entrada) deve ser capaz de identificar que o ID de rede é diferente,
  para que possa colocar na lista negra o IP do peer.

- Para o SSU,
  o receptor (conexão de entrada) não pode colocar na lista negra na fase de solicitação de sessão, porque
  o IP de entrada pode ser falsificado. É suficiente mudar a criptografia do handshake.

- Prevenir o reabastecimento da rede errada

- Deve ser compatível com versões anteriores


## Não-Objetivos

- O NTCP 1 não está mais em uso, portanto não será alterado.


## Design

Para o NTCP2,
fazer XOR em um valor apenas causaria a falha na criptografia, e o
receptor não teria informações suficientes para colocar o originador na lista negra,
então essa abordagem não é a preferida.

Para o SSU,
faremos XOR no ID de rede em algum lugar na Solicitação de Sessão.
Como isso deve ser compatível com versões anteriores, faremos XOR em (id - 2)
para que não tenha efeito no valor atual do ID de rede de 2.



## Especificação

### Documentação

Adicione a seguinte especificação para valores válidos de ID de rede:


| Uso | Número de NetID |
|-------|--------------|
| Reservado | 0 |
| Reservado | 1 |
| Rede Atual (padrão) | 2 |
| Reservado para Redes Futuras | 3 - 15 |
| Forks e Redes de Teste | 16 - 254 |
| Reservado | 255 |


A configuração do I2P em Java para mudar o padrão é "router.networkID=nnn".
Documente isso melhor e incentive forks e redes de teste a adicionar essa configuração ao seu arquivo de configuração.
Incentive outras implementações a implementar e documentar essa opção.


### NTCP2

Use o primeiro byte reservado das opções (byte 0) na mensagem de Solicitação de Sessão para conter o ID de rede, atualmente 2.
Ele contém o ID de rede.
Se diferente de zero, o receptor deve verificá-lo em relação ao byte menos significativo do ID de rede local.
Se não coincidirem, o receptor deve desconectar imediatamente e colocar na lista negra o IP do originador.


### SSU

Para SSU, adicione um XOR de ((netid - 2) << 8) no cálculo HMAC-MD5.

Existente:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' significa adicionar e '^' significa ou exclusivo.
  payloadLength é um inteiro sem sinal de 2 bytes
  protocolVersion é um byte 0x00
```

Novo:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' significa adicionar, '^' significa ou exclusivo, '<<' significa deslocamento à esquerda.
  payloadLength é um inteiro sem sinal de dois bytes, big endian
  protocolVersion é dois bytes 0x0000, big endian
  netid é um inteiro sem sinal de dois bytes, big endian, valores legais são 2-254
```


### Reseeding

Adicione um parâmetro ?netid=nnn ao fetch do arquivo reseed su3.
Atualize o software de reseed para verificar o netid. Se estiver presente e não for igual a "2",
o fetch deve ser rejeitado com um código de erro, talvez 403.
Adicione opção de configuração ao software de reseed para que um netid alternativo possa ser configurado
para redes de teste ou bifurcadas.


## Notas

Não podemos forçar redes de teste e forks a mudarem o ID de rede.
O melhor que podemos fazer é documentação e comunicação.
Se descobrirmos contaminação cruzada com outras redes, devemos tentar
contatar os desenvolvedores ou operadores para explicar a importância de mudar o ID de rede.


## Problemas



## Migração

Isso é compatível com versões anteriores para o valor atual de ID de rede de 2.
Se algumas pessoas estiverem operando redes (de teste ou outras) com um valor de ID de rede diferente,
esta mudança é incompatível com versões anteriores.
No entanto, não temos conhecimento de ninguém fazendo isso.
Se é apenas uma rede de teste, não é um problema, basta atualizar todos os roteadores de uma vez.
