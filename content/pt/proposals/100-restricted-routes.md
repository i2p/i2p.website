---
title: "Rotas Restritas"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Reserva"
thread: "http://zzz.i2p/topics/114"
---

## Introdução


## Reflexões

- Adicionar um novo transporte "IND" (indireto) que publica um hash de leaseSet na
  estrutura RouterAddress: "IND: [key=aababababababababb]". Este transporte oferece
  a prioridade mais baixa quando o roteador de destino o publica. Para enviar a um par via
  este transporte, obtenha o leaseset de um par ff como de costume, e envie
  diretamente para o lease.

- Um par que anuncia IND deve construir e manter um conjunto de túneis para outro
  par. Estes não são túneis exploratórios nem túneis de cliente, mas um segundo
  conjunto de túneis de roteador.

  - 1-hop é suficiente?
  - Como selecionar pares para estes túneis?
  - Eles precisam ser "não restritos", mas como saber isso? Mapeamento de
    alcance? Teoria dos grafos, algoritmos, estruturas de dados podem ajudar aqui. Preciso
    ler mais sobre isso. Veja túneis TODO.

- Se você tem túneis IND, então seu transporte IND deve oferecer (baixa prioridade) para
  enviar mensagens por estes túneis.

- Como decidir habilitar a construção de túneis indiretos

- Como implementar e testar sem comprometer a cobertura
