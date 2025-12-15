---
title: "Mensagens de Construção de Túnel Menores"
number: "157"
author: "zzz, original"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Fechado"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
toc: true
---

## Nota
Implementado a partir da versão API 0.9.51.
Implantação e teste de rede em andamento.
Sujeito a pequenas revisões.
Veja [I2NP] e [Tunnel-Creation-ECIES] para a especificação final.



## Visão Geral


### Resumo

O tamanho atual dos registros criptografados de Solicitação e Resposta de Construção de Túnel é 528.
Para mensagens típicas de Construção de Túnel Variável e Resposta de Construção de Túnel Variável,
o tamanho total é de 2113 bytes. Esta mensagem é fragmentada em três mensagens de túnel de 1KB para o caminho reverso.

Mudanças no formato de registro de 528 bytes para roteadores ECIES-X25519 são especificadas em [Prop152] e [Tunnel-Creation-ECIES].
Para uma mistura de roteadores ElGamal e ECIES-X25519 em um túnel, o tamanho do registro deve permanecer
528 bytes. No entanto, se todos os roteadores em um túnel forem ECIES-X25519, um novo e menor
registro de construção é possível, porque a criptografia ECIES-X25519 tem muito menos sobrecarga
do que ElGamal.

Mensagens menores economizariam largura de banda. Além disso, se as mensagens pudessem caber em uma
única mensagem de túnel, o caminho reverso seria três vezes mais eficiente.

Esta proposta define novos registros de solicitação e resposta e novas mensagens de Solicitação de Construção e Resposta de Construção.

O criador do túnel e todos os saltos no túnel criado devem ser ECIES-X25519, e pelo menos na versão 0.9.51.
Esta proposta não será útil até que a maioria dos roteadores na rede sejam ECIES-X25519.
Isso é esperado para acontecer até o final de 2021.


### Objetivos

Veja [Prop152] e [Prop156] para objetivos adicionais.

- Registros e mensagens menores
- Manter espaço suficiente para opções futuras, como em [Prop152] e [Tunnel-Creation-ECIES]
- Caber em uma mensagem de túnel para o caminho reverso
- Suportar apenas saltos ECIES
- Manter melhorias implementadas em [Prop152] e [Tunnel-Creation-ECIES]
- Maximizar a compatibilidade com a rede atual
- Ocultar mensagens de construção de entrada do OBEP
- Ocultar mensagens de resposta de construção de saída do IBGW
- Não exigir uma atualização "flag day" para toda a rede
- Implantação gradual para minimizar o risco
- Reutilizar primitivas criptográficas existentes


### Não-Objetivos

Veja [Prop156] para objetivos adicionais.

- Nenhum requisito para túneis mistos ElGamal/ECIES
- Mudanças na criptografia de camada, para isso veja [Prop153]
- Nenhuma aceleração de operações criptográficas. Presume-se que ChaCha20 e AES sejam similares,
  mesmo com AESNI, pelo menos para os pequenos tamanhos de dados em questão.


## Design


### Registros

Veja o apêndice para cálculos.

Os registros de solicitação e resposta criptografados terão 218 bytes, em comparação com 528 bytes agora.

Os registros de solicitação em texto claro terão 154 bytes,
em comparação com 222 bytes para registros ElGamal,
e 464 bytes para registros ECIES como definidos em [Prop152] e [Tunnel-Creation-ECIES].

Os registros de resposta em texto claro terão 202 bytes,
em comparação com 496 bytes para registros ElGamal,
e 512 bytes para registros ECIES como definidos em [Prop152] e [Tunnel-Creation-ECIES].

A criptografia da resposta será ChaCha20 (NÃO ChaCha20/Poly1305),
então os registros em texto claro não precisam ser múltiplos de 16 bytes.

Registros de solicitação serão menores usando HKDF para criar as
chaves de camada e resposta, para que não precisem ser incluídas explicitamente na solicitação.


### Mensagens de Construção de Túnel

Ambos serão "variáveis" com um campo de número de registros de um byte,
como nas mensagens Variáveis existentes.

#### ShortTunnelBuild: Tipo 25

Comprimento típico (com 4 registros): 873 bytes

