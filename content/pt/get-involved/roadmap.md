---
title: "Roteiro de Desenvolvimento do I2P"
description: "Planos de desenvolvimento atuais e marcos históricos para a rede I2P"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**O I2P segue um modelo de desenvolvimento incremental** com lançamentos aproximadamente a cada 13 semanas. Este roteiro cobre lançamentos de Java para desktop e Android em um único caminho de lançamento estável.

**Última Atualização:** Agosto de 2025

</div>

## 🎯 Próximos Lançamentos

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Versão 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Meta: Início de Dezembro de 2025
</div>

- Ratchet final Hybrid PQ MLKEM, habilitar por padrão (prop. 169)
- Jetty 12, requer Java 17+
- Continuar trabalho com PQ (transportes) (prop. 169)
- Suporte de pesquisa I2CP para parâmetros de registro de serviço LS (prop. 167)
- Limitação por túnel
- Subsistema de estatísticas compatível com Prometheus
- Suporte SAM para Datagram 2/3

</div>

---

## 📦 Lançamentos Recentes

### Lançamentos de 2025

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versão 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lançada em 8 de Setembro de 2025</span>

- Suporte a tracking UDP i2psnark (prop. 160)
- Parâmetros de registro de serviço I2CP LS (parcial) (prop. 167)
- API de busca assíncrona I2CP
- Ratchet Beta Hybrid PQ MLKEM (prop. 169)
- Continuar trabalho com PQ (transportes) (prop. 169)
- Parâmetros de largura de banda de construção de túnel (prop. 168) Parte 2 (manuseio)
- Continuar trabalho com limitação por túnel
- Remover código ElGamal de transporte não utilizado
- Remover código antigo de "limitação ativa" SSU2
- Remover suporte antigo de registro de estatísticas
- Limpeza do subsistema de estatísticas/gráficos
- Melhorias e correções no modo oculto

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versão 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lançada em 2 de Junho de 2025</span>

- Mapa Netdb
- Implementar Datagram2, Datagram3 (prop. 163)
- Iniciar trabalho com o parâmetro de registro de serviço LS (prop. 167)
- Iniciar trabalho com PQ (prop. 169)
- Continuar trabalho com limitação por túnel
- Parâmetros de largura de banda de construção de túnel (prop. 168) Parte 1 (envio)
- Usar /dev/random para PRNG por padrão no Linux
- Remover código de renderização LS redundante
- Exibir changelog em HTML
- Reduzir uso de threads do servidor HTTP
- Corrigir inscrição automática de floodfill
- Atualizar Wrapper para 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versão 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lançada em 29 de Março de 2025</span>

- Corrigir bug de corrupção SHA256

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versão 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lançada em 17 de Março de 2025</span>

- Corrigir falha do instalador no Java 21+
- Corrigir bug "loopback"
- Corrigir testes de túnel para túneis de cliente de saída
- Corrigir instalação em caminhos com espaços
- Atualizar contêiner Docker desatualizado e bibliotecas de contêiner
- Bolhas de notificação na console
- Classificação por "mais recente" no SusiDNS
- Usar pool de SHA256 no Noise
- Correções e melhorias no tema escuro da console
- Suporte para .i2p.alt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versão 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lançada em 3 de Fevereiro de 2025</span>

- Melhorias na publicação de RouterInfo
- Melhorar a eficiência do ACK do SSU2
- Melhorar manuseio de mensagens duplicadas no SSU2
- Tempos limite de pesquisa mais rápidos/variáveis
- Melhorias na expiração do LS
- Alterar capacidade NAT simétrica
- Reforçar POST em mais formulários
- Correções no tema escuro do SusiDNS
- Limpezas no teste de largura de banda
- Nova tradução para chinês Gan
- Adicionar opção de interface em curdo
- Nova build Jammy
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 Lançamentos de 2024</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 de Outubro de 2024</span>

- Reduzir uso de threads no servidor HTTP do i2ptunnel
- Túneis UDP genéricos no I2PTunnel
- Proxy do navegador no I2PTunnel
- Migração de website
- Correção para túneis ficando amarelos
- Refatoração da console /netdb

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 de Agosto de 2024</span>

- Corrigir problemas de tamanho de iframe na console
- Converter gráficos para SVG
- Relatório de status de tradução em pacote

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 19 de Julho de 2024</span>

- Reduzir uso de memória netdb
- Remover código SSU1
- Corrigir vazamentos e travamentos de arquivos temporários do i2psnark
- Mais eficiente PEX no i2psnark
- Atualização em JS dos gráficos da console
- Melhoria no render de gráficos
- Busca em JS no Susimail
- Manuseio de mensagens mais eficiente no OBEP
- Mais eficientização nas buscas de destino local do I2CP
- Corrigir problemas de escopo de variáveis JS

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 15 de Maio de 2024</span>

- Corrigir truncamento HTTP
- Publicar capacidade G se NAT simétrica detectada
- Atualização para rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 de Maio de 2024</span>

- Mitigações de DDoS NetDB
- Lista de bloqueio do Tor
- Correções e busca do Susimail
- Continuar remoção de código SSU1
- Atualização para Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 de Abril de 2024</span>

- Melhorias no iframe da console
- Redesenho do limitador de largura de banda do i2psnark
- Arrastar e soltar em Javascript para i2psnark e susimail
- Melhorias no manuseio de erros SSL do i2ptunnel
- Suporte a conexão HTTP persistente no i2ptunnel
- Início da remoção de código SSU1
- Melhorias no manuseio de pedidos de etiquetas de relé SSU2
- Correções de teste de pares no SSU2
- Melhorias no Susimail (carregamento, markdown, suporte a e-mail HTML)
- Ajustes na seleção de pares de túnel
- Atualizar RRD4J para 3.9
- Atualizar gradlew para 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versão 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 18 de Dezembro de 2023</span>

