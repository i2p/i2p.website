---
title: "Reunião de Desenvolvedores do I2P - 03 de setembro de 2019"
date: 2019-09-03
author: "zzz"
description: "Registro da reunião de desenvolvimento do I2P de 03 de setembro de 2019."
categories: ["meeting"]
---

## Resumo rápido

<p class="attendees-inline"><strong>Presentes:</strong> eyedeekay, sadie, zlatinb, zzz</p>

## Registro da reunião

<div class="irc-log">                Nota: as linhas de sadie não foram recebidas durante a reunião; foram coladas abaixo.

20:00:00 &lt;zzz&gt; 0) Oi
20:00:00 &lt;zzz&gt; 1) status do lançamento 0.9.42 (zzz)
20:00:00 &lt;zzz&gt; 2) status do projeto "labs" do I2P Browser (sadie, meeh)
20:00:00 &lt;zzz&gt; 3) Casos de uso de outproxy (proxy de saída) / status (sadie)
20:00:00 &lt;zzz&gt; 4) status do desenvolvimento 0.9.43 (zzz)
20:00:00 &lt;zzz&gt; 5) status das propostas (zzz)
20:00:00 &lt;zzz&gt; 6) Scrum de status (zlatinb)
20:00:04 &lt;zzz&gt; 0) Oi
20:00:06 &lt;zzz&gt; oi
20:00:17 &lt;zlatinb&gt; oi
20:00:30 &lt;zzz&gt; 1) status do lançamento 0.9.42 (zzz)
20:00:48 &lt;zzz&gt; o lançamento correu muito bem na semana passada
20:00:56 &lt;zzz&gt; há apenas algumas pendências
20:01:27 &lt;zzz&gt; colocar a bridge do GitHub para funcionar novamente (nextloop), o pacote do Debian sid (mhatta) e a biblioteca cliente Android que esquecemos para a 41 (meeh)
20:01:37 &lt;zzz&gt; nextloop, meeh, vocês têm ETAs (previsão de entrega) para esses itens?
20:03:06 &lt;zzz&gt; mais alguma coisa sobre 1)?
20:04:02 &lt;zzz&gt; 2) status do projeto "labs" do I2P Browser (sadie, meeh)
20:04:25 &lt;zzz&gt; sadie, meeh, qual é o status e qual é o próximo marco?          &lt;sadie&gt; A Beta 5 deveria ter saído na sexta-feira, mas houve alguns problemas. Parece que alguns estão prontos https://i2bbparts.meeh.no/i2p-browser/ mas eu realmente precisava ouvir do meeh qual é o próximo prazo para isso          &lt;sadie&gt; A página do Lab estará no ar até o fim desta semana. O próximo marco do Browser será discutir os requisitos do console para o lançamento da beta 6
20:05:51 &lt;zzz&gt; mais alguma coisa sobre 2)?
20:06:43 &lt;zzz&gt; 3) Casos de uso de outproxy / status (sadie)
20:06:57 &lt;zzz&gt; sadie, qual é o status e qual é o próximo marco?          &lt;sadie&gt; Qualquer pessoa pode acompanhar as atas da nossa reunião no ticket 2472. Definimos os status dos casos de uso e temos uma lista de requisitos. O próximo marco serão os requisitos de usuário para um caso de uso de Amigos e Família, bem como os requisitos de desenvolvimento para Amigos e Família e para o caso de uso Geral, para ver onde eles podem se sobrepor
20:08:05 &lt;zzz&gt; mais alguma coisa sobre 3)?
20:08:19 &lt;eyedeekay&gt; Desculpem o atraso
20:09:01 &lt;zzz&gt; 4) status do desenvolvimento 0.9.43 (zzz)
20:09:21 &lt;zzz&gt; estamos apenas começando o ciclo da .43, que planejamos lançar em cerca de 7 semanas
20:09:40 &lt;zzz&gt; atualizamos o roteiro no site, mas vamos adicionar mais alguns itens
20:10:06 &lt;zzz&gt; tenho corrigido alguns bugs de IPv6 e acelerado o processamento de AES no tunnel
20:10:30 &lt;zzz&gt; em breve vou voltar minha atenção para a nova mensagem I2CP de blinding info (informações de cegamento)
20:10:59 &lt;zzz&gt; eyedeekay, zlatinb, vocês têm algo a acrescentar sobre a .43?
20:11:46 &lt;eyedeekay&gt; Não, acho que não
20:12:02 &lt;zlatinb&gt; provavelmente mais coisas de testnet (rede de testes)
20:12:32 &lt;zzz&gt; sim, temos mais alguns tickets do jogger para analisar, no que diz respeito ao SSU
20:12:48 &lt;zzz&gt; mais alguma coisa sobre 4)?
20:14:00 &lt;zzz&gt; 5) status das propostas (zzz)
20:14:20 &lt;zzz&gt; nosso foco principal é a nova e muito complexa proposta de criptografia 144
20:14:48 &lt;zzz&gt; fizemos bons avanços nas últimas semanas e fizemos algumas atualizações importantes na própria proposta
20:15:35 &lt;zzz&gt; ainda há algumas limpezas e lacunas a preencher, mas estou confiante de que está em estado suficientemente bom para que possamos começar a codificar algumas implementações de testes unitários em breve, talvez até o fim do mês
20:16:17 &lt;zzz&gt; além disso, a mensagem de blinding info para a proposta 123 (LS2 criptografado) terá outra análise depois que eu começar a codificá-la na próxima semana
20:16:52 &lt;zzz&gt; também, estamos esperando uma atualização da proposta 152 (mensagens de construção de tunnel) do chisana em breve
20:17:27 &lt;zzz&gt; concluímos a proposta 147 (prevenção entre redes) no mês passado e tanto o i2p quanto o i2pd têm isso codificado e incluído no lançamento .42
20:18:23 &lt;zzz&gt; então as coisas estão avançando; mesmo que a 144 pareça lenta e assustadora, até ela está progredindo bem
20:18:27 &lt;zzz&gt; mais alguma coisa sobre 5)?
20:20:00 &lt;zzz&gt; 6) Scrum de status (zlatinb)
20:20:05 &lt;zzz&gt; a palavra é sua, zlatinb
20:20:42 &lt;zlatinb&gt; Oi, por favor digam em poucas palavras: 1) o que vocês têm feito desde o último scrum 2) o que planejam fazer no próximo mês 3) vocês têm algum impedimento ou precisam de ajuda.  Digam EOT quando terminarem
20:21:23 &lt;zlatinb&gt; eu: 1) Vários experimentos no testnet para acelerar transferências em massa 2) mais trabalho no testnet, de preferência em um servidor/rede maior 3) sem impedimentos EOT
20:22:15 &lt;zzz&gt; 1) correções de bugs, a mudança de separação da configuração, lançamento .42, propostas, workshops na DEFCON (veja meu relato de viagem no i2pforum e em nosso site)
20:23:56 &lt;zzz&gt; 2) correções de bugs, proposta 144, mensagem de blinding info, otimizações de desempenho, ajudar na pesquisa de outproxy, corrigir o assistente de SSL quebrado pela divisão da conf.
20:24:20 &lt;zzz&gt; mais correções de IPv6
20:24:38 &lt;zzz&gt; 3) sem impedimentos EOT
20:24:50 &lt;eyedeekay&gt; 1) Desde o último scrum tenho trabalhado em correções de bugs, no site, na proposta de outproxy e em coisas relacionadas a i2ptunnels. 2) Continuar reorganizando e melhorando a apresentação do site. Trabalhar no avanço da proposta de outproxy 3) sem impedimentos EOT          &lt;sadie&gt; 1) Participei do FOCI, pesquisei opções de financiamento, encontrei potenciais financiadores, tive uma reunião com o Tails (incluindo o Mhatta), trabalhei na identidade do I2P Browser, atualizações do site com o IDK, fiz pequenas alterações no console para o último lançamento          &lt;sadie&gt; 2) no meu próximo mês vou trabalhar em bolsas, melhorias no console e no site, assistente de configuração, participar do Our Networks em Toronto, avançar a pesquisa do I2P Browser e do OutProxy          &lt;sadie&gt; 3) sem impedimentos EOT
20:25:29 &lt;zlatinb&gt; scrum.setTimeout( 60 * 1000 );
20:27:04 &lt;zzz&gt; ok, esgotando o tempo
20:27:10 &lt;zlatinb&gt; ScrumTimeoutException
20:27:41 &lt;zzz&gt; última chamada para sadie, meeh, nextloop voltarem aos itens 1)-3)
20:27:52 &lt;zzz&gt; mais algum tópico para a reunião?
20:28:47 * zzz pega o baffer
20:30:00 * zzz ***bafs*** encerra a reunião
</div>
