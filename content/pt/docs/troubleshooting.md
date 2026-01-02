---
title: "Guia de Solução de Problemas do I2P Router"
description: "Guia abrangente de solução de problemas para problemas comuns do I2P router, incluindo problemas de conectividade, desempenho e configuração"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Os routers do I2P falham mais comumente devido a **problemas de redirecionamento de portas**, **alocação de largura de banda insuficiente** e **tempo de bootstrap (inicialização da rede) inadequado**. Esses três fatores respondem por mais de 70% dos problemas relatados. O router requer pelo menos **10-15 minutos** após a inicialização para se integrar completamente à rede, **largura de banda mínima de 128 KB/sec** (256 KB/sec recomendado), e **redirecionamento de portas UDP/TCP** adequado para alcançar status não bloqueado por firewall. Usuários novos frequentemente esperam conectividade imediata e reiniciam prematuramente, o que reinicia o progresso de integração e cria um ciclo frustrante. Este guia fornece soluções detalhadas para todos os principais problemas do I2P que afetam as versões 2.10.0 e posteriores.

A arquitetura de anonimato do I2P intrinsecamente sacrifica velocidade em favor da privacidade por meio de tunnel criptografado de múltiplos saltos. Compreender esse design fundamental ajuda os usuários a estabelecer expectativas realistas e a solucionar problemas de forma eficaz, em vez de confundir comportamento normal com problemas.

## Router não inicia ou falha imediatamente

As falhas de inicialização mais comuns geralmente decorrem de **conflitos de portas**, **incompatibilidade de versão do Java** ou **arquivos de configuração corrompidos**. Verifique se outra instância do I2P já está em execução antes de investigar problemas mais profundos.

**Verifique se não há processos em conflito:**

Linux: `ps aux | grep i2p` ou `netstat -tulpn | grep 7657`

Windows: Gerenciador de Tarefas → Detalhes → procure por java.exe com i2p na linha de comando

macOS: Monitor de Atividade → pesquise por "i2p"

Se existir um processo zumbi, finalize-o: `pkill -9 -f i2p` (Linux/Mac) ou `taskkill /F /IM javaw.exe` (Windows)

**Verifique a compatibilidade da versão do Java:**

I2P 2.10.0+ requer **Java 8 mínimo**, com Java 11 ou posterior recomendado. Verifique se sua instalação mostra "mixed mode" (não "interpreted mode"):

```bash
java -version
```
Deve exibir: OpenJDK ou Oracle Java, versão 8+, "mixed mode"

**Evite:** GNU GCJ, implementações desatualizadas do Java, modos somente interpretados

**Conflitos comuns de portas** ocorrem quando vários serviços competem pelas portas padrão do I2P. O console do router (7657), I2CP (7654), SAM (7656) e o proxy HTTP (4444) devem estar disponíveis. Verifique se há conflitos: `netstat -ano | findstr "7657 4444 7654"` (Windows) ou `lsof -i :7657,4444,7654` (Linux/Mac).

**Corrupção do arquivo de configuração** se manifesta como falhas imediatas com erros de análise nos logs. Router.config exige **codificação UTF-8 sem BOM**, usa `=` como separador (não `:`) e proíbe certos caracteres especiais. Faça backup e depois examine: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Para redefinir a configuração preservando a identidade: Pare o I2P, faça backup de router.keys e do diretório keyData, apague router.config, reinicie. O router regenera a configuração padrão.

**Alocação de heap do Java muito baixa** causa falhas por OutOfMemoryError. Edite o arquivo wrapper.config e aumente `wrapper.java.maxmemory` do padrão 128 ou 256 para **mínimo 512** (1024 para routers de alta largura de banda). Isso exige um desligamento completo, aguardar 11 minutos e então reiniciar - clicar em "Restart" no console não aplicará a alteração.

## Resolvendo o status "Network: Firewalled"

O estado de bloqueio por firewall significa que o router não consegue receber conexões de entrada diretas, obrigando a depender de introducers (pares introdutores). Embora o router funcione nesse estado, **o desempenho se degrada significativamente** e a contribuição para a rede permanece mínima. Alcançar o estado sem bloqueio por firewall requer configurar corretamente o redirecionamento de portas.

**O router seleciona aleatoriamente uma porta** entre 9000-31000 para comunicações. Encontre sua porta em http://127.0.0.1:7657/confignet - procure por "UDP Port" e "TCP Port" (normalmente o mesmo número). Você deve encaminhar **tanto UDP quanto TCP** para obter desempenho ideal, embora apenas o UDP permita a funcionalidade básica.

**Ativar o redirecionamento automático de portas via UPnP** (método mais simples):

1. Acesse http://127.0.0.1:7657/confignet
2. Marque "Enable UPnP"
3. Salve as alterações e reinicie o router
4. Aguarde 5-10 minutos e verifique se o status muda de "Network: Firewalled" para "Network: OK"

O UPnP requer suporte do router (ativado por padrão na maioria dos routers de consumo fabricados após 2010) e uma configuração de rede adequada.

**Redirecionamento manual de portas** (necessário quando o UPnP falha):

1. Anote sua porta do I2P em http://127.0.0.1:7657/confignet (por exemplo, 22648)
2. Encontre seu endereço IP local: `ipconfig` (Windows), `ip addr` (Linux), Preferências do Sistema → Rede (macOS)
3. Acesse a interface de administração do seu router (normalmente 192.168.1.1 ou 192.168.0.1)
4. Navegue até Redirecionamento de Portas (pode estar em Avançado, NAT ou Servidores Virtuais)
5. Crie duas regras:
   - Porta Externa: [sua porta do I2P] → IP Interno: [seu computador] → Porta Interna: [mesma] → Protocolo: **UDP**
   - Porta Externa: [sua porta do I2P] → IP Interno: [seu computador] → Porta Interna: [mesma] → Protocolo: **TCP**
6. Salve as configurações e reinicie seu router se necessário

**Verifique o redirecionamento de portas** usando verificadores online após a configuração. Se a detecção falhar, verifique as configurações do firewall - tanto o firewall do sistema quanto qualquer firewall do antivírus devem permitir a porta do I2P.

**Alternativa "Hidden mode"** para redes restritivas onde o redirecionamento de portas é impossível: Ative em http://127.0.0.1:7657/confignet → marque "Hidden mode". O router permanece atrás de firewall, mas otimiza-se para esse estado usando exclusivamente SSU introducers (pares intermediários do SSU). O desempenho será mais lento, porém funcional.

## Router travado nos estados "Iniciando" ou "Testando"

Esses estados transitórios durante a inicialização normalmente se resolvem em **10-15 minutos para novas instalações** ou **3-5 minutos para routers estabelecidos**. Intervenções prematuras frequentemente pioram os problemas.