- Gerenciamento de contexto NetDB/NetDB segmentado
- Lidando com capacidades de congestão ao despriorizar roteadores sobrecarregados
- Revitalizar biblioteca auxiliar Android
- Seletor de arquivo torrent local do i2psnark
- Correções no manuseio de pesquisas NetDB
- Desativação do SSU1
- Banir roteadores publicando no futuro
- Correções no SAM
- Correções no susimail
- Correções no UPnP

</div>

---

### Lançamentos 2023-2022

<details>
<summary>Cliqe para expandir lançamentos 2023-2022</summary>

**Versão 2.3.0** — Lançada em 28 de Junho de 2023

- Melhorias na seleção de pares de túnel
- Expiração de lista de bloqueios configurável pelo usuário
- Limitar surtos rápidos de busca da mesma origem
- Corrigir vazamento de informação de detecção de replay
- Correções no NetDB para conjuntos de arrendamento multihomed
- Correções no NetDB para conjuntos de arrendamento recebidos como resposta antes de serem recebidos como armazenamento

**Versão 2.2.1** — Lançada em 12 de Abril de 2023

- Correções de empacotamento

**Versão 2.2.0** — Lançada em 13 de Março de 2023

- Melhorias na seleção de pares de túnel
- Correção de replay em streaming

**Versão 2.1.0** — Lançada em 10 de Janeiro de 2023

- Correções no SSU2
- Correções de congestionamento na construção de túnel
- Correções de teste de pares SSU e detecção de NAT simétrica
- Corrigir conjuntos de arrendamento LS2 criptografados quebrados
- Opção para desabilitar SSU 1 (preliminar)
- Padding compressível (proposta 161)
- Nova aba de status de peers na console
- Adicionar suporte a torsocks ao proxy SOCKS e outras melhorias e correções SOCKS

**Versão 2.0.0** — Lançada em 21 de Novembro de 2022

- Migração de conexão SSU2
- Acks imediatos SSU2
- Habilitar SSU2 por padrão
- Autenticação proxy digest SHA-256 no i2ptunnel
- Atualizar processo de build do Android para usar AGP moderno
- Suporte a configuração automática para navegador I2P em Plataforma Cruzada(Desktop)

**Versão 1.9.0** — Lançada em 22 de Agosto de 2022

- Implementação de teste e relé de pares no SSU2
- Correções no SSU2
- Melhorias SSU MTU/PMTU
- Habilitar SSU2 para uma pequena porção de roteadores
- Adicionar detector de deadlock
- Mais correções de importação de certificados
- Corrigir reinício do DHT no i2psnark após reinício do roteador

**Versão 1.8.0** — Lançada em 23 de Maio de 2022

- Correções e melhorias na família de roteadores
- Correções no soft restart
- Correções e melhorias de desempenho no SSU
- Correções e melhorias no I2PSnark standalone
- Evitar penalidade Sybil para famílias de confiança
- Reduzir tempo limite de resposta na construção de túnel
- Correções no UPnP
- Remover fonte BOB
- Correções na importação de certificados
- Tomcat 9.0.62
- Refatorar para suporte ao SSU2 (proposta 159)
- Implementação inicial do protocolo base do SSU2 (proposta 159)
- Popup de autorização SAM para aplicativos Android
- Melhorar suporte a instalações de diretórios personalizados no i2p.firefox

**Versão 1.7.0** — Lançada em 21 de Fevereiro de 2022

- Remover BOB
- Novo editor de torrent i2psnark
- Correções e melhorias no i2psnark standalone
- Melhorias na confiabilidade do NetDB
- Adicionar mensagens popup na systray
- Melhorias de desempenho no NTCP2
- Remover tunnel de saída quando a primeira hop falha
- Relegar para exploração em resposta de falha repetida na construção de túneis de cliente
- Restaurar restrições de mesmo IP no túnel
- Refatorar suporte UDP do i2ptunnel para portas I2CP
- Continuar trabalho no SSU2, iniciar implementação (proposta 159)
- Criar pacote Debian/Ubuntu do Perfil do Navegador I2P
- Criar Plugin do Perfil do Navegador I2P
- Documentar I2P para aplicativos Android
- Melhorias no i2pcontrol
- Melhorias no suporte a plugins
- Novo plugin local de outproxy
- Suporte a etiqueta de mensagens IRCv3

</details>

---

### Lançamentos 2021

<details>
<summary>Cliqe para expandir lançamentos 2021</summary>

**Versão 1.6.1** — Lançada em 29 de Novembro de 2021

- Acelerar recodificação de roteadores para ECIES
- Melhorias de desempenho no SSU
- Melhorar segurança no teste de pares SSU
- Adicionar seleção de tema ao assistente de nova instalação
- Continuar trabalho no SSU2 (proposta 159)
- Enviar novas mensagens de construção de túnel (proposta 157)
- Incluir ferramenta de configuração automática de navegador no instalador IzPack
- Tornar Plugins Fork-and-Exec Gerenciáveis
- Documentar processos de instalação jpackage
- Completar, documentar Ferramentas de Geração de Plugins Go/Java
- Plugin de Reseed para reseed HTTPS auto-assinado

**Vers
