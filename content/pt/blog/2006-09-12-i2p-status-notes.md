---
title: "Notas de status do I2P de 2006-09-12"
date: 2006-09-12
author: "jr"
description: "Versão 0.6.1.25 com melhorias na estabilidade da rede, otimizações do I2PSnark e uma reformulação abrangente do Syndie com fóruns distribuídos offline"
categories: ["status"]
---

Olá, pessoal, aqui estão as nossas *cof* notas de status semanais

* Index:

1) 0.6.1.25 e estado da rede 2) I2PSnark 3) Syndie (o quê/por quê/quando) 4) Perguntas sobre criptografia do Syndie 5) ???

* 1) 0.6.1.25 and net status

Há poucos dias lançamos a versão 0.6.1.25, incluindo um grande conjunto de correções de bugs acumuladas ao longo do último mês, bem como o trabalho do zzz no I2PSnark e o trabalho do Complication tentando tornar nosso código de sincronização de tempo um pouco mais robusto. No momento, a rede parece estar bastante estável, embora o IRC tenha estado um pouco instável nos últimos dias (por motivos não relacionados ao I2P). Com talvez metade da rede atualizada para a versão mais recente, as taxas de sucesso na construção de tunnel não mudaram muito, embora a vazão geral pareça ter aumentado (provavelmente devido a um aumento no número de pessoas usando o I2PSnark).

* 2) I2PSnark

As atualizações de zzz no I2PSnark incluíram otimizações de protocolo, bem como alterações nas interfaces web, conforme descrito no log de histórico [1]. Também houve algumas pequenas atualizações para o I2PSnark desde a versão 0.6.1.25, e talvez zzz possa nos dar uma visão geral do que há de novo durante a reunião desta noite.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Como todos vocês sabem, tenho concentrado meu tempo em reformular o Syndie, embora “reformulação” talvez não seja a palavra certa. Talvez vocês possam considerar o que está atualmente implantado como uma “prova de conceito”, já que o novo Syndie foi redesenhado e reimplementado do zero, embora muitos conceitos permaneçam. Quando me refiro ao Syndie abaixo, estou falando do novo Syndie.

* 3.1) What is Syndie

Syndie é, em seu nível mais básico, um sistema para operar fóruns distribuídos offline. Embora sua estrutura leve a um grande número de configurações diferentes, a maioria das necessidades será atendida selecionando uma das opções de cada um dos três critérios a seguir:  - Tipos de fórum:    - Autor único (blog típico)    - Vários autores (blog multiautor)**    - Aberto (grupos de notícias, embora possam ser incluídas restrições para que apenas      usuários autorizados** possam abrir novos tópicos, enquanto qualquer pessoa pode comentar      nesses novos tópicos)  - Visibilidade:    - Qualquer pessoa pode ler qualquer coisa    - Apenas pessoas autorizadas* podem ler as postagens, mas alguns metadados são expostos    - Apenas pessoas autorizadas* podem ler as postagens, ou mesmo saber quem está publicando    - Apenas pessoas autorizadas* podem ler as postagens, e ninguém sabe quem está      publicando  - Comentários/respostas:    - Qualquer pessoa pode comentar ou enviar respostas privadas ao autor/proprietário
      do fórum    - Apenas pessoas autorizadas** podem comentar, e qualquer pessoa pode enviar
      respostas privadas    - Ninguém pode comentar, mas qualquer pessoa pode enviar respostas privadas
    - Ninguém pode comentar, e ninguém pode enviar respostas privadas

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** publicar, atualizar e/ou comentar é autorizado fornecendo a esses usuários chaves privadas assimétricas com as quais assinar as postagens, cujas chaves públicas correspondentes são incluídas nos metadados do fórum como autorizadas a publicar, gerenciar ou comentar no fórum.  Alternativamente, as chaves públicas de assinatura de usuários individuais autorizados podem ser listadas nos metadados.

