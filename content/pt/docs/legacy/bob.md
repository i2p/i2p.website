---
title: "BOB - Basic Open Bridge"
description: "API descontinuada para gerenciamento de destinos"
slug: "bob"
aliases:
  - "/pt/docs/api/bob"
  - "/pt/docs/api/bob/"
  - "/pt/bob"
  - "/pt/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Aviso - Descontinuado

Não deve ser usado por novas aplicações. BOB, conforme especificado aqui, suporta apenas o tipo de assinatura DSA-SHA1. BOB não será estendido para suportar novos tipos de assinatura ou outros recursos avançados. Novas aplicações devem usar [SAM V3](/docs/api/samv3).

O suporte ao BOB foi removido das novas instalações do Java I2P a partir da versão 1.7.0 (2022-02). Ainda funcionará no Java I2P originalmente instalado como versão 1.6.1 ou anterior, mesmo após atualizações, mas não é suportado e pode quebrar a qualquer momento. O BOB ainda é suportado pelo i2pd em 2025-05, mas as aplicações ainda devem migrar para SAMv3 pelas razões mencionadas acima. Consulte [a documentação do i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) para quaisquer extensões à API documentada aqui que sejam suportadas pelo i2pd.

Neste ponto, a maioria das boas ideias do BOB foram incorporadas ao SAMv3, que tem mais recursos e mais uso no mundo real. O BOB ainda pode funcionar em algumas instalações (veja acima), mas não está ganhando os recursos avançados disponíveis para o SAMv3 e é essencialmente não suportado, exceto pelo i2pd.

## Bibliotecas de Linguagem para a API BOB

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Visão Geral

`KEYS` = par de chaves pública+privada, estas são BASE64

`KEY` = chave pública, também BASE64

`ERROR` como implícito retorna a mensagem `"ERROR "+DESCRIPTION+"\n"`, onde `DESCRIPTION` é o que deu errado.

`OK` retorna `"OK"`, e se dados devem ser retornados, eles estão na mesma linha. `OK` significa que o comando foi concluído.

Linhas `DATA` contêm informações que você solicitou. Pode haver múltiplas linhas `DATA` por solicitação.

**NOTA:** O comando help é o ÚNICO comando que tem uma exceção às regras... ele pode realmente não retornar nada! Isto é intencional, já que help é um comando HUMANO e não de APLICAÇÃO.

## Conexão e Versão

Toda a saída de status do BOB é por linhas. As linhas podem terminar com \\n ou \\r\\n, dependendo do sistema. Na conexão, o BOB produz duas linhas:

```
BOB version
OK
```
A versão atual é: 00.00.10

Note que versões anteriores usavam dígitos hexadecimais em maiúscula e não estavam em conformidade com os padrões de versionamento do I2P. É recomendado que versões subsequentes usem apenas dígitos 0-9.

### Histórico de Versões

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Comandos

**IMPORTANTE:** Para detalhes ATUAIS sobre os comandos, POR FAVOR use o comando de ajuda integrado. Apenas faça telnet para localhost 2827 e digite help para obter documentação completa sobre cada comando.

Os comandos nunca ficam obsoletos ou são alterados, porém novos comandos são adicionados de tempos em tempos.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Uma vez configurado, todos os sockets TCP podem e irão bloquear conforme necessário, e não há necessidade de mensagens adicionais de/para o canal de comando. Isso permite que o router controle o ritmo do fluxo sem explodir com OOM como o SAM faz quando se engasga ao tentar empurrar muitos fluxos para dentro ou para fora de um socket -- isso não pode escalar quando você tem muitas conexões!

O que também é interessante sobre esta interface específica é que escrever qualquer coisa para fazer interface com ela é muito, muito mais fácil do que SAM. Não há nenhum outro processamento a fazer após a configuração. Sua configuração é tão simples que ferramentas muito simples, como nc (netcat), podem ser usadas para apontar para alguma aplicação. O valor disso é que se pode programar horários de atividade e inatividade para uma aplicação, sem ter que alterar a aplicação para fazer isso, ou até mesmo ter que parar essa aplicação. Em vez disso, você pode literalmente "desconectar" o destino e "conectá-lo" novamente. Contanto que os mesmos endereços IP/porta e chaves de destino sejam usados ao ativar a ponte, a aplicação TCP normal não se importará e não notará. Ela será simplesmente enganada -- os destinos não estão alcançáveis e nada está chegando.

