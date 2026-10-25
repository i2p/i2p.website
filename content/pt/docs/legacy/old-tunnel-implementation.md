---
title: "Implementação de Tunnel Antiga"
description: "Documentação histórica da implementação original de tunnel do I2P antes da versão 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/pt/docs/historical/tunnel-alt"
  - "/pt/docs/historical/tunnel-alt/"
  - "/pt/tunnel"
  - "/pt/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Nota: Obsoleto - NÃO usado! Substituído na versão 0.6.1.10 - veja a [implementação atual](/docs/specs/tunnel-implementation) para a especificação ativa.**

## 1) Visão geral do tunnel {#tunnel.overview}

Dentro do I2P, as mensagens são passadas em uma direção através de um tunnel virtual de peers, usando qualquer meio disponível para passar a mensagem para o próximo salto. As mensagens chegam ao gateway do tunnel, são empacotadas para o caminho, e são encaminhadas para o próximo salto no tunnel, que processa e verifica a validade da mensagem e a envia para o próximo salto, e assim por diante, até chegar ao endpoint do tunnel. Esse endpoint pega as mensagens empacotadas pelo gateway e as encaminha conforme instruído - seja para outro router, para outro tunnel em outro router, ou localmente.

Todos os tunnels funcionam da mesma forma, mas podem ser segmentados em dois grupos diferentes - tunnels de entrada e tunnels de saída. Os tunnels de entrada têm um gateway não confiável que passa mensagens para baixo em direção ao criador do tunnel, que serve como o ponto final do tunnel. Para tunnels de saída, o criador do tunnel serve como gateway, passando mensagens para o ponto final remoto.

O criador do tunnel seleciona exatamente quais peers irão participar no tunnel, e fornece a cada um os dados de configuração necessários. Eles podem variar em comprimento de 0 saltos (onde o gateway é também o endpoint) até 7 saltos (onde há 6 peers após o gateway e antes do endpoint). A intenção é tornar difícil tanto para os participantes quanto para terceiros determinar o comprimento de um tunnel, ou mesmo para participantes em conluio determinar se fazem parte do mesmo tunnel (exceto na situação onde peers em conluio estão próximos uns dos outros no tunnel). Mensagens que foram corrompidas também são descartadas o mais rapidamente possível, reduzindo a carga da rede.

Além do seu comprimento, existem parâmetros configuráveis adicionais para cada tunnel que podem ser usados, como uma limitação no tamanho ou frequência das mensagens entregues, como o preenchimento deve ser usado, por quanto tempo um tunnel deve estar em operação, se deve injetar mensagens falsas, se deve usar fragmentação, e quais estratégias de agrupamento, se houver, devem ser empregadas.

Na prática, uma série de pools de tunnel são usados para diferentes propósitos - cada destino de cliente local tem seu próprio conjunto de tunnels de entrada e tunnels de saída, configurados para atender às suas necessidades de anonimato e desempenho. Além disso, o próprio router mantém uma série de pools para participar no netDb e para gerenciar os próprios tunnels.

I2P é uma rede inerentemente comutada por pacotes, mesmo com esses tunnels, permitindo que tire vantagem de múltiplos tunnels executando em paralelo, aumentando a resiliência e balanceando a carga. Fora da camada central do I2P, há uma biblioteca de streaming ponto a ponto opcional disponível para aplicações cliente, expondo operação semelhante ao TCP, incluindo reordenação de mensagens, retransmissão, controle de congestionamento, etc.

## 2) Operação do tunnel {#tunnel.operation}

A operação do tunnel tem quatro processos distintos, realizados por vários pares no tunnel. Primeiro, o gateway do tunnel acumula uma quantidade de mensagens do tunnel e as pré-processa em algo para entrega do tunnel. Em seguida, esse gateway criptografa esses dados pré-processados, depois os encaminha para o primeiro salto. Esse par, e os participantes subsequentes do tunnel, removem uma camada da criptografia, verificando a integridade da mensagem, depois a encaminham para o próximo par. Eventualmente, a mensagem chega ao endpoint onde as mensagens agrupadas pelo gateway são separadas novamente e encaminhadas conforme solicitado.

