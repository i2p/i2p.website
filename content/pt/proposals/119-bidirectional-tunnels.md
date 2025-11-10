--- 
title: "Túneis Bidirecionais" 
number: "119" 
author: "orignal" 
created: "2016-01-07" 
lastupdated: "2016-01-07" 
status: "Needs-Research" 
thread: "http://zzz.i2p/topics/2041" 
---

## Visão Geral

Esta proposta trata da implementação de túneis bidirecionais no I2P.

## Motivação

O i2pd vai introduzir a construção de túneis bidirecionais através de outros roteadores i2pd, por enquanto. Para a rede, eles aparecerão como túneis regulares de entrada e saída.

## Desenho

### Objetivos

1. Reduzir o uso de rede e CPU reduzindo o número de mensagens TunnelBuild
2. Capacidade de saber instantaneamente se um participante deixou de estar ativo.
3. Perfis e estatísticas mais precisas
4. Utilizar outras darknets como pares intermediários

### Modificações no Túnel

TunnelBuild
```````````
Os túneis são construídos da mesma forma que os túneis de entrada. Não é necessária mensagem de resposta. Há um tipo especial de participante chamado "entrada", marcado por uma bandeira, que serve como IBGW e OBEP ao mesmo tempo. A mensagem tem o mesmo formato que o VaribaleTunnelBuild, mas o ClearText contém campos diferentes::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

Também conterá um campo mencionando a qual darknet o próximo par pertence e algumas informações adicionais se não for I2P.

TunnelTermination
`````````````````
Se um par quiser sair, ele cria mensagens TunnelTermination, encripta com a chave da camada e envia na direção "in". Se um participante receber tal mensagem, ele a encripta com sua própria chave de camada e a envia para o próximo par. Uma vez que a mensagem chega ao proprietário do túnel, ele começa a decifrar de par em par até obter a mensagem descriptografada. Ele descobre qual par saiu e termina o túnel.
