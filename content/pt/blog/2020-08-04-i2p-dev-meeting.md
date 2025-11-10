---
title: "Reunião de Desenvolvedores do I2P - 4 de agosto de 2020"
date: 2020-08-04
author: "i2p"
description: "Registro da reunião de desenvolvimento do I2P de 04 de agosto de 2020."
categories: ["meeting"]
---

## Resumo rápido

<p class="attendees-inline"><strong>Presentes:</strong> eyedeekay, zlatinb, zzz</p>

## Registro da Reunião

<div class="irc-log">

(04:00:50 PM) eyedeekay1: Olá zlatinb zzz mikalvmeeh eche|on, se todos estiverem prontos vamos começar a reunião.
(04:00:50 PM) eyedeekay1: 1) Olá
(04:00:50 PM) eyedeekay1: 2) Lançamento 0.9.47
(04:00:50 PM) eyedeekay1: 3) Acompanhamento das reuniões mensais
(04:00:50 PM) eyedeekay1: 4) Atualização do Git
(04:01:38 PM) eyedeekay1: Olá a todos, antes de mais nada, desculpem por não ter percebido que coloquei a data errada no título do meu anúncio.
(04:02:38 PM) zzz: oi
(04:02:58 PM) eyedeekay1: oi zzz
(04:03:31 PM) zlatinb: oi
(04:03:42 PM) eyedeekay1: Oi zlatinb
(04:04:49 PM) eyedeekay1: OK então 2) o lançamento 0.9.47
(04:05:27 PM) eyedeekay1: Parece que também não vou conseguir concluir o rekeyOnIdle a tempo para a 0.9.47.
(04:05:58 PM) eyedeekay1: O que será incluído são principalmente atualizações de elementos visuais do meu lado.
(04:06:19 PM) eyedeekay1: Algo de zzz ou zlatinb sobre o lançamento 0.9.47?
(04:06:43 PM) zzz: o resumo está em http://zzz.i2p/topics/2905
(04:06:49 PM) zzz: congelamento de tag daqui a uma semana a partir de amanhã
(04:06:53 PM) zzz: lançamento em cerca de 3 semanas
(04:07:07 PM) zzz: o diff está em cerca de 18.500 linhas, o que é bem típico
(04:07:23 PM) zzz: as coisas parecem boas. Tenho algumas coisas para finalizar
(04:07:40 PM) zzz: mas estou bastante confiante de que podemos manter o cronograma
(04:07:49 PM) zzz: EOT
(04:08:08 PM) eyedeekay1: Vi bastante coisa entrar ontem, tenho tentado olhar incrementalmente conforme você envia. É realmente empolgante ver seu trabalho. Muito obrigado.
(04:08:41 PM) zzz: isso foi só material diverso que estava parado no meu workspace há semanas, nada digno de nota realmente
(04:09:42 PM) eyedeekay1: Bem, acompanhar é educativo mesmo assim, eu não sei onde tudo fica; ver você trabalhar me ajuda a reconhecer onde diferentes coisas acontecem
(04:09:43 PM) zzz: só tentando limpar as coisas e enviar. às vezes eu testo algo por meses e meses
(04:10:28 PM) zzz: claro, revisar alterações de outras pessoas é uma ótima maneira de aprender e de pegar erros, continue assim
(04:10:39 PM) eyedeekay1: Pode deixar
(04:10:42 PM) eyedeekay1: Se não houver mais nada, vou passar para 3) timeout 1m
(04:12:40 PM) eyedeekay1: 2) Acompanhamento da Reunião Mensal:
(04:12:53 PM) eyedeekay1: Esta é a reunião mensal.
(04:12:53 PM) eyedeekay1: Eu não configurei um gateway WebIRC, pois, pelo que entendi, isso teria sido contra nossas regras do IRC.
(04:13:13 PM) eyedeekay1: Agora eu tenho uma cópia das regras de anúncios de reuniões e a responsabilidade por esses anúncios foi esclarecida para mim.
(04:13:25 PM) eyedeekay1: O anúncio para 1º de setembro, com a data correta desta vez, foi publicado. Ainda não há tópicos, por favor, adicione-os conforme necessário: http://zzz.i2p/topics/2931-meeting-tues-september-1-8pm-utc
(04:14:55 PM) eyedeekay1: Isso, claro, virá pouco depois do lançamento 0.9.47
(04:15:45 PM) eyedeekay1: Algo sobre o 2) de mais alguém?
(04:17:57 PM) eyedeekay1: 3) Transição para Git
(04:18:34 PM) eyedeekay1: A transição para Git está finalmente em andamento; temos um plano e estamos começando a executá-lo
(04:19:08 PM) eyedeekay1: o nextloop e eu estamos fazendo progressos para espelhar as próximas poucas branches significativas do mtn no github
(04:19:27 PM) eyedeekay1: estas ainda são somente leitura até a conclusão de suas respectivas fases na migração para git, ou seja, nada de pulls ou MRs ainda
(04:20:04 PM) eyedeekay1: Para uma descrição detalhada dessas fases, veja: http://zzz.i2p/topics/2920-flipping-the-switch-on-git#10
(04:20:42 PM) eyedeekay1: Seria útil para o nextloop e para mim se eu desse ao nextloop permissão para criar repositórios no namespace i2p no github e para escrever nos repositórios que ele criar.
(04:20:47 PM) zzz: bom trabalho ao redigir o plano
(04:21:24 PM) eyedeekay1: Obrigado, zzz, feliz por finalmente tê-lo em um estado utilizável
(04:22:17 PM) zzz: não está perfeito, mas está 'utilizável' no sentido de que podemos comentar sobre ele
(04:24:39 PM) eyedeekay1: A próxima coisa que vamos mover é o site, o que é bom porque é bastante simples e não tem nada que dependa dele; isso deve acontecer esta semana
(04:25:26 PM) eyedeekay1: Mas, sobre o nextloop, eu gostaria de saber se há ampla aprovação para conceder a ele essa permissão de criar/escrever em repositórios do github para nós?
(04:25:54 PM) zzz: ok. aguardando sua edição no plano/cronograma para evitar conflitos com o lançamento .47
(04:26:25 PM) eyedeekay1: Ack, já abri no meu editor :)
(04:26:48 PM) zzz: Você terá que perguntar às pessoas que atualmente são admins do github, que não estão aqui, e eu não sou membro
(04:27:39 PM) eyedeekay1: Até agora, esta proposta conta com a aprovação deles, embora eu ainda tenha um que não respondeu.
(04:29:05 PM) zzz: por mim tudo bem, desde que vocês dois tenham um método de comunicação confiável e backup. Acho que não precisamos de mais admins que não respondem :)
(04:29:53 PM) eyedeekay1: Acho que conseguimos administrar isso
(04:30:06 PM) eyedeekay1: Então o nextloop vai receber permissões no github
(04:31:40 PM) zzz: pessoas que ficam muito tempo sem responder e têm muitos privilégios podem ser boas como backup para o pior caso de 'foi atropelado por um ônibus', mas isso também é um risco potencial de segurança, então precisa ser gerenciado
(04:33:12 PM) eyedeekay1: É
(04:33:20 PM) eyedeekay1: Se houver mais alguma coisa que possamos tratar aqui no 3), então acho que é agora; caso contrário, veremos o plano revisado no tópico do zzz.i2p provavelmente dentro do próximo dia.
(04:33:45 PM) zzz: super
(04:34:18 PM) mikalvmeeh: (Estou meio aqui, perdi o oi)
(04:34:56 PM) eyedeekay1: Bem, cobrimos os tópicos planejados, alguém tem mais alguma coisa?
(04:36:43 PM) eyedeekay1: timeout 1m
(04:38:51 PM) eyedeekay1: *bafs* Certo, isso encerra esta reunião. Por favor, lembrem-se: 1º de setembro, a próxima reunião marcada para este mesmo horário, 20h UTC
(04:39:12 PM) eyedeekay1: Obrigado a todos por virem </div>
