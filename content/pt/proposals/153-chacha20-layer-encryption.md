---
title: "Criptografia de Camada de Túnel ChaCha"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Open"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Visão Geral

Esta proposta baseia-se e requer as alterações da proposta 152: Túneis ECIES.

Somente túneis construídos através de saltos que suportam o formato BuildRequestRecord para túneis ECIES-X25519 podem implementar esta especificação.

Esta especificação requer o formato de Opções de Construção de Túnel para indicar o tipo de criptografia de camada de túnel e transmitir chaves AEAD de camada.

### Objetivos

Os objetivos desta proposta são:

- Substituir AES256/ECB+CBC por ChaCha20 para IV estabelecido de túnel e criptografia de camada
- Usar ChaCha20-Poly1305 para proteção AEAD entre saltos
- Ser indetectável da criptografia de camada de túnel existente por não participantes do túnel
- Não fazer alterações no comprimento geral da mensagem do túnel

### Processamento de Mensagens de Túnel Estabelecido

Esta seção descreve alterações para:

- Pré-processamento + criptografia de Gateway de Saída e Entrada
- Criptografia e pós-processamento de Participantes
- Criptografia e pós-processamento de Ponto de Extremidade de Saída e Entrada

Para uma visão geral do processamento atual de mensagens de túnel, veja a especificação [Tunnel Implementation](/docs/tunnels/implementation/).

Apenas alterações para roteadores que suportam criptografia de camada ChaCha20 são discutidas.

Nenhuma alteração é considerada para túneis mistos com criptografia de camada AES, até que um protocolo seguro possa ser elaborado
para converter um IV AES de 128 bits em um nonce ChaCha20 de 64 bits. Filtros de Bloom garantem a exclusividade
para o IV completo, mas a primeira metade dos IVs únicos poderia ser idêntica.

Isso significa que a criptografia de camada deve ser uniforme para todos os saltos no túnel, e estabelecida usando
opções de construção de túnel durante o processo de criação do túnel.

Todos os gateways e participantes do túnel precisarão manter um filtro de Bloom para validar os dois nonces independentes.

A ``nonceKey`` mencionada ao longo desta proposta toma o lugar da ``IVKey`` usada na criptografia de camada AES.
É gerada usando o mesmo KDF da proposta 152.

### Criptografia AEAD de Mensagens Entre Saltos

Uma ``AEADKey`` única adicional precisará ser gerada para cada par de saltos consecutivos.
Essa chave será usada por saltos consecutivos para criptografar e descriptografar ChaCha20-Poly1305 a
mensagem de túnel interna criptografada com ChaCha20.

As mensagens de túnel precisarão reduzir o comprimento do quadro criptografado interno em 16 bytes para
acomodar o MAC Poly1305.

AEAD não pode ser usado diretamente nas mensagens, já que a descriptografia iterativa é necessária por túneis de saída.
A descriptografia iterativa só pode ser alcançada, da maneira que é usada atualmente, usando ChaCha20 sem AEAD.

```text
+----+----+----+----+----+----+----+----+
  |    ID do Túnel      |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | tunnelNonce continuar |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  |  obfsNonce continuar  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Dados Criptografados              +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  ID do Túnel :: `TunnelId`
         4 bytes
         o ID do próximo salto

  tunnelNonce ::
         8 bytes
         o nonce de camada de túnel

  obfsNonce ::
         8 bytes
         o nonce de criptografia de camada de túnel

  Dados Criptografados ::
         992 bytes
         a mensagem de túnel criptografada

  Poly1305 MAC ::
         16 bytes

  tamanho total: 1028 Bytes
```

Saltos internos (com saltos precedentes e seguintes), terão duas ``AEADKeys``, uma para descriptografar
a camada AEAD do salto anterior, e criptografar a camada AEAD para o salto seguinte.

Todos os participantes de saltos internos terão, portanto, 64 bytes adicionais de material de chave incluídos em seus BuildRequestRecords.

O Ponto de Extremidade de Saída e o Gateway de Entrada precisarão apenas de 32 bytes adicionais de dados de chave,
já que eles não criptografam camadas de túnel entre si.

