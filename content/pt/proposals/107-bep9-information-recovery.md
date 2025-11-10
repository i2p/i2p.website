---
title: "Recuperação de Informação BEP9"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Desativado"
thread: "http://zzz.i2p/topics/860"
---

## Visão Geral

Esta proposta é sobre adicionar recuperação total de informações à implementação do BEP9 no I2P.

## Motivação

O BEP9 não envia o arquivo torrent inteiro, perdendo assim vários itens importantes do dicionário, e altera o total do SHA1 dos arquivos torrent. Isso é ruim para links maggot e ruim porque informações importantes são perdidas. Listas de rastreadores, comentários e qualquer dado adicional desaparecem. Um meio de recuperar essas informações é importante, e precisa acrescentar o mínimo possível ao arquivo torrent. Também não deve depender de forma circular. A informação de recuperação não deve afetar os clientes atuais de nenhuma maneira. Torrents que não possuem rastreador (a URL do rastreador é literalmente 'sem rastreador') não contêm o campo extra, pois são específicos para usar o protocolo maggot de descoberta e download, que não perde a informação em primeiro lugar.

## Solução

Tudo o que precisa ser feito é comprimir a informação que seria perdida e armazená-la no dicionário de informações.

### Implementação
1. Gerar o dicionário de informações normal.
2. Gerar o dicionário principal, deixando de fora a entrada de informações.
3. Codificar com Bencode e comprimir o dicionário principal com gzip.
4. Adicionar o dicionário principal comprimido ao dicionário de informações.
5. Adicionar informações ao dicionário principal.
6. Escrever o arquivo torrent.

### Recuperação
1. Descomprimir a entrada de recuperação no dicionário de informações.
2. Decodificar a entrada de recuperação com Bencode.
3. Adicionar informações ao dicionário recuperado.
4. Para clientes com reconhecimento maggot, agora você pode verificar se o SHA1 está correto.
5. Escrever o arquivo torrent recuperado.

## Discussão

Usando o método delineado acima, o aumento no tamanho do torrent é muito pequeno, de 200 a 500 bytes é típico. Robert será distribuído com a nova criação de entrada do dicionário de informações, e isso não poderá ser desligado. Aqui está a estrutura:

```
dicionário principal {
    Strings de rastreadores, comentários, etc...
    info : {
        dicionário principal bencode comprimido com gzip menos o dicionário de informações e todas as outras
        informações usuais
    }
}
```