## Exemplos

Para o exemplo seguinte, vamos configurar uma conexão de loopback local muito simples, com dois destinos. O destino "mouth" será o serviço CHARGEN do daemon de superservidor INET. O destino "ear" será uma porta local na qual você pode fazer telnet e assistir ao belo vômito de teste ASCII sendo exibido.

### Exemplo de Diálogo de Sessão

Simples telnet 127.0.0.1 2827 funciona.

- A = Aplicação
- C = Resposta de comando do BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**ANOTE A CHAVE DE DESTINO ACIMA, A SUA SERÁ DIFERENTE!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
Neste ponto, não houve erro, um destino com o apelido "mouth" foi configurado. Quando você contata o destino fornecido, na verdade se conecta ao serviço `CHARGEN` na porta `19/TCP`.

Agora para a outra metade, para que possamos realmente contactar este destino.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Agora tudo o que precisamos fazer é conectar via telnet em 127.0.0.1, porta 37337, enviar a chave de destino ou endereço do host do catálogo de endereços que queremos contactar. Neste caso, queremos contactar "mouth", tudo o que fazemos é colar a chave e ela funciona.

**NOTA:** O comando "quit" no canal de comando NÃO desconecta os tunnels como o SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Depois de algumas milhas virtuais desta saída de dados, pressione `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Aqui está o que aconteceu...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
Você também pode se conectar a sites I2P!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Muito legal, não é? Experimente alguns outros I2P SITES conhecidos se quiser, inexistentes, etc., para ter uma ideia do tipo de saída a esperar em diferentes situações. Na maior parte, sugere-se que ignore qualquer uma das mensagens de erro. Elas seriam sem sentido para a aplicação, e são apresentadas apenas para depuração humana.

### Limpeza

Vamos encerrar nossos destinos agora que terminamos com eles.

Primeiro, vamos ver que apelidos de destino temos.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Muito bem, aí estão eles. Primeiro, vamos remover "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Agora para remover "ear", note que isso é o que acontece quando você digita muito rápido, e mostra como são as mensagens de ERRO típicas.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Modo Silencioso

Não vou me preocupar em mostrar um exemplo da extremidade receptora de uma ponte porque é muito simples. Existem duas configurações possíveis para ela, e é alternada com o comando "quiet".

O padrão NÃO é silencioso, e os primeiros dados que chegam ao seu socket de escuta são o destino que está fazendo o contato. É uma única linha consistindo do endereço BASE64 seguido de uma nova linha. Tudo depois disso é para a aplicação realmente consumir.

No modo silencioso, pense nisso como uma conexão normal à Internet. Nenhum dado extra entra de forma alguma. É como se você estivesse simplesmente conectado à Internet normal. Este modo permite uma forma de transparência muito parecida com a disponível nas páginas de configurações de tunnel do console do router, para que você possa usar o BOB para apontar um destino para um servidor web, por exemplo, e não precisaria modificar o servidor web de forma alguma.

## Vantagens do BOB

A vantagem de usar BOB para isso é como discutido anteriormente. Você poderia agendar tempos de atividade aleatórios para a aplicação, redirecionar para uma máquina diferente, etc. Um uso disso pode ser algo como querer tentar confundir a adivinhação de disponibilidade router-para-destino. Você poderia parar e iniciar o destino com um processo totalmente diferente para criar tempos aleatórios de atividade e inatividade nos serviços. Dessa forma, você estaria apenas interrompendo a capacidade de contactar tal serviço, e não teria que se preocupar em desligá-lo e reiniciá-lo. Você poderia redirecionar e apontar para uma máquina diferente na sua LAN enquanto faz atualizações, ou apontar para um conjunto de máquinas de backup dependendo do que está executando, etc, etc. Apenas sua imaginação limita o que você poderia fazer com BOB.
