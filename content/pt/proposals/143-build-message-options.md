---
title: "Opções de Mensagem de Construção de Túnel"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Rejeitado"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Nota
Esta proposta não foi implementada conforme especificado,
no entanto, as mensagens de construção longas e curtas ECIES (propostas 152 e 157)
foram projetadas com campos de opções extensíveis.
Veja a [especificação Tunnel Creation ECIES](/docs/specs/implementation/#tunnel-creation-ecies) para a especificação oficial.


## Visão Geral

Adicione um mecanismo flexível e extensível para opções nos Registros de Construção de Túnel I2NP
que estão contidas nas mensagens de Construção de Túnel e Resposta de Construção de Túnel.


## Motivação

Há algumas propostas tentativas e não documentadas surgindo para definir opções ou configuração na Mensagem de Construção de Túnel,
para que o criador do túnel possa passar alguns parâmetros para cada salto do túnel.

Há 29 bytes sobrando no TBM. Queremos manter flexibilidade para melhorias futuras, mas também usar o espaço com sabedoria.
Usar a construção 'mapping' utilizaria pelo menos 6 bytes por opção ("1a=1b;").
Definir mais campos de opção de forma rígida poderia causar problemas mais tarde.

Este documento propõe um novo esquema de mapeamento de opções flexível.


## Design

Precisamos de uma representação de opção que seja compacta e ainda assim flexível, para que possamos encaixar múltiplas
opções, de comprimento variado, em 29 bytes.
Essas opções ainda não estão definidas e não são necessárias neste momento.
Não use a estrutura "mapping" (que codifica um objeto de Propriedades Java), ela é muito desperdiçadora.
Use um número para indicar cada opção e comprimento, o que resulta em uma codificação compacta e ainda flexível.
As opções devem ser registradas por número nas nossas especificações, mas também reservaremos um intervalo para opções experimentais.


## Especificação

Preliminar - várias alternativas são descritas abaixo.

Isso estaria presente apenas se o bit 5 nos flags (byte 184) estiver definido como 1.

Cada opção é um número de opção de dois bytes e comprimento, seguido por bytes de comprimento do valor da opção.

As opções começam no byte 193 e continuam através de no máximo o último byte 221.

Número/comprimento da opção:

Dois bytes. Bits 15-4 são o número da opção de 12 bits, 1 - 4095.
Bits 3-0 são o número de bytes de valor da opção a seguir, 0 - 15.
Uma opção booleana poderia ter zero bytes de valor.
Manteremos um registro dos números de opção nas nossas especificações e também definiremos um intervalo para opções experimentais.

O valor da opção é de 0 a 15 bytes, a ser interpretado por quem precisa dessa opção. Os números de opção desconhecidos devem ser ignorados.

As opções são concluídas com um número de opção/comprimento de 0/0, ou seja, dois bytes 0.
 O restante dos 29 bytes, se houver, deve ser preenchido com preenchimento aleatório, como de costume.

Essa codificação nos dá espaço para 14 opções de 0 bytes, ou 9 opções de 1 byte, ou 7 opções de 2 bytes.
Uma alternativa seria usar apenas um byte para o número de opção/comprimento,
talvez com 5 bits para o número da opção (32 máx e 3 bits para comprimento (7 máx).
Isso aumentaria a capacidade para 28 opções de 0 bytes, 14 opções de 1 byte ou 9 opções de dois bytes.
Também poderíamos torná-lo variável, onde um número de opção de 5 bits de 31 significa ler mais 8 bits para o número da opção.

Se o salto do túnel precisar retornar opções para o criador, podemos usar o mesmo formato na mensagem de resposta de construção do túnel,
prefixado por algum número mágico de vários bytes (já que não temos um byte de flag definido para indicar que opções estão presentes).
Há 495 bytes sobrando no TBRM.


## Notas

Estas mudanças são para os Registros de Construção de Túnel, e assim podem ser usadas em todos os sabores de Mensagem de Construção -
Pedido de Construção de Túnel, Pedido de Construção de Túnel Variável, Resposta de Construção de Túnel e Resposta de Construção de Túnel Variável.


## Migração

O espaço não utilizado nos Registros de Construção de Túnel é preenchido com dados aleatórios e atualmente ignorado.
O espaço pode ser convertido para conter opções sem problemas de migração.
Na mensagem de construção, a presença de opções é indicada no byte de flags.
Na mensagem de resposta de construção, a presença de opções é indicada por um número mágico de vários bytes.