O Gateway de Saída gera sua chave ``outAEAD``, que é a mesma que a primeira chave ``inAEAD`` do salto de saída.

O Ponto de Extremidade de Entrada gera sua chave ``inAEAD``, que é a mesma que a chave ``outAEAD`` do salto final
de entrada.

Saltos internos receberão uma ``inAEADKey`` e uma ``outAEADKey`` que serão usadas para descriptografar AEAD
mensagens recebidas e criptografar mensagens enviadas, respectivamente.

Como um exemplo, em um túnel com saltos internos OBGW, A, B, OBEP:

- A chave ``inAEADKey`` de A é a mesma que a chave ``outAEADKey`` do OBGW
- A chave ``inAEADKey`` de B é a mesma que a chave ``outAEADKey`` de A
- A chave ``outAEADKey`` de B é a mesma que a chave ``inAEADKey`` do OBEP

As chaves são únicas para pares de saltos, então a chave ``inAEADKey`` do OBEP será diferente da chave ``inAEADKey`` de A,
a chave ``outAEADKey`` de A diferente da chave ``outAEADKey`` de B, etc.

### Processamento de Mensagens por Criadores de Gateway e Túnel

Gateways irão fragmentar e agrupar mensagens da mesma forma, reservando espaço após o
quadro de fragmento de instruções para o MAC Poly1305.

Mensagens I2NP internas contendo quadros AEAD (incluindo o MAC) podem ser divididas entre fragmentos,
mas qualquer fragmento perdido resultará em falha na descriptografia AEAD (falha na verificação de MAC) no
ponto de extremidade.

### Pré-processamento e Criptografia do Gateway

Quando os túneis suportam criptografia por camada ChaCha20, gateways irão gerar dois nonces de 64 bits por conjunto de mensagens.

Túneis de entrada:

- Criptografar o IV e mensagens de túnel usando ChaCha20
- Usar ``tunnelNonce`` de 8 bytes e ``obfsNonce`` dado o tempo de vida dos túneis
- Usar ``obfsNonce`` de 8 bytes para criptografia de ``tunnelNonce``
- Destruir túnel antes de 2^(64 - 1) - 1 conjuntos de mensagens: 2^63 - 1 = 9.223.372.036.854.775.807

  - Limite de nonce em lugar para evitar colisão dos nonces de 64 bits
  - Limite de nonce quase impossível de ser atingido, dado que isso seria mais de ~15.372.286.728.091.294 msgs/segundo para túneis de 10 minutos

- Ajustar o filtro de Bloom baseado em um número razoável de elementos esperados (128 msgs/seg, 1024 msgs/seg? A definir)

O Gateway de Entrada do túnel (IBGW), processa mensagens recebidas do Ponto de Extremidade de Saída (OBEP) de outro túnel.

Neste ponto, a camada mais externa da mensagem está criptografada usando criptografia de transporte ponto a ponto.
Os cabeçalhos das mensagens I2NP são visíveis, na camada de túnel, para o OBEP e IBGW.
As mensagens I2NP internas estão envolvidas em dentes de alho, criptografadas usando criptografia de sessão de ponta a ponta.

O IBGW pré-processa as mensagens nos formatos de mensagem de túnel apropriados, e criptografa como a seguir:

```text

// IBGW gera nonces aleatórios, garantindo que não há colisão em seu filtro de Bloom para cada nonce
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW ChaCha20 "criptografa" cada uma das mensagens de túnel pré-processadas com seu tunnelNonce e layerKey
  encMsg = ChaCha20(msg = mensagem de túnel, nonce = tunnelNonce, key = layerKey)

  // ChaCha20-Poly1305 criptografa cada quadro de dados criptografado da mensagem com o tunnelNonce e outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

O formato da mensagem de túnel mudará ligeiramente, usando dois nonces de 8 bytes em vez de um IV de 16 bytes.
O ``obfsNonce`` usado para criptografar o nonce é anexado ao ``tunnelNonce`` de 8 bytes,
e é criptografado por cada salto usando o ``tunnelNonce`` criptografado e a ``nonceKey`` do salto.

Após o conjunto de mensagens ter sido descriptografado de forma preemptiva para cada salto, o Gateway de Saída
criptografa AEAD ChaCha20-Poly1305 a parte de texto cifrado de cada mensagem de túnel usando
o ``tunnelNonce`` e sua chave ``outAEADKey``.

Túneis de saída:

- Descriptografar iterativamente mensagens de túnel
- ChaCha20-Poly1305 criptografa quadros de mensagens de túnel descriptografados de forma preemptiva
- Use as mesmas regras para nonces de camada como túneis de entrada
- Gerar nonces aleatórios uma vez por conjunto de mensagens de túnel enviadas

```text


