---
title: "Multicast"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Descontinuado"
thread: "http://zzz.i2p/topics/172"
---

## Visão Geral

Ideia básica: Enviar uma cópia através do seu túnel de saída, o ponto final de saída distribui para todos os gateways de entrada. Criptografia de ponta a ponta inviabilizada.

## Design

- Novo tipo de mensagem de túnel multicast (tipo de entrega = 0x03)
- Distribuição multicast do ponto final de saída
- Novo tipo de Mensagem Multicast I2NP?
- Novo tipo de Mensagem SendMessageMessage Multicast I2CP
- Não criptografar router-router em OutNetMessageOneShotJob (alho?)

Aplicativo:

- Proxy RTSP?

Streamr:

- Ajustar MTU? Ou apenas fazer isso no aplicativo?
- Recepção e transmissão sob demanda