Quando usado para construções de túnel de entrada,
é recomendado (mas não exigido) que esta mensagem seja criptografada com alho pelo originador,
direcionada ao gateway de entrada (instruções de entrega ROUTER),
para ocultar mensagens de construção de entrada do OBEP.
O IBGW decifra a mensagem,
coloca a resposta no slot correto,
e envia a ShortTunnelBuildMessage para o próximo salto.

O comprimento do registro é selecionado para que uma STBM criptografada com alho caiba
em uma única mensagem de túnel. Veja o apêndice abaixo.



#### OutboundTunnelBuildReply: Tipo 26

Definimos uma nova mensagem OutboundTunnelBuildReply.
Esta é usada apenas para construções de túnel de saída.
O objetivo é ocultar mensagens de resposta de construção de saída do IBGW.
Deve ser criptografada com alho pelo OBEP, direcionada ao originador
(instruções de entrega TUNNEL).
O OBEP decifra a mensagem de construção de túnel,
constrói uma mensagem OutboundTunnelBuildReply,
e coloca a resposta no campo de texto claro.
Os outros registros vão para os outros slots.
Em seguida, criptografa a mensagem com alho para o originador com as chaves simétricas derivadas.


#### Notas

Criptografando com alho o OTBRM e a STBM, também evitamos quaisquer
problemas potenciais de compatibilidade no IBGW e OBEP dos túneis emparelhados.




### Fluxo de Mensagem


```
STBM: Mensagem de construção de túnel curto (tipo 25)
  OTBRM: Mensagem de resposta de construção de túnel de saída (tipo 26)

  Construção de saída A-B-C
  Resposta por caminho de entrada existente D-E-F


                  Novo Túnel
           STBM      STBM      STBM
  Criador ------> A ------> B ------> C ---\
                                     OBEP   \
                                            | Criptografado com alho
                                            | OTBRM
                                            | (entrega TUNNEL)
                                            | do OBEP para
                                            | criador
                Túnel Existente             /
  Criador <-------F---------E-------- D <--/
                                     IBGW



  Construção de entrada D-E-F
  Enviado por caminho de saída existente A-B-C


                Túnel Existente
  Criador ------> A ------> B ------> C ---\
                                    OBEP    \
                                            | Criptografado com alho (opcional)
                                            | STBM
                                            | (entrega ROUTER)
                                            | do criador
                  Novo Túnel                | para IBGW
            STBM      STBM      STBM        /
  Criador <------ F <------ E <------ D <--/
                                     IBGW



```



### Criptografia de Registro

Criptografia de registro de solicitação e resposta: como definido em [Prop152] e [Tunnel-Creation-ECIES].

Criptografia de registros de resposta para outros slots: ChaCha20.


### Criptografia de Camada

Atualmente, não há plano para mudar a criptografia de camada para túneis construídos com
esta especificação; ela continuaria AES, como atualmente usado para todos os túneis.

Mudar a criptografia de camada para ChaCha20 é um tópico para pesquisa adicional.



### Nova Mensagem de Dados de Túnel

Atualmente não há plano para mudar a Mensagem de Dados de Túnel de 1KB usada para túneis construídos com
esta especificação.

Pode ser útil introduzir uma nova mensagem I2NP que seja maior ou de tamanho variável, concomitantemente com esta proposta,
para uso sobre esses túneis.
Isso reduziria a sobrecarga para mensagens grandes.
Este é um tópico para pesquisa adicional.




## Especificação


### Registro de Solicitação Curta



#### Registro de Solicitação Curta Não Criptografado

Esta é a especificação proposta do BuildRequestRecord de túnel para roteadores ECIES-X25519.
Resumo de alterações de [Tunnel-Creation-ECIES]:

- Mudar o comprimento não criptografado de 464 para 154 bytes
- Mudar o comprimento criptografado de 528 para 218 bytes
- Remover chaves de camada e de resposta e IVs, eles serão gerados a partir de split() e um KDF


O registro de solicitação não contém nenhuma chave de resposta ChaCha.
Essas chaves são derivadas de um KDF. Veja abaixo.

Todos os campos estão em big-endian.

