---
title: "Especificação SAM V1"
description: "Protocolo Simple Anonymous Messaging legado versão 1 (descontinuado)"
slug: "sam"
aliases:
  - "/pt/docs/api/sam"
  - "/pt/docs/api/sam/"
  - "/pt/sam"
  - "/pt/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Aviso - Obsoleto - Não suportado - Use [SAMv3](/docs/api/samv3)

Especificado abaixo está a versão 1 de um protocolo de cliente simples para interagir com I2P. Alternativas mais recentes: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Bibliotecas de linguagem para a API SAMv1

- C
- C#
- Perl
- Python

As bibliotecas estão no repositório de código-fonte do I2P.

### Alterações do I2P 0.9.14

A versão relatada permanece "1.0".

- DEST GENERATE agora suporta um parâmetro SIGNATURE_TYPE.
- O parâmetro MIN no HELLO VERSION agora é opcional.
- Os parâmetros MIN e MAX no HELLO VERSION agora suportam versões de um dígito como "3".

## Protocolo Versão 1

A aplicação cliente comunica com a ponte SAMv3, que lida com toda a funcionalidade I2P (usando a biblioteca de streaming para streams virtuais, ou I2CP diretamente para mensagens assíncronas).

Toda a comunicação cliente\<--\>ponte SAM é não criptografada e não autenticada através de um único socket TCP. O acesso à ponte SAM deve ser protegido através de firewalls ou outros meios (talvez a ponte possa ter ACLs sobre quais IPs ela aceita conexões).

Todas essas mensagens SAM são enviadas em uma única linha em ASCII simples, terminadas pelo caractere de nova linha (\\n). A formatação mostrada abaixo é apenas para legibilidade, e embora as duas primeiras palavras em cada mensagem devam permanecer em sua ordem específica, a ordenação dos pares chave=valor pode mudar (por exemplo, "ONE TWO A=B C=D" ou "ONE TWO C=D A=B" são ambas construções perfeitamente válidas). Além disso, o protocolo é sensível a maiúsculas e minúsculas.

As mensagens SAM são interpretadas em UTF-8. Os pares chave=valor devem ser separados por um único espaço. Os valores podem ser delimitados por aspas duplas se contiverem espaços, por exemplo chave="texto longo de valor". Não há mecanismo de escape.

A comunicação pode assumir três formas distintas:

