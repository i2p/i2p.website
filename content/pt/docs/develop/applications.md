---
title: "Desenvolvimento de Aplicações"
description: "Por que escrever aplicações específicas para I2P, conceitos-chave, opções de desenvolvimento e um guia simples de introdução"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Por que escrever código específico para I2P?

Existem várias maneiras de usar aplicações no I2P. Usando o [I2PTunnel](/docs/api/i2ptunnel/), você pode usar aplicações regulares sem precisar programar suporte explícito ao I2P. Isso é muito eficaz para cenários cliente-servidor, onde você precisa se conectar a um único site. Você pode simplesmente criar um tunnel usando o I2PTunnel para se conectar a esse site, como mostrado na Figura 1.

Se sua aplicação for distribuída, ela exigirá conexões com uma grande quantidade de peers. Usando I2PTunnel, você precisará criar um novo tunnel para cada peer que deseja contatar, conforme mostrado na Figura 2. Este processo pode, é claro, ser automatizado, mas executar muitas instâncias de I2PTunnel cria uma grande quantidade de sobrecarga. Além disso, com muitos protocolos você precisará forçar todos a usarem o mesmo conjunto de portas para todos os peers — por exemplo, se você quiser executar chat DCC de forma confiável, todos precisam concordar que a porta 10001 é Alice, a porta 10002 é Bob, a porta 10003 é Charlie, e assim por diante, já que o protocolo inclui informações específicas de TCP/IP (host e porta).

Aplicações de rede gerais frequentemente enviam muitos dados adicionais que podem ser usados para identificar usuários. Nomes de host, números de porta, fusos horários, conjuntos de caracteres, etc. são frequentemente enviados sem informar o usuário. Por isso, projetar o protocolo de rede especificamente com anonimato em mente pode evitar comprometer as identidades dos usuários.

Existem também considerações de eficiência a serem revisadas ao determinar como interagir sobre o I2P. A biblioteca de streaming e as coisas construídas sobre ela operam com handshakes semelhantes ao TCP, enquanto os protocolos principais do I2P (I2NP e I2CP) são estritamente baseados em mensagens (como UDP ou, em alguns casos, IP bruto). A distinção importante é que com o I2P, a comunicação está operando sobre uma rede longa e ampla — cada mensagem ponto a ponto terá latências não triviais, mas pode conter cargas úteis de até vários KB. Uma aplicação que precisa de uma simples requisição e resposta pode eliminar qualquer estado e reduzir a latência incorrida pelos handshakes de inicialização e encerramento usando datagramas (melhor esforço) sem ter que se preocupar com detecção de MTU ou fragmentação de mensagens.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
Em resumo, várias razões para escrever código específico para I2P:

- Criar uma grande quantidade de instâncias I2PTunnel consome uma quantidade não trivial de recursos, o que é problemático para aplicações distribuídas (um novo tunnel é necessário para cada peer).
- Protocolos de rede gerais frequentemente enviam muitos dados adicionais que podem ser usados para identificar usuários. Programar especificamente para I2P permite a criação de um protocolo de rede que não vaza tais informações, mantendo os usuários anônimos e seguros.
- Protocolos de rede projetados para uso na internet comum podem ser ineficientes no I2P, que é uma rede com latência muito maior.

I2P suporta uma [interface de plugins](/docs/plugins/) padrão para desenvolvedores, de modo que aplicações possam ser facilmente integradas e distribuídas.

Aplicações escritas em Java e acessíveis/executáveis usando uma interface HTML através do webapps/app.war padrão podem ser consideradas para inclusão na distribuição I2P.

## Conceitos Importantes

Existem algumas mudanças que exigem adaptação ao usar o I2P:

### Destinos

Uma aplicação executada no I2P envia mensagens de e recebe mensagens para um ponto final único e criptograficamente seguro — um "destination" (destino). Em termos de TCP ou UDP, um destination pode (em grande parte) ser considerado o equivalente de um par de nome de host mais número de porta, embora existam algumas diferenças.