// Para cada conjunto de mensagens, gerar nonces únicos e aleatórios
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // Para cada salto, ChaCha20 o tunnelNonce anterior com a chave IV do salto atual
  tunnelNonce = ChaCha20(msg = tunnelNonce anterior, nonce = obfsNonce, key = nonceKey do salto)

  // Para cada salto, ChaCha20 "descriptografa" a mensagem de túnel com o tunnelNonce e layerKey do salto atual
  decMsg = ChaCha20(msg = mensagem de túnel(s), nonce = tunnelNonce, key = layerKey do salto)

  // Para cada salto, ChaCha20 "descriptografa" o obfsNonce com o tunnelNonce criptografado do salto atual e nonceKey
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey do salto)

  // Após o processamento de salto, ChaCha20-Poly1305 criptografa cada quadro de dados "descriptografado" da mensagem de túnel com o tunnelNonce criptografado do primeiro salto e inAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = tunnelNonce criptografado do primeiro salto, key = inAEADKey do primeiro salto / GW outAEADKey)
```

### Processamento de Participantes

Os participantes acompanharão mensagens vistas da mesma forma, usando filtros de Bloom decrescentes.

Os nonces de túnel precisarão ser criptografados uma vez por salto, para evitar ataques de confirmação
por saltos colaterais, não consecutivos.

Os saltos criptografarão o nonce recebido para evitar ataques de confirmação entre saltos anteriores e posteriores,
isto é, impede que saltos colaterais não consecutivos sejam capazes de dizer que pertencem ao mesmo túnel.

Para validar ``tunnelNonce`` e ``obfsNonce`` recebidos, os participantes verificam cada nonce
individualmente contra seu filtro de Bloom para duplicatas.

Após a validação, o participante:

- Descriptografa cada AEAD de mensagem de túnel ChaCha20-Poly1305 com o ``tunnelNonce`` recebido e sua ``inAEADKey``
- Criptografa o ``tunnelNonce`` com sua ``nonceKey`` e ``obfsNonce`` recebidos
- Criptografa cada quadro de dados criptografado da mensagem de túnel com o ``tunnelNonce`` criptografado e sua ``layerKey``
- Criptografa cada quadro de dados criptografado da mensagem de túnel com o ``tunnelNonce`` criptografado e sua ``outAEADKey`` 
- Criptografa o ``obfsNonce`` com sua ``nonceKey`` e ``tunnelNonce`` criptografado
- Envia o tuplo {``nextTunnelId``, criptografado (``tunnelNonce`` || ``obfsNonce``), ciphertext AEAD || MAC} para o próximo salto.

```text

// Para verificação, saltos de túnel devem verificar o filtro de Bloom para a exclusividade de cada nonce recebido
  // Após a verificação, desinvolve o quadro AEAD através da descriptografia ChaCha20-Poly1305 de cada quadro criptografado de mensagem de túnel
  // com o túnel nonce recebido e inAEADKey 
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = encMsg \|\| MAC recebida, nonce = tunnelNonce recebido, key = inAEADKey)

  // ChaCha20 criptografa o tunnelNonce com o obfsNonce e a nonceKey do salto
  tunnelNonce = ChaCha20(msg = tunnelNonce recebido, nonce = obfsNonce recebido, key = nonceKey)

  // ChaCha20 criptografa cada quadro de dados criptografado da mensagem de túnel com o tunnelNonce criptografado e a layerKey do salto
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // Para proteção AEAD, também ChaCha20-Poly1305 criptografa cada quadro de dados criptografado da mensagem
  // com o tunnelNonce criptografado e a outAEADKey do salto
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // ChaCha20 criptografa o obfsNonce recebido com o tunnelNonce criptografado e a nonceKey do salto
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### Processamento do Ponto de Extremidade de Entrada