IDs de tunnel são números de 4 bytes usados em cada salto - os participantes sabem qual ID de tunnel devem escutar para mensagens e qual ID de tunnel as mensagens devem ser encaminhadas para o próximo salto. Os tunnels em si são de curta duração (10 minutos no momento), mas dependendo do propósito do tunnel, e embora tunnels subsequentes possam ser construídos usando a mesma sequência de peers, o ID de tunnel de cada salto mudará.

### 2.1) Pré-processamento de mensagens {#tunnel.preprocessing}

Quando o gateway quer entregar dados através do tunnel, ele primeiro coleta zero ou mais mensagens I2NP (não mais que 32KB no total), seleciona quanto padding será usado, e decide como cada mensagem I2NP deve ser tratada pelo endpoint do tunnel, codificando esses dados no payload bruto do tunnel:

- inteiro sem sinal de 2 bytes especificando o número de bytes de preenchimento
- essa quantidade de bytes aleatórios
- uma série de zero ou mais pares { instruções, mensagem }

As instruções são codificadas da seguinte forma:

- Valor de 1 byte:
  ```
  bits 0-1: tipo de entrega
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: atraso incluído?  (1 = verdadeiro, 0 = falso)
     bit 3: fragmentado?  (1 = verdadeiro, 0 = falso)
     bit 4: opções estendidas?  (1 = verdadeiro, 0 = falso)
  bits 5-7: reservado
  ```
- se o tipo de entrega foi TUNNEL, um ID de tunnel de 4 bytes
- se o tipo de entrega foi TUNNEL ou ROUTER, um hash de router de 32 bytes
- se a flag de atraso incluído for verdadeira, um valor de 1 byte:
  ```
     bit 0: tipo (0 = rigoroso, 1 = randomizado)
  bits 1-7: expoente de atraso (2^valor minutos)
  ```
- se a flag de fragmentado for verdadeira, um ID de mensagem de 4 bytes, e um valor de 1 byte:
  ```
  bits 0-6: número do fragmento
     bit 7: é o último?  (1 = verdadeiro, 0 = falso)
  ```
- se a flag de opções estendidas for verdadeira:
  ```
  = um tamanho de opção de 1 byte (em bytes)
  = essa quantidade de bytes
  ```
- Tamanho de 2 bytes da mensagem I2NP

A mensagem I2NP é codificada em sua forma padrão, e a carga útil pré-processada deve ser preenchida para um múltiplo de 16 bytes.

### 2.2) Processamento do gateway {#tunnel.gateway}

Após o pré-processamento das mensagens em uma carga útil preenchida, o gateway criptografa a carga útil com as oito chaves, construindo um bloco de checksum para que cada peer possa verificar a integridade da carga útil a qualquer momento, bem como um bloco de verificação fim a fim para o endpoint do tunnel verificar a integridade do bloco de checksum. Os detalhes específicos seguem.

A criptografia usada é tal que a descriptografia requer apenas executar os dados com AES no modo CBC, calcular o SHA256 de uma determinada porção fixa da mensagem (bytes 16 até $size-144), e procurar pelos primeiros 16 bytes desse hash no bloco de checksum. Há um número fixo de saltos definido (8 peers) para que possamos verificar a mensagem sem vazar a posição no tunnel ou fazer com que a mensagem continue "encolhendo" conforme as camadas são removidas. Para tunnels com menos de 8 saltos, o criador do tunnel assumirá o lugar dos saltos em excesso, descriptografando com suas chaves (para tunnels de saída, isso é feito no início, e para tunnels de entrada, no final).

A parte difícil na criptografia é construir aquele bloco de checksum entrelaçado, que requer essencialmente descobrir como será o hash da carga útil em cada etapa, ordenar aleatoriamente esses hashes, depois construir uma matriz de como cada um desses hashes ordenados aleatoriamente será em cada etapa. O próprio gateway deve fingir que é um dos pares dentro do bloco de checksum para que o primeiro salto não possa dizer que o salto anterior foi o gateway. Para visualizar isso um pouco:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
No exemplo acima, P[7] é o mesmo que os dados originais sendo passados através do tunnel (as mensagens pré-processadas), e V[7] são os primeiros 16 bytes do SHA256 de eH[0-7] como visto no peer7 após a descriptografia. Para células na matriz "acima" do hash, seu valor é derivado criptografando a célula abaixo dela com a chave do peer abaixo dela, usando o final da coluna à esquerda como IV. Para células na matriz "abaixo" do hash, elas são iguais à célula acima delas, descriptografadas pela chave do peer atual, usando o final do bloco criptografado anterior naquela linha.

