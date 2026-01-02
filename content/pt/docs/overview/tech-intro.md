---
title: "I2P: Uma estrutura escalável para comunicação anônima"
description: "Introdução técnica à arquitetura e operação do I2P"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Introdução

I2P é uma camada de rede anônima escalável, auto-organizada e resiliente baseada em comutação de pacotes, sobre a qual qualquer número de aplicações diferentes conscientes de anonimato ou segurança podem operar. Cada uma dessas aplicações pode fazer suas próprias compensações entre anonimato, latência e throughput (taxa de transferência) sem se preocupar com a implementação adequada de uma mixnet (rede de mistura) de rota livre, permitindo que elas mesclem sua atividade com o conjunto maior de anonimato dos usuários já em execução sobre o I2P.

As aplicações já disponíveis fornecem toda a gama de atividades típicas da Internet — navegação web **anônima**, hospedagem de sites, chat, compartilhamento de arquivos, e-mail, blogs e distribuição de conteúdo, bem como várias outras aplicações em desenvolvimento.

- **Navegação web:** usando qualquer navegador existente que suporte um proxy  
- **Chat:** IRC e outros protocolos  
- **Compartilhamento de arquivos:** [I2PSnark](#i2psnark) e outras aplicações  
- **E-mail:** [Susimail](#i2pmail) e outras aplicações  
- **Blog:** usando qualquer servidor web local, ou plugins disponíveis

Ao contrário de sites hospedados em redes de distribuição de conteúdo como [Freenet](/docs/overview/comparison#freenet) ou [GNUnet](https://www.gnunet.org/), os serviços hospedados no I2P são totalmente interativos — existem motores de busca tradicionais estilo web, fóruns de discussão, blogs nos quais você pode comentar, sites baseados em banco de dados e pontes para consultar sistemas estáticos como Freenet sem precisar instalá-los localmente.

Com todas essas aplicações habilitadas para anonimato, o I2P atua como **middleware orientado a mensagens** — as aplicações especificam os dados a serem enviados para um identificador criptográfico (um "destination"), e o I2P garante que cheguem de forma segura e anônima. O I2P também inclui uma [biblioteca de streaming](#streaming) simples para permitir que as mensagens anônimas de melhor esforço do I2P sejam transferidas como fluxos confiáveis e ordenados, oferecendo controle de congestionamento baseado em TCP ajustado para o alto produto largura de banda-atraso da rede.

Embora proxies SOCKS simples tenham sido desenvolvidos para conectar aplicações existentes, seu valor é limitado, pois a maioria das aplicações vaza informações sensíveis em um contexto anônimo. A abordagem mais segura é **auditar e adaptar** a aplicação para usar as APIs do I2P diretamente.

I2P não é um projeto de pesquisa — acadêmico, comercial ou governamental — mas um esforço de engenharia voltado para fornecer anonimato utilizável. Está em desenvolvimento contínuo desde o início de 2003 por um grupo distribuído de colaboradores em todo o mundo. Todo o trabalho do I2P é **open source** no [site oficial](https://geti2p.net/), principalmente lançado em domínio público, com alguns componentes sob licenças permissivas estilo BSD. Várias aplicações cliente licenciadas sob GPL estão disponíveis, como [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail) e [I2PSnark](#i2psnark). O financiamento vem exclusivamente de doações de usuários.

---

## Operação

### Overview

O I2P distingue claramente entre routers (nós participantes da rede) e destinos (endpoints anônimos para aplicações). Executar o I2P em si não é secreto; o que é oculto é **o que** o usuário está fazendo e qual router seus destinos utilizam. Os usuários finais geralmente executam vários destinos (por exemplo, um para navegação web, outro para hospedagem, outro para IRC).

Um conceito-chave no I2P é o **tunnel** — um caminho criptografado unidirecional através de uma série de routers. Cada router descriptografa apenas uma camada e conhece apenas o próximo salto. Os tunnels expiram a cada 10 minutos e devem ser reconstruídos.

![Esquema de túneis de entrada e saída](/images/tunnels.png)   *Figura 1: Existem dois tipos de túneis — de entrada e de saída.*

- **Túneis de saída** enviam mensagens para longe do criador.  
- **Túneis de entrada** trazem mensagens de volta para o criador.

Combinar estes elementos permite a comunicação bidirecional. Por exemplo, "Alice" usa um tunnel de saída para enviar para o tunnel de entrada de "Bob". Alice criptografa sua mensagem com instruções de roteamento para o gateway de entrada de Bob.

Outro conceito fundamental é o **network database** ou **netDb**, que distribui metadados sobre routers e destinos:

- **RouterInfo:** Contém informações de contato do router e material de chaves.  
- **LeaseSet:** Contém informações necessárias para contactar um destino (gateways de túnel, tempos de expiração, chaves de criptografia).

Os routers publicam suas RouterInfo diretamente no netDb; os LeaseSets são enviados através de túneis de saída para anonimato.

Para construir tunnels, Alice consulta o netDb em busca de entradas RouterInfo para escolher peers, e envia mensagens criptografadas de construção de tunnel hop-by-hop até que o tunnel esteja completo.

![Informações do router são usadas para construir tunnels](/images/netdb_get_routerinfo_2.png)   *Figura 2: Informações do router são usadas para construir tunnels.*

Para enviar dados para Bob, Alice procura o LeaseSet de Bob e usa um dos seus túneis de saída para rotear os dados através do gateway do túnel de entrada de Bob.

![LeaseSets conectam túneis de entrada e saída](/images/netdb_get_leaseset.png)   *Figura 3: LeaseSets conectam túneis de saída e de entrada.*

Como o I2P é baseado em mensagens, ele adiciona **criptografia garlic ponta-a-ponta** para proteger mensagens até mesmo do endpoint de saída ou gateway de entrada. Uma mensagem garlic encapsula múltiplos "dentes" (mensagens) criptografados para ocultar metadados e melhorar o anonimato.

As aplicações podem usar a interface de mensagens diretamente ou depender da [biblioteca de streaming](#streaming) para conexões confiáveis.

---

### Tunnels

Tanto os túneis de entrada quanto os de saída usam criptografia em camadas, mas diferem na construção:

- Nos **túneis de entrada (inbound tunnels)**, o criador (o endpoint) descriptografa todas as camadas.
- Nos **túneis de saída (outbound tunnels)**, o criador (o gateway) pré-descriptografa as camadas para garantir clareza no endpoint.

O I2P cria perfis de peers através de métricas indiretas como latência e confiabilidade, sem sondagem direta. Com base nesses perfis, os peers são agrupados dinamicamente em quatro níveis:

1. Rápido e alta capacidade  
2. Alta capacidade  
3. Não falhando  
4. Falhando

A seleção de pares de túnel normalmente prefere pares de alta capacidade, escolhidos aleatoriamente para equilibrar anonimato e desempenho, com estratégias adicionais de ordenação baseadas em XOR para mitigar ataques de predecessor e coleta de netDb.

Para mais detalhes, consulte a [Especificação de Tunnel](/docs/specs/implementation).

---

### Visão Geral

Routers que participam na tabela hash distribuída (DHT) **floodfill** armazenam e respondem a consultas de LeaseSet. A DHT utiliza uma variante de [Kademlia](https://en.wikipedia.org/wiki/Kademlia). Routers floodfill são selecionados automaticamente se tiverem capacidade e estabilidade suficientes, ou podem ser configurados manualmente.

- **RouterInfo:** Descreve as capacidades e transportes de um router.  
- **LeaseSet:** Descreve os tunnels e chaves de criptografia de um destino.

Todos os dados no netDb são assinados pelo editor e possuem carimbo de data/hora para prevenir ataques de repetição ou entradas obsoletas. A sincronização de tempo é mantida através de SNTP e detecção de desvio na camada de transporte.

#### Additional concepts

- **LeaseSets não publicados e criptografados:**  
  Um destino pode permanecer privado ao não publicar seu LeaseSet, compartilhando-o apenas com peers confiáveis. O acesso requer a chave de descriptografia apropriada.

- **Bootstrapping (reseeding):**  
  Para se juntar à rede, um novo router busca arquivos RouterInfo assinados de servidores reseed HTTPS confiáveis.

- **Escalabilidade de pesquisa:**  
  O I2P usa pesquisas **iterativas**, não recursivas, para melhorar a escalabilidade e segurança da DHT.

---

### Túneis

A comunicação moderna do I2P utiliza dois transportes totalmente criptografados:

- **[NTCP2](/docs/specs/ntcp2):** Protocolo baseado em TCP criptografado  
- **[SSU2](/docs/specs/ssu2):** Protocolo baseado em UDP criptografado

Ambos são construídos no moderno [Noise Protocol Framework](https://noiseprotocol.org/), fornecendo autenticação forte e resistência à impressão digital de tráfego. Eles substituíram os protocolos legados NTCP e SSU (completamente descontinuados desde 2023).

**NTCP2** oferece streaming criptografado e eficiente sobre TCP.

**SSU2** fornece confiabilidade baseada em UDP, travessia de NAT e perfuração de firewall opcional. O SSU2 é conceitualmente semelhante ao WireGuard ou QUIC, equilibrando confiabilidade e anonimato.

Os routers podem suportar tanto IPv4 quanto IPv6, publicando seus endereços de transporte e custos no netDb. O transporte de uma conexão é selecionado dinamicamente por um **sistema de lances** que otimiza para condições e links existentes.

---

### Base de Dados da Rede (netDb)

I2P utiliza criptografia em camadas para todos os componentes: transportes, tunnels, mensagens garlic e o netDb.

As primitivas atuais incluem:

- X25519 para troca de chaves  
- EdDSA (Ed25519) para assinaturas  
- ChaCha20-Poly1305 para criptografia autenticada  
- SHA-256 para hashing  
- AES256 para criptografia de camada de túnel

Os algoritmos legados (ElGamal, DSA-SHA1, ECDSA) permanecem para compatibilidade retroativa.

O I2P está atualmente introduzindo esquemas criptográficos híbridos pós-quânticos (PQ) que combinam **X25519** com **ML-KEM** para resistir a ataques de "coletar agora, descriptografar depois".

#### Garlic Messages

Mensagens garlic estendem o roteamento cebola ao agrupar múltiplos "cravos" criptografados com instruções de entrega independentes. Isso permite flexibilidade de roteamento no nível de mensagem e preenchimento uniforme de tráfego.

#### Session Tags

Dois sistemas criptográficos são suportados para criptografia ponta a ponta:

- **ElGamal/AES+SessionTags (legado):**  
  Usa tags de sessão pré-entregues como nonces de 32 bytes. Agora obsoleto devido à ineficiência.

- **ECIES-X25519-AEAD-Ratchet (atual):**  
  Usa ChaCha20-Poly1305 e PRNGs baseados em HKDF sincronizados para gerar chaves de sessão efêmeras e tags de 8 bytes dinamicamente, reduzindo a sobrecarga de CPU, memória e largura de banda enquanto mantém o sigilo perfeito para frente (forward secrecy).

---

## Future of the Protocol

As principais áreas de pesquisa concentram-se em manter a segurança contra adversários de nível estatal e introduzir proteções pós-quânticas. Dois conceitos de design iniciais — **rotas restritas** e **latência variável** — foram substituídos por desenvolvimentos modernos.

### Restricted Route Operation

Os conceitos originais de roteamento restrito visavam ocultar endereços IP. Esta necessidade foi amplamente mitigada por:

- UPnP para encaminhamento automático de portas  
- Travessia robusta de NAT no SSU2  
- Suporte a IPv6  
- Introdutores cooperativos e perfuração de NAT  
- Conectividade opcional por overlay (ex.: Yggdrasil)

Assim, o I2P moderno alcança os mesmos objetivos de forma mais prática, sem roteamento restrito complexo.

---

## Similar Systems

O I2P integra conceitos de middleware orientado a mensagens, DHTs e mixnets. Sua inovação reside em combinar esses elementos em uma plataforma de anonimato utilizável e auto-organizável.

### Protocolos de Transporte

*[Website](https://www.torproject.org/)*

**Tor** e **I2P** compartilham objetivos mas diferem arquiteturalmente:

- **Tor:** Comutação de circuitos; depende de autoridades de diretório confiáveis. (~10k relays)  
- **I2P:** Comutação de pacotes; rede totalmente distribuída baseada em DHT. (~50k routers)

Os túneis unidirecionais do I2P expõem menos metadados e permitem caminhos de roteamento flexíveis, enquanto o Tor foca no acesso anônimo à **Internet (outproxying)**.   O I2P, em vez disso, suporta **hospedagem anônima dentro da rede**.

### Criptografia

*[Website](https://freenetproject.org/)*

**Freenet** foca-se na publicação e recuperação anônima e persistente de arquivos. **I2P**, em contraste, fornece uma **camada de comunicações em tempo real** para uso interativo (web, chat, torrents). Juntos, os dois sistemas complementam-se — Freenet fornece armazenamento resistente à censura; I2P fornece anonimato no transporte.

### Other Networks

- **Lokinet:** Overlay baseado em IP usando nós de serviço incentivados.  
- **Nym:** Mixnet de próxima geração enfatizando proteção de metadados com tráfego de cobertura em latência mais alta.

---

## Appendix A: Application Layer

O I2P em si apenas gerencia o transporte de mensagens. A funcionalidade da camada de aplicação é implementada externamente através de APIs e bibliotecas.

### Streaming Library {#streaming}

A **biblioteca de streaming** funciona como o análogo TCP do I2P, com um protocolo de janela deslizante e controle de congestionamento ajustado para transporte anônimo de alta latência.

Padrões típicos de requisição/resposta HTTP frequentemente podem ser concluídos em uma única viagem de ida e volta devido a otimizações de agrupamento de mensagens.

### Naming Library and Address Book

*Desenvolvido por: mihi, Ragnarok*   Consulte a página [Nomenclatura e Catálogo de Endereços](/docs/overview/naming).

O sistema de nomenclatura do I2P é **local e descentralizado**, evitando nomes globais no estilo DNS. Cada router mantém um mapeamento local de nomes legíveis por humanos para destinos. Catálogos de endereços opcionais baseados em rede de confiança podem ser compartilhados ou importados de pares confiáveis.

Esta abordagem evita autoridades centralizadas e contorna vulnerabilidades Sybil inerentes a sistemas de nomenclatura globais ou baseados em votação.

### Operação de Rota Restrita

*Desenvolvido por: mihi*

**I2PTunnel** é a principal interface da camada cliente que permite proxy TCP anônimo. Ele suporta:

- **Túneis cliente** (saída para destinos I2P)  
- **Cliente HTTP (eepproxy)** para domínios ".i2p"  
- **Túneis servidor** (entrada do I2P para um serviço local)  
- **Túneis servidor HTTP** (proxy seguro de serviços web)

O outproxying (para a Internet regular) é opcional, implementado por túneis "servidor" operados por voluntários.

### I2PSnark {#i2psnark}

*Desenvolvido por: jrandom, et al — portado de [Snark](http://www.klomp.org/snark/)*

Incluído com I2P, **I2PSnark** é um cliente BitTorrent anônimo multi-torrent com suporte a DHT e UDP, acessível através de uma interface web.

### Tor

*Desenvolvido por: postman, susi23, mastiejaner*

**I2Pmail** fornece email anônimo através de conexões I2PTunnel. **Susimail** é um cliente baseado na web construído especificamente para prevenir vazamentos de informação comuns em clientes de email tradicionais. O serviço [mail.i2p](https://mail.i2p/) possui filtragem de vírus, quotas de [hashcash](https://en.wikipedia.org/wiki/Hashcash) e separação de outproxy para proteção adicional.

---