**"Network: Testing"** indica que o router está verificando a capacidade de ser alcançado por meio de vários tipos de conexão (direta, introducers (nós introdutores), várias versões de protocolo). Isso é **normal nos primeiros 5-10 minutos** após a inicialização. O router testa vários cenários para determinar a configuração ideal.

**"Rejecting tunnels: starting up"** aparece durante a inicialização enquanto o router não tiver informações suficientes sobre pares. O router não participará do tráfego de retransmissão até estar adequadamente integrado. Esta mensagem deve desaparecer após 10-20 minutos, assim que o netDb estiver populado com mais de 50 routers.

**O desvio do relógio compromete os testes de alcançabilidade.** I2P exige que o horário do sistema esteja dentro de **±60 segundos** do horário da rede. Uma diferença superior a 90 segundos causa rejeição automática da conexão. Sincronize o relógio do sistema:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Painel de Controle → Data e Hora → Hora da Internet → Atualizar agora → Ativar sincronização automática

macOS: Preferências do Sistema → Data e Hora → Ativar "Definir data e hora automaticamente"

Após corrigir o desvio de relógio, reinicie o I2P completamente para uma integração adequada.

**Alocação de largura de banda insuficiente** impede testes bem-sucedidos. O router precisa de capacidade adequada para construir tunnels de teste. Configure em http://127.0.0.1:7657/config:

- **Mínimo viável:** Entrada 96 KB/sec, Saída 64 KB/sec
- **Padrão recomendado:** Entrada 256 KB/sec, Saída 128 KB/sec  
- **Desempenho ideal:** Entrada 512+ KB/sec, Saída 256+ KB/sec
- **Percentual de compartilhamento:** 80% (permite ao router contribuir com largura de banda para a rede)

Uma largura de banda mais baixa pode funcionar, mas prolonga o tempo de integração de minutos para horas.