Com esta matriz randomizada de blocos de checksum, cada peer será capaz de encontrar o hash do payload, ou se não estiver lá, saber que a mensagem está corrompida. O emaranhamento usando o modo CBC aumenta a dificuldade em marcar os próprios blocos de checksum, mas ainda é possível que essa marcação passe brevemente despercebida se as colunas após os dados marcados já tiverem sido usadas para verificar o payload em um peer. Em qualquer caso, o endpoint do tunnel (peer 7) sabe com certeza se algum dos blocos de checksum foi marcado, pois isso corromperia o bloco de verificação (V[7]).

O IV[0] é um valor aleatório de 16 bytes, e IV[i] são os primeiros 16 bytes de H(D(IV[i-1], K[i-1]) xor IV_WHITENER). Não usamos o mesmo IV ao longo do caminho, pois isso permitiria conluio trivial, e usamos o hash do valor descriptografado para propagar o IV de forma a dificultar o vazamento de chaves. IV_WHITENER é um valor fixo de 16 bytes.

Quando o gateway quer enviar a mensagem, ele exporta a linha correta para o peer que é o primeiro salto (geralmente a linha peer1.recv) e encaminha isso inteiramente.

### 2.3) Processamento de participante {#tunnel.participant}

Quando um participante em um tunnel recebe uma mensagem, eles descriptografam uma camada com sua chave de tunnel usando AES256 no modo CBC com os primeiros 16 bytes como IV. Em seguida, calculam o hash do que veem como payload (bytes 16 até $size-144) e procuram pelos primeiros 16 bytes desse hash dentro do bloco de checksum descriptografado. Se nenhuma correspondência for encontrada, a mensagem é descartada. Caso contrário, o IV é atualizado descriptografando-o, fazendo XOR desse valor com o IV_WHITENER, e substituindo-o pelos primeiros 16 bytes do seu hash. A mensagem resultante é então encaminhada para o próximo peer para processamento.

Para prevenir ataques de replay ao nível do tunnel, cada participante mantém registro dos IVs recebidos durante o tempo de vida do tunnel, rejeitando duplicatas. O uso de memória necessário deve ser menor, já que cada tunnel tem apenas um tempo de vida muito curto (10m no momento). Um fluxo constante de 100KBps através de um tunnel com mensagens completas de 32KB resultaria em 1875 mensagens, exigindo menos de 30KB de memória. Gateways e endpoints lidam com replay rastreando os IDs de mensagem e expirações nas mensagens I2NP contidas no tunnel.

### 2.4) Processamento de endpoint {#tunnel.endpoint}

Quando uma mensagem alcança o endpoint do tunnel, eles a descriptografam e verificam como um participante normal. Se o bloco de checksum tem uma correspondência válida, o endpoint então calcula o hash do próprio bloco de checksum (como visto após a descriptografia) e compara isso com o hash de verificação descriptografado (os últimos 16 bytes). Se esse hash de verificação não corresponder, o endpoint toma nota da tentativa de marcação por um dos participantes do tunnel e talvez descarte a mensagem.

Neste ponto, o endpoint do tunnel tem os dados pré-processados enviados pelo gateway, que pode então analisar para extrair as mensagens I2NP incluídas e encaminhá-las conforme solicitado em suas instruções de entrega.

### 2.5) Preenchimento {#tunnel.padding}

Várias estratégias de preenchimento de tunnel são possíveis, cada uma com suas próprias vantagens:

- Sem preenchimento
- Preenchimento para um tamanho aleatório
- Preenchimento para um tamanho fixo
- Preenchimento para o KB mais próximo
- Preenchimento para o tamanho exponencial mais próximo (2^n bytes)

*Qual usar? sem padding é mais eficiente, padding aleatório é o que temos agora, tamanho fixo seria um desperdício extremo ou nos forçaria a implementar fragmentação. Padding para o tamanho exponencial mais próximo (como o Freenet) parece promissor. Talvez devêssemos coletar algumas estatísticas na rede sobre quais tamanhos de mensagens existem, então ver quais custos e benefícios surgiriam de diferentes estratégias?*

### 2.6) Fragmentação de tunnel {#tunnel.fragmentation}

