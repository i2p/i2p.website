---
title: "Limites de Congestionamento"
number: "162"
author: "dr|z3d, idk, orignal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Open"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Visão Geral

Adicionar indicadores de congestionamento à Router Info (RI) publicada.




## Motivação

"Capacidades" de largura de banda indicam limites de compartilhamento de largura de banda e acessibilidade, mas não o estado de congestionamento. Um indicador de congestionamento ajudará os roteadores a evitar tentativas de construção através de um roteador congestionado, o que contribui para mais congestionamento e redução no sucesso da construção de túneis.



## Design

Definir novas capacidades para indicar vários níveis de congestionamento ou problemas de capacidade. Estas estarão nas capacidades de RI de nível superior, não nas capacidades de endereço.


### Definição de Congestionamento

Congestionamento, em geral, significa que o par provavelmente não receberá e aceitará um pedido de construção de túnel. Como definir ou classificar os níveis de congestionamento é específico para cada implementação.

As implementações podem considerar um ou mais dos seguintes:

- Nos limites ou próximo dos limites de largura de banda
- Nos limites ou próximo do número máximo de túneis participantes
- Nos limites ou próximo do número máximo de conexões em um ou mais transportes
- Acima do limite para profundidade de fila, latência ou uso de CPU; estouro de fila interna
- Capacidades de CPU e memória da plataforma / sistema operacional base
- Congestionamento de rede percebido
- Estado da rede como firewall ou NAT simétrico ou oculto ou em proxy
- Configurado para não aceitar túneis

O estado de congestionamento deve se basear na média das condições ao longo de vários minutos, não em uma medição instantânea.



## Especificação

Atualizar [NETDB](/docs/how/network-database/) da seguinte forma:


```text
D: Congestionamento médio, ou um roteador de baixo desempenho (por exemplo, Android, Raspberry Pi)
     Outros roteadores devem rebaixar ou limitar a aparente capacidade de túnel deste roteador no perfil.

  E: Alto congestionamento, este roteador está próximo ou no limite,
     e está rejeitando ou descartando a maioria dos pedidos de túnel.
     Se este RI foi publicado nos últimos 15 minutos, outros roteadores
     devem severamente rebaixar ou limitar a capacidade deste roteador.
     Se este RI for mais antigo que 15 minutos, trate como 'D'.

  G: Este roteador está rejeitando todos os túneis temporária ou permanentemente.
     Não tente construir um túnel através deste roteador,
     até receber um novo RI sem o 'G'.
```

Para consistência, as implementações devem adicionar quaisquer capacidades de congestionamento no final (após R ou U).



## Análise de Segurança

Qualquer informação de par publicada não pode ser confiada. Capacidades, como qualquer outra coisa na Router Info, podem ser falsificadas. Nunca usamos nada na Router Info para aumentar a capacidade percebida de um roteador.

Publicar indicadores de congestionamento, dizendo aos pares para evitar este roteador, é inerentemente muito mais seguro do que indicadores permissivos ou de capacidade solicitando mais túneis.

Os indicadores atuais de capacidade de largura de banda (L-P, X) são confiáveis apenas para evitar roteadores de largura de banda muito baixa. A capacidade "U" (inacessível) tem um efeito semelhante.

Qualquer indicador de congestionamento publicado deve ter o mesmo efeito que rejeitar ou descartar um pedido de construção de túnel, com propriedades de segurança semelhantes.



## Notas

Os pares não devem evitar completamente os roteadores 'D', apenas rebaixá-los.

Deve-se ter cuidado para não evitar completamente os roteadores 'E', para que quando toda a rede estiver em congestionamento e publicando 'E', as coisas não quebrem completamente.

Os roteadores podem usar diferentes estratégias para quais tipos de túneis construir através de roteadores 'D' e 'E', por exemplo, exploratórios vs. cliente, ou túneis de cliente de alta vs. baixa largura de banda.

Os roteadores provavelmente não devem publicar uma capacidade de congestionamento ao iniciar ou desligar por padrão, mesmo que seu estado de rede seja desconhecido, para prevenir a detecção de reinício por pares.




## Compatibilidade

Sem problemas, todas as implementações ignoram capacidades desconhecidas.


## Migração

As implementações podem adicionar suporte a qualquer momento, sem necessidade de coordenação.

Plano preliminar:
Publicar capacidades em 0.9.58 (abril de 2023);
agir sobre as capacidades publicadas em 0.9.59 (julho de 2023).



## Referências

* [NETDB](/docs/how/network-database/)