Publicações individuais podem conter muitos elementos diferentes:  - Qualquer número de páginas, com out of band data (dados fora de banda) para cada página especificando    o tipo de conteúdo, idioma, etc.  Qualquer formatação pode ser usada, pois cabe    ao aplicativo cliente renderizar o conteúdo com segurança - texto simples    deve ser suportado, e os clientes que puderem devem suportar HTML.  - Qualquer número de anexos (novamente, com out of band data descrevendo o    anexo)  - Um pequeno avatar para a publicação (mas, se não especificado, o avatar    padrão do autor é usado)  - Um conjunto de referências a outras publicações, fóruns, arquivos, URLs, etc (que    podem incluir as chaves necessárias para publicar, gerenciar ou ler os fóruns    referenciados)

De modo geral, o Syndie opera na *camada de conteúdo* - as publicações individuais estão contidas em arquivos ZIP criptografados, e participar do fórum significa simplesmente compartilhar esses arquivos. Não há dependência quanto à forma como os arquivos são transferidos (via I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email), mas ferramentas simples de agregação e distribuição serão incluídas na versão padrão do Syndie.

A interação com o conteúdo do Syndie ocorrerá de várias maneiras. Primeiro, há uma interface baseada em texto e scriptável, permitindo operações básicas pela linha de comando e, de forma interativa, ler a partir dos fóruns, escrever neles, gerenciá-los e sincronizá-los. Por exemplo, a seguir está um script simples para gerar uma nova postagem de "mensagem do dia" -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Basta canalizar isso através do executável syndie e pronto: cat motd-script | ./syndie > syndie.log

Além disso, há trabalho em andamento para uma interface gráfica do Syndie, que inclui a renderização segura de texto simples e páginas HTML (claro, com suporte para integração transparente com as funcionalidades do Syndie).

Aplicativos baseados no antigo código "sucker" do Syndie permitirão a raspagem e a reescrita de páginas e sites da web normais, para que possam ser usados como publicações do Syndie de página única ou de várias páginas, incluindo imagens e outros recursos como anexos.

No futuro, prevê-se que plugins do Firefox/Mozilla tanto detectem quanto importem arquivos no formato Syndie e referências do Syndie, além de notificar a GUI (interface gráfica do usuário) local do Syndie de que um determinado fórum, tópico, tag, autor ou resultado de pesquisa deve ser colocado em foco.

Claro que, como o Syndie é, em essência, uma camada de conteúdo com um formato de arquivo definido e algoritmos criptográficos, outras aplicações ou implementações alternativas provavelmente surgirão ao longo do tempo.

* 3.2) Why does Syndie matter?

Tenho ouvido várias pessoas perguntarem, ao longo dos últimos meses, por que estou trabalhando em uma ferramenta de fórum/blog - o que isso tem a ver com oferecer anonimato forte?

A resposta: *tudo*.

Para resumir brevemente:  - O design do Syndie, como um aplicativo cliente sensível ao anonimato,    
    evita cuidadosamente os intrincados problemas de sensibilidade dos dados que    
    quase todos os aplicativos que não são construídos com o anonimato em mente não evitam.  - Ao operar na camada de conteúdo, o Syndie não depende do    
    desempenho ou da confiabilidade de redes distribuídas como I2P, Tor ou    
    Freenet, embora possa aproveitá-las quando apropriado.  - Ao fazer isso, ele pode operar plenamente com pequenos mecanismos ad-hoc de    
    distribuição de conteúdo - mecanismos que talvez não valham o esforço    
    para adversários poderosos contrariarem (já que o 'retorno' de desmascarar    
    apenas algumas dezenas de pessoas provavelmente excederá o custo de realizar os    
    ataques)  - Isso implica que o Syndie será útil mesmo sem alguns milhões    
    de pessoas o utilizando - pequenos grupos de pessoas, sem relação entre si, devem    
    configurar seu próprio esquema privado de distribuição do Syndie sem exigir qualquer    
    interação com, ou mesmo conhecimento por parte de, quaisquer outros grupos.  - Como o Syndie não depende de interação em tempo real, ele pode até    
    fazer uso de sistemas e técnicas de anonimato de alta latência para evitar os    
    ataques aos quais todos os sistemas de baixa latência são vulneráveis (como    
    ataques de interseção passivos, ataques de temporização passivos e ativos e    
    ataques de mistura ativos).