Para vários esquemas de preenchimento e mistura, pode ser útil do ponto de vista do anonimato fragmentar uma única mensagem I2NP em múltiplas partes, cada uma entregue separadamente através de diferentes mensagens de tunnel. O endpoint pode ou não suportar essa fragmentação (descartando ou mantendo fragmentos conforme necessário), e o tratamento de fragmentação não será implementado imediatamente.

### 2.7) Alternativas {#tunnel.alternatives}

#### 2.7.1) Não use um bloco de checksum {#tunnel.nochecksum}

Uma alternativa ao processo acima é remover completamente o bloco de checksum e substituir o hash de verificação por um hash simples da carga útil. Isso simplificaria o processamento no gateway do tunnel e economizaria 144 bytes de largura de banda em cada salto. Por outro lado, atacantes dentro do tunnel poderiam trivialmente ajustar o tamanho da mensagem para um que seja facilmente rastreável por observadores externos conluiados, além de participantes posteriores do tunnel. A corrupção também incorreria no desperdício de toda a largura de banda necessária para transmitir a mensagem. Sem a validação por salto, também seria possível consumir recursos excessivos da rede construindo tunnels extremamente longos, ou criando loops no tunnel.

#### 2.7.2) Ajustar processamento de tunnel no meio do fluxo {#tunnel.reroute}

Embora o algoritmo simples de roteamento de tunnel deva ser suficiente para a maioria dos casos, existem três alternativas que podem ser exploradas:

- Atrasar uma mensagem dentro de um tunnel em um hop arbitrário por um período específico de tempo ou por um período aleatório. Isso poderia ser alcançado substituindo o hash no bloco de checksum com, por exemplo, os primeiros 8 bytes do hash, seguidos de algumas instruções de atraso. Alternativamente, as instruções poderiam dizer ao participante para realmente interpretar o payload bruto como está, e descartar a mensagem ou continuar a encaminhá-la pelo caminho (onde seria interpretada pelo endpoint como uma mensagem chaff). A parte posterior disso exigiria que o gateway ajustasse seu algoritmo de criptografia para produzir o payload de texto claro em um hop diferente, mas não deveria ser muito problemático.

- Permitir que os routers participando em um tunnel remixem a mensagem antes
  de encaminhá-la - fazendo-a ricochetear através de um dos próprios tunnels de saída desse peer,
  portando instruções para entrega ao próximo salto. Isso poderia ser usado de forma
  controlada (com instruções en-route como os atrasos mencionados acima) ou
  probabilística.

- Implementar código para o criador de tunnel redefinir o "próximo salto" de um peer no tunnel, permitindo redirecionamento dinâmico adicional.

#### 2.7.3) Use túneis bidirecionais {#tunnel.bidirectional}

A estratégia atual de usar dois tunnels separados para comunicação de entrada e saída não é a única técnica disponível, e ela tem implicações para o anonimato. Do lado positivo, ao usar tunnels separados, reduz-se os dados de tráfego expostos para análise aos participantes em um tunnel - por exemplo, peers em um tunnel de saída de um navegador web veriam apenas o tráfego de um HTTP GET, enquanto os peers em um tunnel de entrada veriam a carga útil entregue ao longo do tunnel. Com tunnels bidirecionais, todos os participantes teriam acesso ao fato de que, por exemplo, 1KB foi enviado em uma direção, depois 100KB na outra. Do lado negativo, usar tunnels unidirecionais significa que há dois conjuntos de peers que precisam ser perfilados e contabilizados, e cuidado adicional deve ser tomado para abordar a velocidade aumentada de ataques predecessor. O processo de pooling e construção de tunnels descrito abaixo deve minimizar as preocupações do ataque predecessor, embora se fosse desejado, não seria muito trabalho construir tanto os tunnels de entrada quanto os de saída ao longo dos mesmos peers.

#### 2.7.4) Usar tamanho de bloco menor {#tunnel.smallerhashes}

No momento, nosso uso do AES limita o tamanho do bloco a 16 bytes, o que por sua vez fornece o tamanho mínimo para cada uma das colunas do bloco de checksum. Se outro algoritmo fosse usado com um tamanho de bloco menor, ou pudesse de outra forma permitir a construção segura do bloco de checksum com porções menores do hash, poderia valer a pena explorar. Os 16 bytes usados agora em cada hop devem ser mais do que suficientes.

