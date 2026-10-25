---
title: "Discussão de Nomenclatura"
description: "Debate histórico sobre o modelo de nomenclatura do I2P e por que esquemas globais estilo DNS foram rejeitados"
slug: "naming"
aliases:
  - "/pt/docs/legacy/naming"
  - "/pt/docs/legacy/naming/"
  - "/pt/naming_discussion"
  - "/pt/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

NOTA: O seguinte é uma discussão sobre as razões por trás do sistema de nomenclatura do I2P, argumentos comuns e possíveis alternativas. Consulte [a página de nomenclatura](/docs/naming) para documentação atual.

## Alternativas Descartadas

A nomenclatura dentro do I2P tem sido um tópico muito debatido desde o início, com defensores em todo o espectro de possibilidades. No entanto, dada a demanda inerente do I2P por comunicação segura e operação descentralizada, o sistema de nomenclatura tradicional no estilo DNS está claramente fora de questão, assim como os sistemas de votação de "maioria manda".

O I2P não promove o uso de serviços similares ao DNS, já que os danos causados pelo sequestro de um site podem ser tremendos - e destinos inseguros não têm valor. O próprio DNSsec ainda depende de registradores e autoridades certificadoras, enquanto no I2P, solicitações enviadas para um destino não podem ser interceptadas ou as respostas falsificadas, pois são criptografadas com as chaves públicas do destino, e um destino em si é apenas um par de chaves públicas e um certificado. Sistemas no estilo DNS, por outro lado, permitem que qualquer um dos servidores de nome no caminho de busca execute ataques simples de negação de serviço e falsificação. Adicionar um certificado que autentica as respostas como assinadas por alguma autoridade certificadora centralizada resolveria muitas das questões de servidores de nome hostis, mas deixaria em aberto ataques de replay, bem como ataques de autoridades certificadoras hostis.

O sistema de nomenclatura por votação também é perigoso, especialmente dada a eficácia dos ataques Sybil em sistemas anônimos - o atacante pode simplesmente criar um número arbitrariamente alto de pares e "votar" com cada um para assumir o controle de um determinado nome. Métodos de prova de trabalho podem ser usados para tornar a identidade não gratuita, mas à medida que a rede cresce, a carga necessária para contatar todos para conduzir votação online torna-se implausível, ou se a rede completa não for consultada, diferentes conjuntos de respostas podem ser alcançáveis.

