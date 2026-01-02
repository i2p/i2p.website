---
title: "Tipos de Mime I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Aberto"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Visão Geral

Defina tipos de mime para formatos de arquivos comuns do I2P.
Inclua as definições em pacotes Debian.
Forneça um manipulador para o tipo .su3, e possivelmente outros.


## Motivação

Para tornar o reabastecimento e a instalação de plugins mais fáceis ao baixar com um navegador,
precisamos de um tipo de mime e um manipulador para arquivos .su3.

Enquanto isso, após aprender a escrever o arquivo de definição de mime,
seguindo o padrão freedesktop.org, podemos adicionar definições para outros tipos de arquivo comuns
do I2P. Embora menos úteis para arquivos que normalmente não são baixados, como o
banco de dados do arquivo de bloco do catálogo de endereços (hostsdb.blockfile), essas definições permitirão
que os arquivos sejam melhor identificados e iconificados ao usar um visualizador de diretório gráfico
como o "nautilus" no Ubuntu.

Ao padronizar os tipos de mime, cada implementação de roteador pode escrever manipuladores
conforme apropriado, e o arquivo de definição de mime pode ser compartilhado por todas as implementações.


## Design

Escreva um arquivo fonte XML seguindo o padrão freedesktop.org e inclua-o
em pacotes Debian. O arquivo é "debian/(pacote).sharedmimeinfo".

Todos os tipos de mime I2P começarão com "application/x-i2p-", exceto para o jrobin rrd.

Os manipuladores para esses tipos de mime são específicos de cada aplicativo e não serão
especificados aqui.

Também incluiremos as definições com o Jetty e as incluiremos com
o software de reabastecimento ou instruções.


## Especificação

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(genérico)	application/x-i2p-su3

.su3	(atualização de roteador)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reabastecimento)	application/x-i2p-su3-reseed

.su3	(noticias)		application/x-i2p-su3-news

.su3	(lista de bloqueio)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Notas

Nem todos os formatos de arquivo listados acima são usados por implementações de roteadores não-Java;
alguns podem não estar nem bem especificados. No entanto, documentá-los aqui
pode permitir a consistência entre implementações no futuro.

Alguns sufixos de arquivo, como ".config", ".dat" e ".info", podem se sobrepor com outros
tipos de mime. Estes podem ser desambiguados com dados adicionais, tais como
nome completo do arquivo, um padrão de nome de arquivo ou números mágicos.
Veja o rascunho do arquivo i2p.sharedmimeinfo no tópico zzz.i2p para exemplos.

Os importantes são os tipos .su3, e esses tipos têm tanto
um sufixo único quanto definições de número mágico robustas.


## Migração

Não aplicável.