## 3) Construção de tunnel {#tunnel.building}

Ao construir um tunnel, o criador deve enviar uma solicitação com os dados de configuração necessários para cada um dos saltos, então aguardar o participante potencial responder declarando que concorda ou não concorda. Essas mensagens de solicitação de tunnel e suas respostas são envolvidas com garlic encryption para que apenas o router que conhece a chave possa descriptografá-las, e o caminho percorrido em ambas as direções também é roteado por tunnel. Há três dimensões importantes a se manter em mente ao produzir os tunnels: quais peers são usados (e onde), como as solicitações são enviadas (e respostas recebidas), e como são mantidos.

### 3.1) Seleção de peers {#tunnel.peerselection}

Além dos dois tipos de tunnels - inbound e outbound - há dois estilos de seleção de peers usados para diferentes tunnels - exploratórios e de cliente. Tunnels exploratórios são usados tanto para manutenção da base de dados da rede quanto para manutenção de tunnels, enquanto tunnels de cliente são usados para mensagens cliente de ponta a ponta.

#### 3.1.1) Seleção de peers para tunnel exploratório {#tunnel.selection.exploratory}

Tunnels exploratórios são construídos a partir de uma seleção aleatória de pares de um subconjunto da rede. O subconjunto específico varia no router local e em suas necessidades de roteamento de tunnel. Em geral, os tunnels exploratórios são construídos a partir de pares selecionados aleatoriamente que estão na categoria de perfil "não falhando mas ativo" do par. O propósito secundário dos tunnels, além do mero roteamento de tunnel, é encontrar pares de alta capacidade subutilizados para que possam ser promovidos para uso em tunnels de cliente.

#### 3.1.2) Seleção de peers de tunnel do cliente {#tunnel.selection.client}

Os túneis de cliente são construídos com um conjunto mais rigoroso de requisitos - o router local selecionará pares de sua categoria de perfil "rápido e alta capacidade" para que o desempenho e a confiabilidade atendam às necessidades da aplicação cliente. No entanto, existem vários detalhes importantes além dessa seleção básica que devem ser seguidos, dependendo das necessidades de anonimato do cliente.

Para alguns clientes que estão preocupados com adversários executando um ataque predecessor, a seleção de tunnel pode manter os peers selecionados em uma ordem estrita - se A, B e C estão em um tunnel, o salto após A é sempre B, e o salto após B é sempre C. Uma ordenação menos estrita também é possível, assegurando que embora o salto após A possa ser B, B nunca pode estar antes de A. Outras opções de configuração incluem a capacidade de apenas os gateways de tunnel de entrada e endpoints de tunnel de saída serem fixos, ou alternados em uma taxa MTBF.

### 3.2) Entrega de solicitação {#tunnel.request}

Como mencionado acima, uma vez que o criador do tunnel sabe quais peers devem entrar no tunnel e em que ordem, o criador constrói uma série de mensagens de solicitação de tunnel, cada uma contendo as informações necessárias para esse peer. Por exemplo, tunnels participantes receberão o ID de tunnel de 4 bytes no qual devem receber mensagens, o ID de tunnel de 4 bytes no qual devem enviar as mensagens, o hash de 32 bytes da identidade do próximo hop, e a chave de camada de 32 bytes usada para remover uma camada do tunnel. Naturalmente, endpoints de tunnels de saída não recebem informações sobre "próximo hop" ou "próximo ID de tunnel". Gateways de tunnels de entrada, no entanto, recebem as 8 chaves de camada na ordem em que devem ser criptografadas (como descrito acima). Para permitir respostas, a solicitação contém uma session tag aleatória e uma chave de sessão aleatória com a qual o peer pode usar garlic encryption para sua decisão, bem como o tunnel para o qual esse garlic deve ser enviado. Além das informações acima, várias opções específicas do cliente podem ser incluídas, como qual limitação aplicar ao tunnel, quais estratégias de preenchimento ou lote usar, etc.

Após construir todas as mensagens de solicitação, elas são embrulhadas com garlic encryption para o router de destino e enviadas através de um tunnel exploratório. Ao receber, esse peer determina se pode ou vai participar, criando uma mensagem de resposta e tanto embrulhando com garlic encryption quanto roteando pelo tunnel a resposta com as informações fornecidas. Ao receber a resposta no criador do tunnel, o tunnel é considerado válido nesse salto (se aceito). Uma vez que todos os peers aceitaram, o tunnel fica ativo.

