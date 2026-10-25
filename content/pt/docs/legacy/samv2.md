---
title: "Especificação SAM V2"
description: "Protocolo Legacy Simple Anonymous Messaging versão 2 (descontinuado)"
slug: "samv2"
aliases:
  - "/pt/docs/api/samv2"
  - "/pt/docs/api/samv2/"
  - "/pt/samv2"
  - "/pt/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Aviso - Obsoleto - Sem Suporte - Use [SAMv3](/docs/api/samv3)

Especificado abaixo está a versão 2 de um protocolo cliente simples para interagir com I2P.

SAM V2 foi introduzido na versão 0.6.1.31 do I2P. Diferenças significativas do SAM V1 estão marcadas com "\*\*\*". Alternativas: [SAM V1](/docs/api/sam), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Alterações da Versão 2

SAM V2 foi introduzido no lançamento 0.6.1.31 do I2P. Comparado à versão 1, o SAM v2 fornece uma maneira de gerenciar vários sockets no mesmo destino I2P *em paralelo*, ou seja, o cliente não precisa esperar que os dados sejam enviados com sucesso em um socket antes de enviar dados em outro socket. Todos os dados transitam através do mesmo socket cliente\<--\>SAM. Para múltiplos sockets, veja [SAM V3](/docs/api/samv3).

### Alterações do I2P 0.9.14

A versão reportada permanece "2.0".

- DEST GENERATE agora suporta um parâmetro SIGNATURE_TYPE.
- O parâmetro MIN em HELLO VERSION agora é opcional.
- Os parâmetros MIN e MAX em HELLO VERSION agora suportam versões de um dígito como "3".

## Protocolo Versão 2

A aplicação cliente comunica com a ponte SAM, que lida com toda a funcionalidade I2P (usando a biblioteca de streaming para fluxos virtuais, ou I2CP diretamente para mensagens assíncronas).

Toda a comunicação client\<--\>SAM bridge é não criptografada e não autenticada através de um único socket TCP. O acesso ao SAM bridge deve ser protegido através de firewalls ou outros meios (talvez o bridge possa ter ACLs sobre quais IPs aceita conexões).

Todas essas mensagens SAM são enviadas em uma única linha em ASCII simples, terminadas pelo caractere de nova linha (\\n). A formatação mostrada abaixo é apenas para legibilidade, e embora as duas primeiras palavras em cada mensagem devam permanecer em sua ordem específica, a ordem dos pares chave=valor pode mudar (por exemplo, "ONE TWO A=B C=D" ou "ONE TWO C=D A=B" são ambas construções perfeitamente válidas). Além disso, o protocolo é sensível a maiúsculas e minúsculas.

Mensagens SAM são interpretadas em UTF-8. Pares chave=valor devem ser separados por um único espaço. Valores podem ser colocados entre aspas duplas se contiverem espaços, por exemplo, chave="texto de valor longo". Não há mecanismo de escape.

A comunicação pode assumir três formas distintas:

