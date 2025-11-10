---
title: "Notas de status do I2P para 2006-01-24"
date: 2006-01-24
author: "jr"
description: "Atualização do estado da rede, novo processo de construção de tunnel para 0.6.2 e melhorias de confiabilidade"
categories: ["status"]
---

Oi, pessoal, terça-feira insiste em voltar...

* Index

1) Estado da rede 2) Novo processo de compilação 3) ???

* 1) Net status

Na última semana, não houve muitas mudanças na rede, com a maioria dos usuários (77%) atualizada para a versão mais recente. Ainda assim, há mudanças significativas a caminho, relacionadas ao novo processo de construção de tunnel, e essas mudanças causarão alguns percalços para aqueles que estão ajudando a testar as compilações não lançadas. No geral, porém, aqueles que usam as versões lançadas devem continuar a ter um nível de serviço razoavelmente confiável.

* 2) New build process

Como parte da reformulação do tunnel para a versão 0.6.2, estamos alterando o procedimento usado dentro do router para se adaptar melhor às condições em mudança e para lidar de forma mais limpa com a carga.  Isto é um precursor da integração das novas estratégias de seleção de pares e da nova criptografia de criação de tunnel, e é totalmente compatível com versões anteriores.  No entanto, ao longo do caminho estamos corrigindo algumas das peculiaridades no processo de construção de tunnels, e embora algumas dessas peculiaridades tenham ajudado a encobrir alguns problemas de confiabilidade, podem ter acarretado um compromisso entre anonimato e confiabilidade menos que ideal.  Especificamente, eles usariam tunnels de 1 salto de contingência em caso de falhas catastróficas - o novo processo, em vez disso, preferirá a inacessibilidade em vez de usar tunnels de contingência, o que significa que as pessoas verão mais problemas de confiabilidade.  Pelo menos, eles ficarão visíveis até que a origem do problema de confiabilidade dos tunnels seja resolvida.

De qualquer forma, no momento o processo de build não oferece confiabilidade aceitável, mas, assim que oferecer, vamos disponibilizá-lo para vocês em uma versão.

* 3) ???

Eu sei que alguns outros estão trabalhando em diferentes atividades relacionadas, mas vou deixar por conta deles nos trazer as novidades quando acharem apropriado. De qualquer forma, vejo vocês na reunião em alguns minutos!

=jr
