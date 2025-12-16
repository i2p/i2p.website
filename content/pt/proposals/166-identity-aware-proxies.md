---
title: "Proposta I2P nº 166: Tipos de Túneis Conscientes de Identidade/Host"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Open"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Proposta para um Tipo de Túnel HTTP Proxy Consciente de Host

Esta é uma proposta para resolver o "Problema de Identidade Compartilhada" no uso convencional de HTTP sobre I2P, introduzindo um novo tipo de túnel HTTP proxy. Este tipo de túnel possui um comportamento suplementar que visa prevenir ou limitar a utilidade do rastreamento realizado por operadores de serviços ocultos potenciais hostis, contra agentes de usuário alvo (navegadores) e a própria Aplicação Cliente I2P.

#### O que é o problema da “Identidade Compartilhada”?

O problema da “Identidade Compartilhada” ocorre quando um agente de usuário em uma rede sobreposta endereçada criptograficamente compartilha uma identidade criptográfica com outro agente de usuário. Isso ocorre, por exemplo, quando um Firefox e o GNU Wget estão ambos configurados para usar o mesmo Proxy HTTP.

Neste cenário, é possível que o servidor colete e armazene o endereço criptográfico (Destino) usado para responder à atividade. Ele pode tratar isso como uma "Impressão Digital" que é sempre 100% única, pois é de origem criptográfica. Isso significa que a vinculabilidade observada pelo problema da Identidade Compartilhada é perfeita.

Mas é um problema?
^^^^^^^^^^^^^^^^^^^^

O problema da identidade compartilhada é um problema quando os agentes de usuário que falam o mesmo protocolo desejam desvinculação. [Foi mencionado pela primeira vez no contexto do HTTP neste Tópico Reddit](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/), com os comentários apagados acessíveis graças ao [pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi). *Na época*, eu era um dos respondentes mais ativos, e *na época* eu acreditava que o problema era pequeno. Nos últimos 8 anos, a situação e minha opinião sobre ela mudaram, e agora acredito que a ameaça representada pela correlação maliciosa de destino cresce consideravelmente à medida que mais sites estão em posição de "proﬁlar" usuários especíﬁcos.

Este ataque tem uma barreira de entrada muito baixa. Ele apenas requer que um operador de serviço oculto opere múltiplos serviços. Para ataques em visitas contemporâneas (visitando múltiplos sites ao mesmo tempo), este é o único requisito. Para vinculação não contemporânea, um desses serviços deve ser um serviço que hospede "contas" que pertençam a um único usuário alvo de rastreamento.

Atualmente, qualquer operador de serviço que hospede contas de usuário poderá correlacioná-las com atividades em quaisquer sites que eles controlem explorando o problema da Identidade Compartilhada. Mastodon, Gitlab, ou até mesmo fóruns simples poderiam ser atacantes disfarçados, contanto que operem mais de um serviço e tenham interesse em criar um perfil para um usuário. Essa vigilância poderia ser realizada por perseguição, ganho financeiro ou razões relacionadas à inteligência. Agora, existem dezenas de grandes operadores que poderiam realizar esse ataque e obter dados significativos a partir dele. Confiamos principalmente neles para não fazer agora, mas jogadores que não se importam com nossas opiniões poderiam facilmente emergir.

Isso está diretamente relacionado a uma forma bastante básica de construção de perfil na web aberta, onde organizações podem correlacionar interações em seus sites com interações em redes que controlam. No I2P, como o destino criptográfico é único, essa técnica às vezes pode ser ainda mais confiável, embora sem o poder adicional de geolocalização.

A Identidade Compartilhada não é útil contra um usuário que está usando o I2P exclusivamente para ofuscar a geolocalização. Também não pode ser usado para quebrar o roteamento I2P. É apenas um problema de gerenciamento de identidade contextual.

- É impossível usar o problema da Identidade Compartilhada para geolocalizar um usuário I2P.
- É impossível usar o problema da Identidade Compartilhada para vincular sessões I2P se não forem contemporâneas.

No entanto, é possível usá-lo para degradar o anonimato de um usuário I2P em circunstâncias que provavelmente são muito comuns. Uma razão pela qual são comuns é porque encorajamos o uso do Firefox, um navegador web que suporta operação "Tabulada".