Assim como com a Internet, no entanto, I2P está mantendo o design e operação de um sistema de nomeação fora da camada de comunicação (semelhante ao IP). A biblioteca de nomeação incluída possui uma interface simples de provedor de serviços na qual [sistemas de nomeação alternativos](#alternatives) podem se conectar, permitindo que os usuários finais determinem que tipo de compromissos de nomeação eles preferem.

## Discussão

Veja também [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### Comentários por jrandom

(adaptado de uma postagem no antigo Syndie, 26 de novembro de 2005)

P: O que fazer se alguns hosts não concordam sobre um endereço e se alguns endereços estão funcionando, outros não? Qual é a fonte correta de um nome?

R: Você não pode. Esta é na verdade uma diferença crítica entre nomes no I2P e como o DNS funciona - nomes no I2P são legíveis por humanos, seguros, mas **não globalmente únicos**. Isso é por design, e uma parte inerente da nossa necessidade de segurança.

Se eu pudesse de alguma forma convencê-lo a alterar o destino associado a algum nome, eu conseguiria "assumir o controle" do site com sucesso, e isso não é aceitável sob nenhuma circunstância. Em vez disso, o que fazemos é tornar os nomes **localmente únicos**: eles são o que *você* usa para chamar um site, assim como você pode chamar as coisas como quiser quando as adiciona aos favoritos do seu navegador, ou à lista de contatos do seu cliente de mensagens instantâneas. Quem você chama de "Chefe" pode ser quem outra pessoa chama de "Sally".

Os nomes nunca serão, jamais, legíveis por humanos de forma segura e globalmente únicos.

### Comentários por zzz

O seguinte do zzz é uma revisão de várias reclamações comuns sobre o sistema de nomenclatura do I2P.

- **Ineficiência:** Todo o hosts.txt é baixado (se tiver mudado, já que o eepget usa os cabeçalhos etag e last-modified). São cerca de 400K atualmente para quase 800 hosts.

Verdade, mas isso não é muito tráfego no contexto do I2P, que é em si extremamente ineficiente (bancos de dados floodfill, enorme overhead de encriptação e preenchimento, garlic routing, etc.). Se você baixasse um arquivo hosts.txt de alguém a cada 12 horas, isso resultaria em média cerca de 10 bytes/seg.

Como é geralmente o caso no I2P, há um trade-off fundamental aqui entre anonimato e eficiência. Alguns diriam que usar os cabeçalhos etag e last-modified é perigoso porque expõe quando você solicitou os dados pela última vez. Outros sugeriram solicitar apenas chaves específicas (similar ao que os serviços de jump fazem, mas de forma mais automatizada), possivelmente com um custo adicional no anonimato.

Possíveis melhorias seriam uma substituição ou suplemento ao address book (ver i2host.i2p), ou algo simples como subscrever a http://example.i2p/cgi-bin/recenthosts.cgi em vez de http://example.i2p/hosts.txt. Se um hipotético recenthosts.cgi distribuísse todos os hosts das últimas 24 horas, por exemplo, isso poderia ser tanto mais eficiente quanto mais anônimo do que o atual hosts.txt com last-modified e etag.

Uma implementação de exemplo está em stats.i2p em http://stats.i2p/cgi-bin/newhosts.txt. Este script retorna um Etag com um timestamp. Quando uma solicitação chega com o etag If-None-Match, o script retorna APENAS novos hosts desde esse timestamp, ou 304 Not Modified se não houver nenhum. Desta forma, o script retorna eficientemente apenas os hosts que o assinante não conhece, de uma maneira compatível com o livro de endereços.

Portanto, a ineficiência não é um grande problema e há várias maneiras de melhorar as coisas sem mudanças radicais.

- **Não Escalável:** O hosts.txt de 400K (com busca linear) não é tão grande no momento e provavelmente podemos crescer 10x ou 100x antes que se torne um problema.

Quanto ao tráfego de rede, veja acima. Mas a menos que você vá fazer uma consulta lenta em tempo real pela rede para uma chave, você precisa ter todo o conjunto de chaves armazenado localmente, a um custo de cerca de 500 bytes por chave.

- **Requer configuração e "confiança":** O livro de endereços padrão está apenas inscrito em http://www.i2p2.i2p/hosts.txt, que raramente é atualizado, resultando em uma experiência ruim para novos usuários.

Isto é muito intencional. jrandom quer que um usuário "confie" num provedor de hosts.txt, e como ele gosta de dizer, "confiança não é um booleano". A etapa de configuração tenta forçar os usuários a pensar sobre questões de confiança numa rede anônima.

Como outro exemplo, a página de erro "I2P Site Unknown" no Proxy HTTP lista alguns serviços de jump, mas não "recomenda" nenhum em particular, e cabe ao usuário escolher um (ou não). jrandom diria que confiamos nos provedores listados o suficiente para listá-los, mas não o suficiente para buscar automaticamente a chave deles.

Não tenho certeza de quão bem-sucedido isso é. Mas deve haver algum tipo de hierarquia de confiança para o sistema de nomenclatura. Tratar todos igualmente pode aumentar o risco de sequestro.

- **Não é DNS**

Infelizmente, consultas em tempo real pela I2P deixariam a navegação web significativamente mais lenta.

Além disso, o DNS é baseado em consultas com cache limitado e tempo de vida, enquanto as chaves I2P são permanentes.

Claro, poderíamos fazer funcionar, mas por quê? É uma má escolha.

- **Não confiável:** Depende de servidores específicos para assinaturas de catálogo de endereços.

Sim, depende de alguns servidores que você configurou. Dentro do I2P, servidores e serviços aparecem e desaparecem. Qualquer outro sistema centralizado (por exemplo, servidores DNS root) teria o mesmo problema. Um sistema completamente descentralizado (todos são autoritativos) é possível implementando uma solução "todos são um servidor DNS root", ou por algo ainda mais simples, como um script que adiciona todos no seu hosts.txt ao seu catálogo de endereços.

Pessoas que defendem soluções totalmente autoritativas geralmente não pensaram bem sobre as questões de conflitos e sequestro, no entanto.

- **Desajeitado, não em tempo real:** É uma colcha de retalhos de provedores de hosts.txt, provedores de formulários web de adição de chaves, provedores de serviços de salto, relatores de status de sites I2P. Servidores de salto e assinaturas são problemáticos, deveria funcionar como o DNS.

Veja as seções de confiabilidade e confiança.

Então, em resumo, o sistema atual não está terrivelmente quebrado, ineficiente ou não escalável, e propostas para "apenas usar DNS" não são bem pensadas.

## Alternativas

O código fonte do I2P contém vários sistemas de nomenclatura plugáveis e suporta opções de configuração para permitir experimentação com sistemas de nomenclatura.

- **Meta** - chama dois ou mais outros sistemas de nomenclatura em ordem. Por padrão, chama PetName depois HostsTxt.
- **PetName** - Procura em um arquivo petnames.txt. O formato para este arquivo NÃO é o mesmo que hosts.txt.
- **HostsTxt** - Procura nos seguintes arquivos, em ordem:
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Cada host é listado em um arquivo separado em um diretório addressDb/.
- **Eepget** - faz uma solicitação de consulta HTTP de um servidor externo - deve ser empilhado após a consulta HostsTxt com Meta. Isso poderia aumentar ou substituir o sistema jump. Inclui cache em memória.
- **Exec** - chama um programa externo para consulta, permite experimentação adicional em esquemas de consulta, independente do java. Pode ser usado após HostsTxt ou como o único sistema de nomenclatura. Inclui cache em memória.
- **Dummy** - usado como fallback para nomes Base64, caso contrário falha.

O sistema de nomenclatura atual pode ser alterado com a opção de configuração avançada `i2p.naming.impl` (reinicialização necessária). Veja `core/java/src/net/i2p/client/naming` para detalhes.

Qualquer novo sistema deve ser empilhado com HostsTxt, ou deve implementar armazenamento local e/ou as funções de subscrição do livro de endereços, uma vez que o livro de endereços apenas conhece os arquivos e formato hosts.txt.

## Certificados

Os destinos I2P contêm um certificado, porém no momento esse certificado é sempre nulo. Com um certificado nulo, os destinos base64 têm sempre 516 bytes terminando em "AAAA", e isso é verificado no mecanismo de fusão do livro de endereços, e possivelmente em outros lugares. Além disso, não há nenhum método disponível para gerar um certificado ou adicioná-lo a um destino. Então estes terão que ser atualizados para implementar certificados.

Um possível uso de certificados é para [prova de trabalho](/get-involved/todo#hashcash).

Outra é para "subdomínios" (entre aspas porque realmente não existe tal coisa, o I2P usa um sistema de nomenclatura plano) serem assinados pelas chaves do domínio de 2º nível.

Com qualquer implementação de certificado deve vir o método para verificar os certificados. Presumivelmente isso aconteceria no código de fusão do livro de endereços. Existe um método para múltiplos tipos de certificados, ou múltiplos certificados?

Adicionar um certificado autenticando as respostas como assinadas por alguma autoridade de certificação centralizada abordaria muitas das questões de nameserver hostil, mas deixaria em aberto ataques de replay bem como ataques de autoridade de certificação hostil.