Tamanho não criptografado: 154 bytes.


```
bytes     0-3: ID do túnel para receber mensagens como, não zero
  bytes     4-7: próximo ID do túnel, não zero
  bytes    8-39: hash de identidade do próximo roteador
  byte       40: flags
  bytes   41-42: mais flags, não usados, configurar para 0 para compatibilidade
  byte       43: tipo de criptografia de camada
  bytes   44-47: hora da solicitação (em minutos desde a época, arredondado para baixo)
  bytes   48-51: expiração da solicitação (em segundos desde a criação)
  bytes   52-55: próximo ID de mensagem
  bytes    56-x: opções de construção de túnel (mapeamento)
  bytes     x-x: outros dados como implícitos por flags ou opções
  bytes   x-153: preenchimento aleatório (veja abaixo)

```


O campo flags é o mesmo definido em [Tunnel-Creation] e contém o seguinte::

 Ordem dos bits: 76543210 (bit 7 é o MSB)
 bit 7: se definido, permitir mensagens de qualquer um
 bit 6: se definido, permitir mensagens para qualquer um, e enviar a resposta para o próximo salto
       especificado em uma mensagem de resposta de construção de túnel
 bits 5-0: Indefinido, deve ser configurado para 0 para compatibilidade com opções futuras

O Bit 7 indica que o salto será um gateway de entrada (IBGW). O Bit 6
indica que o salto será um ponto de extremidade de saída (OBEP). Se nenhum dos bits estiver
definido, o salto será um participante intermediário. Ambos não podem ser definidos ao mesmo tempo.

Criptografia de camada: 0 para AES (como nos túneis atuais);
1 para o futuro (ChaCha?)

A expiração da solicitação é para futuras durações de túnel variável.
Por enquanto, o único valor suportado é 600 (10 minutos).

A chave pública efêmera do criador é uma chave ECIES, big-endian.
Ela é usada para o KDF para as chaves e IVs de camada e resposta do IBGW.
Isso é apenas incluído no registro em texto claro em uma mensagem de Construção de Túnel de Entrada.
É necessário porque não há DH nesta camada para o registro de construção.

As opções de construção de túnel são uma estrutura de Mapeamento conforme definido em [Common].
Isso é para uso futuro. Nenhuma opção está atualmente definida.
Se a estrutura de Mapeamento estiver vazia, isso é dois bytes 0x00 0x00.
O tamanho máximo do Mapeamento (incluindo o campo de comprimento) é 98 bytes,
e o valor máximo do campo de comprimento do Mapeamento é 96.



#### Registro de Solicitação Curta Criptografado

Todos os campos são big-endian, exceto a chave pública efêmera, que é little-endian.

Tamanho criptografado: 218 bytes


```
bytes    0-15: Hash de identidade truncado do salto
  bytes   16-47: Chave pública efêmera X25519 do remetente
  bytes  48-201: Registro de Construção Curta Criptografado ChaCha20
  bytes 202-217: MAC Poly1305

```



### Registro de Resposta Curta


#### Registro de Resposta Curta Não Criptografado
Esta é a especificação proposta do ShortBuildReplyRecord de túnel para roteadores ECIES-X25519.
Resumo de alterações de [Tunnel-Creation-ECIES]:

- Mudar o comprimento não criptografado de 512 para 202 bytes
- Mudar o comprimento criptografado de 528 para 218 bytes


As respostas ECIES são criptografadas com ChaCha20/Poly1305.

Todos os campos são big-endian.

Tamanho não criptografado: 202 bytes.


```
bytes    0-x: Opções de Resposta de Construção de Túnel (Mapeamento)
  bytes    x-x: outros dados como implícitos por opções
  bytes  x-200: Preenchimento aleatório (veja abaixo)
  byte     201: Byte de Resposta

```

As opções de resposta de construção de túnel são uma estrutura de Mapeamento conforme definido em [Common].
Isso é para uso futuro. Nenhuma opção está atualmente definida.
Se a estrutura de Mapeamento estiver vazia, isso é dois bytes 0x00 0x00.
O tamanho máximo do Mapeamento (incluindo o campo de comprimento) é 201 bytes,
e o valor máximo do campo de comprimento do Mapeamento é 199.