De modo geral, na minha opinião o Syndie é ainda mais importante para a missão central do I2P (fornecer anonimato forte a quem precisa) do que até mesmo o router. Não é a solução definitiva para tudo, mas é um passo fundamental.

* 3.3) When can we use Syndie?

Embora muito trabalho já tenha sido concluído (incluindo quase toda a interface de texto e uma boa parte da GUI), ainda há trabalho a ser feito. A primeira versão do Syndie incluirá as seguintes funcionalidades básicas:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

O critério que vou usar para lançar isso será "totalmente funcional". O usuário médio não vai ficar mexendo com um aplicativo baseado em texto, mas espero que alguns geeks o façam.

Versões subsequentes aprimorarão as capacidades do Syndie em várias dimensões:  - Interface do usuário:   - GUI baseada em SWT   - Plugins do navegador web   - IU de texto para raspagem da web (capturando e reescrevendo páginas)   - Interface de leitura IMAP/POP3/NNTP  - Suporte a conteúdo   - Texto simples   - HTML (renderização segura dentro da GUI, não em um navegador)   - BBCode (?)  - Sindicação   - Feedspace, Feedtree e outras ferramentas de sincronização de baixa latência   - Freenet (armazenando arquivos .snd em CHK@s e archives (coleções) que referenciam
    os arquivos .snd em SSK@s e USK@s)   - E-mail (enviar via SMTP/mixmaster/mixminion, ler via
    procmail/etc)   - Usenet (enviar via NNTP ou remailers, ler via (via proxy)
    NNTP)  - Pesquisa de texto completo com integração ao Lucene  - Extensão do HSQLDB para criptografia completa do banco de dados  - Heurísticas adicionais de gerenciamento de archives

O que sai e quando sai dependem de quando as coisas são feitas.

* 4) Open questions for Syndie

No momento, o Syndie foi implementado com as primitivas criptográficas padrão do I2P - SHA256, AES256/CBC, ElGamal2048, DSA. Este último é a exceção, porém, pois usa chaves públicas de 1024 bits e depende do SHA1 (que está enfraquecendo rapidamente). Uma sugestão que tenho ouvido na prática é a utilização do DSA com SHA256 e, embora isso seja viável (ainda que não padronizado), isso só oferece chaves públicas de 1024 bits.

Como o Syndie ainda não foi liberado ao público e não há preocupação com compatibilidade com versões anteriores, temos o luxo de trocar as primitivas criptográficas à vontade. Uma linha de pensamento é optar por assinaturas ElGamal2048 ou RSA2048 em vez de DSA, enquanto outra é considerar ECC (Elliptic Curve Cryptography — criptografia de curvas elípticas), com assinaturas ECDSA e criptografia assimétrica ECIES, talvez nos níveis de segurança de 256 bits ou 521 bits (correspondendo a tamanhos de chaves simétricas de 128 bits e 256 bits, respectivamente).

Quanto às questões de patentes relacionadas à ECC (criptografia de curva elíptica), elas parecem ser relevantes apenas para otimizações específicas (compressão de pontos) e algoritmos de que não precisamos (EC MQV). Não há muita coisa por aí em termos de suporte em Java, embora a bouncycastle lib pareça ter algum código. No entanto, provavelmente não seria muito trabalhoso adicionar pequenos wrappers à libtomcrypt, à openssl ou à crypto++, como fizemos para a libGMP (o que nos deu o jbigi).

Alguma opinião sobre isso?

* 5) ???

Há muita coisa para assimilar aí em cima, por isso (por sugestão do cervantes) estou enviando estas notas de status tão cedo. Se você tiver quaisquer comentários, perguntas, preocupações ou sugestões, passe no #i2p esta noite às 8pm UTC em irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p para a nossa *cough* reunião semanal!

=jr
