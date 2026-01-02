---
title: "v3dgsend"
description: "Utilitário CLI para enviar datagramas I2P via SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Status: Esta é uma referência concisa para o utilitário `v3dgsend`. Ele complementa a documentação da [API de Datagramas](/docs/api/datagrams/) e [SAM v3](/docs/api/samv3/).

## Visão Geral

`v3dgsend` é um auxiliar de linha de comando para enviar datagramas I2P usando a interface SAM v3. É útil para testar a entrega de datagramas, prototipar serviços e verificar o comportamento ponta a ponta sem escrever um cliente completo.

Usos típicos incluem:

- Teste de verificação básica de alcance de datagramas para um Destino
- Validação de firewall e configuração do catálogo de endereços
- Experimentação com datagramas brutos vs. assinados (com resposta)

## Uso

A invocação básica varia de acordo com a plataforma e empacotamento. As opções comuns incluem:

- Destination: Destination em base64 ou nome `.i2p`
- Protocol: raw (PROTOCOL 18) ou signed (PROTOCOL 17)
- Payload: string inline ou entrada de arquivo

Consulte a documentação da sua distribuição ou a saída `--help` para ver as flags exatas.

## Veja Também

- [API de Datagram](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Biblioteca de Streaming](/docs/api/streaming/) (alternativa aos datagramas)