O byte de resposta é um dos seguintes valores
como definido em [Tunnel-Creation](/en/docs/spec/tunnel-creation/) para evitar fingerprinting:

- 0x00 (aceitar)
- 30 (TUNNEL_REJECT_BANDWIDTH)


#### Registro de Resposta Curta Criptografado

Tamanho criptografado: 218 bytes


```
bytes   0-201: Registro de Resposta de Construção Curta Criptografado ChaCha20
  bytes 202-217: MAC Poly1305

```



### KDF

Veja a seção KDF abaixo.




### ShortTunnelBuild
I2NP Tipo 25

Esta mensagem é enviada para saltos do meio, OBEP e IBEP (criador).
Não pode ser enviada para o IBGW (use InboundTunnelBuild criptografado com alho em vez disso).
Quando recebida pelo OBEP, ela é transformada em uma OutboundTunnelBuildReply,
criptografada com alho, e enviada ao originador.



```
+----+----+----+----+----+----+----+----+
  | num| ShortBuildRequestRecords...
  +----+----+----+----+----+----+----+----+

  num ::
         1 byte `Integer`
         Valores válidos: 1-8

  tamanho do registro: 218 bytes
  tamanho total: 1+$num*218
```

#### Notas

* Número típico de registros é 4, para um tamanho total de 873.




### OutboundTunnelBuildReply
I2NP Tipo 26

Esta mensagem é enviada apenas pelo OBEP ao IBEP (criador) através de um túnel de entrada existente.
Não pode ser enviada a qualquer outro salto.
Ela é sempre criptografada com alho.


```
+----+----+----+----+----+----+----+----+
  | num|                                  |
  +----+                                  +
  |      ShortBuildReplyRecords...        |
  +----+----+----+----+----+----+----+----+

  num ::
         Número total de registros,
         1 byte `Integer`
         Valores válidos: 1-8

  ShortBuildReplyRecords ::
         Registros criptografados
         comprimento: num * 218

  tamanho do registro criptografado: 218 bytes
  tamanho total: 1+$num*218
```

#### Notas

* Número típico de registros é 4, para um tamanho total de 873.
* Esta mensagem deve ser criptografada com alho.



### KDF

Usamos ck do estado Noise após a criptografia/decifração do registro de construção de túnel
para derivar as seguintes chaves: chave de resposta, chave de camada AES, chave AES IV e chave/tag de resposta de alho para OBEP.

Chave de resposta:
Diferente dos registros longos, não podemos usar a parte esquerda de ck para a chave de resposta, porque não é a última e será usada mais tarde.
A chave de resposta é usada para criptografar a resposta usando AEAD/Chaha20/Poly1305 e ChaCha20 para responder a outros registros.
Ambos usam a mesma chave, nonce é a posição do registro na mensagem começando de 0.


```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
  replyKey = keydata[32:63]
  ck = keydata[0:31]

  Chave de camada:
  A chave de camada é sempre AES para agora, mas o mesmo KDF pode ser usado de Chacha20

  keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
  layerKey = keydata[32:63]

  Chave IV para registro não-OBEP:
  ivKey = keydata[0:31]
  porque é a última

  Chave IV para registro OBEP:
  ck = keydata[0:31]
  keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
  ivKey = keydata[32:63]
  ck = keydata[0:31]

  Chave/tag de resposta de alho do OBEP:
  keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
  replyKey = keydata[32:63]
  replyTag = keydata[0:7]

```





## Justificativa

Este design maximiza o reuso de primitivas criptográficas, protocolos e código existentes.

Este design minimiza o risco.

ChaCha20 é ligeiramente mais rápido do que AES para registros pequenos, em testes Java.
ChaCha20 evita um requisito para tamanhos de dados múltiplos de 16.


## Notas de Implementação

- Assim como a mensagem de construção de túnel variável existente,
  mensagens menores que 4 registros não são recomendadas.
  O padrão típico é 3 saltos.
  Túneis de entrada devem ser construídos com um registro extra para
  o originador, para que o último salto não saiba que é o último.
  Para que os saltos intermediários não saibam se um túnel é de entrada ou saída,
  túneis de saída devem ser construídos com 4 registros também.



