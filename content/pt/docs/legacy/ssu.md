---
title: "SSU (legado)"
description: "Transporte UDP original, seguro e semiconfiável"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Obsoleto:** SSU foi substituído por SSU2. O suporte foi removido no i2pd 2.44.0 (API 0.9.56, nov 2022) e no Java I2P 2.4.0 (API 0.9.61, dez 2023).

SSU fornecia entrega semiconfiável baseada em UDP, com controle de congestionamento, atravessamento de NAT e suporte a introducer (nó introdutor usado no SSU para facilitar conexões a pares atrás de NAT). Complementava o NTCP ao lidar com routers atrás de NAT/firewalls e ao coordenar a descoberta de IP.

## Elementos de endereço

- `transport`: `SSU`
- `caps`: flags de capacidade (`B`, `C`, `4`, `6`, etc.)
- `host` / `port`: ouvinte IPv4 ou IPv6 (opcional quando atrás de firewall)
- `key`: chave de introdução em Base64
- `mtu`: Opcional; padrão 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: entradas de introducer (nó introdutor) quando o router está atrás de firewall

## Recursos

- Atravessamento de NAT cooperativo usando introducers (nós introdutores)
- Detecção de IP local por meio de testes com pares e inspeção de pacotes de entrada
- Estado do firewall encaminhado automaticamente a outros transportes e ao console do router
- Entrega semiconfiável: mensagens retransmitidas até um limite, depois descartadas
- Controle de congestionamento com aumento aditivo / diminuição multiplicativa e campos de bits de ACK de fragmentos

SSU também cuidava de tarefas de metadados, como sinais de temporização e negociação de MTU. Toda a funcionalidade agora é fornecida (com criptografia moderna) pelo [SSU2](/docs/specs/ssu2/).
