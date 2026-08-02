---
title: "SAM V3"
description: "Protocolo de Mensagens Anônimas Simples para aplicações I2P não-Java"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM é um protocolo cliente simples para interagir com o I2P. SAM é o protocolo recomendado para aplicações não-Java se conectarem à rede I2P, e é suportado por múltiplas implementações de roteador. Aplicações Java devem usar as APIs de streaming ou I2CP diretamente.

A versão 3 do SAM foi introduzida no lançamento do I2P 0.7.3 (maio de 2009) e é uma interface estável e suportada. A versão 3.1 também é estável e oferece suporte à opção de tipo de assinatura, o que é altamente recomendado. Versões 3.x mais recentes suportam recursos avançados. Observe que o i2pd atualmente não suporta a maioria dos recursos das versões 3.2 e 3.3.

Alternativas: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (obsoleto)](/docs/api/bob). Versões descontinuadas: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Bibliotecas SAM Conhecidas

Aviso: Alguns desses podem ser muito antigos ou sem suporte. Nenhum é testado, revisado ou mantido pelo projeto I2P, salvo indicação em contrário abaixo. Faça sua própria pesquisa.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Início Rápido

Para implementar uma aplicação básica ponto-a-ponto somente TCP, o cliente deve suportar os seguintes comandos:

- `HELLO VERSION MIN=3.1 MAX=3.1` - Necessário para todos os demais comandos
- `DEST GENERATE SIGNATURE_TYPE=7` - Para gerar nossa chave privada e destino
- `NAMING LOOKUP NAME=...` - Para converter endereços .i2p em destinos
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - Necessário para STREAM CONNECT e STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` - Para fazer conexões de saída
- `STREAM ACCEPT ID=...` - Para aceitar conexões de entrada

## Orientações Gerais para Desenvolvedores

### Design da Aplicação

As sessões SAM (ou, dentro do I2P, pools de túneis ou conjuntos de túneis) são projetadas para serem de longa duração. A maioria das aplicações precisará apenas de uma sessão, criada na inicialização e encerrada ao sair. O I2P é diferente do Tor, onde circuitos podem ser rapidamente criados e descartados. Pense cuidadosamente e consulte os desenvolvedores do I2P antes de projetar sua aplicação para usar mais de uma ou duas sessões simultâneas, ou para criar e descartar sessões rapidamente. A maioria dos modelos de ameaça não exigirá uma sessão exclusiva para cada conexão.

Além disso, certifique-se de que as configurações do seu aplicativo (e as orientações fornecidas aos usuários sobre as configurações do roteador, ou as configurações padrão do roteador caso você o inclua) farão com que seus usuários contribuam com mais recursos para a rede do que consumam. O I2P é uma rede ponto a ponto, e a rede não pode sobreviver se um aplicativo popular causar congestionamento permanente na rede.

### Compatibilidade e Testes

As implementações do roteador Java I2P e i2pd são independentes e possuem pequenas diferenças em comportamento, suporte a recursos e configurações padrão. Por favor, teste sua aplicação com a versão mais recente de ambos os roteadores.

O SAM do i2pd está habilitado por padrão; o SAM do Java I2P não está. Forneça instruções aos seus usuários sobre como habilitar o SAM no Java I2P (via /configclients no console do roteador) e/ou exiba uma mensagem de erro clara ao usuário caso a conexão inicial falhe, por exemplo: "verifique se o I2P está em execução e se a interface SAM está habilitada".

Os roteadores Java I2P e i2pd possuem padrões diferentes para quantidades de túneis. O padrão do Java é 2 e o padrão do i2pd é 5. Para a maioria dos casos com largura de banda baixa a média e contagem baixa a média de conexões, 2 ou 3 é suficiente. Especifique a quantidade de túneis na mensagem SESSION CREATE para obter desempenho consistente com os roteadores Java I2P e i2pd. Veja abaixo.

Para obter mais orientações aos desenvolvedores sobre como garantir que seu aplicativo use apenas os recursos de que precisa, consulte [nosso guia sobre como incorporar o I2P ao seu aplicativo](/docs/applications/embedding).

### Tipos de Assinatura e Criptografia

O I2P suporta múltiplos tipos de assinatura e criptografia. Por compatibilidade com versões anteriores, o SAM usa por padrão tipos antigos e ineficientes, portanto todos os clientes devem especificar tipos mais recentes.

O tipo de assinatura é especificado nos comandos DEST GENERATE e SESSION CREATE (para transiente). Todos os clientes devem definir `SIGNATURE_TYPE=7` (Ed25519).

O tipo de criptografia é especificado no comando SESSION CREATE. Múltiplos tipos de criptografia são permitidos. Os clientes devem definir `i2cp.leaseSetEncType=4` (apenas para ECIES-X25519) ou `i2cp.leaseSetEncType=6,4` (para MLKEM-768 e ECIES-X25519, para roteadores que suportam a API 0.9.67 ou superior).

## Alterações da versão 3

### Alterações da versão 3.0

A versão 3.0 foi introduzida na versão do I2P 0.7.3. O SAM v2 oferecia uma maneira de gerenciar vários sockets na mesma destinatário I2P *em paralelo*, ou seja, o cliente não precisava esperar os dados serem enviados com sucesso em um socket antes de enviar dados em outro socket. Porém, todos os dados passavam pelo mesmo socket cliente-SAM, o que era bastante complicado de gerenciar para o cliente.

O SAM v3 gerencia soquetes de maneira diferente: cada *soquete I2P* corresponde a um soquete único de cliente para SAM, o que é muito mais simples de manipular. Isso é semelhante ao [BOB](/docs/api/bob).

O SAM v3 também oferece uma porta UDP para enviar datagramas através do I2P e pode retransmitir de volta ao cliente os datagramas I2P recebidos em seu servidor de datagramas.

### Alterações na versão 3.1

A versão 3.1 foi introduzida no lançamento do Java I2P 0.9.14 (julho de 2014). O SAM 3.1 é a implementação mínima recomendada por oferecer suporte a tipos de assinatura melhores do que o SAM 3.0. O i2pd também suporta a maioria dos recursos do 3.1.

- DEST GENERATE e SESSION CREATE agora suportam um parâmetro SIGNATURE_TYPE.
- Os parâmetros MIN e MAX em HELLO VERSION agora são opcionais.
- Os parâmetros MIN e MAX em HELLO VERSION agora suportam versões de um único dígito, como "3".
- RAW SEND agora é suportado no socket da ponte.

### Alterações da versão 3.2

A versão 3.2 foi introduzida no lançamento do Java I2P 0.9.24 (janeiro de 2016). Observe que o i2pd atualmente não suporta a maioria dos recursos da versão 3.2.

#### Suporte a Portas e Protocolos I2CP

- Opções FROM_PORT e TO_PORT no SESSION CREATE
- Opção PROTOCOL no SESSION CREATE com STYLE=RAW
- Opções FROM_PORT e TO_PORT no STREAM CONNECT, DATAGRAM SEND e RAW SEND
- Opção PROTOCOL no RAW SEND
- DATAGRAM RECEIVED, RAW RECEIVED e fluxos ou datagramas recebidos ou reencaminhados incluem FROM_PORT e TO_PORT
- A opção de sessão RAW HEADER=true fará com que datagramas raw reencaminhados tenham uma linha inicial contendo PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- A primeira linha de datagramas enviados pela porta 7655 pode agora começar com qualquer versão 3.x
- A primeira linha de datagramas enviados pela porta 7655 pode conter qualquer uma das opções FROM_PORT, TO_PORT, PROTOCOL
- RAW RECEIVED inclui PROTOCOL=nnn

#### SSL e Autenticação

- USUÁRIO/SENHA nos parâmetros do HELLO para autorização. Veja [abaixo](#authorization).
- Configuração opcional de autorização com o comando AUTH. Veja [abaixo](#authorization-configuration-sam-32-or-higher-optional-feature).
- Suporte opcional a SSL/TLS no socket de controle. Veja [abaixo](#ssl).
- Opção STREAM FORWARD SSL=true

#### Multithreading

- São permitidas múltiplas operações STREAM ACCEPT pendentes simultâneas no mesmo ID de sessão.

#### Análise de Linha de Comando e Keepalive

- Comandos opcionais QUIT, STOP e EXIT para encerrar a sessão e o socket. Veja [abaixo](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- A análise de comandos tratará corretamente o UTF-8
- A análise de comandos lida de forma confiável com espaços em branco dentro de aspas
- Uma barra invertida '\\' pode escapar aspas na linha de comando
- Recomenda-se que o servidor mapeie comandos para maiúsculas, para facilitar testes via telnet.
- Valores de opção vazios, como PROTOCOL ou PROTOCOL=, podem ser permitidos, dependendo da implementação.
- PING/PONG para manter a conexão ativa. Veja abaixo.
- Os servidores podem implementar timeouts para o comando HELLO ou comandos subsequentes, dependendo da implementação.

### Alterações na versão 3.3

A versão 3.3 foi introduzida no lançamento do Java I2P 0.9.25 (março de 2016). Observe que o i2pd atualmente não oferece suporte à maioria dos recursos da versão 3.3.

- A mesma sessão pode ser usada simultaneamente para streams, datagramas e modo bruto (raw). Pacotes e streams recebidos serão roteados com base no protocolo I2P e na porta de destino. Veja [a seção PRIMARY abaixo](#sam-primary-sessions-v33-and-higher).
- Os comandos DATAGRAM SEND e RAW SEND agora suportam as opções SEND_TAGS, TAG_THRESHOLD, EXPIRES e SEND_LEASESET. Veja [a seção de envio de datagramas abaixo](#sending-repliable-or-raw-datagrams).

### Mudanças de 2025-04

Duas propostas foram aprovadas e incorporadas à especificação aqui em abril de 2025. Não houve alteração de versão para indicar suporte. Algumas implementações ainda não dão suporte, e em outras, o suporte é preliminar.

- Suporte a Datagram 2/3 (proposta 163). Especificado em SESSION CREATE e SESSION ADD (subsessões). Veja abaixo.
- Recuperação de opções de leaseset (proposta 167). Especificado com NAMING LOOKUP OPTIONS=true. Veja abaixo.

## Protocolo versão 3

### Visão Geral da Especificação do Simple Anonymous Messaging (SAM) Versão 3.3

O aplicativo cliente se comunica com a ponte SAM, que lida com toda a funcionalidade do I2P (usando a [biblioteca de streaming](/docs/api/streaming) para fluxos virtuais, ou [I2CP](/docs/protocol/i2cp) diretamente para datagramas).

Por padrão, a comunicação entre o cliente e a ponte SAM é não criptografada e não autenticada. A ponte SAM pode suportar conexões SSL/TLS; detalhes de configuração e implementação estão fora do escopo desta especificação. A partir da versão SAM 3.2, são suportados parâmetros opcionais de autenticação usuário/senha durante a negociação inicial e podem ser exigidos pela ponte.

As comunicações I2P podem assumir várias formas distintas:

- [Streams virtuais](/docs/api/streaming)
- [Datagramas autenticados e com resposta](/docs/specs/datagrams#repliable) (mensagens com campo FROM)
- [Datagramas anônimos](/docs/specs/datagrams#raw) (mensagens anônimas brutas)
- [Datagram2](/docs/specs/datagrams#datagram2) (um novo formato autenticado e com resposta)
- [Datagram3](/docs/specs/datagrams#datagram3) (um novo formato com resposta, mas não autenticado)

As comunicações I2P são suportadas por sessões I2P, e cada sessão I2P está vinculada a um endereço (chamado destino). Uma sessão I2P está associada a um dos três tipos acima e não pode transportar comunicações de outro tipo, a menos que use [sessões PRIMÁRIAS](#sam-primary-sessions-v33-and-higher).

### Codificação e Escapamento

Todas essas mensagens SAM são enviadas em uma única linha, terminadas pelo caractere de nova linha (\\n). Antes do SAM 3.2, somente ASCII de 7 bits era suportado. A partir do SAM 3.2, a codificação deve ser UTF-8. Quaisquer chaves ou valores codificados em UTF-8 devem funcionar.

A formatação mostrada nesta especificação abaixo é apenas para facilitar a leitura, e embora as duas primeiras palavras de cada mensagem devam permanecer na ordem específica, a ordem dos pares chave=valor pode mudar (por exemplo, "UM DOIS A=B C=D" ou "UM DOIS C=D A=B" são ambas construções perfeitamente válidas). Além disso, o protocolo diferencia maiúsculas de minúsculas. A seguir, exemplos de mensagens são precedidos por "->" para mensagens enviadas pelo cliente para a ponte SAM, e por "<-" para mensagens enviadas pela ponte SAM para o cliente.

A linha básica de comando ou resposta assume uma das seguintes formas:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
COMANDO sem SUBCOMANDO é suportado apenas para alguns novos comandos no SAM 3.2.

Os pares chave=valor devem ser separados por um único espaço. (A partir do SAM 3.2, múltiplos espaços são permitidos.) Os valores devem ser colocados entre aspas duplas se contiverem espaços, por exemplo: chave="texto com espaços". (Antes do SAM 3.2, isso não funcionava de forma confiável em algumas implementações))

Antes do SAM 3.2, não havia mecanismo de escape. A partir do SAM 3.2, aspas duplas podem ser escapadas com uma barra invertida '\\' e uma barra invertida pode ser representada como duas barras invertidas '\\\\'.

### Valores vazios

A partir do SAM 3.2, valores de opções vazios como KEY, KEY= ou KEY="" podem ser permitidos, dependendo da implementação.

### Sensibilidade a Maiúsculas e Minúsculas

O protocolo, conforme especificado, diferencia maiúsculas de minúsculas. Recomenda-se, embora não seja obrigatório, que o servidor mapeie comandos para letras maiúsculas, facilitando testes via telnet. Isso permitiria, por exemplo, que "hello version" funcionasse. Isso depende da implementação. Não mapeie chaves ou valores para letras maiúsculas, pois isso corromperia as opções [I2CP](/docs/protocol/i2cp).

### Handshake de Conexão SAM

Nenhuma comunicação SAM pode ocorrer até que o cliente e a ponte concordem em uma versão de protocolo, o que é feito enviando o cliente um HELLO e a ponte enviando um HELLO REPLY:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
e

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
A partir da versão 3.1 (I2P 0.9.14), os parâmetros MIN e MAX são opcionais. O SAM sempre retornará a versão mais alta possível dentro das restrições MIN e MAX, ou a versão atual do servidor se nenhuma restrição for fornecida.

Se a ponte SAM não conseguir encontrar uma versão adequada, ela responde com:

```
<- HELLO REPLY RESULT=NOVERSION
```
Se ocorrer algum erro, como um formato de solicitação inválido, ele responde com:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

O socket de controle do servidor pode opcionalmente oferecer suporte a SSL/TLS, conforme configurado no servidor e no cliente. As implementações podem oferecer outras camadas de transporte também; isso está fora do escopo da definição do protocolo.

#### Autorização

Para autorização, o cliente adiciona USER="xxx" PASSWORD="yyy" aos parâmetros do HELLO. Aspas duplas para usuário e senha são recomendadas, mas não obrigatórias. Uma aspa dupla dentro de um usuário ou senha deve ser escapada com uma barra invertida. Em caso de falha, o servidor responderá com um I2P_ERROR e uma mensagem. Recomenda-se que SSL seja habilitado em qualquer servidor SAM onde a autorização seja exigida.

#### Tempos limite

Servidores podem implementar tempos limite para o HELLO ou comandos subsequentes, dependendo da implementação. Os clientes devem enviar imediatamente o HELLO e o próximo comando após a conexão.

Se ocorrer um tempo limite antes do recebimento do HELLO, a ponte responde com:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
e então se desconecta.

Se ocorrer um tempo limite após o recebimento do HELLO, mas antes do próximo comando, a ponte responde com:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
e então se desconecta.

### Portas e Protocolo I2CP

A partir do SAM 3.2, as portas e o protocolo [I2CP](/docs/protocol/i2cp) podem ser especificados pelo remetente cliente SAM para serem repassados ao [I2CP](/docs/protocol/i2cp), e a ponte SAM repassará ao cliente SAM as informações de porta e protocolo [I2CP](/docs/protocol/i2cp) recebidas.

Para FROM_PORT e TO_PORT, a faixa válida é 0-65535, e o padrão é 0.

Para PROTOCOL, que pode ser especificado apenas para RAW, a faixa válida é 0-255, e o padrão é 18.

Para comandos SESSION, as portas e o protocolo especificados são os padrões para aquela sessão. Para fluxos ou datagramas individuais, as portas e o protocolo especificados substituem os padrões da sessão. Para fluxos ou datagramas recebidos, as portas e o protocolo indicados são os recebidos via [I2CP](/docs/protocol/i2cp).

#### Diferenças importantes em relação ao IP padrão

As portas I2CP são para sockets e datagramas I2P. Elas não têm relação com seus sockets locais que se conectam ao SAM.

- A porta 0 é válida e possui significado especial.
- As portas 1-1023 não são especiais nem privilegiadas.
- Servidores escutam na porta 0 por padrão, o que significa "todas as portas".
- Clientes enviam para a porta 0 por padrão, o que significa "qualquer porta".
- Clientes enviam da porta 0 por padrão, o que significa "não especificado".
- Servidores podem ter um serviço escutando na porta 0 e outros serviços escutando em portas superiores. Nesse caso, o serviço na porta 0 é o padrão e será usado se a porta do socket ou datagrama recebido não corresponder a outro serviço.
- A maioria dos destinos I2P executa apenas um serviço, portanto você pode usar os valores padrão e ignorar a configuração de portas I2CP.
- É necessário o SAM 3.2 ou 3.3 para especificar portas I2CP.
- Se você não precisa de portas I2CP, não precisa do SAM 3.2 ou 3.3; o SAM 3.1 é suficiente.
- O protocolo 0 é válido e significa "qualquer protocolo". Isso não é recomendado e provavelmente não funcionará.
- Os sockets I2P são rastreados por um ID de conexão interno. Portanto, não é necessário que a 5-tupla dest:porta:dest:porta:protocolo seja única. Por exemplo, pode haver múltiplos sockets com as mesmas portas entre dois destinos. Os clientes não precisam escolher uma "porta livre" para uma conexão de saída.

Se você estiver desenvolvendo uma aplicação SAM 3.3 com múltiplas subsessões, pense cuidadosamente sobre como usar portas e protocolos de forma eficaz. Veja a especificação [I2CP](/docs/protocol/i2cp) para obter mais informações.

### Sessões SAM

Uma sessão SAM é criada quando um cliente abre um socket para a ponte SAM, realiza um handshake e envia uma mensagem SESSION CREATE, e a sessão é encerrada quando o socket é desconectado.

Cada Destino I2P registrado está exclusivamente associado a um ID de sessão (ou apelido). Os IDs de sessão, incluindo IDs de subsessão para sessões PRIMÁRIAS, devem ser globalmente únicos no servidor SAM. Para evitar possíveis colisões de ID com outros clientes, a melhor prática é que o cliente gere os IDs aleatoriamente.

Cada sessão está exclusivamente associada a:

- o socket a partir do qual o cliente cria a sessão
- seu ID (ou apelido)

#### Solicitação de Criação de Sessão

A mensagem de criação de sessão pode usar apenas uma dessas formas (mensagens recebidas por outras formas são respondidas com uma mensagem de erro):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION especifica qual destino deve ser usado para enviar e receber mensagens/fluxos. O $privkey é a representação base 64 da concatenação da [Destination](/docs/specs/common-structures#type_Destination), seguida pela [Private Key](/docs/specs/common-structures#type_PrivateKey), seguida pela [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), opcionalmente seguida pela [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), que possui 663 ou mais bytes em formato binário e 884 ou mais bytes em base 64, dependendo do tipo de assinatura. O formato binário é especificado em Arquivo de Chave Privada. Veja notas adicionais sobre a [Private Key](/docs/specs/common-structures#type_PrivateKey) na seção Geração de Chave de Destino abaixo.

Se a chave privada de assinatura for composta apenas por zeros, a seção [Assinatura Offline](/docs/specs/common-structures#struct_OfflineSignature) é incluída. Assinaturas offline são suportadas apenas para sessões STREAM e RAW. Assinaturas offline não podem ser criadas com DESTINATION=TRANSIENT. O formato da seção de assinatura offline é:

1. Carimbo de tempo de expiração (4 bytes, big endian, segundos desde a época, reinicia em 2106)
2. Tipo de assinatura da Chave Pública de Assinatura transitória (2 bytes, big endian)
3. Chave Pública de Assinatura transitória (comprimento conforme especificado pelo tipo de assinatura transitória)
4. Assinatura dos três campos acima pela chave offline (comprimento conforme especificado pelo tipo de assinatura do destino)
5. Chave Privada de Assinatura transitória (comprimento conforme especificado pelo tipo de assinatura transitória)

Se o destino for especificado como TRANSIENTE, a ponte SAM cria um novo destino. A partir da versão 3.1 (I2P 0.9.14), se o destino for TRANSIENTE, o parâmetro opcional SIGNATURE_TYPE é suportado. O valor de SIGNATURE_TYPE pode ser qualquer nome (por exemplo, ECDSA_SHA256_P256, sem distinção entre maiúsculas e minúsculas) ou número (por exemplo, 1) suportado por [Certificados de Chave](/docs/specs/common-structures#type_Certificate). O padrão é DSA_SHA1, que NÃO é o que você deseja. Para a maioria das aplicações, por favor especifique SIGNATURE_TYPE=7.

$nickname é a escolha do cliente. Espaços em branco não são permitidos.

Opções adicionais fornecidas são passadas para a configuração da sessão I2P caso não sejam interpretadas pela ponte SAM (por exemplo, outbound.length=0).

Os roteadores Java I2P e i2pd possuem padrões diferentes para quantidades de túneis. O padrão do Java é 2 e o padrão do i2pd é 5. Para a maioria dos casos com largura de banda baixa a média e com contagem baixa a média de conexões, 2 ou 3 é suficiente. Especifique as quantidades de túneis na mensagem SESSION CREATE para obter desempenho consistente com os roteadores Java I2P e i2pd, usando opções como, por exemplo, inbound.quantity=3 outbound.quantity=3. Essas e outras opções [estão documentadas nos links abaixo](#tunnel-i2cp-and-streaming-options).

A própria ponte SAM já deve estar configurada com qual roteador ela deve se comunicar através da I2P (embora, se necessário, possa haver uma maneira de fornecer uma substituição, por exemplo, i2cp.tcp.host=localhost e i2cp.tcp.port=7654).

#### Resposta de Criação de Sessão

Após receber a mensagem de criação de sessão, a ponte SAM responderá com uma mensagem de status de sessão, conforme a seguir:

Se a criação foi bem-sucedida:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
A $privkey é a representação em base 64 da concatenação da [Destination](/docs/specs/common-structures#type_Destination), seguida pela [Private Key](/docs/specs/common-structures#type_PrivateKey), seguida pela [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), opcionalmente seguida pela [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), o que resulta em 663 ou mais bytes em formato binário e 884 ou mais bytes em base 64, dependendo do tipo de assinatura. O formato binário é especificado em Private Key File.

Se o SESSION CREATE contiver uma chave privada de assinatura composta apenas por zeros e uma seção de [Assinatura Offline](/docs/specs/common-structures#struct_OfflineSignature), a resposta SESSION STATUS incluirá os mesmos dados no mesmo formato. Veja a seção SESSION CREATE acima para obter detalhes.

Se o apelido já estiver associado a uma sessão:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Se o destino já estiver em uso:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Se o destino não for uma chave de destino privado válida:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Se algum outro erro ocorreu:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Se não estiver OK, a MENSAGEM deve conter informações legíveis para humanos sobre o motivo pelo qual a sessão não pôde ser criada.

Observe que o roteador constrói túneis antes de responder com SESSION STATUS. Isso pode levar vários segundos, ou, durante a inicialização do roteador ou em caso de congestão severa da rede, um minuto ou mais. Se for malsucedido, o roteador não responderá com uma mensagem de falha por vários minutos. Não defina um tempo limite curto esperando pela resposta. Não abandone a sessão enquanto a construção do túnel estiver em andamento e não tente novamente.

As sessões SAM vivem e terminam com o socket ao qual estão associadas. Quando o socket é fechado, a sessão é encerrada, e todas as comunicações usando essa sessão são interrompidas ao mesmo tempo. E da mesma forma, quando a sessão é encerrada por qualquer motivo, a ponte SAM fecha o socket.

### SAM Streams Virtuais

Os fluxos virtuais são enviados de forma confiável e em ordem, com notificação de falha ou sucesso assim que disponível.

Os fluxos são sockets de comunicação bidirecional entre duas destinações I2P, mas sua abertura precisa ser solicitada por uma delas. A partir de agora, comandos CONNECT são usados pelo cliente SAM para essa solicitação. Comandos FORWARD / ACCEPT são usados pelo cliente SAM quando ele deseja escutar solicitações provenientes de outras destinações I2P.

### SAM Streams Virtuais: CONNECT

Um cliente solicita uma conexão por:

- abrindo um novo socket com a ponte SAM
- passando o mesmo handshake HELLO conforme acima
- enviando o comando STREAM CONNECT

#### Solicitação de Conexão

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Isso estabelece uma nova conexão virtual da sessão local cujo ID é $nickname ao par especificado.

O destino é $destination, que é a codificação base 64 da [Destination](/docs/specs/common-structures#type_Destination), com 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

**OBSERVAÇÃO:** Desde cerca de 2014 (SAM v3.1), o Java I2P também suporta nomes de host e endereços b32 para o $destination, embora isso anteriormente não fosse documentado. Nomes de host e endereços b32 são agora oficialmente suportados pelo Java I2P a partir da versão 0.9.48. O roteador i2pd suporta nomes de host e endereços b32 a partir da versão 2.38.0 (0.9.50). Para ambos os roteadores, o suporte a "b32" inclui o suporte a endereços "b33" estendidos para destinos ocultados.

#### Resposta de Conexão

Se SILENT=true for informado, a ponte SAM não emitirá nenhuma outra mensagem no socket. Se a conexão falhar, o socket será fechado. Se a conexão for bem-sucedida, todos os dados restantes que passam pelo socket atual serão encaminhados para e a partir do par de destino I2P conectado.

Se SILENT=false, que é o valor padrão, a ponte SAM envia uma última mensagem ao seu cliente antes de encaminhar ou desligar o socket:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
O valor de RESULTADO pode ser um dos seguintes:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Se o RESULTADO for OK, todos os dados restantes que passam pelo soquete atual são encaminhados de e para o par de destino I2P conectado. Se a conexão não foi possível (tempo limite, etc), o RESULTADO conterá o valor de erro apropriado (acompanhado por uma MENSAGEM opcional legível por humanos), e a ponte SAM fecha o soquete.

O tempo limite interno para conexão de stream do roteador é de aproximadamente um minuto, dependendo da implementação. Não defina um tempo limite mais curto ao aguardar a resposta.

### Fluxos Virtuais SAM: ACEITAR

Um cliente aguarda uma solicitação de conexão de entrada por:

- abrindo um novo socket com a ponte SAM
- passando o mesmo handshake HELLO conforme acima
- enviando o comando STREAM ACCEPT

#### Aceitar Solicitação

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Isso faz a sessão ${nickname} escutar uma solicitação de conexão recebida da rede I2P. ACCEPT não é permitido enquanto houver um FORWARD ativo na sessão.

A partir do SAM 3.2, são permitidas múltiplas solicitações STREAM ACCEPT simultâneas no mesmo ID de sessão (mesmo com a mesma porta). Antes da versão 3.2, as aceitações simultâneas falhavam com ALREADY_ACCEPTING. Observação: o Java I2P também suporta aceitações simultâneas no SAM 3.1, a partir da versão 0.9.24 (2016-01). O i2pd também suporta aceitações simultâneas no SAM 3.1, a partir da versão 2.50.0 (2023-12).

#### Aceitar Resposta

Se SILENT=true for informado, a ponte SAM não emitirá nenhuma outra mensagem no socket. Se a aceitação falhar, o socket será fechado. Se a aceitação for bem-sucedida, todos os dados restantes que passam pelo socket atual serão encaminhados da e para a peer de destino I2P conectada. Para maior confiabilidade, e para receber o destino das conexões recebidas, recomenda-se SILENT=false.

Se SILENT=false, que é o valor padrão, a ponte SAM responde com:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
O valor de RESULTADO pode ser um dos seguintes:

```
OK
I2P_ERROR
INVALID_ID
```
Se o resultado não for OK, o socket é fechado imediatamente pela ponte SAM. Se o resultado for OK, a ponte SAM começa a aguardar uma solicitação de conexão de entrada de outro par I2P. Quando uma solicitação chega, a ponte SAM a aceita e:

Se SILENT=true for informado, a ponte SAM não emitirá nenhuma outra mensagem no soquete do cliente. Todos os dados restantes que passam pelo soquete atual são encaminhados de e para o par de destino I2P conectado.

Se SILENT=false for informado, que é o valor padrão, a ponte SAM envia ao cliente uma linha ASCII contendo a chave pública da destinatário na base64 do par solicitante, e informações adicionais somente para o SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Após esta linha terminada em '\\n', todos os dados restantes que passam pelo socket atual são encaminhados para e a partir do par de destino I2P conectado, até que um dos pares feche o socket.

#### Erros após OK

Em casos raros, a ponte SAM pode encontrar um erro após enviar RESULT=OK, mas antes de uma conexão chegar e enviar a linha $destination ao cliente. Esses erros podem incluir desligamento do roteador, reinício do roteador e fechamento da sessão. Nesses casos, quando SILENT=false, a ponte SAM pode, mas não é obrigada a (dependente da implementação), enviar a linha:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
antes de fechar imediatamente o socket. Esta linha não é, é claro, decodificável como um destino Base 64 válido.

### Streams Virtuais SAM: FORWARD

Um cliente pode usar um servidor de soquete comum e aguardar solicitações de conexão provenientes do I2P. Para isso, o cliente deve:

- abrir um novo socket com a ponte SAM
- enviar o mesmo handshake HELLO conforme acima
- enviar o comando de encaminhamento

#### Solicitação de Encaminhamento

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Isso faz a sessão ${nickname} escutar solicitações de conexão recebidas da rede I2P. FORWARD não é permitido enquanto houver um ACCEPT pendente na sessão.

#### Resposta de Encaminhamento

SILENT tem como padrão false. Independentemente de SILENT ser true ou false, a ponte SAM sempre responde com uma mensagem STREAM STATUS. Observe que esse é um comportamento diferente de STREAM ACCEPT e STREAM CONNECT quando SILENT=true. A mensagem STREAM STATUS é:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
O valor de RESULTADO pode ser um dos seguintes:

```
OK
I2P_ERROR
INVALID_ID
```
$host é o nome do host ou endereço IP do servidor de soquete ao qual o SAM encaminhará as solicitações de conexão. Se não for fornecido, o SAM usa o IP do soquete que emitiu o comando de encaminhamento.

$port é o número da porta do servidor de soquete para o qual o SAM encaminhará as solicitações de conexão. É obrigatório.

Quando uma solicitação de conexão chega do I2P, a ponte SAM abre uma conexão de soquete para $host:$port. Se for aceita em menos de 3 segundos, o SAM aceitará a conexão do I2P e então:

Se SILENT=true for informado, todos os dados que passam pelo socket atual obtido são encaminhados de e para o par de destino I2P conectado.

Se SILENT=false for passado, que é o valor padrão, a ponte SAM envia pelo socket obtido uma linha ASCII contendo a chave pública da destinatário em base64 do par solicitante, e informações adicionais somente para o SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Após esta linha terminada em '\\n', todos os dados restantes que passam pelo socket são encaminhados para e do par de destino I2P conectado, até que um dos lados feche o socket.

A partir do SAM 3.2, se SSL=true for especificado, o socket de encaminhamento será sobre SSL/TLS.

O roteador I2P deixará de escutar solicitações de conexão de entrada assim que o socket "forwarding" for fechado.

### Datagramas SAM

O SAMv3 fornece mecanismos para enviar e receber datagramas por meio de soquetes locais de datagrama. Algumas implementações do SAMv3 também suportam o método mais antigo v1/v2 de envio/recebimento de datagramas pelo soquete da ponte SAM. Ambos são documentados abaixo.

O I2P suporta quatro tipos de datagramas:

- Os datagramas retransmissíveis e autenticados são prefixados com o destino do remetente e contêm a assinatura do remetente, para que o receptor possa verificar se o destino do remetente não foi falsificado e possa responder ao datagrama. O novo formato Datagram2 também é retransmissível e autenticado.
- O novo formato Datagram3 é retransmissível, mas não autenticado. As informações do remetente não são verificadas.
- Datagramas brutos (raw) não contêm o destino do remetente nem uma assinatura.

As portas I2CP padrão são definidas tanto para datagramas com resposta quanto para datagramas brutos. A porta I2CP pode ser alterada para datagramas brutos.

Um padrão comum no design de protocolos é o envio de datagramas com resposta para servidores, incluindo algum identificador, e o servidor responder com um datagrama bruto que contém esse identificador, permitindo que a resposta seja correlacionada com a solicitação. Esse padrão de design elimina a sobrecarga substancial dos datagramas com resposta nas respostas. Todas as escolhas de protocolos e portas I2CP são específicas para cada aplicação, e os projetistas devem levar essas questões em consideração.

Veja também as notas importantes sobre MTU de datagrama na seção abaixo.

#### Enviando Datagramas Repliáveis ou Brutos

Embora o I2P não contenha intrinsecamente um endereço FROM, para facilitar o uso é fornecida uma camada adicional chamada datagramas com resposta - mensagens não ordenadas e não confiáveis de até 31744 bytes que incluem um endereço FROM (restando até 1KB para cabeçalhos). Esse endereço FROM é autenticado internamente pelo SAM (fazendo uso da chave de assinatura do destino para verificar a origem) e inclui prevenção contra replay.

O tamanho mínimo é 1. Para melhor confiabilidade na entrega, o tamanho máximo recomendado é aproximadamente 11 KB. A confiabilidade é inversamente proporcional ao tamanho da mensagem, talvez até exponencialmente.

Após estabelecer uma sessão SAM com STYLE=DATAGRAM ou STYLE=RAW, o cliente pode enviar datagramas com resposta ou datagramas brutos pela porta UDP do SAM (7655 por padrão).

A primeira linha de um datagrama enviado por esta porta deve estar no seguinte formato. Tudo isso está em uma única linha (separado por espaços), mostrado em várias linhas para maior clareza:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 é a versão do SAM. A partir do SAM 3.2, qualquer versão 3.x é permitida.
- $nickname é o ID da sessão DATAGRAM que será usada
- O destino é $destination, que é a codificação base 64 da [Destination](/docs/specs/common-structures#type_Destination), com 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura. **OBSERVAÇÃO:** Desde cerca de 2014 (SAM v3.1), o Java I2P também suporta nomes de host e endereços b32 para o $destination, mas isso anteriormente não era documentado. Nomes de host e endereços b32 são agora oficialmente suportados pelo Java I2P a partir da versão 0.9.48. O roteador i2pd atualmente não suporta nomes de host nem endereços b32; o suporte pode ser adicionado em uma versão futura.
- Todas as opções são configurações por datagrama que substituem os padrões especificados no SESSION CREATE.
- As opções da versão 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES e SEND_LEASESET serão repassadas ao [I2CP](/docs/protocol/i2cp) se suportadas. Veja [a especificação do I2CP](/docs/protocol/i2cp#msg_SendMessageExpire) para detalhes. O suporte pelo servidor SAM é opcional, e essas opções serão ignoradas se não forem suportadas.
- esta linha termina com '\\n'.

A primeira linha será descartada pelo SAM antes de enviar os dados restantes da mensagem para o destino especificado.

Para um método alternativo de envio de datagramas com resposta e brutos, consulte [DATAGRAM SEND e RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagramas Replícaveis SAM: Recebendo um Datagrama

Os datagramas recebidos são escritos pelo SAM no socket a partir do qual a sessão de datagrama foi aberta, caso uma PORTA de encaminhamento não seja especificada no comando SESSION CREATE. Esta é a maneira compatível com v1/v2 de receber datagramas.

Quando um datagrama chega, a ponte o entrega ao cliente por meio da mensagem:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
A origem é $destination, que é a codificação base 64 da [Destination](/docs/specs/common-structures#type_Destination), com 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A ponte SAM nunca expõe ao cliente os cabeçalhos de autenticação ou outros campos, apenas os dados fornecidos pelo remetente. Isso continua até que a sessão seja encerrada (quando o cliente desconecta).

#### Encaminhamento de Datagramas Brutos ou Reutilizáveis

Ao criar uma sessão de datagrama, o cliente pode solicitar ao SAM que encaminhe mensagens recebidas para um ip:porta especificado. Isso é feito emitindo o comando CREATE com as opções PORT e HOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
O $privkey é o base 64 da concatenação da [Destination](/docs/specs/common-structures#type_Destination), seguida pela [Private Key](/docs/specs/common-structures#type_PrivateKey), seguida pela [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), opcionalmente seguida pela [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), totalizando 884 ou mais caracteres em base 64 (663 ou mais bytes em binário), dependendo do tipo de assinatura. O formato binário é especificado em Private Key File.

Assinaturas offline são suportadas para datagramas RAW, DATAGRAM2 e DATAGRAM3, mas não para DATAGRAM. Veja a seção CRIAR SESSÃO acima e a seção DATAGRAM2/3 abaixo para detalhes.

$host é o nome do host ou endereço IP do servidor de datagramas para o qual o SAM encaminhará os datagramas. Se não for fornecido, o SAM usa o IP do socket que emitiu o comando de encaminhamento.

$port é o número da porta do servidor datagrama para o qual o SAM encaminhará os datagramas. Se $port não for definido, os datagramas NÃO serão encaminhados, eles serão recebidos no socket de controle, da maneira compatível com v1/v2.

As opções adicionais fornecidas são passadas para a configuração da sessão I2P se não forem interpretadas pela ponte SAM (por exemplo, outbound.length=0). Essas opções [são documentadas abaixo](#tunnel-i2cp-and-streaming-options).

Datagramas encaminhados com resposta habilitada sempre têm como prefixo o destino em base64, exceto para Datagrama3, veja abaixo. Quando um datagrama com resposta habilitada chega, a ponte envia ao host:porta especificado um pacote UDP contendo os seguintes dados:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Datagramas brutos encaminhados são enviados como estão para o host:porta especificado sem um prefixo. O pacote UDP contém os seguintes dados:

```
$datagram_payload
```
A partir do SAM 3.2, quando HEADER=true é especificado em SESSION CREATE, o datagrama bruto encaminhado será precedido por uma linha de cabeçalho da seguinte forma:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
O $destination é a codificação base 64 da [Destination](/docs/specs/common-structures#type_Destination), que possui 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

#### Datagramas Anônimos SAM (Bruto)

Maximizando ao máximo a largura de banda do I2P, o SAM permite que clientes enviem e recebam datagramas anônimos, deixando a autenticação e as informações de resposta por conta do próprio cliente. Esses datagramas são não confiáveis e sem ordem definida, e podem ter até 32768 bytes.

O tamanho mínimo é 1. Para melhor confiabilidade na entrega, o tamanho máximo recomendado é de aproximadamente 11 KB.

Após estabelecer uma sessão SAM com STYLE=RAW, o cliente pode enviar datagramas anônimos através da ponte SAM exatamente da mesma maneira que [enviar datagramas com resposta ou brutos](#sending-repliable-or-raw-datagrams).

Ambas as formas de receber datagramas também estão disponíveis para datagramas anônimos.

Os datagramas recebidos são escritos pelo SAM no socket a partir do qual a sessão de datagrama foi aberta, caso uma PORTA de encaminhamento não seja especificada no comando SESSION CREATE. Esta é a maneira compatível com v1/v2 de receber datagramas.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Quando datagramas anônimos devem ser encaminhados para algum host:porta, a ponte envia para o host:porta especificado uma mensagem contendo os seguintes dados:

```
$datagram_payload
```
A partir do SAM 3.2, quando HEADER=true é especificado em SESSION CREATE, o datagrama bruto encaminhado será precedido por uma linha de cabeçalho da seguinte forma:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Para um método alternativo de envio de datagramas anônimos, consulte [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagrama 2/3

Datagrama 2/3 são novos formatos especificados no início de 2025. Atualmente não existem implementações conhecidas. Consulte a documentação da implementação para obter o status atual. Veja [a especificação](/docs/specs/datagrams) para mais informações.

Não há planos atuais para aumentar a versão do SAM para indicar suporte a Datagrama 2/3. Isso pode ser problemático, pois algumas implementações podem desejar suportar Datagrama 2/3, mas não os recursos do SAM v3.3. Qualquer alteração de versão está a ser definida (TBD).

Tanto o Datagram2 quanto o Datagram3 são passíveis de resposta. Apenas o Datagram2 é autenticado.

Datagram2 é idêntico aos datagramas com resposta do ponto de vista do SAM. Ambos são autenticados. Apenas o formato I2CP e a assinatura são diferentes, mas isso não é visível para os clientes SAM. Datagram2 também suporta assinaturas offline, portanto pode ser usado por destinos com assinatura offline.

A intenção é que o Datagram2 substitua os datagramas com resposta (Repliable) para novas aplicações que não exigem compatibilidade com versões anteriores. O Datagram2 oferece proteção contra repetição (replay protection), que não está presente nos datagramas Repliable. Se a compatibilidade com versões anteriores for necessária, uma aplicação pode suportar tanto Datagram2 quanto Repliable na mesma sessão, usando sessões PRIMARY do SAM 3.3.

O Datagram3 é repliável, mas não autenticado. O campo 'from' no formato I2CP é um hash, não um destino. O $destination enviado pelo servidor SAM para o cliente será um hash base64 de 44 bytes. Para convertê-lo em um destino completo para resposta, decodifique-o de base64 para 32 bytes binários, depois codifique em base32 para obter 52 caracteres e acrescente ".b32.i2p" para uma PESQUISA DE NOME. Como de costume, os clientes devem manter seu próprio cache para evitar pesquisas de nome repetidas.

Os projetistas de aplicações devem ter extrema cautela e considerar as implicações de segurança dos datagramas não autenticados.

#### Considerações sobre MTU de Datagrama V3

Datagramas I2P podem ser maiores que o MTU típico da internet de 1500. Datagramas enviados localmente e datagramas reencaminhados com resposta habilitada, prefixados com o destino em base64 de 516+ bytes, provavelmente excederão esse MTU. No entanto, os MTUs de localhost em sistemas Linux são tipicamente muito maiores, por exemplo, 65536. Os MTUs de localhost variam conforme o sistema operacional. Datagramas I2P nunca serão maiores que 65536. O tamanho do datagrama depende do protocolo da aplicação.

Se o cliente SAM estiver local em relação ao servidor SAM e o sistema suportar um MTU maior, então os datagramas não serão fragmentados localmente. No entanto, se o cliente SAM for remoto, os datagramas IPv4 serão fragmentados e os datagramas IPv6 falharão (IPv6 não suporta fragmentação UDP).

Desenvolvedores de bibliotecas e aplicações cliente devem estar cientes desses problemas e documentar recomendações para evitar fragmentação e prevenir perda de pacotes, especialmente em conexões remotas cliente-servidor SAM.

#### ENVIO DE DATAGRAMA, ENVIO BRUTO (Manipulação de Datagrama Compatível com V1/V2)

No SAM V3, a maneira preferida de enviar datagramas é por meio do socket de datagrama na porta 7655, conforme documentado acima. No entanto, datagramas com resposta podem ser enviados diretamente pelo socket da ponte SAM usando o comando DATAGRAM SEND, conforme documentado em [SAM V1](/docs/api/sam) e [SAM V2](/docs/api/samv2).

A partir da versão 0.9.14 (versão 3.1), datagramas anônimos podem ser enviados diretamente através do socket da ponte SAM usando o comando RAW SEND, conforme documentado em [SAM V1](/docs/api/sam) e [SAM V2](/docs/api/samv2).

A partir da versão 0.9.24 (versão 3.2), DATAGRAM SEND e RAW SEND podem incluir os parâmetros FROM_PORT=nnnn e/ou TO_PORT=nnnn para substituir as portas padrão. A partir da versão 0.9.24 (versão 3.2), RAW SEND pode incluir o parâmetro PROTOCOL=nnn para substituir o protocolo padrão.

Esses comandos *não* suportam o parâmetro ID. Os datagramas são enviados para a sessão do tipo DATAGRAM ou RAW mais recentemente criada, conforme apropriado. O suporte ao parâmetro ID pode ser adicionado em uma versão futura.

Os formatos DATAGRAM2 e DATAGRAM3 *não* são compatíveis com as versões V1/V2.

### Sessões SAM PRIMÁRIAS (V3.3 e superiores)

*A versão 3.3 foi introduzida no lançamento do I2P 0.9.25.*

*Em uma versão anterior desta especificação, as sessões PRIMÁRIAS eram conhecidas como sessões MESTRE. Tanto no `i2pd` quanto no `I2P+`, elas ainda são conhecidas apenas como sessões MESTRE.*

O SAM v3.3 adiciona suporte para executar streaming, datagramas e subsessões brutas na mesma sessão primária, e para executar múltiplas subsessões do mesmo estilo. Todo o tráfego das subsessões utiliza um único destino, ou conjunto de túneis. O roteamento de tráfego para a I2P é baseado nas opções de porta e protocolo das subsessões.

Para criar subsessões multiplexadas, você deve criar uma sessão primária e depois adicionar subsessões à sessão primária. Cada subsessão deve ter um ID único e um protocolo e porta de escuta únicos. As subsessões também podem ser removidas da sessão primária.

Com uma sessão PRIMÁRIA e uma combinação de sub-sessões, um cliente SAM pode suportar múltiplas aplicações, ou uma única aplicação sofisticada utilizando diversos protocolos, sobre um único conjunto de túneis. Por exemplo, um cliente bittorrent poderia configurar uma sub-sessão de streaming para conexões peer-to-peer, juntamente com sub-sessões de datagrama e sub-sessões brutas para comunicação DHT.

#### Criando uma Sessão PRIMÁRIA

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
A ponte SAM responderá com sucesso ou falha, conforme descrito na [resposta à criação de sessão padrão](#session-creation-response).

Não defina as opções PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL ou HEADER em uma sessão primária. Você não pode enviar nenhum dado em um ID de sessão PRIMÁRIA nem no socket de controle. Todos os comandos, como STREAM CONNECT, DATAGRAM SEND, etc., devem usar o ID de subsessão em um socket separado.

A sessão PRIMÁRIA se conecta ao roteador e cria túneis. Quando a ponte SAM responde, os túneis já foram criados e a sessão está pronta para receber subsessões. Todas as opções [I2CP](/docs/protocol/i2cp) relativas aos parâmetros dos túneis, como comprimento, quantidade e apelido, devem ser fornecidas na criação da sessão primária (SESSION CREATE).

Todos os comandos de utilidade são suportados em uma sessão primária.

Quando a sessão principal é fechada, todas as subsessões também são encerradas.

NOTA: Antes da versão 0.9.47, use STYLE=MASTER. STYLE=PRIMARY é suportado a partir da versão 0.9.47. MASTER ainda é suportado para compatibilidade com versões anteriores.

#### Criando uma Subsessão

Usando o mesmo soquete de controle no qual a sessão PRIMÁRIA foi criada:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
A ponte SAM responderá com sucesso ou falha conforme descrito na [resposta à criação de sessão padrão](#session-creation-response). Como os túneis já foram criados na criação da sessão primária, a ponte SAM deve responder imediatamente.

Não defina a opção DESTINATION em um SESSION ADD. A subsessão usará o destino especificado na sessão primária. Todas as subsessões devem ser adicionadas no soquete de controle, ou seja, na mesma conexão em que você criou a sessão primária.

As múltiplas subsessões devem ter opções suficientemente únicas para que os dados recebidos possam ser roteados corretamente. Em particular, múltiplas sessões do mesmo estilo devem ter opções LISTEN_PORT diferentes (e/ou LISTEN_PROTOCOL, apenas para RAW). Um SESSION ADD com porta e protocolo de escuta que dupliquem uma subsessão existente resultará em um erro.

A LISTEN_PORT é a porta I2P local, ou seja, a porta de recebimento (TO) para dados entrantes. Se a LISTEN_PORT não for especificada, o valor de FROM_PORT será usado. Se LISTEN_PORT e FROM_PORT não forem especificados, o roteamento de entrada será baseado apenas em STYLE e PROTOCOL. Para LISTEN_PORT e LISTEN_PROTOCOL, 0 significa qualquer valor, ou seja, um curinga. Se ambos LISTEN_PORT e LISTEN_PROTOCOL forem 0, esta subsessão será a padrão para tráfego entrante que não for roteado para outra subsessão. Tráfego de streaming entrante (protocolo 6) nunca será roteado para uma subsessão RAW, mesmo que seu LISTEN_PROTOCOL seja 0. Uma subsessão RAW não pode definir um LISTEN_PROTOCOL igual a 6. Se não houver uma subsessão padrão ou alguma que corresponda ao protocolo e porta do tráfego entrante, esses dados serão descartados.

Use o ID da subsessão, não o ID da sessão primária, para enviar e receber dados. Todos os comandos, como STREAM CONNECT, DATAGRAM SEND, etc., devem usar o ID da subsessão.

Todos os comandos de utilidade são suportados em uma sessão principal ou subsessão. O envio/recebimento de datagramas/v2 não é suportado em uma sessão principal ou em subsessões.

#### Parando uma Subsessão

Usando o mesmo soquete de controle no qual a sessão PRIMÁRIA foi criada:

```
->  SESSION REMOVE
          ID=$nickname