**netDb corrompido** devido a encerramento incorreto ou erros de disco causa loops de teste intermináveis. O router não consegue concluir os testes sem dados de pares válidos:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: Apague o conteúdo de `%APPDATA%\I2P\netDb\` ou `%LOCALAPPDATA%\I2P\netDb\`

**Firewall bloqueando o reseed (obtenção inicial de pares)** impede a obtenção de pares iniciais. Durante a inicialização, o I2P obtém informações do router em servidores de reseed via HTTPS. Firewalls corporativos ou de provedores (ISP) podem bloquear essas conexões. Configure o proxy de reseed em http://127.0.0.1:7657/configreseed se estiver operando por trás de redes restritivas.

## Velocidades lentas, timeouts (tempo esgotado) e falhas na construção de tunnel

A arquitetura do I2P produz inerentemente **velocidades 3-10x mais lentas do que a clearnet (internet aberta)** devido à criptografia de múltiplos saltos, à sobrecarga de pacotes e à imprevisibilidade das rotas. O estabelecimento de um tunnel percorre múltiplos routers, cada um adicionando latência. Entender isso evita confundir o comportamento normal com problemas.

**Expectativas típicas de desempenho:**

- Navegação na web em sites .i2p: tempos de carregamento de página de 10-30 segundos inicialmente, mais rápido após o estabelecimento do tunnel
- Torrenting via I2PSnark: 10-100 KB/s por torrent, dependendo dos semeadores e das condições da rede  
- Downloads de arquivos grandes: Requer paciência - arquivos de megabytes podem levar minutos; de gigabytes, horas
- A primeira conexão é a mais lenta: a construção do tunnel leva 30-90 segundos; conexões subsequentes usam tunnels existentes

**Taxa de sucesso na construção de Tunnel** indica a saúde da rede. Verifique em http://127.0.0.1:7657/tunnels:

- **Acima de 60%:** Funcionamento normal e saudável
- **40-60%:** Marginal, considere aumentar a largura de banda ou reduzir a carga
- **Abaixo de 40%:** Problemático - indica largura de banda insuficiente, problemas de rede ou seleção de pares deficiente

**Aumente a alocação de largura de banda** como primeira otimização. A maior parte do desempenho lento decorre de escassez de largura de banda. Em http://127.0.0.1:7657/config, aumente os limites incrementalmente e monitore os gráficos em http://127.0.0.1:7657/graphs.

**Para DSL/Cabo (conexões de 1-10 Mbps):** - Entrada: 400 KB/sec - Saída: 200 KB/sec - Compartilhamento: 80% - Memória: 384 MB (edite wrapper.config)

**Para alta velocidade (conexões de 10-100+ Mbps):** - Entrada: 1500 KB/sec   - Saída: 1000 KB/sec - Compartilhamento: 80-100% - Memória: 512-1024 MB - Considere: aumentar o número de tunnels participantes para 2000-5000 em http://127.0.0.1:7657/configadvanced

**Otimize a configuração do tunnel** para melhor desempenho. Acesse as configurações específicas de tunnel em http://127.0.0.1:7657/i2ptunnel e edite cada tunnel:

- **Quantidade de tunnel:** Aumente de 2 para 3-4 (mais caminhos disponíveis)
- **Quantidade de backup:** Defina para 1-2 (failover (comutação por falha) rápido se o tunnel falhar)
- **Comprimento do tunnel:** O padrão de 3 saltos oferece bom equilíbrio; reduzir para 2 melhora a velocidade, mas diminui o anonimato

**Biblioteca nativa de criptografia (jbigi)** oferece desempenho 5-10x melhor do que a criptografia em Java puro. Verifique se foi carregada em http://127.0.0.1:7657/logs - procure por "jbigi loaded successfully" ou "Using native CPUID implementation". Se ausente:

Linux: Normalmente é detectado automaticamente e carregado a partir de ~/.i2p/jbigi-*.so Windows: Verifique se há jbigi.dll no diretório de instalação do I2P Se ausente: Instale as ferramentas de compilação e compile a partir do código-fonte, ou faça download de binários pré-compilados dos repositórios oficiais

**Mantenha o router em execução continuamente.** Cada reinício redefine a integração, exigindo 30-60 minutos para reconstruir a rede de tunnel e os relacionamentos com pares. Routers estáveis com alto tempo de atividade são preferidos para a construção de tunnel, criando um feedback positivo para o desempenho.

## Alto consumo de CPU e memória

Uso excessivo de recursos normalmente indica **alocação de memória inadequada**, **ausência de bibliotecas nativas de criptografia** ou **compromisso excessivo com a participação na rede**. Routers bem configurados devem consumir 10–30% de CPU durante o uso ativo e manter o uso de memória estável abaixo de 80% do heap alocado.

**Problemas de memória manifestam-se como:** - Gráficos de memória com topo plano (fixados no máximo) - Coleta de lixo frequente (padrão em dente de serra com quedas acentuadas) - OutOfMemoryError nos logs - Router ficando sem resposta sob carga - Desligamento automático devido ao esgotamento de recursos

**Aumente a alocação de heap do Java** no wrapper.config (requer encerramento completo):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Crítico:** Após editar o wrapper.config, você **deve encerrar completamente** (não reiniciar), aguardar 11 minutos para uma finalização limpa e então iniciar do zero. O botão "Restart" do console do Router não recarrega as configurações do wrapper.

**A otimização da CPU requer uma biblioteca de criptografia nativa.** Operações de BigInteger em Java puro consomem 10-20x mais CPU do que implementações nativas. Verifique o status do jbigi em http://127.0.0.1:7657/logs durante a inicialização. Sem o jbigi, a CPU terá picos de 50-100% durante a construção de tunnel e operações de criptografia.

**Reduza a carga de tunnels participantes** se o router estiver sobrecarregado:

1. Acesse http://127.0.0.1:7657/configadvanced
2. Defina `router.maxParticipatingTunnels=1000` (padrão 8000)
3. Reduza o percentual de compartilhamento em http://127.0.0.1:7657/config de 80% para 50%
4. Desative o modo floodfill (nó que mantém e distribui a netDb) se estiver ativado: `router.floodfillParticipant=false`

**Limite a largura de banda do I2PSnark e o número de torrents simultâneos.** O uso de torrents consome muitos recursos. Em http://127.0.0.1:7657/i2psnark:

- Limite o número de torrents ativos a no máximo 3-5
- Defina "Up BW Limit" e "Down BW Limit" para valores razoáveis (50-100 KB/sec cada)
- Pare os torrents quando não forem necessários
- Evite semear dezenas de torrents simultaneamente

**Monitore o uso de recursos** por meio de gráficos integrados em http://127.0.0.1:7657/graphs. A memória deve mostrar folga, não um topo achatado. Picos de CPU durante a construção de tunnel são normais; CPU alta sustentada indica problemas de configuração.

**Para sistemas com recursos severamente limitados** (Raspberry Pi, hardware antigo), considere o **i2pd** (implementação em C++) como alternativa. O i2pd requer ~130 MB de RAM contra 350+ MB do Java I2P e usa ~7% de CPU contra 70% sob cargas semelhantes. Observe que o i2pd não inclui aplicativos integrados e requer ferramentas externas.

## Problemas com torrents no I2PSnark

A integração do I2PSnark com a arquitetura do router I2P exige compreender que **o uso de torrents depende inteiramente da saúde dos router tunnels**. Os torrents não começarão até que o router alcance integração adequada com 10+ pares ativos e tunnels em funcionamento.

**Torrents travados em 0% geralmente indicam:**

1. **Router não totalmente integrado:** Aguarde 10-15 minutos após a inicialização do I2P antes de esperar atividade de torrent
2. **DHT desativado:** Ative em http://127.0.0.1:7657/i2psnark → Configuration → marque "Enable DHT" (habilitado por padrão desde a versão 0.9.2)
3. **Rastreadores inválidos ou inativos:** Torrents do I2P exigem rastreadores específicos do I2P - rastreadores da clearnet não funcionarão
4. **Configuração de tunnel insuficiente:** Aumente os tunnels em I2PSnark Configuration → Tunnels section

**Configure os tunnels do I2PSnark para melhor desempenho:**

- Tunnels de entrada: 3-5 (padrão: 2 no Java I2P, 5 no i2pd)
- Tunnels de saída: 3-5  
- Comprimento do tunnel: 3 saltos (reduza para 2 para maior velocidade, menos anonimato)
- Quantidade de tunnels: 3 (fornece desempenho consistente)

**Trackers de torrent essenciais do I2P** para incluir: - tracker2.postman.i2p (principal, mais confiável) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Remova quaisquer rastreadores clearnet (internet pública; não-.i2p) - eles não têm utilidade e geram tentativas de conexão que excedem o tempo limite.

**"Torrent not registered" erros** ocorrem quando a comunicação com o tracker falha. Clique com o botão direito no torrent → "Start" para forçar um novo anúncio. Se persistir, verifique a acessibilidade do tracker acessando http://tracker2.postman.i2p em um navegador configurado para o I2P. Trackers inativos devem ser substituídos por alternativas funcionais.

**Nenhum par se conectando** apesar do sucesso do tracker (rastreador) sugere: - Router bloqueado por firewall (melhora com redirecionamento de portas, mas não é obrigatório) - Largura de banda insuficiente (aumente para 256+ KB/sec)   - Swarm (enxame de pares) muito pequeno (alguns torrents têm 1-2 seeders (semeadores); paciência necessária) - DHT (Tabela de Hash Distribuída) desativada (ative para descoberta de pares sem tracker)

**Ativar DHT e PEX (Peer Exchange)** nas configurações do I2PSnark. A DHT permite encontrar pares sem depender de um rastreador. O PEX descobre pares a partir dos pares conectados, acelerando a descoberta do enxame.

**Corrupção de arquivos baixados** raramente ocorre com a verificação de integridade integrada do I2PSnark. Se detectada:

1. Clique com o botão direito no torrent → "Verificar" força o recálculo do hash de todas as partes
2. Exclua os dados corrompidos do torrent (mantém o arquivo .torrent)  
3. Clique com o botão direito → "Iniciar" para baixar novamente com verificação das partes
4. Verifique o disco em busca de erros se a corrupção persistir: `chkdsk` (Windows), `fsck` (Linux)

**Diretório monitorado não está funcionando** requer configuração adequada:

1. Configuração do I2PSnark → "Watch directory": Defina um caminho absoluto (por exemplo, `/home/user/torrents/watch`)
2. Garanta que o processo do I2P tenha permissões de leitura: `chmod 755 /path/to/watch`
3. Coloque arquivos .torrent no diretório de monitoramento - o I2PSnark os adiciona automaticamente
4. Configure "Auto start": Defina se os torrents devem iniciar imediatamente ao serem adicionados

**Otimização de desempenho para uso de torrents:**

- Limite o número de torrents ativos simultâneos: no máximo 3-5 para conexões padrão
- Priorize downloads importantes: interrompa temporariamente os torrents de baixa prioridade
- Aumente a alocação de largura de banda do router: mais largura de banda = melhor desempenho de torrents
- Tenha paciência: torrents no I2P são por natureza mais lentos do que o BitTorrent na clearnet (internet pública)
- Semeie após o download: a rede prospera com a reciprocidade

## Configuração e solução de problemas do Git via I2P

Operações do Git via I2P requerem **configuração de proxy SOCKS** ou **I2P tunnels dedicados** para acesso SSH/HTTP. O design do Git pressupõe conexões de baixa latência, o que torna desafiadora a arquitetura de alta latência do I2P.

**Configurar o Git para usar um proxy SOCKS do I2P:**

Edite ~/.ssh/config (crie se não existir):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Isso encaminha todas as conexões SSH para hosts .i2p através do proxy SOCKS do I2P (porta 4447). As configurações ServerAlive (opções do SSH para manter a sessão ativa) mantêm a conexão durante a latência do I2P.

Para operações HTTP/HTTPS do git, configure o git globalmente:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Nota: `socks5h` realiza a resolução de DNS através do proxy - crucial para domínios .i2p.

**Criar tunnel I2P dedicado para SSH do Git** (mais confiável que SOCKS):

1. Acesse http://127.0.0.1:7657/i2ptunnel
2. "Novo tunnel cliente" → "Padrão"
3. Configure:
   - Nome: Git-SSH  
   - Tipo: Cliente
   - Porta: 2222 (porta local para acesso ao Git)
   - Destino: [seu-servidor-git].i2p:22
   - Inicialização automática: Ativado
   - Contagem de tunnel: 3-4 (valores mais altos aumentam a confiabilidade)
4. Salve e inicie o tunnel
5. Configure o SSH para usar o tunnel: `ssh -p 2222 git@127.0.0.1`

**Erros de autenticação SSH** via I2P geralmente decorrem de:

- Chave não adicionada ao ssh-agent: `ssh-add ~/.ssh/id_rsa`
- Permissões incorretas do arquivo da chave: `chmod 600 ~/.ssh/id_rsa`
- Tunnel não está em execução: Verifique em http://127.0.0.1:7657/i2ptunnel se o status está verde
- Servidor Git requer tipo de chave específico: gere uma chave ed25519 se RSA falhar

**O tempo limite nas operações do Git** está relacionado às características de latência do I2P:

- Aumente o tempo limite do Git: `git config --global http.postBuffer 524288000` (buffer de 500 MB)
- Aumente o limite de baixa velocidade: `git config --global http.lowSpeedLimit 1000` e `git config --global http.lowSpeedTime 600` (aguarda 10 minutos)
- Use um clone raso para o checkout inicial: `git clone --depth 1 [url]` (busca apenas o commit mais recente, mais rápido)
- Clone durante períodos de baixa atividade: O congestionamento da rede afeta o desempenho do I2P

**Operações lentas de git clone/fetch** são inerentes à arquitetura do I2P. Um repositório de 100MB pode levar 30-60 minutos via I2P, contra segundos na clearnet (internet comum). Estratégias:

- Use clones superficiais: `--depth 1` reduz drasticamente a transferência inicial de dados
- Busque incrementalmente: Em vez de um clone completo, busque ramificações específicas: `git fetch origin branch:branch`
- Considere rsync sobre I2P: Para repositórios muito grandes, o rsync pode ter melhor desempenho
- Aumente a quantidade de tunnels: Mais tunnels proporcionam melhor taxa de transferência para transferências grandes e de longa duração

**Erros "Connection refused"** indicam configuração incorreta do tunnel:

1. Verifique se o I2P router está em execução: acesse http://127.0.0.1:7657
2. Confirme que o tunnel está ativo e verde em http://127.0.0.1:7657/i2ptunnel
3. Teste o tunnel: `nc -zv 127.0.0.1 2222` (deve conectar se o tunnel estiver funcionando)
4. Verifique se o destino está acessível: acesse a interface HTTP do destino, se disponível
5. Revise os logs do tunnel em http://127.0.0.1:7657/logs para erros específicos

**Melhores práticas para usar Git via I2P:**

- Mantenha o I2P router em execução continuamente para acesso estável ao Git
- Use chaves SSH em vez de autenticação por senha (menos solicitações interativas)
- Configure tunnels persistentes em vez de conexões SOCKS efêmeras
- Considere hospedar seu próprio servidor Git no I2P para maior controle
- Documente seus pontos de extremidade Git .i2p para colaboradores

## Acessando eepsites e resolvendo domínios .i2p

A razão mais frequente pela qual os usuários não conseguem acessar sites .i2p é **configuração incorreta do proxy do navegador**. Os sites I2P existem apenas dentro da rede I2P e exigem encaminhamento por meio do proxy HTTP do I2P.

**Configure as configurações de proxy do navegador exatamente:**

**Firefox (recomendado para I2P):**

1. Menu → Configurações → Configurações de rede → botão Configurações
2. Selecione "Configuração manual de proxy"
3. Proxy HTTP: **127.0.0.1** Porta: **4444**
4. Proxy SSL: **127.0.0.1** Porta: **4444**  
5. Proxy SOCKS: **127.0.0.1** Porta: **4447** (opcional, para aplicativos SOCKS)
6. Marque "Proxy DNS ao usar SOCKS v5"
7. Clique em OK para salvar

**Configurações críticas do Firefox em about:config:**

Navegue até `about:config` e modifique:

- `media.peerconnection.ice.proxy_only` = **true** (impede vazamentos de IP via WebRTC)
- `keyword.enabled` = **false** (impede que endereços .i2p redirecionem para mecanismos de busca)
- `network.proxy.socks_remote_dns` = **true** (DNS através do proxy)

**Limitações do Chrome/Chromium:**

O Chrome usa as configurações de proxy do sistema em vez de específicas do aplicativo. No Windows: Configurações → pesquise por "proxy" → "Abrir as configurações de proxy do seu computador" → Configure HTTP: 127.0.0.1:4444 e HTTPS: 127.0.0.1:4445.

Melhor abordagem: use as extensões FoxyProxy ou Proxy SwitchyOmega para roteamento seletivo de .i2p.

**Erros "Website Not Found In Address Book"** significam que o router não tem o endereço criptográfico do domínio .i2p. O I2P usa livros de endereços locais em vez de DNS centralizado. Soluções:

**Método 1: Use os jump services** (mais fácil para sites novos):

Acesse http://stats.i2p e pesquise pelo site. Clique no link addresshelper (auxiliar de endereço): `http://example.i2p/?i2paddresshelper=base64destination`. Seu navegador mostra "Salvar no livro de endereços?" - confirme para adicionar.

