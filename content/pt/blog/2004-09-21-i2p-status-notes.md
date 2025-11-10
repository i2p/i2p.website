---
title: "Notas de status do I2P de 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Atualização semanal de status do I2P cobrindo o progresso do desenvolvimento, melhorias no transporte TCP e o novo recurso userhosts.txt"
categories: ["status"]
---

Olá pessoal, atualização rápida esta semana

## Índice

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Status do desenvolvimento

A rede tem estado bastante estável na última semana, então consegui dedicar meu tempo à versão 0.4.1 - reformulando o transporte TCP e adicionando suporte para detecção de endereços IP e removendo aquela coisa antiga de "target changed identities". Isso também deve eliminar a necessidade de entradas dyndns.

Não será a configuração ideal de 0 cliques para pessoas atrás de NATs ou firewalls — elas ainda precisarão fazer o encaminhamento de portas para poder receber conexões TCP de entrada. Ainda assim, deve ser menos sujeito a erros. Estou fazendo o possível para manter a compatibilidade com versões anteriores, mas não estou fazendo nenhuma promessa nesse sentido. Mais novidades quando estiver pronto.

## 2) Novo userhosts.txt vs. hosts.txt

Na próxima versão, teremos o muito solicitado suporte para um par de arquivos hosts.txt - um que é sobrescrito durante as atualizações (ou a partir de `http://dev.i2p.net/i2p/hosts.txt`) e outro que o usuário pode manter localmente. Na próxima versão (ou no CVS HEAD) você pode editar o arquivo "userhosts.txt", que é verificado antes de hosts.txt para quaisquer entradas - por favor, faça suas alterações locais lá, pois o processo de atualização sobrescreverá hosts.txt (mas não userhosts.txt).

## 3) ???

Como mencionei, apenas algumas notas breves esta semana. Alguém tem mais alguma coisa que queira trazer à tona? Apareçam na reunião daqui a alguns minutos.

=jr