```
Isso remove uma subsessão da sessão principal. Não defina nenhuma outra opção em um SESSION REMOVE. As subsessões devem ser removidas no socket de controle, ou seja, na mesma conexão em que você criou a sessão principal. Após uma subsessão ser removida, ela é fechada e não pode mais ser usada para enviar ou receber dados.

A ponte SAM responderá com sucesso ou falha, conforme descrito na [resposta à criação de sessão padrão](#session-creation-response).

### Comandos de Utilitário SAM

Alguns comandos utilitários exigem uma sessão pré-existente e outros não. Veja os detalhes abaixo.

#### Pesquisa de Nome de Host

A seguinte mensagem pode ser usada pelo cliente para consultar a ponte SAM sobre a resolução de nomes:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
que é respondido por

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
O valor de RESULTADO pode ser um dos seguintes:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Se NOME=EU, então a resposta conterá o destino usado pela sessão atual (útil se você estiver usando um destino TRANSITÓRIO). Se $result não for OK, MENSAGEM pode transmitir uma mensagem descritiva, como "formato inválido", etc. CHAVE_INVÁLIDA implica que há algo errado com $nome na solicitação, possivelmente caracteres inválidos.

O $destination é a codificação base 64 da [Destination](/docs/specs/common-structures#type_Destination), que possui 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A CONSULTA DE NOMEAÇÃO não exige que uma sessão tenha sido criada previamente. No entanto, em algumas implementações, uma consulta .b32.i2p sem cache que exija uma pesquisa na rede pode falhar, já que não há túneis de cliente disponíveis para a consulta.

#### Opções de Pesquisa de Nome

NAMING LOOKUP foi estendido a partir da API do roteador 0.9.66 para suportar consultas de serviço. O suporte pode variar conforme a implementação. Consulte a proposta 167 para obter informações adicionais.

NAMING LOOKUP NAME=example.i2p OPTIONS=true solicita o mapeamento de opções na resposta. NAME pode ser um destino base64 completo quando OPTIONS=true.

Se a busca pelo destino for bem-sucedida e houver opções presentes no leaseset, então na resposta, após o destino, haverá uma ou mais opções no formato OPTION:chave=valor. Cada opção terá um prefixo OPTION: separado. Todas as opções do leaseset serão incluídas, não apenas as opções de registro de serviço. Por exemplo, opções para parâmetros definidos no futuro podem estar presentes. Exemplo:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Chaves contendo '=', e chaves ou valores contendo uma nova linha, são considerados inválidos e o par chave/valor será removido da resposta. Se nenhuma opção for encontrada no leaseset, ou se o leaseset for da versão 1, a resposta não incluirá nenhuma opção. Se OPTIONS=true estiver na consulta e o leaseset não for encontrado, um novo valor de resultado LEASESET_NOT_FOUND será retornado.

#### Geração da Chave de Destino

As chaves base64 públicas e privadas podem ser geradas usando a seguinte mensagem:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
que é respondido por

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
A partir da versão 3.1 (I2P 0.9.14), um parâmetro opcional SIGNATURE_TYPE é suportado. O valor de SIGNATURE_TYPE pode ser qualquer nome (por exemplo, ECDSA_SHA256_P256, não sensível a maiúsculas/minúsculas) ou número (por exemplo, 1) que seja suportado por [Certificados de Chave](/docs/specs/common-structures#type_Certificate). O padrão é DSA_SHA1, que NÃO é o que você deseja. Para a maioria das aplicações, por favor especifique SIGNATURE_TYPE=7.

O $destination é a codificação base 64 da [Destination](/docs/specs/common-structures#type_Destination), que possui 516 ou mais caracteres base 64 (387 ou mais bytes em binário), dependendo do tipo de assinatura.

A $privkey é a representação base 64 da concatenação da [Destination](/docs/specs/common-structures#type_Destination), seguida pela [Private Key](/docs/specs/common-structures#type_PrivateKey) e depois pela [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), totalizando 884 ou mais caracteres em base 64 (663 ou mais bytes em binário), dependendo do tipo de assinatura. O formato binário é especificado em Private Key File.

Notas sobre a chave privada binária de 256 bytes [Private Key](/docs/specs/common-structures#type_PrivateKey): Este campo não tem sido usado desde a versão 0.6 (2005). Implementações SAM podem enviar dados aleatórios ou todos os zeros neste campo; não se preocupe com uma sequência de AAAA na codificação base 64. A maioria das aplicações simplesmente armazenará a string base 64 e a devolverá inalterada no SESSION CREATE, ou fará a decodificação para binário para armazenamento, e depois a recodificação novamente para o SESSION CREATE. No entanto, as aplicações podem decodificar o base 64, analisar o binário segundo a especificação PrivateKeyFile, descartar a parte da chave privada de 256 bytes e substituí-la por 256 bytes de dados aleatórios ou todos os zeros ao re-codificá-la para o SESSION CREATE. TODOS os outros campos na especificação PrivateKeyFile devem ser preservados. Isso economizaria 256 bytes de armazenamento no sistema de arquivos, mas provavelmente não vale o esforço para a maioria das aplicações. Veja a proposta 161 para informações e contexto adicionais.

DEST GENERATE não exige que uma sessão tenha sido criada anteriormente.

DEST GENERATE não pode ser usado para criar uma destinatário com assinaturas offline.

#### PING/PONG (SAM 3.2 ou superior)

O cliente ou o servidor podem enviar:

```
PING[ arbitrary text]
```
na porta de controle, com a resposta:

```
PONG[ arbitrary text from the ping]
```
para ser usado na manutenção da conexão do soquete de controle. Qualquer lado pode encerrar a sessão e o soquete se nenhuma resposta for recebida em um tempo razoável, dependendo da implementação.

Se ocorrer um tempo limite ao aguardar um PONG do cliente, a ponte pode enviar:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
e então desconecte.

Se ocorrer um tempo limite ao aguardar um PONG da ponte, o cliente pode simplesmente se desconectar.

PING/PONG não requerem que uma sessão tenha sido criada anteriormente.

#### QUIT/STOP/EXIT (SAM 3.2 ou superior, recursos opcionais)

Os comandos QUIT, STOP e EXIT fecharão a sessão e o socket. A implementação é opcional, para facilitar testes via telnet. Se haverá ou não alguma resposta antes do fechamento do socket (por exemplo, uma mensagem SESSION STATUS) depende da implementação e está fora do escopo desta especificação.

QUIT/STOP/EXIT não exigem que uma sessão tenha sido criada anteriormente.

#### AJUDA (recurso opcional)

Os servidores podem implementar um comando HELP. A implementação é opcional, para facilitar testes via telnet. O formato da saída e a detecção do fim da saída são específicos da implementação e estão fora do escopo desta especificação.

O HELP não exige que uma sessão tenha sido criada primeiro.

#### Configuração de Autorização (SAM 3.2 ou superior, recurso opcional)

Configuração de autorização usando o comando AUTH. Um servidor SAM pode implementar esses comandos para facilitar o armazenamento persistente de credenciais. A configuração de autenticação diferente da realizada com esses comandos é específica da implementação e está fora do escopo desta especificação.

- AUTH ENABLE ativa a autorização nas conexões subsequentes
- AUTH DISABLE desativa a autorização nas conexões subsequentes
- AUTH ADD USER="foo" PASSWORD="bar" adiciona um usuário/senha
- AUTH REMOVE USER="foo" remove este usuário

Aspas duplas para usuário e senha são recomendadas, mas não obrigatórias. Uma aspa dupla dentro de um usuário ou senha deve ser escapada com uma barra invertida. Em caso de falha, o servidor responderá com um I2P_ERROR e uma mensagem.

O AUTH não exige que uma sessão tenha sido criada primeiro.

### Valores RESULT

Esses são os valores que podem ser transportados pelo campo RESULT, com seus significados:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Diferentes implementações podem não ser consistentes quanto ao RESULTADO retornado em vários cenários.

A maioria das respostas com um RESULTADO, diferente de OK, também incluirá uma MENSAGEM com informações adicionais. A MENSAGEM geralmente será útil para depurar problemas. No entanto, as strings de MENSAGEM dependem da implementação, podem ou não ser traduzidas pelo servidor SAM para o idioma atual, podem conter informações internas específicas da implementação, como exceções, e estão sujeitas a alterações sem aviso prévio. Embora clientes SAM possam optar por exibir as strings de MENSAGEM aos usuários, eles não devem tomar decisões programáticas com base nessas strings, pois isso tornaria o sistema frágil.

### Opções de Tunnel, I2CP e Streaming

Essas opções podem ser passadas como pares nome=valor na linha SAM SESSION CREATE.

Todas as sessões podem incluir [opções I2CP, como comprimentos e quantidades de túneis](/docs/protocol/i2cp#options). Sessões STREAM podem incluir [opções da biblioteca de streaming](/docs/api/streaming#options).

Consulte essas referências para nomes de opções e valores padrão. A documentação referenciada é para a implementação do roteador Java. Os padrões estão sujeitos a alterações. Nomes e valores de opções diferenciam maiúsculas de minúsculas. Outras implementações de roteadores podem não suportar todas as opções e podem ter padrões diferentes; consulte a documentação do roteador para obter detalhes.

### Notas sobre Base 64

A codificação Base 64 deve usar o alfabeto Base 64 padrão do I2P: "A-Z, a-z, 0-9, -, ~".

### Configuração padrão do SAM

A porta SAM padrão é 7656. O SAM não é habilitado por padrão no Roteador Java I2P; ele deve ser iniciado manualmente ou configurado para iniciar automaticamente, na página de configuração de clientes no console do roteador, ou no arquivo clients.config. A porta UDP SAM padrão é 7655, escutando em 127.0.0.1. Essas configurações podem ser alteradas no roteador Java adicionando os argumentos sam.udp.port=nnnnn e/ou sam.udp.host=w.x.y.z à chamada, ou na linha SESSION.

A configuração em outros roteadores é específica da implementação. Veja [o guia de configuração do i2pd aqui](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
