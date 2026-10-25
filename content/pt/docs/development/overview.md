---
title: "Índice da Documentação Técnica"
description: "Índice da documentação técnica do I2P"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/pt/docs/develop/overview"
  - "/pt/docs/develop/overview/"
---


## Visão Geral {#overview}

- [Introdução Técnica](/docs/overview/intro)
- [Uma Introdução Menos Técnica](/docs/overview/intro/)
- [Modelo de ameaças e análise](/docs/overview/threat-model)
- [Comparações com outras redes anônimas](/docs/overview/comparison)
- [Diagrama da pilha de protocolos](/docs/development/protocol-stack)
- [Artigos sobre I2P](/papers/)
- [Apresentações, artigos, tutoriais, vídeos e entrevistas](/about/media/)
- [Visão Geral do Projeto Invisible Internet (I2P) - 28 de agosto de 2003 (PDF)](/docs/historical/i2p_philosophy.pdf)


## Tópicos da Camada de Aplicação {#applications}

- [Visão geral e guia de desenvolvimento de aplicações](/docs/development/applications)
- [Nomenclatura e livro de endereços](/docs/overview/naming)
- [Comandos de feed de assinatura do livro de endereços](/docs/specs/subscription)
- [Visão geral de plugins](/docs/guides/plugins)
- [Especificação de plugins](/docs/specs/plugin)
- [Clientes gerenciados](/docs/applications/managed-clients)
- [Incorporando o roteador em sua aplicação](/docs/applications/embedding)
- [Bittorrent sobre I2P](/docs/applications/bittorrent)
- [API do Plugin I2PControl](/docs/api/i2pcontrol)
- [Formato hostsdb.blockfile](/docs/specs/blockfile)
- [Formato do arquivo de configuração](/docs/specs/configuration)


## API e Protocolos da Camada de Aplicação {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [Configuração do I2PTunnel](/docs/specs/configuration)
- [Proxy SOCKS](/docs/api/socks)
- [Protocolo SAMv3](/docs/api/samv3)
- [Protocolo SAM](/docs/legacy/sam) (Obsoleto)
- [Protocolo SAMv2](/docs/legacy/samv2) (Obsoleto)
- [Protocolo BOB](/docs/legacy/bob) (Obsoleto)


## API e Protocolos de Transporte Ponta a Ponta {#transport-api}

- [Visão geral do protocolo de streaming](/docs/api/streaming)
- [Especificação do protocolo de streaming](/docs/specs/streaming)
- [Datagramas](/docs/api/datagrams)
- [Especificação de datagramas](/docs/specs/datagrams)


## API e Protocolo de Interface Cliente-Roteador {#i2cp}

- [Visão geral do I2CP](/docs/specs/i2cp)
- [Especificação do I2CP](/docs/specs/i2cp)
- [Especificação de estruturas de dados comuns](/docs/specs/common-structures)


## Criptografia Ponta a Ponta {#encryption}

- [Criptografia ECIES-X25519-AEAD-Ratchet para destinos](/docs/specs/ecies)
- [Criptografia híbrida ECIES-X25519](/docs/specs/ecies-hybrid)
- [Criptografia ECIES-X25519 para roteadores](/docs/specs/ecies-routers)
- [Criptografia ElGamal/AES+SessionTag](/docs/specs/elgamal-aes)
- [Detalhes de criptografia ElGamal e AES](/docs/specs/cryptography)


## Banco de Dados da Rede {#netdb}

- [Visão geral do banco de dados da rede, detalhes e análise de ameaças](/docs/overview/network-database)
- [Hashes criptográficos](/docs/specs/cryptography#hashes)
- [Assinaturas criptográficas](/docs/specs/cryptography#signatures)
- [Assinaturas Red25519](/docs/specs/red25519)
- [Especificação de reseed do roteador](/docs/misc/reseed)
- [Endereços Base32 para leasesets criptografados](/docs/specs/b32encrypted)


## Protocolo de Mensagens do Roteador {#i2np}

- [Visão geral do I2NP](/docs/specs/i2np)
- [Especificação do I2NP](/docs/specs/i2np)
- [Especificação de estruturas de dados comuns](/docs/specs/common-structures)
- [Especificação de leaseset criptografado](/docs/specs/encryptedleaseset)


## Túneis {#tunnels}

- [Perfilamento e seleção de pares](/docs/overview/peer-selection)
- [Visão geral do roteamento de túneis](/docs/overview/tunnel-routing)
- [Roteamento garlic e terminologia](/docs/overview/garlic-routing)
- [Construção e criptografia de túneis](/docs/specs/tunnel-creation)
- [ElGamal/AES para criptografia de requisição de construção](/docs/specs/elgamal-tunnel-creation)
- [Detalhes de criptografia ElGamal e AES](/docs/specs/cryptography)
- [Especificação de construção de túneis (ElGamal)](/docs/specs/tunnel-creation)
- [Especificação de construção de túneis (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [Especificação de mensagens de túnel de baixo nível](/docs/specs/tunnel-message)
- [Túneis unidirecionais](/docs/legacy/unidirectional)
- [Perfilamento e seleção de pares na rede anônima I2P - 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## Camada de Transporte {#transports}

- [Visão geral da camada de transporte](/docs/overview/transport)
- [Especificação NTCP2](/docs/specs/ntcp2)
- [Especificação SSU2](/docs/specs/ssu2)
- [NTCP (Legado)](/docs/legacy/ntcp)
- [Visão geral do SSU (Legado)](/docs/legacy/ssu-overview)


## Outros Tópicos do Roteador {#router}

- [Atualizações do software do roteador](/docs/specs/updates)
- [Especificação de reseed do roteador](/docs/misc/reseed)
- [Desempenho](/docs/overview/performance)
- [Formato do arquivo de configuração](/docs/specs/configuration)
- [Formato do arquivo GeoIP](/docs/legacy/geoip)
- [Portas usadas pelo I2P](/docs/overview/ports)


## Guias e Recursos para Desenvolvedores {#develop}

- [Guia para novos desenvolvedores](/docs/development/new-developers)
- [Guia para novos tradutores](/docs/development/new-translators)
- [Diretrizes para desenvolvedores](/docs/development/dev-guidelines)
- [Propostas](/proposals/)
- [Incorporando o roteador em sua aplicação](/docs/applications/embedding)
- [Como configurar um servidor de reseed](/docs/guides/reseed-server)
- [Portas usadas pelo I2P](/docs/overview/ports)
- [Roteiro do projeto](/get-involved/roadmap/)
- [Documentos antigos do invisiblenet I2P - 2003](/docs/historical/)