**Método 2: Atualizar as assinaturas do livro de endereços:**

1. Acesse http://127.0.0.1:7657/dns (SusiDNS)
2. Clique na guia "Subscriptions"  
3. Verifique as assinaturas ativas (padrão: http://i2p-projekt.i2p/hosts.txt)
4. Adicione as assinaturas recomendadas:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Clique em "Update Now" para forçar a atualização imediata das assinaturas
6. Aguarde 5-10 minutos para o processamento

**Método 3: Use endereços base32** (sempre funciona se o site estiver online):

Cada site .i2p tem um endereço base32: 52 caracteres aleatórios seguidos de .b32.i2p (por exemplo, `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Endereços base32 ignoram o livro de endereços - o router realiza uma consulta criptográfica direta.

**Erros comuns na configuração do navegador:**

- Tentando HTTPS em sites somente HTTP: A maioria dos sites .i2p usa apenas HTTP - tentar `https://example.i2p` falha
- Esquecendo o prefixo `http://`: O navegador pode pesquisar em vez de se conectar - sempre use `http://example.i2p`
- WebRTC (tecnologia de comunicação em tempo real do navegador) habilitado: Pode vazar o endereço IP real - desative nas configurações do Firefox ou via extensões
- DNS sem proxy: O DNS da Clearnet (internet pública) não consegue resolver .i2p - é necessário passar as consultas DNS por um proxy
- Porta do proxy incorreta: 4444 para HTTP (não 4445, que é um outproxy (proxy de saída) HTTPS para a clearnet)

**Router não totalmente integrado** impede o acesso a qualquer site. Verifique se há integração adequada:

1. Verifique se http://127.0.0.1:7657 mostra "Network: OK" ou "Network: Firewalled" (não "Network: Testing")
2. "Active peers" mostra 10+ no mínimo (50+ ideal)  
3. Sem a mensagem "Rejecting tunnels: starting up"
4. Aguarde de 10 a 15 minutos completos após a inicialização do router antes de esperar acesso a .i2p

**Configuração de IRC e de cliente de e-mail** segue padrões de proxy semelhantes:

**IRC:** Clientes conectam-se a **127.0.0.1:6668** (tunnel de proxy IRC do I2P). Desative as configurações de proxy do cliente IRC - a conexão com localhost:6668 já é encaminhada por proxy através do I2P.

**E-mail (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - Sem SSL/TLS (criptografia gerenciada pelo I2P tunnel) - Credenciais do registro da conta em postman.i2p

Todos esses tunnels devem exibir o status "running" (verde) em http://127.0.0.1:7657/i2ptunnel.

## Falhas de instalação e problemas de pacotes

Instalações baseadas em pacotes (Debian, Ubuntu, Arch) ocasionalmente falham devido a **alterações no repositório**, **expiração da chave GPG** ou **conflitos de dependências**. Os repositórios oficiais foram alterados de deb.i2p2.de/deb.i2p2.no (fim de vida) para **deb.i2p.net** em versões recentes.

**Atualize o repositório do Debian/Ubuntu para a versão atual:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**Falhas na verificação de assinaturas GPG** ocorrem quando as chaves do repositório expiram ou são alteradas:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**O serviço não inicia após a instalação do pacote** geralmente se deve a problemas nos perfis do AppArmor no Debian/Ubuntu:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**Problemas de permissão** no I2P instalado via pacote:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Problemas de compatibilidade com Java:**

I2P 2.10.0 requer **Java 8 no mínimo**. Sistemas mais antigos podem ter Java 7 ou anterior:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Erros de configuração do Wrapper** impedem a inicialização do serviço:

A localização do Wrapper.config varia conforme o método de instalação: - Instalação do usuário: `~/.i2p/wrapper.config` - Instalação por pacote: `/etc/i2p/wrapper.config` ou `/var/lib/i2p/wrapper.config`

Problemas comuns no wrapper.config:

- Caminhos incorretos: `wrapper.java.command` deve apontar para uma instalação válida do Java
- Memória insuficiente: `wrapper.java.maxmemory` definido muito baixo (aumente para 512+)
- Localização incorreta do pidfile: `wrapper.pidfile` deve ser um local gravável
- Binário do wrapper ausente: Algumas plataformas não possuem wrapper pré-compilado (use runplain.sh como alternativa)

**Falhas de atualização e atualizações corrompidas:**

Ocasionalmente, as atualizações da console do router falham no meio do download devido a interrupções na rede. Procedimento de atualização manual:

1. Baixe i2pupdate_X.X.X.zip de https://geti2p.net/en/download
2. Verifique se o checksum SHA256 corresponde ao hash publicado
3. Copie para o diretório de instalação do I2P como `i2pupdate.zip`
4. Reinicie o router - detecta e extrai a atualização automaticamente
5. Aguarde 5-10 minutos para a instalação da atualização
6. Verifique a nova versão em http://127.0.0.1:7657

**Migração a partir de versões muito antigas** (pré-0.9.47) para versões atuais pode falhar devido a chaves de assinatura incompatíveis ou funcionalidades removidas. Atualizações incrementais necessárias:

- Versões anteriores à 0.9.9: Não é possível verificar as assinaturas atuais - é necessária atualização manual
- Versões com Java 6/7: É necessário atualizar o Java antes de atualizar o I2P para a versão 2.x
- Grandes saltos de versão: Atualize primeiro para uma versão intermediária (0.9.47 é a recomendada)

**Quando usar instalador vs pacote:**

- **Pacotes (apt/yum):** Melhor para servidores, atualizações automáticas de segurança, integração ao sistema, gerenciamento com o systemd
- **Instalador (.jar):** Melhor para instalação no nível do usuário, Windows, macOS, instalações personalizadas, disponibilidade da versão mais recente

## Corrupção do arquivo de configuração e recuperação

A persistência da configuração do I2P depende de vários arquivos críticos. A corrupção geralmente resulta de **desligamento inadequado**, **erros de disco** ou **erros de edição manual**. Compreender a finalidade de cada arquivo permite um reparo cirúrgico em vez de uma reinstalação completa.

**Arquivos críticos e suas funções:**

- **router.keys** (516+ bytes): Identidade criptográfica do router - perder isso cria uma nova identidade
- **router.info** (gerado automaticamente): Informações do router publicadas - é seguro apagar, regenera-se  
- **router.config** (texto): Configuração principal - largura de banda, configurações de rede, preferências
- **i2ptunnel.config** (texto): Definições de tunnel - tunnels cliente/servidor, chaves, destinos
- **netDb/** (diretório): Base de dados de pares - informações do router para participantes da rede
- **peerProfiles/** (diretório): Estatísticas de desempenho dos pares - influencia a seleção de tunnels
- **keyData/** (diretório): Chaves de destino para eepsites e serviços - perder isto altera endereços
- **addressbook/** (diretório): Mapeamentos locais de nomes de host .i2p

**Procedimento de backup completo** antes de qualquer modificação:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Sintomas de corrupção do Router.config:**

- O router não inicia, com erros de análise sintática nos logs
- As configurações não persistem após a reinicialização
- Valores padrão inesperados aparecem  
- Caracteres ilegíveis ao visualizar o arquivo

**Reparar router.config corrompido:**

1. Faça backup do existente: `cp router.config router.config.broken`
2. Verifique a codificação do arquivo: Deve ser UTF-8 sem BOM (marca de ordem de bytes)
3. Valide a sintaxe: As chaves usam o separador '=' (não ':'), sem espaços à direita nas chaves, '#' apenas para comentários
4. Problemas comuns de corrupção: caracteres não ASCII nos valores, problemas de final de linha (CRLF vs LF)
5. Se não for possível corrigir: Exclua router.config - o router gera uma configuração padrão, preservando a identidade

**Configurações essenciais do router.config que devem ser preservadas:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**router.keys perdido ou inválido** cria uma nova identidade do router (roteador do I2P). Isso é aceitável, a menos que:

- Executando floodfill (perde o status de floodfill)
- Hospedando eepsites com endereço publicado (perde a continuidade)  
- Reputação estabelecida na rede

Sem cópia de segurança, não é possível recuperar - crie uma nova: apague router.keys, reinicie o I2P; uma nova identidade será criada.

**Distinção crítica:** router.keys (identidade) vs keyData/* (serviços). Perder router.keys altera a identidade do router. Perder keyData/mysite-keys.dat altera o endereço .i2p do seu eepsite - catastrófico se o endereço tiver sido publicado.

**Faça backup das chaves do eepsite/serviço separadamente:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**Corrupção em NetDb e peerProfiles (perfis de pares):**

Sintomas: Zero pares ativos, não é possível construir tunnels, "Database corruption detected" nos logs

Correção segura (todos farão reseed (obter novamente os dados iniciais da rede) e reconstruirão automaticamente):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Esses diretórios contêm apenas informações de rede em cache - excluí-los força uma nova inicialização (bootstrap), mas não resulta em perda de dados críticos.

**Estratégias de prevenção:**

1. **Sempre desligue corretamente:** Use `i2prouter stop` ou o botão "Shutdown" do console do router - nunca mate o processo à força
2. **Backups automatizados:** Tarefa cron de backup semanal de ~/.i2p para um disco separado
3. **Monitoramento da integridade do disco:** Verifique periodicamente o status SMART - discos com falhas corrompem dados
4. **Espaço em disco suficiente:** Mantenha 1+ GB livre - discos cheios causam corrupção
5. **Nobreak (UPS) recomendado:** Falhas de energia durante gravações corrompem arquivos
6. **Controle de versão das configurações críticas:** Repositório Git para router.config, i2ptunnel.config permite reversão

**As permissões de arquivo são importantes:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Mensagens de erro comuns decodificadas

O sistema de logs do I2P fornece mensagens de erro específicas que localizam exatamente os problemas. Compreender essas mensagens acelera a solução de problemas.

**"No tunnels available"** aparece quando o router ainda não construiu tunnels suficientes para o funcionamento. Isso é **normal durante os primeiros 5-10 minutos** após a inicialização. Se persistir por mais de 15 minutos:

1. Verifique se os pares ativos > 10 em http://127.0.0.1:7657
2. Verifique se a alocação de largura de banda é adequada (mínimo de 128+ KB/sec)
3. Examine a taxa de sucesso do tunnel em http://127.0.0.1:7657/tunnels (deve ser >40%)
4. Revise os logs para identificar os motivos de rejeição na construção do tunnel

**"Desvio de relógio detectado"** ou **"NTCP2 disconnect code 7"** indicam que a hora do sistema difere do consenso da rede em mais de 90 segundos. O I2P exige precisão de ±60 segundos. Conexões com routers com desvio de horário são rejeitadas automaticamente.

Corrigir imediatamente:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** ou **"Tunnel build timeout exceeded"** significa que a construção do tunnel através da cadeia de pares não foi concluída dentro da janela de tempo limite (geralmente 60 segundos). Causas:

- **Pares lentos:** Router selecionou participantes sem resposta para o tunnel
- **Congestionamento de rede:** A rede I2P está enfrentando alta carga
- **Largura de banda insuficiente:** Seus limites de largura de banda impedem a construção de tunnel em tempo hábil
- **Router sobrecarregado:** Tunnels participantes em excesso consumindo recursos

Soluções: aumentar a largura de banda, reduzir os tunnels participantes (`router.maxParticipatingTunnels` em http://127.0.0.1:7657/configadvanced), ativar o redirecionamento de portas para melhorar a seleção de pares.

**"Router is shutting down"** ou **"Graceful shutdown in progress"** aparecem durante o encerramento normal ou a recuperação após uma falha. Um encerramento controlado pode levar **até 10 minutos** enquanto o router fecha os tunnels, notifica os pares e salva o estado.

Se ficar preso no estado de encerramento por mais de 11 minutos, force a finalização:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** indica esgotamento do heap (área de memória dinâmica). Soluções imediatas:

1. Edite wrapper.config: `wrapper.java.maxmemory=512` (ou superior)
2. **Encerramento completo obrigatório** - reiniciar não aplicará a alteração
3. Aguarde 11 minutos para o encerramento completo  
4. Inicie o router do zero
5. Verifique a alocação de memória em http://127.0.0.1:7657/graphs - deve mostrar folga

**Erros de memória relacionados:**

- **"GC overhead limit exceeded":** Gastando tempo excessivo na coleta de lixo - aumente o heap
- **"Metaspace" (área de metadados da JVM):** Espaço de metadados de classes Java esgotado - adicione `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**Específico do Windows:** O Kaspersky Antivirus limita o heap (área de memória dinâmica) do Java a 512MB independentemente das configurações do wrapper.config - desinstale-o ou adicione o I2P às exclusões.

**"Tempo limite de conexão"** ou **"Erro do I2CP - porta 7654"** quando os aplicativos tentam se conectar ao router:

1. Verifique se o router está em execução: http://127.0.0.1:7657 deve responder
2. Verifique a porta I2CP: `netstat -an | grep 7654` deve mostrar LISTENING
3. Certifique-se de que o firewall do localhost permite: `sudo ufw allow from 127.0.0.1`  
4. Verifique se a aplicação está usando a porta correta (I2CP=7654, SAM=7656)

**"Certificate validation failed"** ou **"RouterInfo corrupt"** durante o reseed (processo de obtenção inicial da netDb):

Causas-raiz: Desvio de relógio (corrigir primeiro), netDb corrompida, certificados de reseed (processo de inicialização da rede) inválidos

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Corrupção de banco de dados detectada"** indica corrupção de dados em nível de disco em netDb ou em peerProfiles:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Verifique a saúde do disco com ferramentas SMART - corrupção recorrente sugere falha iminente no armazenamento.

## Desafios específicos da plataforma

Diferentes sistemas operacionais apresentam desafios específicos de implantação do I2P relacionados a permissões, políticas de segurança e integração com o sistema.

### Problemas de permissões e serviços no Linux

O I2P instalado via pacote é executado como o usuário do sistema **i2psvc** (Debian/Ubuntu) ou **i2p** (outras distribuições), exigindo permissões específicas:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Limites de descritores de arquivo** afetam a capacidade do router para conexões. Os limites padrão (1024) são insuficientes para routers de alta largura de banda:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**Conflitos do AppArmor** comuns no Debian/Ubuntu impedem a inicialização do serviço:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**Problemas com o SELinux** em RHEL/CentOS/Fedora:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**Solução de problemas de serviços do SystemD:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Interferência do Firewall do Windows e de programas antivírus

O Windows Defender e produtos antivírus de terceiros frequentemente sinalizam o I2P devido a padrões de comportamento de rede. Uma configuração adequada evita bloqueios desnecessários, mantendo a segurança.

**Configurar o Firewall do Windows Defender:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Substitua a porta 22648 pela sua porta I2P correta indicada em http://127.0.0.1:7657/confignet.

**Problema específico do Kaspersky Antivirus:** O "Application Control" da Kaspersky limita o heap do Java a 512MB, independentemente das configurações do wrapper.config. Isso causa OutOfMemoryError em routers de alta largura de banda.

Soluções: 1. Adicione o I2P às exclusões do Kaspersky: Configurações → Adicional → Ameaças e Exclusões → Gerenciar Exclusões 2. Ou desinstale o Kaspersky (recomendado para o funcionamento do I2P)

**Orientações gerais para antivírus de terceiros:**

- Adicione o diretório de instalação do I2P às exclusões  
- Adicione %APPDATA%\I2P e %LOCALAPPDATA%\I2P às exclusões
- Exclua o javaw.exe da análise comportamental
- Desative os recursos de "Network Attack Protection" que possam interferir com os protocolos do I2P

### Gatekeeper do macOS bloqueando a instalação

O Gatekeeper do macOS impede a execução de aplicativos não assinados. Os instaladores do I2P não são assinados com um Apple Developer ID, o que gera alertas de segurança.

**Ignorar o Gatekeeper para o instalador do I2P:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Após a instalação, a execução** ainda pode gerar avisos:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Nunca desative permanentemente o Gatekeeper (recurso de segurança do macOS)** - risco de segurança para outros aplicativos. Use apenas exceções específicas por arquivo.

**Configuração do firewall no macOS:**

1. Preferências do Sistema → Segurança e Privacidade → Firewall → Opções do Firewall
2. Clique em "+" para adicionar o aplicativo  
3. Navegue até a instalação do Java (por exemplo, `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Adicione e defina como "Permitir conexões de entrada"

### Problemas do aplicativo I2P para Android

As restrições de versão do Android e as limitações de recursos criam desafios únicos.

**Requisitos mínimos:** - Android 5.0+ (nível de API 21+) obrigatório para as versões atuais - 512 MB de RAM no mínimo, 1 GB+ recomendado   - 100 MB de armazenamento para o aplicativo + dados do router - Restrições de aplicativos em segundo plano desativadas para o I2P

**O aplicativo falha imediatamente:**

1. **Verifique a versão do Android:** Configurações → Sobre o telefone → Versão do Android (deve ser 5.0+)
2. **Desinstale todas as versões do I2P:** Instale apenas uma variante:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Instalações múltiplas entram em conflito
3. **Limpe os dados do app:** Configurações → Apps → I2P → Armazenamento → Limpar dados
4. **Reinstale a partir de um estado limpo**

**Otimização de bateria encerrando o router:**

O Android encerra agressivamente aplicativos em segundo plano para economizar bateria. O I2P precisa ser excluído:

1. Configurações → Bateria → Otimização da bateria (ou Uso da bateria do app)
2. Localize I2P → Não otimizar (ou Permitir atividade em segundo plano)
3. Configurações → Apps → I2P → Bateria → Permitir atividade em segundo plano + Remover restrições

**Problemas de conexão em dispositivos móveis:**

- **Bootstrap (inicialização) requer WiFi:** O processo de reseed inicial (obtenção inicial de pares) baixa uma quantidade significativa de dados - use WiFi, não dados móveis
- **Mudanças na rede:** O I2P não lida bem com trocas de rede - reinicie o aplicativo após uma transição WiFi/celular
- **Largura de banda para dispositivos móveis:** Configure de forma conservadora em 64-128 KB/sec para evitar o esgotamento dos dados móveis

**Otimização de desempenho para dispositivos móveis:**

1. App I2P → Menu → Configurações → Largura de banda
2. Defina limites apropriados: 64 KB/sec de entrada, 32 KB/sec de saída para dados móveis
3. Reduza os tunnels participantes: Configurações → Avançado → Máximo de tunnels participantes: 100-200
4. Ative "Parar o I2P quando a tela estiver desligada" para economizar bateria

**Uso de torrents no Android:**

- Limite para no máximo 2-3 torrents simultâneos
- Reduza a agressividade do DHT  
- Use apenas WiFi para transferências por torrent
- Aceite velocidades mais baixas em hardware móvel

## Problemas de reseed e bootstrap

Novas instalações do I2P exigem **reseeding** (processo inicial de obtenção de pares) - buscar informações iniciais de pares em servidores HTTPS públicos para ingressar na rede. Problemas de reseeding deixam os usuários com zero pares e sem acesso à rede.

**"No active peers" após uma instalação limpa** normalmente indica falha no reseed (processo de obtenção inicial de pares). Sintomas:

- Pares conhecidos: 0 ou fica abaixo de 5
- "Network: Testing" permanece por mais de 15 minutos
- Os logs mostram "Reseed failed" ou erros de conexão com servidores de reseed

**Por que o reseed (processo inicial de obtenção de pares) falha:**

1. **Firewall bloqueando HTTPS:** Firewalls corporativos/ISPs bloqueiam conexões aos reseed servers (servidores de inicialização da rede) (porta 443)
2. **Erros de certificado SSL:** O sistema não possui certificados raiz atualizados
3. **Requisito de proxy:** A rede exige um proxy HTTP/SOCKS para conexões externas
4. **Desvio de relógio:** A validação do certificado SSL falha quando o horário do sistema está errado
5. **Censura geográfica:** Alguns países/ISPs bloqueiam reseed servers conhecidos

**Forçar reseed manual (carregamento inicial da rede):**

1. Acesse http://127.0.0.1:7657/configreseed
2. Clique em "Save changes and reseed now"  
3. Monitore http://127.0.0.1:7657/logs em busca de "Reseed got XX router infos"
4. Aguarde 5-10 minutos para o processamento
5. Verifique http://127.0.0.1:7657 - os pares conhecidos devem aumentar para 50+

**Configurar proxy de reseed** para redes restritivas:

http://127.0.0.1:7657/configreseed → Configuração do proxy:

- Proxy HTTP: [proxy-server]:[port]
- Ou SOCKS5: [socks-server]:[port]  
- Ative "Usar proxy apenas para reseed (processo de inicialização/bootstrapping da rede)"
- Credenciais, se necessário
- Salve e force o reseed

**Alternativa: proxy do Tor para reseed (processo de inicialização da netDb):**

Se o Tor Browser ou o daemon do Tor estiver em execução:

- Tipo de proxy: SOCKS5
- Host: 127.0.0.1
- Porta: 9050 (porta SOCKS padrão do Tor)
- Ativar e reseed (obter novamente os pares iniciais da rede)

**Reseed manual (processo de obtenção de pares iniciais) via arquivo su3** (último recurso):

Quando todas as tentativas de reseed (obtenção inicial de entradas do netDb) automatizado falharem, obtenha o arquivo de reseed por um canal fora de banda:

1. Baixe i2pseeds.su3 de uma fonte confiável em uma conexão sem restrições (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. Encerre o I2P completamente
3. Copie i2pseeds.su3 para o diretório ~/.i2p/  
4. Inicie o I2P - extrai e processa o arquivo automaticamente
5. Exclua i2pseeds.su3 após o processamento
6. Verifique se o número de pares aumenta em http://127.0.0.1:7657

**Erros de certificado SSL durante o reseed (processo inicial de obtenção de pares do netDb):**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Soluções:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**Travado em 0 pares conhecidos por mais de 30 minutos:**

Indica falha completa de reseed (processo de obtenção inicial de pares). Procedimento de solução de problemas:

1. **Verifique se a data e hora do sistema estão corretas** (problema mais comum - corrija PRIMEIRO)
2. **Teste a conectividade HTTPS:** Tente acessar https://reseed.i2p.rocks no navegador - se falhar, é um problema de rede
3. **Verifique os logs do I2P** em http://127.0.0.1:7657/logs para erros específicos de reseed (bootstrap inicial da rede do I2P)
4. **Tente uma URL de reseed diferente:** http://127.0.0.1:7657/configreseed → adicione uma URL de reseed personalizada: https://reseed-fr.i2pd.xyz/
5. **Use o método manual com arquivo su3** se as tentativas automatizadas estiverem esgotadas

**Reseed servers ocasionalmente fora do ar (servidores que fornecem os pares iniciais):** I2P inclui vários reseed servers pré-configurados no código. Se um falhar, o router tenta outros automaticamente. A falha completa de todos os reseed servers é extremamente rara, mas possível.

**reseed servers (servidores de inicialização da rede) ativos no momento** (em outubro de 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Adicione como URLs personalizadas se tiver problemas com os valores padrão.

**Para usuários em regiões fortemente censuradas:**

Considere usar as pontes Snowflake/Meek através do Tor para o reseed inicial (processo de obtenção inicial de pares e endereços da rede), e depois alternar para acesso direto ao I2P assim que estiver integrado à rede. Ou obtenha i2pseeds.su3 por meio de esteganografia, e-mail ou USB de fora da zona de censura.

## Quando procurar ajuda adicional

Este guia abrange a vasta maioria dos problemas do I2P, mas alguns exigem a atenção de desenvolvedores ou o conhecimento especializado da comunidade.

**Procure ajuda da comunidade I2P quando:**

- O router trava repetidamente após seguir todas as etapas de solução de problemas
- Vazamentos de memória provocando crescimento contínuo além do heap (área de memória dinâmica) alocado
- A taxa de sucesso do tunnel permanece abaixo de 20% apesar de uma configuração adequada  
- Novos erros nos logs não cobertos por este guia
- Vulnerabilidades de segurança descobertas
- Solicitações de funcionalidades ou sugestões de melhoria

**Antes de solicitar ajuda, reúna informações de diagnóstico:**

1. Versão do I2P: http://127.0.0.1:7657 (por exemplo, "2.10.0")
2. Versão do Java: saída de `java -version`
3. Sistema operacional e versão
4. Status do router: estado da rede, contagem de pares ativos, tunnels participantes
5. Configuração de largura de banda: limites de entrada/saída
6. Status do encaminhamento de portas: bloqueado por firewall ou OK
7. Trechos relevantes do log: últimas 50 linhas mostrando erros de http://127.0.0.1:7657/logs

**Canais oficiais de suporte:**

- **Fórum:** https://i2pforum.net (clearnet) ou http://i2pforum.i2p (dentro do I2P)
- **IRC:** #i2p em Irc2P (irc.postman.i2p via I2P) ou irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p para discussões da comunidade
- **Rastreador de bugs:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues para bugs confirmados
- **Lista de discussão:** i2p-dev@lists.i2p-projekt.de para perguntas sobre desenvolvimento

**Expectativas realistas importam.** I2P é mais lento do que a clearnet (internet aberta) por design fundamental - o tunneling (encapsulamento em túnel) criptografado de múltiplos saltos cria latência inerente. Um router I2P funcionando com carregamentos de página de 30 segundos e velocidades de torrent de 50 KB/sec está **funcionando corretamente**, não está com defeito. Usuários que esperam velocidades de clearnet ficarão desapontados independentemente da otimização da configuração.

## Conclusão

A maioria dos problemas no I2P decorre de três categorias: paciência insuficiente durante o bootstrap (processo de inicialização; requer 10-15 minutos), alocação de recursos inadequada (mínimo de 512 MB de RAM, 256 KB/sec de largura de banda) ou redirecionamento de portas mal configurado. Compreender a arquitetura distribuída do I2P e o design voltado ao anonimato ajuda os usuários a distinguir o comportamento esperado de problemas reais.

O status "Firewalled" do router, embora não seja o ideal, não impede o uso do I2P — apenas limita a contribuição para a rede e degrada ligeiramente o desempenho. Novos usuários devem priorizar a **estabilidade em vez da otimização**: execute o router continuamente por vários dias antes de ajustar configurações avançadas, pois a integração melhora naturalmente com o tempo de atividade.

Ao solucionar problemas, verifique primeiro o básico: hora correta do sistema, largura de banda adequada, router em execução contínua e 10 ou mais pares ativos. A maioria dos problemas se resolve ao tratar desses fundamentos, em vez de ajustar parâmetros de configuração obscuros. O I2P recompensa a paciência e a operação contínua com desempenho aprimorado, à medida que o router constrói reputação e otimiza a seleção de pares ao longo de dias e semanas de tempo de atividade.