- Um destino I2P em si é uma construção criptográfica — todos os dados enviados para um são criptografados como se houvesse implementação universal de IPsec, com a localização (anonimizada) do ponto final assinada como se houvesse implementação universal de DNSSEC.
- Destinos I2P são identificadores móveis — eles podem ser movidos de um router I2P para outro (ou podem até fazer "multihome" — operar em múltiplos routers ao mesmo tempo). Isso é bastante diferente do mundo TCP ou UDP, onde um único ponto final (porta) deve permanecer em um único host.
- Destinos I2P são grandes e complexos — nos bastidores, eles contêm uma chave pública ElGamal de 2048 bits para criptografia, uma chave pública DSA de 1024 bits para assinatura e um certificado de tamanho variável, que pode conter prova de trabalho ou dados ofuscados.

Existem formas de referenciar esses destinos grandes e feios através de nomes curtos e bonitos (por exemplo, "irc.duck.i2p"), mas essas técnicas não garantem exclusividade global (já que são armazenados localmente num banco de dados na máquina de cada pessoa) e o mecanismo atual não é especialmente escalável nem seguro (as atualizações da lista de hosts são geridas usando "subscrições" a serviços de nomes). Pode haver algum sistema de nomes seguro, legível por humanos, escalável e globalmente exclusivo algum dia, mas as aplicações não devem depender dele estar implementado. [Mais informações sobre o sistema de nomes](/docs/overview/naming/) estão disponíveis.

Embora a maioria das aplicações não precise distinguir protocolos e portas, o I2P *suporta* isso. Aplicações complexas podem especificar um protocolo, porta de origem e porta de destino, por mensagem, para multiplexar o tráfego em um único destino. Consulte a [página de datagramas](/docs/api/datagrams/) para mais detalhes. Aplicações simples operam escutando "todos os protocolos" em "todas as portas" de um destino.

### Anonimato e Confidencialidade

I2P possui criptografia e autenticação de ponta a ponta transparentes para todos os dados transmitidos pela rede — se Bob enviar para o destino de Alice, apenas o destino de Alice poderá recebê-los, e se Bob estiver usando a biblioteca de datagramas ou streaming, Alice sabe com certeza que o destino de Bob é aquele que enviou os dados.

Claro, o I2P anonimiza de forma transparente os dados enviados entre Alice e Bob, mas não faz nada para anonimizar o conteúdo do que eles enviam. Por exemplo, se Alice enviar a Bob um formulário com seu nome completo, documentos de identificação governamentais e números de cartão de crédito, não há nada que o I2P possa fazer. Assim sendo, protocolos e aplicativos devem ter em mente quais informações estão tentando proteger e quais informações estão dispostos a expor.

### Datagramas I2P Podem Ter Até Vários KB

Aplicações que usam datagramas I2P (seja brutos ou respondíveis) podem essencialmente ser pensadas em termos de UDP — os datagramas são desordenados, de melhor esforço e sem conexão — mas ao contrário do UDP, as aplicações não precisam se preocupar com detecção de MTU e podem simplesmente enviar datagramas grandes. Embora o limite superior seja nominalmente 32 KB, a mensagem é fragmentada para transporte, reduzindo assim a confiabilidade do todo. Datagramas acima de cerca de 10 KB não são recomendados atualmente. Consulte a [página de datagramas](/docs/api/datagrams/) para detalhes. Para muitas aplicações, 10 KB de dados é suficiente para uma solicitação ou resposta inteira, permitindo que elas operem de forma transparente no I2P como uma aplicação similar a UDP sem ter que escrever fragmentação, reenvios, etc.

## Opções de Desenvolvimento

Existem várias formas de enviar dados através do I2P, cada uma com suas próprias vantagens e desvantagens. A streaming lib é a interface recomendada, utilizada pela maioria das aplicações I2P.

### Biblioteca de Streaming