## Questões



## Migração

A implementação, teste e implantação levarão várias versões
e aproximadamente um ano. As fases são as seguintes. A atribuição de
cada fase para uma versão particular é TBD e depende do
ritmo de desenvolvimento.

Os detalhes da implementação e migração podem variar para
cada implementação do I2P.

O criador do túnel deve garantir que todos os saltos no túnel criado sejam ECIES-X25519, E que tenham pelo menos a versão TBD.
O criador do túnel NÃO precisa ser ECIES-X25519; ele pode ser ElGamal.
No entanto, se o criador for ElGamal, ele revela ao salto mais próximo que é o criador.
Assim, na prática, esses túneis só devem ser criados por roteadores ECIES.

Não deve ser necessário que o OBEP ou o IBGW do túnel emparelhado sejam ECIES ou
de qualquer versão particular.
As novas mensagens são criptografadas com alho e não são visíveis no OBEP ou IBGW
do túnel emparelhado.

Fase 1: Implementação, não habilitada por padrão

Fase 2 (próxima versão): Habilitar por padrão

Não há problemas de compatibilidade retroativa. As novas mensagens podem ser enviadas apenas para roteadores que as suportam.




## Apêndice


Sem sobrecarga de alho para STBM de entrada não criptografada,
se não usarmos ITBM:



```
Tamanho atual de 4 slots: 4 * 528 + sobrecarga = 3 mensagens de túnel

  Mensagem de construção de 4 slots para caber em uma mensagem de túnel, somente ECIES:

  1024
  - 21 cabeçalho de fragmento
  ----
  1003
  - 35 instruções de entrega ROUTER não fragmentadas
  ----
  968
  - 16 cabeçalho I2NP
  ----
  952
  - 1 número de slots
  ----
  951
  / 4 slots
  ----
  237 Novo tamanho de registro de construção criptografado (vs. 528 agora)
  - 16 hash truncado
  - 32 chave efêmera
  - 16 MAC
  ----
  173 tamanho máximo do registro de construção em texto claro (vs. 222 agora)



```


Com sobrecarga de alho para o padrão de ruído 'N' para criptografar STBM de entrada, se não usarmos ITBM:


```
Tamanho atual de 4 slots: 4 * 528 + sobrecarga = 3 mensagens de túnel

  Mensagem de construção criptografada com alho de 4 slots para caber em uma mensagem de túnel, somente ECIES:

  1024
  - 21 cabeçalho de fragmento
  ----
  1003
  - 35 instruções de entrega ROUTER não fragmentadas
  ----
  968
  - 16 cabeçalho I2NP
  -  4 comprimento
  ----
  948
  - 32 byte chave efêmera
  ----
  916
  - 7 byte bloco DateTime
  ----
  909
  - 3 byte sobrecarga do bloco de Alho
  ----
  906
  - 9 byte cabeçalho I2NP
  ----
  897
  - 1 byte instruções de entrega LOCAL do Alho
  ----
  896
  - 16 byte MAC Poly1305
  ----
  880
  - 1 número de slots
  ----
  879
  / 4 slots
  ----
  219 Novo tamanho de registro de construção criptografado (vs. 528 agora)
  - 16 hash truncado
  - 32 chave efêmera
  - 16 MAC
  ----
  155 tamanho máximo do registro de construção em texto claro (vs. 222 agora)


```

Notas:

Tamanho atual do registro de construção em texto claro antes do preenchimento não utilizado: 193

A remoção do hash de roteador completo e a geração HKDF de chaves/IVs liberaria muito espaço para opções futuras.
Se tudo for HKDF, o espaço necessário em texto claro é cerca de 58 bytes (sem quaisquer opções).

O OTBRM envolto em alho será ligeiramente menor do que o STBM envolto em alho,
porque as instruções de entrega são LOCAL e não ROUTER,
não há bloco DATETIME incluído, e
ele usa uma tag de 8 bytes em vez da chave efêmera de 32 bytes para uma mensagem 'N' completa.