- [Streams virtuais](/docs/api/streaming)
- [Datagramas com resposta](/docs/specs/datagrams#repliable) (mensagens com um campo FROM)
- [Datagramas anônimos](/docs/specs/datagrams#raw) (mensagens anônimas brutas)

## Handshake de Conexão SAM

Nenhuma comunicação SAM pode ocorrer até que o cliente e a ponte tenham acordado sobre uma versão do protocolo, o que é feito através do cliente enviando um HELLO e a ponte enviando um HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
e

```
HELLO REPLY RESULT=$result VERSION=1.0
```
A partir do I2P 0.9.14, o parâmetro MIN é opcional. O parâmetro MAX deve ser fornecido e ser maior ou igual a "1" e menor que "2" para usar a versão 1.

O valor RESULT pode ser um dos seguintes:

- `OK`
- `NOVERSION`

## Sessões SAM

Uma sessão SAM é criada por um cliente abrindo um socket para a bridge SAM, realizando um handshake e enviando uma mensagem SESSION CREATE, e a sessão termina quando o socket é desconectado.

Cada Destination I2P só pode ser usado para uma sessão SAM por vez, e só pode usar uma dessas formas (mensagens recebidas através de outras formas são descartadas).

A mensagem SESSION CREATE enviada pelo cliente para a ponte é a seguinte:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION especifica que destino deve ser usado para enviar e receber mensagens/streams. Se um $name for fornecido, a ponte SAM procura em seu próprio armazenamento local (o arquivo sam.keys) por um destino associado (e chave privada). Se não existir uma associação correspondente a esse nome, ela cria uma nova. Se o destino for especificado como TRANSIENT, sempre cria um novo.

Note que DESTINATION é um identificador, *não* dados codificados em Base 64. Para especificar o Destination, você deve usar [SAM V3](/docs/api/samv3).

A DIRECTION pode ser especificada apenas para sessões STREAM, instruindo a ponte que o cliente estará criando ou recebendo streams, ou ambos. Se isso não for especificado, BOTH será assumido. Tentar criar um stream de saída quando DIRECTION=RECEIVE deve resultar em um erro, e streams de entrada quando DIRECTION=CREATE serão ignorados.

Opções adicionais fornecidas devem ser enviadas para a configuração da sessão I2P se não forem interpretadas pela ponte SAM (por exemplo, "tunnels.depthInbound=0"). Essas opções estão documentadas abaixo.

A própria bridge SAM já deve estar configurada com qual router deve se comunicar através do I2P (embora, se necessário, possa haver uma forma de fornecer uma substituição, por exemplo, i2cp.tcp.host=localhost e i2cp.tcp.port=7654).

Após receber a mensagem de criação de sessão, a ponte SAM responderá com uma mensagem de status da sessão, como segue:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
O valor RESULT pode ser um dos seguintes:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Se não estiver OK, a MESSAGE deve conter informações legíveis por humanos sobre por que a sessão não pôde ser criada.

Note que não há aviso dado se o $name não for encontrado e um destino transitório for criado no lugar. Note que o destino base 64 transitório real não é exibido na resposta; é o $name ou TRANSIENT como fornecido em SESSION CREATE. Se você precisar dessas funcionalidades, deve usar [SAM V3](/docs/api/samv3).

## SAM Virtual Streams

Os fluxos virtuais são garantidos de serem enviados de forma confiável e em ordem, com notificação de falha e sucesso assim que estiver disponível.

Após estabelecer a sessão com STYLE=STREAM, tanto o cliente quanto a ponte SAM podem enviar assincronamente várias mensagens de ida e volta para gerenciar os streams, conforme listado abaixo:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Isso estabelece uma nova conexão virtual do destino local para o peer especificado, marcando-a com o ID único com escopo de sessão. O ID único é um inteiro ASCII base 10 de 1 até (2^31-1).

O $destination é a base 64 do [Destination](/docs/specs/common-structures#type_Destination), que são 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A bridge SAM deve responder a isso com uma mensagem de status de stream:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
O valor RESULT pode ser um dos seguintes:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

Se o RESULT for OK, o destino especificado está ativo e autorizou a conexão; se a conexão não foi possível (timeout, etc), RESULT conterá o valor de erro apropriado (acompanhado de uma MESSAGE opcional legível por humanos).

No lado receptor, a ponte SAM simplesmente notifica o cliente da seguinte forma:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Isso informa ao cliente que o destino fornecido criou uma conexão virtual com ele. O fluxo de dados seguinte será marcado com o ID único fornecido, que é um inteiro ASCII base 10 de -1 até -(2^31-1).

O $destination é o base 64 do [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

Quando o cliente deseja enviar dados na conexão virtual, ele faz isso da seguinte forma:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Isto adiciona os dados especificados ao buffer sendo enviado para o peer através da conexão virtual. O tamanho de envio $numBytes é quantos bytes de 8 bits são incluídos após a nova linha, que pode ser de 1 até 32768 (32KB).

A ponte SAM fará então o seu melhor para entregar a mensagem o mais rápida e eficientemente possível, talvez agrupando múltiplas mensagens SEND em buffer. Se houver um erro na entrega dos dados, ou se o lado remoto fechar a conexão, a ponte SAM informará o cliente:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
O valor RESULT pode ser um dos seguintes:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

Se a conexão foi fechada corretamente pelo outro peer, $result é definido como OK. Se $result não for OK, MESSAGE pode transmitir uma mensagem descritiva, como "peer unreachable", etc. Sempre que um cliente quiser fechar a conexão, ele envia a mensagem de fechamento para a bridge SAM:

```
STREAM CLOSE
       ID=$id
```
A bridge então limpa o que precisa e descarta esse ID - nenhuma mensagem adicional pode ser enviada ou recebida através dele.

Para o outro lado da comunicação, sempre que o peer tiver enviado alguns dados e estiverem disponíveis para o cliente, a ponte SAM irá entregá-los prontamente:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Todos os fluxos são implicitamente fechados pela conexão entre a ponte SAM e o cliente sendo interrompida.

## SAM Repliable Datagrams

Embora o I2P não contenha inerentemente um endereço FROM, para facilitar o uso é fornecida uma camada adicional como datagramas respondíveis - mensagens não ordenadas e não confiáveis de até 31744 bytes que incluem um endereço FROM (deixando até 1KB para material de cabeçalho). Este endereço FROM é autenticado internamente pelo SAM (fazendo uso da chave de assinatura do destino para verificar a origem) e inclui prevenção de replay.

O tamanho mínimo é 1. Para melhor confiabilidade de entrega, o tamanho máximo recomendado é aproximadamente 11 KB.

Após estabelecer uma sessão SAM com STYLE=DATAGRAM, o cliente pode enviar ao bridge SAM:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Quando um datagrama chega, a ponte o entrega ao cliente via:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
O $destination é a base 64 da [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres em base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A ponte SAM nunca expõe ao cliente os cabeçalhos de autenticação ou outros campos, apenas os dados que o remetente forneceu. Isso continua até que a sessão seja fechada (pelo cliente interrompendo a conexão).

## Datagramas Anônimos SAM

Aproveitando ao máximo a largura de banda do I2P, SAM permite que clientes enviem e recebam datagramas anônimos, deixando as informações de autenticação e resposta a cargo dos próprios clientes. Esses datagramas são não confiáveis e não ordenados, e podem ter até 32768 bytes.

O tamanho mínimo é 1. Para melhor confiabilidade de entrega, o tamanho máximo recomendado é aproximadamente 11 KB.

Após estabelecer uma sessão SAM com STYLE=RAW, o cliente pode enviar para a ponte SAM:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
O $destination é a base 64 do [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

Quando um datagrama bruto chega, a ponte o entrega ao cliente via:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Funcionalidade do Utilitário SAM

A seguinte mensagem pode ser usada pelo cliente para consultar a ponte SAM para resolução de nomes:

```
NAMING LOOKUP
       NAME=$name
```
que é respondido por

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
O valor RESULT pode ser um dos seguintes:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

Se NAME=ME, então a resposta conterá o destino usado pela sessão atual (útil se você estiver usando um TRANSIENT). Se $result não for OK, MESSAGE pode transmitir uma mensagem descritiva, como "bad format", etc.

O $destination é o base 64 do [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

Chaves base64 públicas e privadas podem ser geradas usando a seguinte mensagem:

```
DEST GENERATE
```
que é respondido por

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
A partir do I2P 0.9.14, um parâmetro opcional SIGNATURE_TYPE é suportado. O valor SIGNATURE_TYPE pode ser qualquer nome (ex: ECDSA_SHA256_P256, insensível a maiúsculas/minúsculas) ou número (ex: 1) que seja suportado pelos [Key Certificates](/docs/specs/common-structures#type_Certificate). O padrão é DSA_SHA1.

O $destination é o base 64 da [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

O $privkey é a base 64 da concatenação do [Destination](/docs/specs/common-structures#type_Destination) seguido pela [Private Key](/docs/specs/common-structures#type_PrivateKey) seguida pela [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), que tem 884 ou mais caracteres em base 64 (663 ou mais bytes em binário), dependendo do tipo de assinatura.

## Valores RESULT

Estes são os valores que podem ser transportados pelo campo RESULT, com seus significados:

| Valor | Significado |
|-------|-------------|
| `OK` | Operação concluída com sucesso |
| `CANT_REACH_PEER` | O peer existe, mas não pode ser alcançado |
| `DUPLICATED_DEST` | O Destination especificado já está em uso |
| `I2P_ERROR` | Um erro genérico do I2P (ex. desconexão I2CP, etc.) |
| `INVALID_KEY` | A chave especificada não é válida (formato incorreto, etc.) |
| `KEY_NOT_FOUND` | O sistema de nomenclatura não consegue resolver o nome fornecido |
| `PEER_NOT_FOUND` | O peer não pode ser encontrado na rede |
| `TIMEOUT` | Timeout enquanto aguardava por um evento (ex. resposta do peer) |
## Opções de Tunnel, I2CP e Streaming

Estas opções podem ser passadas como pares nome=valor no final de uma linha SAM SESSION CREATE.

Todas as sessões podem incluir [opções I2CP como comprimentos de tunnel](/docs/protocol/i2cp#options). Sessões STREAM podem incluir [opções da biblioteca Streaming](/docs/api/streaming#options). Consulte essas referências para nomes de opções e valores padrão.

## Notas sobre Base 64

A codificação Base 64 deve usar o alfabeto Base 64 padrão do I2P "A-Z, a-z, 0-9, -, ~".

## Implementações de Biblioteca Cliente

Bibliotecas cliente estão disponíveis para C, C++, C#, Perl e Python. Estas estão no diretório apps/sam/ no Pacote de Código-Fonte do I2P.

## Configuração SAM Padrão

A porta SAM padrão é 7656. O SAM não está habilitado por padrão no Router I2P; deve ser iniciado manualmente, ou configurado para iniciar automaticamente, na página de configuração de clientes no console do router, ou no arquivo clients.config.