- Sempre é possível produzir uma impressão digital a partir do problema de Identidade Compartilhada em qualquer navegador web que suporte solicitação de recursos de terceiros.
- Desativar Javascript não realiza **nada** contra o problema da Identidade Compartilhada.
- Se um link puder ser estabelecido entre sessões não contemporâneas, como através de "impressão digital" tradicional do navegador, então a Identidade Compartilhada pode ser aplicada de maneira transitiva, potencialmente habilitando uma estratégia de vinculação não contemporânea.
- Se um link puder ser estabelecido entre uma atividade de rede limpa e uma identidade I2P, por exemplo, se o alvo estiver logado em um site com presença tanto no I2P quanto na rede limpa em ambos os lados, a Identidade Compartilhada pode ser aplicada de maneira transitiva, potencialmente habilitando a desanonimização completa.

Como você enxerga a gravidade do problema da Identidade Compartilhada conforme se aplica ao proxy HTTP I2P depende de onde você (ou mais precisamente, um "usuário" com expectativas potencialmente desinformadas) acha que está a "identidade contextual" para a aplicação. Existem várias possibilidades:

1. HTTP é tanto a Aplicação quanto a Identidade Contextual - É assim que funciona agora. Todas as Aplicações HTTP compartilham uma identidade.
2. O Processo é a Aplicação e a Identidade Contextual - É assim que funciona quando uma aplicação usa uma API como SAMv3 ou I2CP, onde uma aplicação cria sua identidade e controla seu tempo de vida.
3. HTTP é a Aplicação, mas o Host é a Identidade Contextual - Este é o objeto desta proposta, que trata cada Host como um potencial "Aplicativo Web" e considera a superfície de ameaça dessa forma.

É Solucionável?
^^^^^^^^^^^^^^^

Provavelmente não é possível criar um proxy que responda de forma inteligente a todos os casos possíveis em que sua operação possa enfraquecer o anonimato de uma aplicação. No entanto, é possível construir um proxy que responda de forma inteligente a uma aplicação específica que se comporte de maneira previsível. Por exemplo, em navegadores web modernos, espera-se que os usuários tenham várias abas abertas, onde interagirão com vários websites diferenciados por nome do host.

Isso nos permite melhorar o comportamento do proxy HTTP para esse tipo de agente de usuário HTTP, fazendo o comportamento do proxy corresponder ao comportamento do agente de usuário, atribuindo a cada host seu próprio Destino quando usado com o proxy HTTP. Essa mudança torna impossível usar o problema da Identidade Compartilhada para derivar uma impressão digital que pode ser usada para correlacionar a atividade do cliente com 2 hosts, pois os 2 hosts simplesmente não mais compartilharão uma identidade de retorno.

Descrição:
^^^^^^^^^^^^

Um novo Proxy HTTP será criado e adicionado ao Gerenciador de Serviços Ocultos (I2PTunnel). O novo Proxy HTTP funcionará como um "multiplexador" de I2PSocketManagers. O próprio multiplexador não tem um destino. Cada I2PSocketManager individual que faz parte do multiplex possui seu próprio destino local e seu próprio pool de túneis. I2PSocketManagers são criados sob demanda pelo multiplexador, onde a "demanda" é a primeira visita ao novo host. É possível otimizar a criação de I2PSocketManagers antes de inseri-los no multiplexador criando um ou mais com antecedência e armazenando-os fora do multiplexador. Isso pode melhorar o desempenho.

Um I2PSocketManager adicional, com seu próprio destino, é configurado como o transportador de um "Outproxy" para qualquer site que não tenha um Destino I2P, por exemplo, qualquer site da Clearnet. Isso efetivamente faz todo o uso do Outproxy uma única Identidade Contextual, com a advertência de que configurar múltiplos Outproxies para o túnel causará a rotação normal "Sticky" do outproxy, onde cada outproxy apenas recebe solicitações para um único site. Isso é *quase* o comportamento equivalente de isolar proxies de HTTP sobre I2P por destino, na internet limpa.

Considerações de Recursos:
''''''''''''''''''''''''

O novo proxy HTTP requer recursos adicionais em comparação com o proxy HTTP existente. Ele irá:

- Potencialmente construir mais túneis e I2PSocketManagers
- Construir túneis com mais frequência

Cada um desses requer:

- Recursos computacionais locais
- Recursos de rede de pares

Configurações:
'''''''''

Para minimizar o impacto do aumento do uso de recursos, o proxy deve ser configurado para usar o mínimo possível. Os proxies que são parte do multiplexador (não o proxy pai) devem ser configurados para:

- I2PSocketManagers multiplexados constroem 1 túnel de entrada, 1 túnel de saída em seus pools de túneis
- I2PSocketManagers multiplexados fazem 3 saltos por padrão.
- Fechar soquetes após 10 minutos de inatividade
- I2PSocketManagers iniciados pelo Multiplexador compartilham a duração do Multiplexador. Túneis multiplexados não são “Destruídos” até que o Multiplexador pai seja.

Diagramas:
^^^^^^^^^

O diagrama abaixo representa a operação atual do proxy HTTP, que corresponde à "Possibilidade 1." na seção "É um problema". Como você pode ver, o proxy HTTP interage com sites I2P diretamente usando apenas um destino. Neste cenário, o HTTP é tanto a aplicação quanto a identidade contextual.

```text
**Situação Atual: HTTP é a Aplicação, HTTP é a Identidade Contextual**
                                                          __-> Outproxy <-> i2pgit.org
                                                         /
   Navegador <-> Proxy HTTP (um Destino) <-> I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

O diagrama abaixo representa a operação de um proxy HTTP consciente de host, que corresponde à "Possibilidade 3." na seção "É um problema". Neste cenário, HTTP é a aplicação, mas o Host define a identidade contextual, onde cada site I2P interage com um proxy HTTP diferente com um destino único por host. Isso impede operadores de múltiplos sites de serem capazes de distinguir quando a mesma pessoa está visitando múltiplos sites que eles operam.

```text
**Após a Mudança: HTTP é a Aplicação, Host é a Identidade Contextual**
                                                        __-> I2PSocketManager(Destino A - Apenas Outproxies) <--> i2pgit.org
                                                       /
   Navegador <-> Multiplexador de Proxy HTTP (Sem Destino) <---> I2PSocketManager(Destino B) <--> idk.i2p
                                                       \__-> I2PSocketManager(Destino C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager(Destino C) <--> git.idk.i2p
```

Status:
^^^^^^^

Uma implementação Java funcional do proxy consciente de host que está de acordo com uma versão mais antiga desta proposta está disponível no fork de idk sob a branch: i2p.i2p.2.6.0-browser-proxy-post-keepalive Link nas citações. Está sob revisão intensa, a fim de dividir as alterações em seções menores.

Implementações com capacidades variadas foram escritas em Go usando a biblioteca SAMv3, podendo ser úteis para embutir em outras aplicações Go ou para go-i2p, mas são inadequadas para Java I2P. Além disso, não têm bom suporte para trabalhar interativamente com leaseSets criptografados.

Adendo: ``i2psocks``
                      

Uma abordagem simples orientada para aplicativos para isolar outros tipos de clientes é possível sem implementar um novo tipo de túnel ou alterar o código I2P existente ao combinar as ferramentas existentes do I2PTunnel, que já estão amplamente disponíveis e testadas na comunidade de privacidade. No entanto, essa abordagem faz uma suposição difícil que não é verdadeira para HTTP e também não é verdadeira para muitos outros tipos de clientes I2P potenciais.

Basicamente, o seguinte script produzirá um proxy SOCKS5 consciente de aplicativo e colocará o comando subjacente:

```sh
#! /bin/sh
comando_para_proxificar="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $comando_para_proxificar
```

Adendo: ``implementação de exemplo do ataque``
                                                  

[Uma implementação de exemplo do ataque de Identidade Compartilhada em Agentes de Usuário HTTP](https://github.com/eyedeekay/colluding_sites_attack/) existe há vários anos. Um exemplo adicional está disponível no subdiretório ``simple-colluder`` do [repositório prop166 de idk](https://git.idk.i2p/idk/i2p.host-aware-proxy) Estes exemplos são deliberadamente projetados para demonstrar que o ataque funciona e requereria modificação (embora menor) para ser transformado em um ataque real.