### 3.3) Agrupamento {#tunnel.pooling}

Para permitir uma operação eficiente, o router mantém uma série de pools de tunnel, cada um gerenciando um grupo de tunnels usados para um propósito específico com sua própria configuração. Quando um tunnel é necessário para esse propósito, o router seleciona um do pool apropriado aleatoriamente. No geral, há dois pools de tunnel exploratórios - um de entrada e um de saída - cada um usando os padrões de exploração do router. Além disso, há um par de pools para cada destino local - um tunnel de entrada e um de saída. Esses pools usam a configuração especificada quando o destino local se conectou ao router, ou os padrões do router se não especificado.

Cada pool tem em sua configuração algumas definições-chave, definindo quantos tunnels manter ativos, quantos tunnels de backup manter em caso de falha, com que frequência testar os tunnels, qual deve ser o comprimento dos tunnels, se esses comprimentos devem ser aleatorizados, com que frequência os tunnels de substituição devem ser construídos, bem como qualquer uma das outras configurações permitidas ao configurar tunnels individuais.

### 3.4) Alternativas {#tunnel.building.alternatives}

#### 3.4.1) Construção telescópica {#tunnel.building.telescoping}

Uma pergunta que pode surgir em relação ao uso dos túneis exploratórios para enviar e receber mensagens de criação de túnel é como isso impacta a vulnerabilidade do túnel a ataques de predecessor. Embora os endpoints e gateways desses túneis sejam distribuídos aleatoriamente pela rede (talvez até incluindo o criador do túnel nesse conjunto), uma alternativa é usar os próprios caminhos do túnel para transmitir a solicitação e resposta, como é feito no [TOR](https://www.torproject.org/). Isso, no entanto, pode levar a vazamentos durante a criação do túnel, permitindo que pares descubram quantos hops existem mais adiante no túnel através do monitoramento do tempo ou contagem de pacotes conforme o túnel é construído. Técnicas poderiam ser usadas para minimizar essa questão, como usar cada um dos hops como endpoints (conforme [2.7.2](#tunnel.reroute)) para um número aleatório de mensagens antes de continuar para construir o próximo hop.

#### 3.4.2) Tunnels não-exploratórios para gestão {#tunnel.building.nonexploratory}

Uma segunda alternativa para o processo de construção de túneis é dar ao router um conjunto adicional de pools de entrada e saída não-exploratórios, usando-os para a solicitação e resposta do túnel. Assumindo que o router tem uma visão bem integrada da rede, isso não deveria ser necessário, mas se o router estivesse particionado de alguma forma, usar pools não-exploratórios para gerenciamento de túneis reduziria o vazamento de informações sobre quais peers estão na partição do router.

## 4) Limitação de tunnel {#tunnel.throttling}

Embora os tunnels dentro do I2P tenham semelhança com uma rede de comutação de circuitos, tudo dentro do I2P é estritamente baseado em mensagens - tunnels são apenas truques contábeis para ajudar a organizar a entrega de mensagens. Nenhuma suposição é feita sobre confiabilidade ou ordenação de mensagens, e retransmissões são deixadas para níveis superiores (por exemplo, a biblioteca de streaming da camada cliente do I2P). Isso permite que o I2P aproveite técnicas de throttling disponíveis tanto para redes de comutação de pacotes quanto de comutação de circuitos. Por exemplo, cada router pode acompanhar a média móvel de quanta dados cada tunnel está usando, combinar isso com todas as médias usadas por outros tunnels dos quais o router está participando, e ser capaz de aceitar ou rejeitar solicitações adicionais de participação em tunnel baseado em sua capacidade e utilização. Por outro lado, cada router pode simplesmente descartar mensagens que estão além de sua capacidade, explorando a pesquisa usada na Internet normal.

## 5) Mistura/agrupamento {#tunnel.mixing}

Que estratégias devem ser usadas no gateway e em cada hop para atrasar, reordenar, redirecionar ou adicionar padding às mensagens? Até que ponto isso deve ser feito automaticamente, quanto deve ser configurado como uma configuração por tunnel ou por hop, e como o criador do tunnel (e por sua vez, o usuário) deve controlar essa operação? Tudo isso permanece desconhecido, a ser resolvido em uma versão futura.
