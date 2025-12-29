---
title: "Perguntas Frequentes"
description: "FAQ Completo do I2P: ajuda do router, configuração, reseeds, privacidade/segurança, desempenho e solução de problemas"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Ajuda do Router I2P

### Em que sistemas o I2P funciona? {#systems}

O I2P é escrito na linguagem de programação Java. Foi testado no Windows, Linux, FreeBSD e OSX. Uma versão para Android também está disponível.

Em termos de uso de memória, o I2P é configurado para usar 128 MB de RAM por padrão. Isso é suficiente para navegação e uso de IRC. No entanto, outras atividades podem exigir maior alocação de memória. Por exemplo, se alguém deseja executar um router de alta largura de banda, participar de torrents I2P ou servir serviços ocultos de alto tráfego, uma quantidade maior de memória é necessária.

Em termos de uso de CPU, o I2P foi testado para funcionar em sistemas modestos, como os computadores de placa única da linha Raspberry Pi. Como o I2P faz uso intenso de técnicas criptográficas, uma CPU mais potente será mais adequada para lidar com a carga de trabalho gerada pelo I2P, bem como com tarefas relacionadas ao resto do sistema (ou seja, Sistema Operacional, Interface Gráfica, Outros processos, por exemplo, Navegação Web).

É recomendado usar Sun/Oracle Java ou OpenJDK.

### É necessário instalar Java para usar o I2P? {#java}

Sim, o Java é necessário para usar o I2P Core. Incluímos o Java nos nossos instaladores fáceis para Windows, Mac OSX e Linux. Se você estiver executando o aplicativo I2P Android, também precisará de um runtime Java como Dalvik ou ART instalado na maioria dos casos.

### O que é um "I2P Site" e como configuro meu navegador para usá-los? {#I2P-Site}

Um Site I2P é um site normal, exceto que está hospedado dentro do I2P. Os sites I2P têm endereços que se parecem com endereços normais da internet, terminando em ".i2p" de forma legível para humanos e não criptográfica, para benefício das pessoas. Na verdade, conectar-se a um Site I2P requer criptografia, o que significa que os endereços de Sites I2P também são os longos Destinations em "Base64" e os endereços "B32" mais curtos. Você pode precisar fazer configurações adicionais para navegar corretamente. Navegar em Sites I2P exigirá ativar o Proxy HTTP na sua instalação do I2P e então configurar seu navegador para usá-lo. Para mais informações, consulte a seção "Navegadores" abaixo ou o Guia de "Configuração de Navegador".

### O que significam os números Ativos x/y no console do roteador? {#active}

Na página Peers no console do seu router, você pode ver dois números - Active x/y. O primeiro número é a quantidade de peers para os quais você enviou ou de quem recebeu uma mensagem nos últimos minutos. O segundo número é a quantidade de peers vistos recentemente, que será sempre maior ou igual ao primeiro número.

### Meu roteador tem muito poucos peers ativos, isso é normal? {#peers}

Sim, isso pode ser normal, especialmente quando o router acabou de ser iniciado. Novos routers precisarão de tempo para inicializar e conectar-se ao resto da rede. Para ajudar a melhorar a integração na rede, tempo de atividade e desempenho, revise estas configurações:

- **Compartilhar largura de banda** - Se um router estiver configurado para compartilhar largura de banda, ele roteará mais tráfego para outros routers, o que ajuda a integrá-lo ao resto da rede, além de melhorar o desempenho da conexão local. Isso pode ser configurado na página [http://localhost:7657/config](http://localhost:7657/config).
- **Interface de rede** - Certifique-se de que não há uma interface especificada na página [http://localhost:7657/confignet](http://localhost:7657/confignet). Isso pode reduzir o desempenho, a menos que seu computador seja multi-homed com múltiplos endereços IP externos.
- **Protocolo I2NP** - Certifique-se de que o router está configurado para esperar conexões em um protocolo válido para o sistema operacional do host e configurações de rede vazias (Avançado). Não insira um endereço IP no campo 'Hostname' na página de configuração de Rede. O Protocolo I2NP que você selecionar aqui só será usado se você ainda não tiver um endereço acessível. A maioria das conexões sem fio Verizon 4G e 5G nos Estados Unidos, por exemplo, bloqueiam UDP e não podem ser alcançadas por ele. Outros usariam UDP à força mesmo que esteja disponível para eles. Escolha uma configuração razoável dos Protocolos I2NP listados.

### Sou contra certos tipos de conteúdo. Como posso evitar distribuí-los, armazená-los ou acessá-los? {#badcontent}

Nenhum deste material é instalado por padrão. No entanto, como o I2P é uma rede peer-to-peer, é possível que você encontre conteúdo proibido acidentalmente. Aqui está um resumo de como o I2P evita que você se envolva desnecessariamente em violações de suas convicções.

- **Distribuição** - O tráfego é interno à rede I2P, você não é um [nó de saída](#exit) (referido como outproxy em nossa documentação).
- **Armazenamento** - A rede I2P não faz armazenamento distribuído de conteúdo, isso tem que ser especificamente instalado e configurado pelo usuário (com Tahoe-LAFS, por exemplo). Essa é uma característica de uma rede anônima diferente, [Freenet](http://freenetproject.org/). Ao executar um router I2P, você não está armazenando conteúdo para ninguém.
- **Acesso** - Seu router não solicitará nenhum conteúdo sem sua instrução específica para fazê-lo.

### É possível bloquear o I2P? {#blocking}

Sim, de longe a maneira mais fácil e comum é bloqueando o bootstrap, ou servidores de "Reseed". Bloquear completamente todo o tráfego ofuscado também funcionaria (embora isso quebrasse muitas, muitas outras coisas que não são I2P e a maioria não está disposta a ir tão longe). No caso do bloqueio de reseed, existe um pacote de reseed no Github, bloqueá-lo também bloqueará o Github. Você pode fazer reseed através de um proxy (muitos podem ser encontrados na Internet se você não quiser usar Tor) ou compartilhar pacotes de reseed com amigos de forma offline.

### No `wrapper.log` vejo um erro que diz "`Protocol family unavailable`" ao carregar o Router Console {#protocolfamily}

Frequentemente, este erro ocorrerá com qualquer software java habilitado para rede em alguns sistemas que estão configurados para usar IPv6 por padrão. Existem algumas maneiras de resolver isso:

- Em sistemas baseados em Linux, você pode executar `echo 0 > /proc/sys/net/ipv6/bindv6only`
- Procure pelas seguintes linhas em `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Se as linhas estiverem presentes, descomente-as removendo os "#"s. Se as linhas não estiverem presentes, adicione-as sem os "#"s.

Outra opção seria remover o `::1` de `~/.i2p/clients.config`

**AVISO**: Para que quaisquer alterações no `wrapper.config` tenham efeito, você deve parar completamente o router e o wrapper. Clicar em *Reiniciar* no console do router NÃO irá reler este arquivo! Você deve clicar em *Desligar*, aguardar 11 minutos e então iniciar o I2P.

### A maioria dos Sites I2P dentro do I2P estão fora do ar? {#down}

Se você considerar todos os I2P Sites que já foram criados, sim, a maioria deles está fora do ar. Pessoas e I2P Sites vêm e vão. Uma boa maneira de começar no I2P é verificar uma lista de I2P Sites que estão atualmente ativos. [identiguy.i2p](http://identiguy.i2p) rastreia I2P Sites ativos.

### Por que o I2P está escutando na porta 32000? {#port32000}

O wrapper de serviço Java Tanuki que usamos abre esta porta — vinculada ao localhost — para se comunicar com o software rodando dentro da JVM. Quando a JVM é iniciada, ela recebe uma chave para poder se conectar ao wrapper. Após a JVM estabelecer sua conexão com o wrapper, o wrapper recusa quaisquer conexões adicionais.

Mais informações podem ser encontradas na [documentação do wrapper](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Como configuro meu navegador? {#browserproxy}

A configuração de proxy para diferentes navegadores está em uma página separada com capturas de tela. Configurações mais avançadas com ferramentas externas, como o plug-in de navegador FoxyProxy ou o servidor proxy Privoxy, são possíveis, mas podem introduzir vazamentos na sua configuração.

### Como me conecto ao IRC dentro do I2P? {#irc}

Um túnel para o servidor IRC principal dentro do I2P, Irc2P, é criado quando o I2P é instalado (veja a [página de configuração do I2PTunnel](http://localhost:7657/i2ptunnel/index.jsp)), e é iniciado automaticamente quando o router I2P inicia. Para se conectar a ele, configure seu cliente IRC para conectar em `localhost 6668`. Usuários de clientes semelhantes ao HexChat podem criar uma nova rede com o servidor `localhost/6668` (lembre-se de marcar "Ignorar servidor proxy" se você tiver um servidor proxy configurado). Usuários do Weechat podem usar o seguinte comando para adicionar uma nova rede:

```
/server add irc2p localhost/6668
```
### Como configurar meu próprio site I2P? {#myI2P-Site}

O método mais fácil é clicar no link [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) no console do router e criar um novo 'Server Tunnel' (túnel servidor). Você pode servir conteúdo dinâmico configurando o destino do tunnel para a porta de um servidor web existente, como Tomcat ou Jetty. Você também pode servir conteúdo estático. Para isso, configure o destino do tunnel para: `0.0.0.0 port 7659` e coloque o conteúdo no diretório `~/.i2p/eepsite/docroot/`. (Em sistemas não-Linux, isso pode estar em um local diferente. Verifique o console do router.) O software 'eepsite' vem como parte do pacote de instalação do I2P e está configurado para iniciar automaticamente quando o I2P é iniciado. O site padrão criado pode ser acessado em http://127.0.0.1:7658. No entanto, seu 'eepsite' também está acessível a outros através do seu arquivo de chave eepsite, localizado em: `~/.i2p/eepsite/i2p/eepsite.keys`. Para saber mais, leia o arquivo readme em: `~/.i2p/eepsite/README.txt`.

### Se eu hospedar um site no I2P em casa, contendo apenas HTML e CSS, é perigoso? {#hosting}

Depende do seu adversário e do seu modelo de ameaça. Se você está apenas preocupado com violações "de privacidade" corporativas, criminosos típicos e censura, então não é realmente perigoso. As autoridades policiais provavelmente vão te encontrar de qualquer forma se realmente quiserem. Apenas hospedar quando você tiver um navegador de usuário doméstico normal (internet) em execução tornará realmente difícil saber quem está hospedando aquela parte. Por favor, considere a hospedagem do seu site I2P da mesma forma que hospedar qualquer outro serviço - é tão perigoso - ou seguro - quanto você mesmo o configurar e gerenciar.

Nota: Já existe uma forma de separar a hospedagem de um serviço i2p (destination) do router i2p. Se você [entender como](/docs/overview/tech-intro#i2pservices) funciona, então pode simplesmente configurar uma máquina separada como servidor para o site (ou serviço) que será publicamente acessível e encaminhar isso para o servidor web através de um túnel SSH [muito] seguro ou usar um sistema de arquivos compartilhado seguro.

### Como o I2P encontra sites ".i2p"? {#addresses}

A aplicação de Livro de Endereços do I2P mapeia nomes legíveis por humanos para destinos de longo prazo, associados a serviços, tornando-a mais parecida com um arquivo hosts ou uma lista de contatos do que com uma base de dados de rede ou um serviço DNS. É também local-primeiro, não há um namespace global reconhecido, você decide a que qualquer domínio .i2p corresponde no final. O meio-termo é algo chamado "Jump Service" (serviço de redirecionamento) que fornece um nome legível por humanos ao redirecioná-lo para uma página onde será perguntado "Você autoriza o router I2P a chamar $SITE_CRYPTO_KEY de $SITE_NAME.i2p" ou algo nesse sentido. Uma vez que esteja no seu livro de endereços, você pode gerar seus próprios URL's de redirecionamento para ajudar a compartilhar o site com outros.

### Como adiciono endereços ao Catálogo de Endereços? {#addressbook}

Você não pode adicionar um endereço sem conhecer pelo menos o base32 ou base64 do site que deseja visitar. O "hostname" que é legível por humanos é apenas um alias para o endereço criptográfico, que corresponde ao base32 ou base64. Sem o endereço criptográfico, não há como acessar um I2P Site, isso é por design. Distribuir o endereço para pessoas que ainda não o conhecem geralmente é responsabilidade do provedor de serviço Jump. Visitar um I2P Site desconhecido acionará o uso de um serviço Jump. stats.i2p é o serviço Jump mais confiável.

Se você está hospedando um site via i2ptunnel, então ele ainda não terá um registro em um serviço de jump. Para dar a ele uma URL localmente, visite a página de configuração e clique no botão que diz "Add to Local Address Book." Em seguida, vá para http://127.0.0.1:7657/dns para consultar a URL addresshelper e compartilhá-la.

### Quais portas o I2P utiliza? {#ports}

As portas que são usadas pelo I2P podem ser divididas em 2 seções:

1. Portas voltadas para a Internet, que são usadas para comunicação com outros roteadores I2P
2. Portas locais, para conexões locais

Estes são descritos em detalhe abaixo.

#### 1. Portas voltadas para a Internet

Nota: Desde a versão 0.7.8, novas instalações não utilizam a porta 8887; uma porta aleatória entre 9000 e 31000 é selecionada quando o programa é executado pela primeira vez. A porta selecionada é exibida na [página de configuração](http://127.0.0.1:7657/confignet) do router.

**SAÍDA**

- UDP da porta aleatória listada na [página de configuração](http://127.0.0.1:7657/confignet) para portas UDP remotas arbitrárias, permitindo respostas
- TCP de portas altas aleatórias para portas TCP remotas arbitrárias
- UDP de saída na porta 123, permitindo respostas. Isto é necessário para a sincronização de tempo interna do I2P (via SNTP - consultando um host SNTP aleatório em pool.ntp.org ou outro servidor que você especificar)

**ENTRADA**

- (Opcional, recomendado) UDP para a porta indicada na [página de configuração](http://127.0.0.1:7657/confignet) de locais arbitrários
- (Opcional, recomendado) TCP para a porta indicada na [página de configuração](http://127.0.0.1:7657/confignet) de locais arbitrários
- O TCP de entrada pode ser desativado na [página de configuração](http://127.0.0.1:7657/confignet)

#### 2. Portas I2P locais

As portas I2P locais escutam apenas conexões locais por padrão, exceto quando indicado:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### Estão faltando muitos hosts no meu livro de endereços. Quais são alguns bons links de subscrição? {#subscriptions}

O livro de endereços está localizado em [http://localhost:7657/dns](http://localhost:7657/dns) onde mais informações podem ser encontradas.

**Quais são alguns bons links de subscrição para o livro de endereços?**

Você pode tentar o seguinte:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### Como posso acessar o console web a partir de outras máquinas ou protegê-lo com senha? {#remote_webconsole}

Por motivos de segurança, o console de administração do router por padrão apenas escuta conexões na interface local.

Existem dois métodos para acessar o console remotamente:

1. Túnel SSH
2. Configurando seu console para estar disponível em um endereço IP público com nome de usuário e senha

Estes são detalhados abaixo:

**Método 1: Túnel SSH**

Se você está executando um Sistema Operacional tipo Unix, este é o método mais fácil para acessar remotamente seu console I2P. (Nota: software de servidor SSH está disponível para sistemas executando Windows, por exemplo [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Após configurar o acesso SSH ao seu sistema, a flag '-L' é passada ao SSH com os argumentos apropriados - por exemplo:

```
ssh -L 7657:localhost:7657 (System_IP)
```
onde '(System_IP)' é substituído pelo endereço IP do seu Sistema. Este comando encaminha a porta 7657 (o número antes dos dois pontos) para a porta 7657 do sistema remoto (conforme especificado pela string 'localhost' entre os primeiros e segundos dois pontos) (o número após os segundos dois pontos). O seu console I2P remoto estará agora disponível no seu sistema local como 'http://localhost:7657' e permanecerá disponível enquanto a sua sessão SSH estiver ativa.

Se você quiser iniciar uma sessão SSH sem iniciar um shell no sistema remoto, pode adicionar a flag '-N':

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Método 2: Configurando seu console para estar disponível em um endereço IP público com nome de usuário e senha**

1. Abra `~/.i2p/clients.config` e substitua:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   por:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   onde você substitui (System_IP) pelo endereço IP público do seu sistema

2. Acesse [http://localhost:7657/configui](http://localhost:7657/configui) e adicione um nome de usuário e senha para o console, se desejar - Adicionar um nome de usuário e senha é altamente recomendado para proteger seu console I2P contra adulterações, o que poderia levar à desanonimização.

3. Vá para [http://localhost:7657/index](http://localhost:7657/index) e clique em "Graceful restart", que reinicia a JVM e recarrega as aplicações cliente

Depois que isso iniciar, você agora deve ser capaz de acessar seu console remotamente. Carregue o console do router em `http://(IP_do_Sistema):7657` e você será solicitado a fornecer o nome de usuário e senha que você especificou no passo 2 acima, se o seu navegador suportar o popup de autenticação.

NOTA: Você pode especificar 0.0.0.0 na configuração acima. Isso especifica uma interface, não uma rede ou máscara de rede. 0.0.0.0 significa "vincular a todas as interfaces", portanto pode ser acessível em 127.0.0.1:7657 bem como em qualquer IP LAN/WAN. Tenha cuidado ao usar esta opção, pois o console estará disponível em TODOS os endereços configurados no seu sistema.

### Como posso usar aplicações de outras máquinas? {#remote_i2cp}

Consulte a resposta anterior para instruções sobre como usar o Encaminhamento de Porta SSH e também veja esta página no seu console: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### É possível usar o I2P como proxy SOCKS? {#socks}

O proxy SOCKS está funcional desde a versão 0.7.1. SOCKS 4/4a/5 são suportados. O I2P não possui um outproxy SOCKS, portanto está limitado ao uso apenas dentro do I2P.

Muitas aplicações vazam informações sensíveis que podem identificá-lo na Internet e este é um risco que deve estar ciente ao usar o proxy SOCKS do I2P. O I2P filtra apenas os dados de conexão, mas se o programa que você pretende executar enviar essas informações como conteúdo, o I2P não tem como proteger seu anonimato. Por exemplo, algumas aplicações de e-mail enviarão o endereço IP da máquina em que estão sendo executadas para um servidor de e-mail. Recomendamos ferramentas ou aplicações específicas do I2P (como [I2PSnark](http://localhost:7657/i2psnark/) para torrents), ou aplicações que são conhecidas por serem seguras de usar com I2P, incluindo plugins populares encontrados no [Firefox](https://www.mozilla.org/).

### Como faço para acessar IRC, BitTorrent ou outros serviços na Internet normal? {#proxy_other}

Existem serviços chamados Outproxies que fazem a ponte entre o I2P e a Internet, como os Tor Exit Nodes. A funcionalidade padrão de outproxy para HTTP e HTTPS é fornecida por `exit.stormycloud.i2p` e é operada pela StormyCloud Inc. Ela é configurada no HTTP Proxy. Além disso, para ajudar a proteger o anonimato, o I2P não permite que você faça conexões anônimas para a Internet regular por padrão. Consulte a página [Socks Outproxy](/docs/api/socks#outproxy) para mais informações.

---

## Reseeds

### Meu roteador está ativo há vários minutos e tem zero ou muito poucas conexões {#reseed}

Primeiro verifique a página [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) no Console do Router – seu banco de dados de rede (netDb). Se você não vir nenhum router listado de dentro do I2P, mas o console indicar que você deveria estar protegido por firewall, então provavelmente você não consegue se conectar aos servidores de reseed. Se você vir outros routers I2P listados, tente diminuir o número máximo de conexões em [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config), talvez seu router não consiga lidar com muitas conexões.

### Como faço o reseed manualmente? {#manual_reseed}

Em circunstâncias normais, o I2P irá conectá-lo à rede automaticamente usando nossos links de bootstrap. Se uma conexão de internet interrompida fizer com que o bootstrap a partir dos servidores de reseed falhe, uma maneira fácil de fazer o bootstrap é usando o navegador Tor (Por padrão ele abre localhost), que funciona muito bem com [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed). Também é possível fazer o reseed de um router I2P manualmente.

Ao usar o navegador Tor para ressemear, você pode selecionar vários URLs de uma vez e prosseguir. Embora o valor padrão que é 2 (dos vários urls) também funcione, será lento.

---

## Privacidade-Segurança

### O meu router é um "nó de saída" (outproxy) para a Internet regular? Não quero que seja. {#exit}

Não, o seu router participa no transporte de tráfego cifrado e2e através da rede i2p para um endpoint de tunnel aleatório, normalmente não um outproxy, mas nenhum tráfego é passado entre o seu router e a Internet na camada de transporte. Como utilizador final, não deve executar um outproxy se não tiver competências em administração de sistemas e redes.

### É fácil detectar o uso do I2P analisando o tráfego de rede? {#detection}

O tráfego I2P geralmente se assemelha ao tráfego UDP, e nada além disso – e fazer com que pareça não muito mais do que isso é um objetivo. Ele também suporta TCP. Com algum esforço, a análise passiva de tráfego pode ser capaz de classificar o tráfego como "I2P", mas esperamos que o desenvolvimento contínuo da ofuscação de tráfego reduza isso ainda mais. Até mesmo uma camada de ofuscação de protocolo bastante simples como obfs4 impedirá que censores bloqueiem o I2P (é um objetivo que o I2P implante).

### É seguro usar o I2P? {#safe}

Depende do seu modelo de ameaça pessoal. Para a maioria das pessoas, o I2P é muito mais seguro do que não usar nenhuma proteção. Algumas outras redes (como Tor, mixminion/mixmaster), são provavelmente mais seguras contra certos adversários. Por exemplo, o tráfego I2P não usa TLS/SSL, então não tem os problemas de "elo mais fraco" que o Tor tem. O I2P foi usado por muitas pessoas na Síria durante a "Primavera Árabe", e recentemente o projeto tem visto maior crescimento em instalações linguísticas menores do I2P no Oriente Próximo e Médio. O mais importante a notar aqui é que o I2P é uma tecnologia e você precisa de um guia/tutorial para melhorar sua privacidade/anonimato na Internet. Também verifique seu navegador ou importe o mecanismo de busca de impressão digital para bloquear ataques de fingerprinting com um conjunto de dados muito grande (significando: caudas longas típicas / estrutura de dados diversificada muito precisa) sobre muitas características do ambiente e não use VPN para reduzir todos os riscos que vêm dela mesma, como o comportamento do próprio cache TLS e a construção técnica do negócio do provedor que pode ser hackeado mais facilmente do que um sistema desktop próprio. Talvez usar um Tor V-Browser isolado com suas excelentes proteções anti-fingerprint e uma proteção geral de tempo de vida appguard permitindo apenas as comunicações de sistema necessárias e um último uso de vm com scripts anti-espionagem desabilitados e live-cd para remover qualquer "risco quase permanente possível" e reduzir todos os riscos por uma probabilidade decrescente sejam uma boa opção em rede pública e modelo de risco individual elevado e pode ser o melhor que você pode fazer com esse objetivo para uso do i2p.

### Vejo endereços IP de todos os outros nós I2P no console do router. Isso significa que meu endereço IP está visível para outros? {#netdb_ip}

Sim, para outros nós I2P que conhecem o seu router. Usamos isso para conectar com o resto da rede I2P. Os endereços estão fisicamente localizados em "routerInfos (objetos chave,valor)", seja obtidos remotamente ou recebidos de peers. Os "routerInfos" contêm algumas informações (algumas opcionais oportunisticamente adicionadas), "publicadas pelo peer", sobre o próprio router para bootstrapping. Nenhum dado está neste objeto sobre clientes. Olhando mais de perto sob o capô, você verá que todos são contados com o tipo mais recente de criação de IDs chamado "SHA-256 Hashes (baixo=hash Positivo(-chave), alto=hash Negativo(+chave))". A rede I2P possui um banco de dados próprio de dados de routerInfos criados durante upload e indexação, mas isso depende profundamente da realização das tabelas chave/valor e da topologia da rede e estado de carga / estado de largura de banda e probabilidades de roteamento para armazenamentos nos componentes do DB.

### É seguro usar um outproxy? {#proxy_safe}

Depende da sua definição de "seguro". Os outproxies são ótimos quando funcionam, mas infelizmente são executados voluntariamente por pessoas que podem perder o interesse ou podem não ter os recursos para mantê-los 24/7 – esteja ciente de que você pode experimentar períodos de tempo durante os quais os serviços ficam indisponíveis, interrompidos ou não confiáveis, e não estamos associados a este serviço e não temos influência sobre ele.

Os próprios outproxys podem ver o seu tráfego entrar e sair, com exceção de dados HTTPS/SSL criptografados de ponta a ponta, assim como o seu provedor de internet (ISP) pode ver o seu tráfego entrar e sair do seu computador. Se você confia no seu provedor de internet, não seria pior com o outproxy.

### E quanto aos ataques de "Desanonimização"? {#deanon}

Para uma explicação mais detalhada, leia mais em nossos artigos sobre [Modelo de Ameaças](/docs/overview/threat-model). Em geral, a desanonimização não é trivial, mas é possível se você não for cauteloso o suficiente.

---

## Acesso à Internet/Desempenho

### Não consigo acessar sites normais da Internet através do I2P. {#outproxy}

O proxy para sites da Internet (eepsites que estão voltados para a Internet) é fornecido como um serviço aos usuários do I2P por provedores sem bloqueio. Este serviço não é o foco principal do desenvolvimento do I2P, e é fornecido de forma voluntária. Eepsites que estão hospedados no I2P devem sempre funcionar sem um outproxy (proxy de saída). Outproxies são uma conveniência, mas por design não são perfeitos nem uma parte importante do projeto. Esteja ciente de que eles podem não ser capazes de fornecer o serviço de alta qualidade que outros serviços do I2P podem oferecer.

### Não consigo acessar sites https:// ou ftp:// através do I2P. {#https}

O proxy HTTP padrão suporta apenas outproxying HTTP e HTTPS.

### Por que meu router está usando muita CPU? {#cpu}

Primeiro, certifique-se de ter a versão mais recente de cada componente relacionado ao I2P – versões antigas possuíam seções de código que consumiam CPU desnecessariamente. Há também um [registro de desempenho](/docs/overview/performance) que documenta algumas das melhorias no desempenho do I2P ao longo do tempo.

### Meus pares ativos / pares conhecidos / túneis participantes / conexões / largura de banda variam drasticamente ao longo do tempo! Há algo errado? {#vary}

A estabilidade geral da rede I2P é uma área de pesquisa contínua. Uma parte considerável dessa pesquisa está focada em como pequenas mudanças nas configurações alteram o comportamento do router. Como o I2P é uma rede peer-to-peer, as ações de outros peers influenciarão o desempenho do seu router.

### O que torna downloads, torrents, navegação web e tudo o mais mais lento no I2P em comparação com a internet comum? {#slow}

O I2P possui diferentes proteções que adicionam roteamento extra e camadas adicionais de criptografia. Ele também redireciona o tráfego através de outros peers (Tunnels) que têm sua própria velocidade e qualidade, alguns são lentos, outros rápidos. Isso resulta em muita sobrecarga e tráfego em ritmos diferentes em direções diferentes. Por design, todas essas coisas o tornarão mais lento em comparação com uma conexão direta na internet, mas muito mais anônimo e ainda rápido o suficiente para a maioria das coisas.

Abaixo está um exemplo apresentado com uma explicação para ajudar a fornecer algum contexto sobre as considerações de latência e largura de banda ao usar o I2P.

Considere o diagrama abaixo. Ele representa uma conexão entre um cliente fazendo uma requisição via I2P, um servidor recebendo a requisição via I2P e então respondendo de volta também via I2P. O circuito pelo qual a requisição trafega também está representado.

A partir do diagrama, considere que as caixas rotuladas 'P', 'Q' e 'R' representam um tunnel de saída para 'A' e que as caixas rotuladas 'X', 'Y' e 'Z' representam um tunnel de saída para 'B'. Da mesma forma, as caixas rotuladas 'X', 'Y' e 'Z' representam um tunnel de entrada para 'B' enquanto as caixas rotuladas 'P_1', 'Q_1' e 'R_1' representam um tunnel de entrada para 'A'. As setas entre as caixas mostram a direção do tráfego. O texto acima e abaixo das setas detalha alguns exemplos de largura de banda entre um par de saltos, bem como exemplos de latências.

Quando tanto o cliente quanto o servidor estão usando tunnels de 3 saltos, um total de 12 outros routers I2P estão envolvidos no relay do tráfego. 6 peers fazem relay do tráfego do cliente para o servidor, que é dividido em um tunnel de saída de 3 saltos de 'A' ('P', 'Q', 'R') e um tunnel de entrada de 3 saltos para 'B' ('X', 'Y', 'Z'). Da mesma forma, 6 peers fazem relay do tráfego do servidor de volta para o cliente.

Primeiro, podemos considerar a latência - o tempo que leva para uma solicitação de um cliente atravessar a rede I2P, alcançar o servidor e retornar ao cliente. Somando todas as latências, vemos que:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
O tempo total de ida e volta no nosso exemplo soma 740 ms - certamente muito maior do que normalmente se veria ao navegar em sites regulares da internet.

Em segundo lugar, podemos considerar a largura de banda disponível. Isso é determinado pelo link mais lento entre os saltos do cliente e do servidor, bem como quando o tráfego está sendo transmitido pelo servidor para o cliente. Para o tráfego indo do cliente para o servidor, vemos que a largura de banda disponível em nosso exemplo entre os saltos 'R' & 'X', assim como os saltos 'X' & 'Y', é de 32 KB/s. Apesar da maior largura de banda disponível entre os outros saltos, esses saltos atuarão como um gargalo e limitarão a largura de banda máxima disponível para o tráfego de 'A' para 'B' em 32 KB/s. Da mesma forma, rastreando o caminho do servidor para o cliente, vemos que há uma largura de banda máxima de 64 KB/s - entre os saltos 'Z_1' & 'Y_1, 'Y_1' & 'X_1' e 'Q_1' & 'P_1'.

Recomendamos aumentar os seus limites de largura de banda. Isso ajuda a rede ao aumentar a quantidade de largura de banda disponível, o que por sua vez melhorará a sua experiência no I2P. As configurações de largura de banda estão localizadas na página [http://localhost:7657/config](http://localhost:7657/config). Por favor, esteja ciente dos limites da sua conexão de internet conforme determinado pelo seu provedor de internet (ISP) e ajuste suas configurações de acordo.

Também recomendamos definir uma quantidade suficiente de largura de banda compartilhada - isso permite que tunnels participantes sejam roteados através do seu router I2P. Permitir tráfego participante mantém seu router bem integrado na rede e melhora suas velocidades de transferência.

O I2P é um trabalho em andamento. Muitas melhorias e correções estão sendo implementadas e, de modo geral, executar a versão mais recente ajudará no seu desempenho. Se você ainda não o fez, instale a versão mais recente.

### Acho que encontrei um bug, onde posso reportá-lo? {#bug}

Você pode reportar quaisquer bugs/problemas que encontrar no nosso rastreador de bugs, que está disponível tanto pela internet não-privada quanto pelo I2P. Temos um fórum de discussão, também disponível no I2P e na internet não-privada. Você também pode participar do nosso canal IRC: através da nossa rede IRC, IRC2P, ou no Freenode.

- **Nosso Bugtracker:**
  - Internet não-privada: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - No I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Nossos fóruns:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Colar logs:** Você pode colar logs interessantes em um serviço de paste como os serviços de internet não-privada listados no [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory), ou um serviço de paste I2P como esta [instância PrivateBin](http://paste.crypthost.i2p) ou este [serviço de paste sem Javascript](http://pasta-nojs.i2p) e acompanhar no IRC em #i2p
- **IRC:** Entre em #i2p-dev para discutir com os desenvolvedores no IRC

Por favor, inclua informações relevantes da página de logs do router disponível em: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Solicitamos que você compartilhe todo o texto da seção 'I2P Version and Running Environment' (Versão do I2P e Ambiente de Execução), bem como quaisquer erros ou avisos exibidos nos diversos logs mostrados na página.

---

### Tenho uma pergunta! {#question}

Ótimo! Encontre-nos no IRC:

- no `irc.freenode.net` canal `#i2p`
- no `IRC2P` canal `#i2p`

ou poste no [fórum](http://i2pforum.i2p/) e nós publicaremos aqui (com a resposta, esperamos).