Para túneis ChaCha20, o seguinte esquema será usado para descriptografar cada mensagem de túnel:

- Validar o ``tunnelNonce`` e ``obfsNonce`` recebidos de forma independente contra seu filtro de Bloom
- Descriptografar o quadro de dados criptografado ChaCha20-Poly1305 usando o ``tunnelNonce`` recebido e ``inAEADKey``
- Descriptografar o quadro de dados criptografado usando o ``tunnelNonce`` recebido e a ``layerKey`` do salto
- Descriptografar o ``obfsNonce`` usando a ``nonceKey`` do salto e o ``tunnelNonce`` recebido para obter o ``obfsNonce`` precedente
- Descriptografar o ``tunnelNonce`` recebido usando a ``nonceKey`` do salto e o ``obfsNonce`` descriptografado para obter o ``tunnelNonce`` precedente
- Descriptografar os dados criptografados usando o ``tunnelNonce`` descriptografado e a ``layerKey`` do salto precedente
- Repetir os passos para descriptografia de nonce e camada em cada salto do túnel, voltando para o IBGW
- A descriptografia do quadro AEAD é necessária apenas na primeira rodada

```text

// Para a primeira rodada, descriptografar cada quadro de dados criptografado da mensagem + MAC usando ChaCha20-Poly1305
  // usando o tunnelNonce recebido e inAEADKey
  msg = encTunMsg \|\| MAC
  tunnelNonce = tunnelNonce recebido
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // Repetir para cada salto do túnel voltando para o IBGW
  // Para cada rodada, descriptografar cada camada de criptografia de cada mensagem de quadro de dados criptografado usando ChaCha20
  // Substituir o tunnelNonce recebido pelo tunnelNonce descriptografado da rodada anterior para cada salto
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### Análise de Segurança para Criptografia de Camada de Túnel ChaCha20+ChaCha20-Poly1305

A mudança de AES256/ECB+AES256/CBC para ChaCha20+ChaCha20-Poly1305 tem várias vantagens e novas considerações de segurança.

As maiores considerações de segurança a serem consideradas são que os nonces ChaCha20 e ChaCha20-Poly1305 devem ser únicos por mensagem para a vida útil da chave que está sendo usada.

O não uso de nonces únicos com a mesma chave em mensagens diferentes compromete ChaCha20 e ChaCha20-Poly1305.

Usar um ``obfsNonce`` anexado permite que o IBEP descriptografe o ``tunnelNonce`` para cada salto de criptografia de camada,
recuperando o nonce anterior.

O ``obfsNonce`` juntamente com o ``tunnelNonce`` não revela nenhuma informação nova para os saltos do túnel,
uma vez que o ``obfsNonce`` é criptografado usando o ``tunnelNonce`` criptografado. Isso também permite que o IBEP recupere 
o ``obfsNonce`` anterior de forma similar à recuperação de ``tunnelNonce``.

A maior vantagem de segurança é que não há ataques de confirmação ou oracle contra ChaCha20,
e usar ChaCha20-Poly1305 entre saltos adiciona proteção AEAD contra manipulação de ciphertext por
atacantes de MitM fora de banda.

Existem ataques oracle práticos contra AES256/ECB + AES256/CBC, quando a chave é reutilizada (como na criptografia de camada de túnel).

Os ataques oracle contra AES256/ECB não funcionarão, por causa da criptografia dupla usada, e a criptografia é sobre um bloco único (o IV do túnel).

Os ataques oracle de padding contra AES256/CBC não funcionarão, porque nenhum padding é usado. Se o comprimento da mensagem do túnel mudar para comprimentos não-múltiplos de 16, o AES256/CBC ainda não seria vulnerável devido à rejeição de IVs duplicados.

Ambos os ataques também são bloqueados por desabilitar múltiplas chamadas oracle usando o mesmo IV, uma vez que IVs duplicados são rejeitados.

## Referências

* [Tunnel-Implementation](/docs/tunnels/implementation/)
