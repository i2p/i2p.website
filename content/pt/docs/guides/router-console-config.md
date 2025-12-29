---
title: "Guia de Configuração do Console do Router"
description: "Um guia completo para compreender e configurar o Console do Router I2P"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: docs
---

Este guia fornece uma visão geral do Console do Router I2P e suas páginas de configuração. Cada seção explica o que a página faz e para que serve, ajudando você a entender como monitorar e configurar seu router I2P.

## Acessando o Console do Router

O Console do Router I2P é o centro de controle para gerenciar e monitorar o seu router I2P. Por padrão, pode ser acessado através do [Console do Router I2P](http://127.0.0.1:7657/home) assim que o seu router I2P estiver em execução.

![Página Inicial do Console do Router](/images/router-console-home.png)

A página inicial exibe várias seções principais:

- **Aplicações** - Acesso rápido às aplicações integradas do I2P como Email, Torrents, Gestor de Serviços Ocultos e Servidor Web
- **Sites da Comunidade I2P** - Links para recursos importantes da comunidade incluindo fóruns, documentação e websites do projeto
- **Configuração e Ajuda** - Ferramentas para configurar definições de largura de banda, gerir plugins e aceder a recursos de ajuda
- **Informações de Rede e Programador** - Acesso a gráficos, logs, documentação técnica e estatísticas de rede

## Livro de Endereços

**URL:** [Catálogo de Endereços](http://127.0.0.1:7657/dns)

![Router Console Address Book](/images/router-console-address-book.png)

O I2P Address Book funciona de forma similar ao DNS na clearnet, permitindo que você gerencie nomes legíveis para destinos I2P (eepsites). É aqui que você pode visualizar e adicionar endereços I2P ao seu catálogo de endereços pessoal.

O sistema de livro de endereços funciona através de múltiplas camadas:

- **Registros Locais** - Seus catálogos de endereços pessoais que são armazenados apenas no seu router
  - **Catálogo de Endereços Local** - Hosts que você adiciona manualmente ou salva para seu próprio uso
  - **Catálogo de Endereços Privado** - Endereços que você não quer compartilhar com outros; nunca distribuídos publicamente

- **Subscrições** - Fontes remotas de catálogo de endereços (como `http://i2p-projekt.i2p/hosts.txt`) que atualizam automaticamente o catálogo de endereços do seu router com sites I2P conhecidos

- **Router Addressbook** - O resultado consolidado dos seus registros locais e subscrições, pesquisável por todas as aplicações I2P no seu router

- **Published Addressbook** - Compartilhamento público opcional do seu catálogo de endereços para que outros possam usá-lo como fonte de subscrição (útil se você estiver executando um site I2P)

O address book realiza consultas regulares às suas subscrições e mescla o conteúdo no address book do seu router, mantendo o seu arquivo hosts.txt atualizado com a rede I2P.

## Configuração

**URL:** [Configuração Avançada](http://127.0.0.1:7657/configadvanced)

A seção de Configuração fornece acesso a todas as definições do router através de múltiplos separadores especializados.

### Advanced

![Router Console Advanced Configuration](/images/router-console-config-advanced.png)

A página de configuração Avançada fornece acesso a configurações de baixo nível do router que normalmente não são necessárias para operação normal. **A maioria dos usuários não deve modificar estas configurações a menos que compreendam a opção de configuração específica e seu impacto no comportamento do router.**

Características principais:

- **Configuração Floodfill** - Controle se o seu roteador participa como um peer floodfill, que auxilia a rede ao armazenar e distribuir informações da base de dados da rede. Isso pode usar mais recursos do sistema, mas fortalece a rede I2P.

- **Configuração Avançada do I2P** - Acesso direto ao arquivo `router.config`, exibindo todos os parâmetros de configuração avançados, incluindo:
  - Limites de largura de banda e configurações de burst
  - Configurações de transporte (NTCP2, SSU2, portas UDP e chaves)
  - Informações de identificação e versão do router
  - Preferências do console e configurações de atualização

A maioria das opções avançadas de configuração não são expostas na interface do usuário porque raramente são necessárias. Para habilitar a edição dessas configurações, você deve adicionar `routerconsole.advanced=true` ao seu arquivo `router.config` manualmente.

**Aviso:** Modificar incorretamente as configurações avançadas pode afetar negativamente o desempenho ou a conectividade do seu router. Apenas altere essas configurações se souber o que está fazendo.

### Bandwidth

**URL:** [Configuração de Largura de Banda](http://127.0.0.1:7657/config)

![Configuração de Largura de Banda do Console do Router](/images/router-console-config-bandwidth.png)

A página de configuração de Largura de Banda permite que você controle quanta largura de banda o seu router contribui para a rede I2P. O I2P funciona melhor quando você configura suas taxas para corresponder à velocidade da sua conexão de internet.

**Configurações Principais:**

- **KBps In** - Largura de banda máxima de entrada que seu roteador aceitará (velocidade de download)
- **KBps Out** - Largura de banda máxima de saída que seu roteador utilizará (velocidade de upload)
- **Share** - Percentual da sua largura de banda de saída dedicado ao tráfego participante (ajudando a rotear tráfego para outros)

**Notas Importantes:**

- Todos os valores são em **bytes por segundo** (KBps), não bits por segundo
- Quanto mais largura de banda você disponibilizar, mais ajuda a rede e melhora seu próprio anonimato
- A quantidade de compartilhamento upstream (KBps Out) determina sua contribuição geral para a rede
- Se não tiver certeza da velocidade da sua rede, use o **Teste de Largura de Banda** para medi-la
- Maior largura de banda compartilhada melhora tanto seu anonimato quanto ajuda a fortalecer a rede I2P

A página de configuração mostra a transferência de dados mensal estimada com base nas suas configurações, ajudando você a planejar a alocação de largura de banda de acordo com os limites do seu plano de internet.

### Client Configuration

**URL:** [Configuração do Cliente](http://127.0.0.1:7657/configclients)

![Router Console Client Configuration](/images/router-console-config-clients.png)

A página de Configuração do Cliente permite que você controle quais aplicações e serviços I2P são executados na inicialização. É aqui que você pode ativar ou desativar clientes I2P integrados sem desinstalá-los.

**Aviso Importante:** Tenha cuidado ao alterar configurações aqui. O console do router e os túneis de aplicação são necessários para a maioria dos usos do I2P. Apenas usuários avançados devem modificar essas configurações.

**Clientes Disponíveis:**

- **Application tunnels** - O sistema I2PTunnel que gerencia túneis de cliente e servidor (proxy HTTP, IRC, etc.)
- **I2P Router Console** - A interface de administração baseada na web que você está usando atualmente
- **I2P webserver (eepsite)** - Servidor web Jetty integrado para hospedar seu próprio site I2P
- **Open Router Console in web browser at startup** - Abre automaticamente seu navegador na página inicial do console
- **SAM application bridge** - Ponte de API para aplicações de terceiros se conectarem ao I2P

Cada cliente mostra: - **Executar na Inicialização?** - Caixa de seleção para ativar/desativar início automático - **Controle** - Botões Iniciar/Parar para controle imediato - **Classe e argumentos** - Detalhes técnicos sobre como o cliente é iniciado

Alterações na configuração "Executar na Inicialização?" requerem uma reinicialização do router para que tenham efeito. Todas as modificações são salvas em `/var/lib/i2p/i2p-config/clients.config.d/`.

### Avançado

**URL:** [Configuração I2CP](http://127.0.0.1:7657/configi2cp)

![Router Console I2CP Configuration](/images/router-console-config-i2cp.png)

A página de configuração do I2CP (I2P Client Protocol) permite que você configure como aplicações externas se conectam ao seu roteador I2P. O I2CP é o protocolo que as aplicações usam para se comunicar com o router e criar tunnels e enviar/receber dados através do I2P.

**Importante:** As configurações padrão funcionarão para a maioria das pessoas. Quaisquer alterações feitas aqui também devem ser configuradas na aplicação cliente externa. Muitos clientes não suportam SSL ou autorização. **Todas as alterações requerem reinicialização para entrar em vigor.**

**Opções de Configuração:**

- **Configuração da Interface I2CP Externa**
  - **Ativada sem SSL** - Acesso I2CP padrão (padrão e mais compatível)
  - **Ativada com SSL obrigatório** - Apenas conexões I2CP criptografadas
  - **Desativada** - Bloqueia clientes externos de se conectarem via I2CP

- **Interface I2CP** - A interface de rede na qual escutar (padrão: 127.0.0.1 apenas para localhost)
- **Porta I2CP** - O número da porta para conexões I2CP (padrão: 7654)

- **Autorização**
  - **Requerer nome de usuário e senha** - Ativa autenticação para conexões I2CP
  - **Nome de usuário** - Define o nome de usuário necessário para acesso I2CP
  - **Senha** - Define a senha necessária para acesso I2CP

**Nota de Segurança:** Se você está executando aplicativos apenas na mesma máquina que o seu router I2P, mantenha a interface configurada como `127.0.0.1` para prevenir acesso remoto. Altere essas configurações apenas se você precisar permitir que aplicativos I2P de outros dispositivos se conectem ao seu router.

### Largura de Banda

**URL:** [Configuração de Rede](http://127.0.0.1:7657/confignet)

![Router Console Network Configuration](/images/router-console-config-network.png)

A página de Configuração de Rede permite configurar como o seu router I2P se conecta à internet, incluindo detecção de endereço IP, preferências IPv4/IPv6 e configurações de porta para os transportes UDP e TCP.

**Endereço IP Externamente Acessível:**

- **Usar todos os métodos de detecção automática** - Detecta automaticamente seu IP público usando múltiplos métodos (recomendado)
- **Desativar detecção de endereço IP via UPnP** - Impede o uso de UPnP para descobrir seu IP
- **Ignorar endereço IP da interface local** - Não usar o IP da sua rede local
- **Usar apenas detecção de endereço IP via SSU** - Usar apenas o transporte SSU2 para detecção de IP
- **Modo oculto - não publicar IP** - Impede a participação no tráfego da rede (reduz o anonimato)
- **Especificar hostname ou IP** - Definir manualmente seu IP público ou hostname

**Configuração IPv4:**

- **Desabilitar entrada (Atrás de firewall)** - Marque esta opção se você estiver atrás de um firewall, rede doméstica, ISP, DS-Lite ou NAT de grau de operadora que bloqueia conexões de entrada

**Configuração IPv6:**

- **Preferir IPv4 em vez de IPv6** - Prioriza conexões IPv4
- **Preferir IPv6 em vez de IPv4** - Prioriza conexões IPv6 (padrão para redes dual-stack)
- **Habilitar IPv6** - Permite conexões IPv6
- **Desabilitar IPv6** - Desabilita toda conectividade IPv6
- **Usar apenas IPv6 (desabilitar IPv4)** - Modo experimental apenas IPv6
- **Desabilitar entrada (Com firewall)** - Marque se seu IPv6 estiver bloqueado por firewall

**Ação Quando o IP Muda:**

- **Modo laptop** - Funcionalidade experimental que altera a identidade do router e a porta UDP quando o seu IP muda para maior anonimato

**Configuração UDP:**

- **Especificar Porta** - Define uma porta UDP específica para o transporte SSU2 (deve ser aberta no seu firewall)
- **Desativar completamente** - Selecione apenas se estiver atrás de um firewall que bloqueia todo o tráfego UDP de saída

**Configuração TCP:**

- **Especificar Porta** - Define uma porta TCP específica para o transporte NTCP2 (deve estar aberta no seu firewall)
- **Usar a mesma porta configurada para UDP** - Simplifica a configuração ao usar uma porta para ambos os transportes
- **Usar endereço IP auto-detectado** - Detecta automaticamente o seu IP público (mostra "currently unknown" se ainda não foi detectado ou está bloqueado por firewall)
- **Sempre usar endereço IP auto-detectado (Not firewalled)** - Melhor opção para routers com acesso direto à internet
- **Desabilitar entrada (Firewalled)** - Marque se as conexões TCP estão bloqueadas pelo seu firewall
- **Desabilitar completamente** - Selecione apenas se estiver atrás de um firewall que limita ou bloqueia TCP de saída
- **Especificar hostname ou IP** - Configure manualmente o seu endereço acessível externamente

**Importante:** Alterações nas configurações de rede podem exigir uma reinicialização do router para terem efeito completo. A configuração adequada de encaminhamento de portas melhora significativamente o desempenho do seu router e ajuda a rede I2P.

### Configuração do Cliente

**URL:** [Configuração de Pares](http://127.0.0.1:7657/configpeer)

![Router Console Peer Configuration](/images/router-console-config-peer.png)

A página de Configuração de Peers fornece controles manuais para gerenciar peers individuais na rede I2P. Este é um recurso avançado normalmente usado apenas para solucionar problemas com peers problemáticos.

**Controles Manuais de Peers:**

- **Hash do Router** - Insira o hash do router em base64 de 44 caracteres do peer que deseja gerenciar

**Banir / Desbanir Manualmente um Peer:**

Banir um peer impede que ele participe de quaisquer túneis que você criar. Esta ação: - Impede que o peer seja usado em seus túneis de cliente ou exploratórios - Entra em vigor imediatamente sem exigir reinicialização - Persiste até que você desbanique manualmente o peer ou reinicie seu router - **Banir peer até reiniciar** - Bloqueia temporariamente o peer - **Desbanir peer** - Remove o banimento de um peer previamente bloqueado

**Ajustar Bônus de Perfil:**

Os bônus de perfil afetam como os peers são selecionados para participação em túneis. Os bônus podem ser positivos ou negativos: - **Peers rápidos** - Usados para túneis de cliente que exigem alta velocidade - **Peers de alta capacidade** - Usados para alguns túneis exploratórios que exigem roteamento confiável - Os bônus atuais são exibidos na página de perfis

**Configuração:** - **Velocidade** - Ajustar o bônus de velocidade para este peer (0 = neutro) - **Capacidade** - Ajustar o bônus de capacidade para este peer (0 = neutro) - **Ajustar bônus de peers** - Aplicar as configurações de bônus

**Casos de Uso:** - Banir um peer que consistentemente causa problemas de conexão - Excluir temporariamente um peer que você suspeita ser malicioso - Ajustar bônus para despriorizar peers com baixo desempenho - Depurar problemas de construção de túnel excluindo peers específicos

**Nota:** A maioria dos usuários nunca precisará usar este recurso. O router I2P gerencia automaticamente a seleção e criação de perfis de peers com base em métricas de desempenho.

### Configuração I2CP

**URL:** [Configuração de Reseed](http://127.0.0.1:7657/configreseed)

![Configuração de Reseed do Console do Router](/images/router-console-config-reseed.png)

A página de Configuração de Reseed permite que você faça o reseed manual do seu router se o reseed automático falhar. Reseed é o processo de inicialização usado para encontrar outros routers quando você instala o I2P pela primeira vez, ou quando seu router tem poucas referências de routers restantes.

**Quando Usar Reseed Manual:**

1. Se o reseed falhou, você deve primeiro verificar sua conexão de rede
2. Se um firewall está bloqueando suas conexões aos hosts de reseed, você pode ter acesso a um proxy:
   - O proxy pode ser um proxy público remoto, ou pode estar rodando no seu computador (localhost)
   - Para usar um proxy, configure o tipo, host e porta na seção Reseeding Configuration
   - Se você está executando o Tor Browser, faça reseed através dele configurando SOCKS 5, localhost, porta 9150
   - Se você está executando o Tor em linha de comando, faça reseed através dele configurando SOCKS 5, localhost, porta 9050
   - Se você tem alguns peers mas precisa de mais, você pode tentar a opção I2P Outproxy. Deixe o host e a porta em branco. Isso não funcionará para um reseed inicial quando você não tem peers
   - Em seguida, clique em "Save changes and reseed now"
   - As configurações padrão funcionarão para a maioria das pessoas. Altere-as apenas se HTTPS estiver bloqueado por um firewall restritivo e o reseed tiver falhado

3. Se você conhece e confia em alguém que executa o I2P, peça para essa pessoa enviar um arquivo de reseed gerado usando esta página no console do router dela. Depois, use esta página para fazer o reseed com o arquivo que você recebeu. Primeiro, selecione o arquivo abaixo. Em seguida, clique em "Reseed from file"

4. Se você conhece e confia em alguém que publica arquivos de reseed, peça a eles o URL. Em seguida, use esta página para fazer reseed com o URL que você recebeu. Primeiro, insira o URL abaixo. Depois, clique em "Reseed from URL"

5. Consulte [as FAQ](/docs/overview/faq/) para instruções sobre como fazer reseed manualmente

**Opções de Reseed Manual:**

- **Ressincronizar a partir de URL** - Insira uma URL zip ou su3 de uma fonte confiável e clique em "Ressincronizar a partir de URL"
  - O formato su3 é preferível, pois será verificado como assinado por uma fonte confiável
  - O formato zip não é assinado; use um arquivo zip apenas de uma fonte em que você confie

- **Reseed a partir de Arquivo** - Navegue e selecione um arquivo zip ou su3 local, depois clique em "Reseed from file"
  - Você pode encontrar arquivos de reseed em [checki2p.com/reseed](https://checki2p.com/reseed)

- **Criar Arquivo de Reseed** - Gera um novo arquivo zip de reseed que você pode compartilhar para que outros façam reseed manualmente
  - Este arquivo nunca conterá a identidade do seu próprio router ou IP

**Configuração de Reseeding:**

As configurações padrão funcionarão para a maioria das pessoas. Altere-as apenas se HTTPS estiver bloqueado por um firewall restritivo e o reseed tiver falhado.

- **URLs de Reseed** - Lista de URLs HTTPS para servidores de reseed (a lista padrão está integrada e é atualizada regularmente)
- **Configuração de Proxy** - Configure proxy HTTP/HTTPS/SOCKS se você precisar acessar servidores de reseed através de um proxy
- **Redefinir lista de URLs** - Restaurar a lista padrão de servidores de reseed

**Importante:** O resseeding manual só deve ser necessário em casos raros onde o resseeding automático falha repetidamente. A maioria dos usuários nunca precisará usar esta página.

### Configuração de Rede

**URL:** [Configuração de Família de Routers](http://127.0.0.1:7657/configfamily)

![Console do Router Configuração de Família de Routers](/images/router-console-config-family.png)

A página de Configuração de Família de Roteadores permite que você gerencie famílias de roteadores. Roteadores na mesma família compartilham uma chave de família, que os identifica como sendo operados pela mesma pessoa ou organização. Isso impede que múltiplos roteadores que você controla sejam selecionados para o mesmo tunnel, o que reduziria o anonimato.

**O que é uma Família de Roteadores?**

Quando você opera múltiplos roteadores I2P, você deve configurá-los para fazer parte da mesma família. Isso garante: - Seus roteadores não serão usados juntos no mesmo caminho de túnel - Outros usuários mantêm o anonimato adequado quando seus túneis usam seus roteadores - A rede pode distribuir adequadamente a participação nos túneis

**Família Atual:**

A página exibe o nome da família atual do seu router. Se você não faz parte de uma família, este campo estará vazio.

**Exportar Chave da Família:**

- **Exporte a chave secreta da família para ser importada em outros roteadores que você controla**
- Clique em "Export Family Key" para baixar o arquivo de chave da sua família
- Importe esta chave em seus outros roteadores para adicioná-los à mesma família

**Deixar Família de Routers:**

- **Deixar de ser membro da família**
- Clique em "Sair da Família" para remover este roteador de sua família atual
- Esta ação não pode ser desfeita sem reimportar a chave da família

**Considerações Importantes:**

- **Registro Público Necessário:** Para que sua família seja reconhecida em toda a rede, sua chave de família deve ser adicionada à base de código do I2P pela equipe de desenvolvimento. Isso garante que todos os routers da rede saibam sobre sua família.
- **Entre em contato com a equipe do I2P** para registrar sua chave de família se você operar múltiplos routers públicos
- A maioria dos usuários que executam apenas um router nunca precisará usar este recurso
- A configuração de família é usada principalmente por operadores de múltiplos routers públicos ou provedores de infraestrutura

**Casos de Uso:**

- Operar múltiplos roteadores I2P para redundância
- Executar infraestrutura como servidores reseed ou outproxies em múltiplas máquinas
- Gerenciar uma rede de roteadores I2P para uma organização

### Configuração de Peers

**URL:** [Configuração de Túneis](http://127.0.0.1:7657/configtunnels)

![Console do Router - Configuração de Túneis](/images/router-console-config-tunnels.png)

A página de Configuração de Túneis permite ajustar as configurações padrão de túneis tanto para túneis exploratórios (usados para comunicação do router) quanto para túneis de cliente (usados por aplicações). **As configurações padrão funcionam para a maioria das pessoas e só devem ser alteradas se você entender as compensações.**

**Avisos Importantes:**

⚠️ **Compensação entre Anonimato e Desempenho:** Existe uma compensação fundamental entre anonimato e desempenho. Tunnels com mais de 3 hops (por exemplo, 2 hops + 0-2 hops, 3 hops + 0-1 hops, 3 hops + 0-2 hops), ou uma quantidade alta + quantidade de backup, podem reduzir severamente o desempenho ou a confiabilidade. Pode resultar em alto uso de CPU e/ou alta largura de banda de saída. Altere essas configurações com cuidado e ajuste-as se tiver problemas.

⚠️ **Persistência:** As alterações nas configurações de túneis exploratórios são armazenadas no arquivo router.config. As alterações em túneis de cliente são temporárias e não são salvas. Para fazer alterações permanentes em túneis de cliente, consulte a [página I2PTunnel](/docs/api/i2ptunnel).

**Túneis Exploratórios:**

Túneis exploratórios são usados pelo seu router para comunicar com a base de dados de rede e participar na rede I2P.

Opções de configuração para Inbound e Outbound: - **Length** - Número de saltos no tunnel (padrão: 2-3 saltos) - **Randomization** - Variação aleatória no comprimento do tunnel (padrão: 0-1 saltos) - **Quantity** - Número de tunnels ativos (padrão: 2 tunnels) - **Backup quantity** - Número de tunnels de backup prontos para ativar (padrão: 0 tunnels)

**Túneis Cliente para Servidor Web I2P:**

Estas configurações controlam os túneis para o servidor web I2P integrado (eepsite).

⚠️ **AVISO DE ANONIMATO** - As configurações incluem túneis de 1 salto. ⚠️ **AVISO DE DESEMPENHO** - As configurações incluem grandes quantidades de túneis.

Opções de configuração para Entrada e Saída: - **Comprimento** - Comprimento do tunnel (padrão: 1 hop para servidor web) - **Aleatorização** - Variação aleatória no comprimento do tunnel - **Quantidade** - Número de tunnels ativos - **Quantidade de backup** - Número de tunnels de backup

**Túneis de Cliente para Clientes Compartilhados:**

Estas configurações aplicam-se a aplicações cliente partilhadas (proxy HTTP, IRC, etc.).

Opções de configuração para Inbound e Outbound: - **Length** - Comprimento do túnel (padrão: 3 saltos) - **Randomization** - Variação aleatória no comprimento do túnel - **Quantity** - Número de túneis ativos - **Backup quantity** - Número de túneis de backup

**Compreendendo os Parâmetros de Tunnel:**

- **Comprimento:** Túneis mais longos fornecem maior anonimato, mas reduzem o desempenho e a confiabilidade
- **Aleatorização:** Adiciona imprevisibilidade aos caminhos dos túneis, melhorando a segurança
- **Quantidade:** Mais túneis melhoram a confiabilidade e a distribuição de carga, mas aumentam o uso de recursos
- **Quantidade de backup:** Túneis pré-construídos prontos para substituir túneis com falha, melhorando a resiliência

**Melhores Práticas:**

- Mantenha as configurações padrão a menos que tenha necessidades específicas
- Apenas aumente o comprimento do tunnel se o anonimato for crítico e você puder aceitar desempenho mais lento
- Aumente a quantidade/backup apenas se estiver enfrentando falhas frequentes de tunnel
- Monitore o desempenho do router após fazer alterações
- Clique em "Save changes" para aplicar as modificações

### Configuração de Reseed

**URL:** [Configuração da Interface](http://127.0.0.1:7657/configui)

![Interface de Configuração do Console do Router](/images/router-console-config-ui.png)

A página de Configuração da UI permite que você personalize a aparência e acessibilidade do console do seu router, incluindo seleção de tema, preferências de idioma e proteção por senha.

**Tema da Console do Router:**

Escolha entre temas escuros e claros para a interface do console do router:
- **Escuro** - Tema de modo escuro (mais confortável para os olhos em ambientes com pouca luz)
- **Claro** - Tema de modo claro (aparência tradicional)

Opções adicionais de tema: - **Definir tema universalmente em todos os aplicativos** - Aplicar o tema selecionado a todos os aplicativos I2P, não apenas ao console do router - **Forçar o uso do console móvel** - Usar a interface otimizada para dispositivos móveis mesmo em navegadores desktop - **Incorporar aplicativos de Email e Torrent no console** - Integrar o Susimail e o I2PSnark diretamente na interface do console em vez de abri-los em abas separadas

**Idioma do Console do Router:**

Selecione seu idioma preferido para a interface do console do router no menu suspenso. O I2P suporta muitos idiomas incluindo inglês, alemão, francês, espanhol, russo, chinês, japonês e outros.

**Contribuições de tradução são bem-vindas:** Se você notar traduções incompletas ou incorretas, pode ajudar a melhorar o I2P contribuindo para o projeto de tradução. Entre em contato com os desenvolvedores em #i2p-dev no IRC ou verifique o relatório de status da tradução (link disponível na página).

**Senha do Console do Router:**

Adicione autenticação de nome de usuário e senha para proteger o acesso ao seu console do router:

- **Nome de usuário** - Insira o nome de usuário para acesso ao console
- **Senha** - Insira a senha para acesso ao console
- **Adicionar usuário** - Crie um novo usuário com as credenciais especificadas
- **Excluir selecionados** - Remova contas de usuário existentes

**Por que Adicionar uma Senha?**

- Impede o acesso local não autorizado ao seu console do router
- Essencial se várias pessoas usam o seu computador
- Recomendado se o seu console do router está acessível na sua rede local
- Protege a sua configuração I2P e definições de privacidade contra adulteração

**Nota de Segurança:** A proteção por senha afeta apenas o acesso à interface web do console do router em [I2P Router Console](http://127.0.0.1:7657). Ela não criptografa o tráfego I2P nem impede que aplicações utilizem o I2P. Se você é o único usuário do seu computador e o console do router escuta apenas em localhost (padrão), uma senha pode não ser necessária.

### Configuração de Família de Routers

**URL:** [Configuração de WebApp](http://127.0.0.1:7657/configwebapps)

![Configuração da WebApp do Console do Router](/images/router-console-config-webapps.png)

A página de Configuração do WebApp permite gerenciar as aplicações web Java que são executadas dentro do seu roteador I2P. Essas aplicações são iniciadas pelo cliente webConsole e executam na mesma JVM que o roteador, fornecendo funcionalidade integrada acessível através do console do roteador.

**O que são WebApps?**

WebApps são aplicações baseadas em Java que podem ser: - **Aplicações completas** (ex: I2PSnark para torrents) - **Interfaces front-end para outros clientes** que devem ser habilitados separadamente (ex: Susidns, I2PTunnel) - **Aplicações web sem interface web** (ex: address book)

**Notas Importantes:**

- Uma webapp pode ser completamente desativada, ou pode apenas ser desativada de execução na inicialização
- Remover um arquivo war do diretório webapps desativa a webapp completamente
- No entanto, o arquivo .war e o diretório da webapp reaparecerão quando você atualizar seu router para uma versão mais recente
- **Para desativar permanentemente uma webapp:** Desative-a aqui, que é o método preferido

**WebApps Disponíveis:**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Controles:**

Para cada webapp: - **Executar na Inicialização?** - Caixa de seleção para ativar/desativar a inicialização automática - **Controle** - Botões Iniciar/Parar para controle imediato   - **Parar** - Para a webapp atualmente em execução   - **Iniciar** - Inicia uma webapp parada

**Botões de Configuração:**

- **Cancelar** - Descartar alterações e retornar à página anterior
- **Salvar Configuração do WebApp** - Salvar suas alterações e aplicá-las

**Casos de Uso:**

- Pare o I2PSnark se você não usa torrents para economizar recursos
- Desabilite o jsonrpc se você não precisa de acesso à API
- Pare o Susimail se você usa um cliente de email externo
- Pare temporariamente webapps para liberar memória ou solucionar problemas

**Dica de Desempenho:** Desabilitar webapps não utilizadas pode reduzir o uso de memória e melhorar o desempenho do router, especialmente em sistemas com recursos limitados.

## Help

**URL:** [Ajuda](http://127.0.0.1:7657/help)

A página de Ajuda fornece documentação abrangente e recursos para ajudá-lo a entender e usar o I2P de forma eficaz. Ela serve como um centro central para solução de problemas, aprendizado e obtenção de suporte.

**O Que Você Encontrará:**

- **Guia de Início Rápido** - Informações essenciais para novos usuários começarem a usar o I2P
- **Perguntas Frequentes (FAQ)** - Respostas para questões comuns sobre instalação, configuração e uso do I2P
- **Solução de Problemas** - Soluções para problemas comuns e questões de conectividade
- **Documentação Técnica** - Informações detalhadas sobre protocolos, arquitetura e especificações do I2P
- **Guias de Aplicações** - Instruções para usar aplicações I2P como torrents, email e serviços ocultos
- **Informações sobre a Rede** - Compreendendo como o I2P funciona e o que o torna seguro
- **Recursos de Suporte** - Links para fóruns, canais IRC e suporte da comunidade

**Obtendo Ajuda:**

Se você está enfrentando problemas com o I2P: 1. Consulte o FAQ para perguntas e respostas comuns 2. Revise a seção de solução de problemas para seu problema específico 3. Visite o fórum I2P em [i2pforum.i2p](http://i2pforum.i2p) ou [i2pforum.net](https://i2pforum.net) 4. Entre no canal IRC #i2p para suporte da comunidade em tempo real 5. Pesquise a documentação para informações técnicas detalhadas

**Dica:** A página de ajuda está sempre acessível pela barra lateral do console do router, facilitando encontrar assistência sempre que precisar.

## Performance Graphs

**URL:** [Gráficos de Desempenho](http://127.0.0.1:7657/graphs)

![Gráficos de Desempenho do Console do Router](/images/router-console-graphs.png)

A página de Gráficos de Desempenho fornece monitoramento visual em tempo real do desempenho do seu router I2P e da atividade de rede. Esses gráficos ajudam você a entender o uso de largura de banda, conexões de peers, consumo de memória e a saúde geral do router.

**Gráficos Disponíveis:**

- **Uso de Largura de Banda**
  - **Taxa de envio de baixo nível (bytes/seg)** - Taxa de tráfego de saída
  - **Taxa de recebimento de baixo nível (bytes/seg)** - Taxa de tráfego de entrada
  - Mostra a utilização de largura de banda atual, média e máxima
  - Ajuda a monitorar se você está se aproximando dos seus limites de largura de banda configurados

- **Pares Ativos**
  - **router.activePeers com média de 60 seg** - Número de pares com os quais você está ativamente se comunicando
  - Mostra a saúde da sua conectividade de rede
  - Mais pares ativos geralmente significa melhor construção de túneis e participação na rede

- **Uso de Memória do Router**
  - **router.memoryUsed média de 60 seg** - Consumo de memória da JVM
  - Mostra o uso de memória atual, médio e máximo em MB
  - Útil para identificar vazamentos de memória ou determinar se você precisa aumentar o tamanho do heap do Java

**Configurar Exibição de Gráfico:**

Personalize como os gráficos são exibidos e atualizados:

- **Tamanho do gráfico** - Define largura (padrão: 400 pixels) e altura (padrão: 100 pixels)
- **Período de exibição** - Intervalo de tempo a ser exibido (padrão: 60 minutos)
- **Intervalo de atualização** - Frequência de atualização dos gráficos (padrão: 5 minutos)
- **Tipo de gráfico** - Escolha entre exibição de Médias ou Eventos
- **Ocultar legenda** - Remove a legenda dos gráficos para economizar espaço
- **UTC** - Usa horário UTC em vez do horário local nos gráficos
- **Persistência** - Armazena dados do gráfico em disco para análise histórica

**Opções Avançadas:**

Clique em **[Select Stats]** para escolher quais estatísticas exibir no gráfico: - Métricas de túnel (taxa de sucesso de construção, contagem de túneis, etc.) - Estatísticas da base de dados de rede - Estatísticas de transporte (NTCP2, SSU2) - Desempenho de túneis de cliente - E muitas outras métricas detalhadas

**Casos de Uso:**

- Monitore a largura de banda para garantir que você não está excedendo os limites configurados
- Verifique a conectividade com peers ao solucionar problemas de rede
- Acompanhe o uso de memória para otimizar as configurações de heap do Java
- Identifique padrões de desempenho ao longo do tempo
- Diagnostique problemas de construção de túneis correlacionando os gráficos

**Dica:** Clique em "Salvar configurações e redesenhar gráficos" após fazer alterações para aplicar sua configuração. Os gráficos serão atualizados automaticamente com base na sua configuração de intervalo de atualização.