A [biblioteca completa de streaming](/docs/specs/streaming/) é agora a interface padrão. Ela permite programar usando sockets similares a TCP, como explicado no [guia de desenvolvimento com Streaming](#developing-with-the-streaming-library).

### BOB

BOB é a [Basic Open Bridge](/docs/legacy/bob/), permitindo que uma aplicação em qualquer linguagem faça conexões streaming de e para I2P. Neste momento, não possui suporte a UDP, mas o suporte a UDP está planejado para o futuro próximo. BOB também contém várias ferramentas, como geração de chaves de destino e verificação de que um endereço está em conformidade com as especificações I2P. Informações atualizadas e aplicações que usam BOB podem ser encontradas neste [I2P Site](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM não é recomendado. SAM V2 é aceitável, SAM V3 é recomendado.*

SAM é o protocolo [Simple Anonymous Messaging](/docs/legacy/sam/), permitindo que uma aplicação escrita em qualquer linguagem se comunique com uma ponte SAM através de um socket TCP simples e tenha essa ponte multiplexando todo o seu tráfego I2P, coordenando de forma transparente a criptografia/descriptografia e o tratamento baseado em eventos. SAM suporta três estilos de operação:

- streams, para quando Alice e Bob querem enviar dados um para o outro de forma confiável e ordenada
- repliable datagrams, para quando Alice quer enviar a Bob uma mensagem à qual Bob pode responder
- raw datagrams, para quando Alice quer extrair o máximo de largura de banda e desempenho possível, e Bob não se importa se o remetente dos dados está autenticado ou não (por exemplo, os dados transferidos são auto-autenticados)

O SAM V3 visa o mesmo objetivo que o SAM e SAM V2, mas não requer multiplexação/demultiplexação. Cada stream I2P é gerenciado por seu próprio socket entre a aplicação e a ponte SAM. Além disso, datagramas podem ser enviados e recebidos pela aplicação através de comunicações de datagrama com a ponte SAM.

[SAM V2](/docs/legacy/samv2/) é uma nova versão usada pelo imule que corrige alguns dos problemas no [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) é usado pelo imule desde a versão 1.4.0.

### I2PTunnel

A aplicação I2PTunnel permite que aplicações construam túneis específicos semelhantes a TCP para peers, criando aplicações 'cliente' I2PTunnel (que escutam numa porta específica e conectam-se a um destino I2P específico sempre que um socket para essa porta é aberto) ou aplicações 'servidor' I2PTunnel (que escutam um destino I2P específico e sempre que recebem uma nova conexão I2P fazem outproxy para um host/porta TCP específico). Estes streams são 8-bit clean e são autenticados e protegidos através da mesma biblioteca de streaming que o SAM usa, mas há uma sobrecarga não trivial envolvida na criação de múltiplas instâncias únicas de I2PTunnel, uma vez que cada uma tem o seu próprio destino I2P exclusivo e o seu próprio conjunto de túneis, chaves, etc.

### SOCKS

O I2P suporta proxy SOCKS V4 e V5. Conexões de saída funcionam bem. Funcionalidades de entrada (servidor) e UDP podem estar incompletas e não testadas.

### Ministreaming

*Removido*

Costumava haver uma biblioteca simples "ministreaming", mas agora o ministreaming.jar contém apenas as interfaces para a biblioteca de streaming completa.

### Datagramas

*Recomendado para aplicações tipo UDP*

A [biblioteca Datagram](/docs/api/datagrams/) permite o envio de pacotes semelhantes a UDP. É possível usar:

- Datagramas replicáveis
- Datagramas brutos

### I2CP

*Não recomendado*

[I2CP](/docs/specs/i2cp/) em si é um protocolo independente de linguagem, mas para implementar uma biblioteca I2CP em algo diferente de Java há uma quantidade significativa de código a ser escrito (rotinas de criptografia, marshalling de objetos, tratamento de mensagens assíncronas, etc). Embora alguém possa escrever uma biblioteca I2CP em C ou outra linguagem, provavelmente seria mais útil usar a biblioteca SAM em C.

### Aplicações Web

O I2P vem com o servidor web Jetty, e configurar para usar o servidor Apache é simples. Qualquer tecnologia padrão de aplicação web deve funcionar.

## Comece a Desenvolver — Um Guia Simples

Desenvolver usando I2P requer uma instalação funcional do I2P e um ambiente de desenvolvimento de sua escolha. Se você estiver usando Java, pode começar o desenvolvimento com a [streaming library](#developing-with-the-streaming-library) ou datagram library. Usando outra linguagem de programação, SAM ou BOB podem ser utilizados.

### Desenvolvimento com a Biblioteca Streaming

Abaixo está uma versão simplificada e modernizada do exemplo na página original. Para o exemplo completo, consulte a página legada ou nossos exemplos em Java no código-fonte.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Exemplo de código: servidor básico recebendo dados.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Exemplo de código: cliente conectando e enviando uma linha.*