- [Fluxos virtuais](/docs/api/streaming)
- [Datagramas com resposta](/docs/specs/datagrams#repliable) (mensagens com um campo FROM)
- [Datagramas anônimos](/docs/specs/datagrams#raw) (mensagens anônimas brutas)

## Handshake de Conexão SAM

Nenhuma comunicação SAM pode ocorrer até que o cliente e a ponte tenham concordado com uma versão de protocolo, o que é feito pelo cliente enviando um HELLO e a ponte enviando um HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
e

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
A partir do I2P 0.9.14, o parâmetro MIN é opcional. O parâmetro MAX deve ser fornecido e ser maior ou igual a "2" e menor que "3" para usar a versão 2.

O valor RESULT pode ser um dos seguintes:

- `OK`
- `NOVERSION`

## Sessões SAM

Uma sessão SAM é criada quando um cliente abre um socket para a ponte SAM, opera um handshake e envia uma mensagem SESSION CREATE, e a sessão termina quando o socket é desconectado.

Cada Destination I2P pode ser usado apenas para uma sessão SAM por vez, e pode usar apenas uma dessas formas (mensagens recebidas através de outras formas são descartadas).

A mensagem SESSION CREATE enviada pelo cliente para a ponte é a seguinte:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION especifica qual destino deve ser usado para enviar e receber mensagens/streams. Se um $name for fornecido, a ponte SAM procura em seu próprio armazenamento local (o arquivo sam.keys) por um destino associado (e chave privada). Se não existir nenhuma associação correspondente a esse nome, ela cria uma nova. Se o destino for especificado como TRANSIENT, ela sempre cria um novo.

Note que DESTINATION é um identificador, *não* dados codificados em Base 64. Para especificar o Destination, você deve usar [SAM V3](/docs/api/samv3).

A DIRECTION pode ser especificada apenas para sessões STREAM, instruindo a ponte que o cliente estará criando ou recebendo streams, ou ambos. Se isso não for especificado, BOTH será assumido. Tentar criar um stream de saída quando DIRECTION=RECEIVE deve resultar em erro, e streams de entrada quando DIRECTION=CREATE serão ignorados.

Opções adicionais fornecidas devem ser passadas para a configuração da sessão I2P se não forem interpretadas pela ponte SAM (ex. "tunnels.depthInbound=0"). Essas opções estão documentadas abaixo.

A própria ponte SAM já deve estar configurada com qual router deve se comunicar através do I2P (embora, se necessário, possa haver uma forma de fornecer uma substituição, por exemplo, i2cp.tcp.host=localhost e i2cp.tcp.port=7654).

Após receber a mensagem de criação de sessão, a ponte SAM responderá com uma mensagem de status da sessão, da seguinte forma:

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

Se não estiver OK, a MESSAGE deve conter informações legíveis para humanos sobre por que a sessão não pôde ser criada.

Note que não há aviso dado se o $name não for encontrado e um destino transitório for criado em seu lugar. Note que o destino base 64 transitório real não é exibido na resposta; é o $name ou TRANSIENT conforme fornecido em SESSION CREATE. Se você precisar dessas funcionalidades, deve usar [SAM V3](/docs/api/samv3).

## Streams Virtuais SAM

Os streams virtuais são garantidos de serem enviados de forma confiável e em ordem, com notificação de falha e sucesso assim que estiver disponível.

Após estabelecer a sessão com STYLE=STREAM, tanto o cliente quanto a bridge SAM podem enviar de forma assíncrona várias mensagens de ida e volta para gerenciar os streams, conforme listado abaixo:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Isso estabelece uma nova conexão virtual do destino local para o peer especificado, marcando-a com o ID único com escopo de sessão. O ID único é um inteiro ASCII base 10 de 1 até (2^31-1).

O $destination é o base 64 do [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres em base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A ponte SAM responde a isso com uma mensagem de status do stream:

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

Se o RESULT for OK, o destino especificado está ativo e autorizou a conexão; se a conexão não foi possível (timeout, etc), RESULT conterá o valor de erro apropriado (acompanhado por uma MESSAGE legível opcional).

Na extremidade receptora, a ponte SAM simplesmente notifica o cliente da seguinte forma:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Isso informa ao cliente que o destino especificado criou uma conexão virtual com ele. O fluxo de dados seguinte será marcado com o ID único fornecido, que é um número inteiro ASCII base 10 de -1 até -(2^31-1).

O $destination é a base 64 do [Destination](/docs/specs/common-structures#type_Destination), que possui 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

Quando o cliente quer enviar dados na conexão virtual, eles fazem isso da seguinte forma:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Isto solicita à ponte SAM que adicione os dados especificados ao buffer sendo enviado ao peer através da conexão virtual. O tamanho de envio $numBytes é quantos bytes de 8 bits estão incluídos após a nova linha, que pode ser de 1 a 32768 (32KB).

**\*\*\* A bridge SAM responde imediatamente com:**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** onde $bufferState pode ser:

- `BUFFER_FULL` - O buffer do SAM possui 32 KB ou mais de dados para enviar, e solicitações SEND subsequentes falharão
- `READY` - O buffer do SAM não está cheio, e a próxima solicitação SEND tem garantia de sucesso

**\*\*\*** e $result é um dos seguintes:

- `OK` - os dados foram armazenados em buffer com sucesso
- `FAILED` - o buffer estava cheio, nenhum dado foi armazenado em buffer

**\*\*\*** Se a bridge SAM respondeu com BUFFER_FULL, ela enviará outra mensagem assim que seu buffer estiver disponível novamente:

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** Quando o resultado é OK, a ponte SAM fará o seu melhor para entregar a mensagem o mais rápida e eficientemente possível, talvez agrupando várias mensagens SEND juntas. Se houver um erro na entrega dos dados, ou se o lado remoto fechar a conexão, a ponte SAM informará o cliente:

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

Se a conexão foi fechada adequadamente pelo outro peer, $result é definido como OK. Se $result não for OK, MESSAGE pode transmitir uma mensagem descritiva, como "peer unreachable", etc. Sempre que um cliente quiser fechar a conexão, ele envia a mensagem de fechamento para a bridge SAM:

```
STREAM CLOSE
       ID=$id
```
O bridge então limpa o que precisa e descarta esse ID - nenhuma mensagem adicional pode ser enviada ou recebida nele.

Para o outro lado da comunicação, sempre que o peer tiver enviado alguns dados e eles estiverem disponíveis para o cliente, a ponte SAM irá entregá-los prontamente:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** Com a versão 2.0 do SAM, porém, o cliente primeiro tem que informar à ponte SAM quanta dados de entrada é permitida para toda a sessão, enviando uma mensagem:

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** onde $limit pode ser:

- `NONE` - a ponte SAM continuará escutando e entregando dados recebidos (mesmo comportamento da versão 1.0)
- um número inteiro (menor que 2^64) - o número de bytes recebidos após o qual a ponte SAM parará de escutar no fluxo de entrada. Sempre que o cliente estiver pronto para aceitar mais bytes do fluxo, ele deve enviar essa mensagem novamente, com um $limit maior.

**\*\*\*** O cliente tem que enviar tais mensagens STREAM RECEIVE após a conexão com o peer ter sido estabelecida, ou seja, depois que o cliente recebeu um "STREAM CONNECTED" ou um "STREAM STATUS RESULT=OK" da ponte SAM.

Todos os streams são implicitamente fechados quando a conexão entre a ponte SAM e o cliente é interrompida.

## Datagramas Replicáveis SAM

Embora o I2P não contenha inerentemente um endereço FROM, para facilitar o uso é fornecida uma camada adicional como datagramas com resposta - mensagens não ordenadas e não confiáveis de até 31744 bytes que incluem um endereço FROM (deixando até 1KB para material de cabeçalho). Este endereço FROM é autenticado internamente pelo SAMv3 (fazendo uso da chave de assinatura do destino para verificar a origem) e inclui prevenção de replay.

O tamanho mínimo é 1. Para melhor confiabilidade de entrega, o tamanho máximo recomendado é aproximadamente 11 KB.

Após estabelecer uma sessão SAM com STYLE=DATAGRAM, o cliente pode enviar para a ponte SAM:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Quando um datagrama chega, a ponte o entrega ao cliente através de:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
O $destination é a base 64 do [Destination](/docs/specs/common-structures#type_Destination), que possui 516 ou mais caracteres em base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A ponte SAM nunca expõe ao cliente os cabeçalhos de autenticação ou outros campos, apenas os dados que o remetente forneceu. Isso continua até que a sessão seja fechada (pelo cliente encerrando a conexão).

## SAM Datagramas Anônimos

Aproveitando ao máximo a largura de banda do I2P, o SAM permite que clientes enviem e recebam datagramas anônimos, deixando a autenticação e informações de resposta por conta dos próprios clientes. Esses datagramas são não confiáveis e não ordenados, e podem ter até 32768 bytes.

O tamanho mínimo é 1. Para melhor confiabilidade de entrega, o tamanho máximo recomendado é de aproximadamente 11 KB.

Após estabelecer uma sessão SAM com STYLE=RAW, o cliente pode enviar para a ponte SAM:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
O $destination é o base 64 da [Destination](/docs/specs/common-structures#type_Destination), que tem 516 ou mais caracteres em base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

Quando um datagrama bruto chega, a ponte o entrega ao cliente através de:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Funcionalidade do Utilitário SAM

A seguinte mensagem pode ser usada pelo cliente para consultar a bridge SAM para resolução de nomes:

```
NAMING LOOKUP
       NAME=$name
```
que é respondida por

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

O $destination é a base 64 do [Destination](/docs/specs/common-structures#type_Destination), que são 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

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
A partir do I2P 0.9.14, um parâmetro opcional SIGNATURE_TYPE é suportado. O valor de SIGNATURE_TYPE pode ser qualquer nome (por exemplo, ECDSA_SHA256_P256, não diferencia maiúsculas de minúsculas) ou número (por exemplo, 1) que seja suportado pelos [Key Certificates](/docs/specs/common-structures#type_Certificate). O padrão é DSA_SHA1.

O $destination é a base 64 do [Destination](/docs/specs/common-structures#type_Destination), que são 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

O $privkey é a base 64 da concatenação do [Destination](/docs/specs/common-structures#type_Destination) seguido pela [Private Key](/docs/specs/common-structures#type_PrivateKey) seguida pela [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), que são 884 ou mais caracteres em base 64 (663 ou mais bytes em binário), dependendo do tipo de assinatura.

## Valores RESULT

Estes são os valores que podem ser transportados pelo campo RESULT, com seus significados:

| Valor | Significado |
|-------|-------------|
| `OK` | Operação concluída com sucesso |
| `CANT_REACH_PEER` | O peer existe, mas não pode ser alcançado |
| `DUPLICATED_DEST` | O Destination especificado já está em uso |
| `I2P_ERROR` | Um erro genérico do I2P (por exemplo, desconexão I2CP, etc.) |
| `INVALID_KEY` | A chave especificada não é válida (formato incorreto, etc.) |
| `KEY_NOT_FOUND` | O sistema de nomes não consegue resolver o nome fornecido |
| `PEER_NOT_FOUND` | O peer não pode ser encontrado na rede |
| `TIMEOUT` | Tempo limite esgotado enquanto aguardava um evento (por exemplo, resposta do peer) |
## Opções de Tunnel, I2CP e Streaming

Essas opções podem ser passadas como pares nome=valor no final de uma linha SAM SESSION CREATE.

Todas as sessões podem incluir [opções I2CP como comprimentos de tunnel](/docs/protocol/i2cp#options). Sessões STREAM podem incluir [opções da biblioteca Streaming](/docs/api/streaming#options). Consulte essas referências para nomes de opções e padrões.

## Notas sobre Base 64

A codificação Base 64 deve usar o alfabeto Base 64 padrão do I2P "A-Z, a-z, 0-9, -, ~".

## Implementações de Bibliotecas Cliente

Bibliotecas de cliente estão disponíveis para C, C++, C#, Perl e Python. Estas estão no diretório apps/sam/ no Pacote de Código-fonte do I2P. Algumas podem ser mais antigas e não foram atualizadas para suporte ao SAMv2.

## Configuração SAM Padrão

A porta SAM padrão é 7656. O SAM não está habilitado por padrão no I2P Router; deve ser iniciado manualmente, ou configurado para iniciar automaticamente, na página de configuração de clientes no console do router, ou no arquivo clients.config.
