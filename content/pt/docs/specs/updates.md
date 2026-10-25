---
title: "Especificação de Atualização de Software"
description: "Especificação para o mecanismo de atualização de software I2P, formato de arquivo SU3 e feed de notícias"
slug: "updates"
aliases:
  - "/pt/updates"
  - "/pt/updates/"
category: "Design"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Visão Geral

O I2P usa um sistema simples, mas seguro, para atualizações automáticas de software. O console do router periodicamente busca um arquivo de notícias de uma URL I2P configurável. Há uma URL de backup codificada que aponta para o site do projeto, caso o host de notícias padrão do projeto fique fora do ar.

O conteúdo do arquivo de notícias é exibido na página inicial do console do router. Além disso, o arquivo de notícias contém o número da versão mais recente do software. Se a versão for superior ao número da versão do router, será exibida uma indicação ao usuário de que uma atualização está disponível.

O router pode opcionalmente baixar, ou baixar e instalar, a nova versão se configurado para fazê-lo.

## Especificação de Arquivo de Notícias Antigas

Este formato foi substituído pelo formato de notícias su3 a partir da versão 0.9.17.

O arquivo news.xml pode conter os seguintes elementos:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
Os parâmetros na entrada i2p.release são os seguintes. Todas as chaves não diferenciam maiúsculas de minúsculas. Todos os valores devem estar entre aspas duplas.

**date** : A data de lançamento da versão do router. Não utilizado. Formato não especificado.

**minJavaVersion** : A versão mínima do Java necessária para executar a versão atual. A partir da versão 0.9.9.

**minVersion** : A versão mínima do router necessária para atualizar para a versão atual. Se um router for mais antigo que isso, o usuário deve (manualmente?) atualizar para uma versão intermediária primeiro. A partir da versão 0.9.9.

**su3Clearnet** : Uma ou mais URLs HTTP onde o arquivo de atualização .su3 pode ser encontrado na clearnet (não-I2P). Múltiplas URLs devem ser separadas por espaço ou vírgula. A partir da versão 0.9.9.

**su3SSL** : Uma ou mais URLs HTTPS onde o arquivo de atualização .su3 pode ser encontrado na clearnet (não-I2P). Múltiplas URLs devem ser separadas por espaço ou vírgula. A partir da versão 0.9.9.

**sudTorrent** : O link magnet para o torrent .sud (não-pack200) da atualização. A partir da versão 0.9.4.

**su2Torrent** : O link magnet para o torrent .su2 (pack200) da atualização. A partir da versão 0.9.4.

**su3Torrent** : O link magnético para o torrent .su3 (novo formato) da atualização. A partir da versão 0.9.9.

**version** : Obrigatório. A versão mais recente do router atualmente disponível.

Os elementos podem ser incluídos dentro de comentários XML para prevenir interpretação pelos navegadores. O elemento i2p.release e a versão são obrigatórios. Todos os outros são opcionais. NOTA: Devido a limitações do analisador, um elemento completo deve estar em uma única linha.

## Especificação do Arquivo de Atualização

A partir da versão 0.9.9, o arquivo de atualização assinado, chamado i2pupdate.su3, utilizará o formato de arquivo "su3" especificado abaixo. Os signatários de versões aprovados utilizarão chaves RSA de 4096 bits. Os certificados de chave pública X.509 para estes signatários são distribuídos nos pacotes de instalação do router. As atualizações podem conter certificados para novos signatários aprovados e/ou conter uma lista de certificados a serem excluídos para revogação.

## Especificação do Arquivo de Atualização Antigo

Este formato está obsoleto desde a versão 0.9.9.

O arquivo de atualização assinado, tradicionalmente chamado i2pupdate.sud, é simplesmente um arquivo zip com um cabeçalho de 56 bytes anexado no início. O cabeçalho contém:

- Uma [Assinatura](/docs/specs/common-structures#signature) DSA de 40 bytes
- Uma versão I2P de 16 bytes em UTF-8, preenchida com zeros à direita se necessário

A assinatura cobre apenas o arquivo zip - não a versão anteposta. A assinatura deve corresponder a uma das chaves DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) configuradas no router, que possui uma lista padrão codificada de chaves dos gerentes de lançamento atuais do projeto.

Para fins de comparação de versões, os campos de versão contêm [0-9]*, os separadores de campo são '-', '_' e '.', e todos os outros caracteres são ignorados.

A partir da versão 0.8.8, a versão também deve ser especificada como um comentário do arquivo zip em UTF-8, sem os zeros finais. O router que está atualizando verifica se a versão no cabeçalho (não coberta pela assinatura) corresponde à versão no comentário do arquivo zip, que é coberta pela assinatura. Isso impede a falsificação do número da versão no cabeçalho.

## Download e Instalação

O router primeiro baixa o cabeçalho do arquivo de atualização de uma URL I2P em uma lista configurável, usando o cliente HTTP integrado e proxy, e verifica se a versão é mais recente. Isso evita o problema de hosts de atualização que não têm o arquivo mais recente. O router então baixa o arquivo de atualização completo. O router verifica se a versão do arquivo de atualização é mais recente antes da instalação. Também, é claro, verifica a assinatura e verifica se o comentário do arquivo zip corresponde à versão do cabeçalho, conforme explicado acima.

O arquivo zip é extraído e copiado para "i2pupdate.zip" no diretório de configuração do I2P (~/.i2p no Linux).

A partir da versão 0.7.12, o router suporta descompressão Pack200. Arquivos dentro do arquivo zip com sufixo .jar.pack ou .war.pack são transparentemente descomprimidos para um arquivo .jar ou .war. Arquivos de atualização contendo arquivos .pack são tradicionalmente nomeados com sufixo '.su2'. Pack200 reduz os arquivos de atualização em cerca de 60%.

A partir da versão 0.8.7, o router irá deletar os arquivos libjbigi.so e libjcpuid.so se o arquivo zip contiver um arquivo lib/jbigi.jar, para que os novos arquivos sejam extraídos do jbigi.jar.

A partir da versão 0.8.12, se o arquivo zip contiver um arquivo deletelist.txt, o router irá deletar os arquivos listados lá. O formato é:

- Um nome de arquivo por linha
- Todos os nomes de arquivo são relativos ao diretório de instalação; nomes de arquivo absolutos não são permitidos, nenhum arquivo começando com ".."
- Comentários começam com '#'

O router irá então excluir o arquivo deletelist.txt.

## Especificação de Arquivo SU3

Esta especificação é usada para atualizações do router a partir da versão 0.9.9, dados de reseed a partir da versão 0.9.14, plugins a partir da versão 0.9.15, e o arquivo de notícias a partir da versão 0.9.17.

### Problemas com o formato anterior .sud/.su2

- Nenhum número mágico ou flags
- Nenhuma forma de especificar compressão, pack200 ou não, ou algoritmo de assinatura
- A versão não é coberta pela assinatura, então é aplicada exigindo que esteja no comentário do arquivo zip (para arquivos do router) ou no arquivo plugin.config (para plugins)
- Signatário não especificado, então o verificador deve tentar todas as chaves conhecidas
- Formato de assinatura-antes-dos-dados requer duas passadas para gerar o arquivo

### Objetivos

- Corrigir os problemas acima
- Migrar para algoritmo de assinatura mais seguro
- Manter informações de versão no mesmo formato e deslocamento para compatibilidade com verificadores de versão existentes
- Verificação de assinatura e extração de arquivo em uma única passagem

### Especificação

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Todos os campos não utilizados devem ser definidos como 0 para compatibilidade com versões futuras.

### Detalhes da Assinatura

A assinatura cobre todo o cabeçalho começando no byte 0, até o final do conteúdo. Usamos assinaturas brutas. Pegue o hash dos dados (usando o tipo de hash implícito pelo tipo de assinatura nos bytes 8-9) e passe isso para uma função de assinatura ou verificação "bruta" (por exemplo, "NONEwithRSA" em Java).

Embora a verificação de assinatura e extração de conteúdo possam ser implementadas em uma única passagem, uma implementação deve ler e armazenar em buffer os primeiros 10 bytes para determinar o tipo de hash antes de começar a verificar.

Os comprimentos de assinatura para os vários tipos de assinatura são fornecidos na especificação de [Signature](/docs/specs/common-structures#signature). Preencha a assinatura com zeros à esquerda se necessário. Consulte a [página de detalhes criptográficos](/docs/specs/cryptography#sig) para os parâmetros dos vários tipos de assinatura.

### Notas

O tipo de conteúdo especifica o domínio de confiança. Para cada tipo de conteúdo, os clientes mantêm um conjunto de certificados de chave pública X.509 para as partes confiáveis para assinar esse conteúdo. Apenas certificados para o tipo de conteúdo especificado podem ser usados. O certificado é localizado pelo ID do signatário. Os clientes devem verificar se o tipo de conteúdo é o esperado para a aplicação.

Todos os valores estão em ordem de bytes de rede (big endian).

Para uma implementação em Python de assinaturas RSA brutas compatível com Java "NONEwithRSA", veja [este artigo do Stack Overflow](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## Especificação do Arquivo de Atualização SU3 do Router

### Detalhes do SU3

- Tipo de Conteúdo SU3: 1 (ROUTER UPDATE)
- Tipo de Arquivo SU3: 0 (ZIP)
- Versão SU3: A versão do router

Arquivos jar e war no zip não são mais comprimidos com pack200 como documentado acima para arquivos "su2", porque as versões recentes do Java não suportam mais essa funcionalidade.

### Notas

- Para lançamentos, a versão SU3 é a versão "base" do router, por exemplo "0.9.20".
- Para builds de desenvolvimento, que são suportados a partir do lançamento 0.9.20, a versão SU3 é a versão "completa" do router, por exemplo "0.9.20-5" ou "0.9.20-5-rc". Veja RouterVersion.java no [código fonte do I2P](https://github.com/i2p/i2p.i2p).

## Especificação de Arquivo SU3 Reseed

A partir da versão 0.9.14, os dados de reseed são entregues em formato de arquivo "su3".

### Objetivos

- Arquivos assinados com assinaturas fortes e certificados confiáveis para prevenir ataques man-in-the-middle que poderiam inicializar vítimas em uma rede separada e não confiável.
- Usar formato de arquivo su3 já utilizado para atualizações e plugins
- Arquivo comprimido único para acelerar o reseeding, que era lento para buscar 200 arquivos

### Especificação

1. O arquivo deve ser nomeado "i2pseeds.su3". A partir da versão 0.9.42, o solicitante deve anexar uma string de consulta "?netid=2" à URL da solicitação, assumindo o ID de rede atual de 2. Isso pode ser usado para prevenir conexões entre redes. Redes de teste devem definir um ID de rede diferente. Veja a proposta 147 para detalhes.
2. O arquivo deve estar no mesmo diretório que os router infos no servidor web.
3. Um router primeiro tentará buscar (URL do índice)/i2pseeds.su3; se isso falhar, ele buscará a URL do índice e então buscará os arquivos de router info individuais encontrados nos links.

### Detalhes do SU3

- Tipo de Conteúdo SU3: 3 (RESEED)
- Tipo de Arquivo SU3: 0 (ZIP)
- Versão SU3: Segundos desde a época, em ASCII (date +%s). NÃO reinicia em 2038 ou 2106.
- Arquivos de informações do router no arquivo zip devem estar no "nível superior". Não há diretórios no arquivo zip.
- Arquivos de informações do router devem ser nomeados "routerInfo-(hash do router em base 64 de 44 caracteres).dat", como no mecanismo de reseed antigo. O alfabeto base 64 do I2P deve ser usado.

### Notas

- Aviso: Vários reseeds são conhecidos por não responder via IPv6. É recomendado forçar ou preferir IPv4.
- Aviso: Alguns reseeds usam certificados CA auto-assinados. As implementações devem importar e confiar nessas CAs ao fazer reseed, ou omitir os reseeds auto-assinados da lista de reseed.
- As chaves de assinatura de reseed são distribuídas às implementações como certificados X.509 auto-assinados com chaves RSA-4096 (tipo de assinatura 6). As implementações devem impor as datas válidas nos certificados.

## Especificação de Arquivo de Plugin SU3

A partir da versão 0.9.15, plugins podem ser empacotados no formato de arquivo "su3".

### Detalhes SU3

- SU3 Content Type: 2 (PLUGIN)
- SU3 File Type: 0 (ZIP) - Veja a [especificação de plugin](/docs/specs/plugin) para detalhes.
- SU3 Version: A versão do plugin, deve corresponder àquela em plugin.config.

Arquivos jar e war no zip não devem ser comprimidos com pack200 como documentado acima para arquivos "su2", pois versões recentes do Java não oferecem mais suporte a isso.

## Especificação do Arquivo de Notícias SU3

A partir da versão 0.9.17, as notícias são entregues no formato de arquivo "su3".

### Objetivos

- Notícias assinadas com assinaturas fortes e certificados confiáveis
- Usa formato de arquivo su3 já utilizado para atualizações, reseeding e plugins
- Formato XML padrão para uso com analisadores padrão
- Formato Atom padrão para uso com leitores e geradores de feed padrão
- Sanitização e verificação de HTML antes da exibição no console
- Adequado para implementação fácil no Android e outras plataformas sem console HTML

### Detalhes do SU3

- Tipo de Conteúdo SU3: 4 (NEWS)
- Tipo de Arquivo SU3: 1 (XML) ou 3 (XML.GZ)
- Versão SU3: Segundos desde a época, em ASCII (date +%s). NÃO redefine em 2038 ou 2106.
- Formato do Arquivo: XML ou XML comprimido com gzip, contendo um Feed XML [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom). O conjunto de caracteres deve ser UTF-8.

### Detalhes do Feed Atom

Os seguintes elementos `<feed>` são utilizados:

**`<entry>`** : Um item de notícia. Veja abaixo.

**`<i2p:release>`** : Metadados de atualização do I2P. Veja abaixo.

**`<i2p:revocations>`** : Revogações de certificado. Veja abaixo.

**`<i2p:blocklist>`** : Dados da lista de bloqueio. Veja abaixo.

**`<updated>`** : Obrigatório. Carimbo de data/hora para o feed (em conformidade com a [RFC 4287](https://tools.ietf.org/html/rfc4287) seção 3.3 e [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Detalhes da Entrada Atom

Cada `<entry>` Atom no feed de notícias pode ser analisada e exibida no console do router. Os seguintes elementos são utilizados:

**`<author>`** : Opcional. Contendo `<name>` - O nome do autor da entrada.

**`<content>`** : Obrigatório. Conteúdo, deve ser type="xhtml". O XHTML será sanitizado com uma lista de elementos permitidos e uma lista negra de atributos não permitidos. Os clientes podem ignorar um elemento, ou a entrada que o contém, ou todo o feed quando um elemento não incluído na lista de permitidos for encontrado.

**`<link>`** : Opcional. Link para mais informações.

**`<summary>`** : Opcional. Resumo curto, adequado para uma dica de ferramenta.

**`<title>`** : Obrigatório. Título da entrada de notícias.

**`<updated>`** : Obrigatório. Timestamp para esta entrada (conforme [RFC 4287](https://tools.ietf.org/html/rfc4287) seção 3.3 e [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Detalhes do Atom i2p:release

Deve haver pelo menos uma entidade `<i2p:release>` no feed. Cada uma contém os seguintes atributos e entidades:

**date (atributo)** : Obrigatório. Timestamp para esta entrada (em conformidade com a [RFC 4287](https://tools.ietf.org/html/rfc4287) seção 3.3 e [RFC 3339](https://tools.ietf.org/html/rfc3339)). A data também pode estar no formato truncado yyyy-mm-dd (sem o 'T'); este é o formato "full-date" na RFC 3339. Neste formato, assume-se que o horário seja 00:00:00 UTC para qualquer processamento.

**minJavaVersion (atributo)** : Se presente, a versão mínima do Java necessária para executar a versão atual.

**minVersion (atributo)** : Se presente, a versão mínima do router necessária para atualizar para a versão atual. Se um router for mais antigo que esta, o usuário deve (manualmente?) atualizar para uma versão intermediária primeiro.

**`<i2p:version>`** : Obrigatório. A versão mais recente do router disponível.

**`<i2p:update>`** : Um arquivo de atualização (um ou mais). Deve conter pelo menos um filho.   - type (atributo): "sud", "su2", ou "su3". Deve ser único em todos os elementos `<i2p:update>`.   - `<i2p:clearnet>`: Links de download direto fora da rede (zero ou mais). href (atributo): Um link http padrão da clearnet.   - `<i2p:clearnetssl>`: Links de download direto fora da rede (zero ou mais). href (atributo): Um link https padrão da clearnet.   - `<i2p:torrent>`: Link magnet dentro da rede. href (atributo): Um link magnet.   - `<i2p:url>`: Links de download direto dentro da rede (zero ou mais). href (atributo): Um link http .i2p dentro da rede.

### Detalhes do Atom i2p:revocations

Esta entidade é opcional e há no máximo uma entidade `<i2p:revocations>` no feed. Esta funcionalidade é suportada a partir da versão 0.9.26.

A entidade `<i2p:revocations>` contém uma ou mais entidades `<i2p:crl>`. A entidade `<i2p:crl>` contém os seguintes atributos:

**updated (atributo)** : Obrigatório. Timestamp para esta entrada (em conformidade com [RFC 4287](https://tools.ietf.org/html/rfc4287) seção 3.3 e [RFC 3339](https://tools.ietf.org/html/rfc3339)). A data também pode estar no formato truncado yyyy-mm-dd (sem o 'T'); este é o formato "full-date" no RFC 3339. Neste formato assume-se que a hora seja 00:00:00 UTC para qualquer processamento.

**id (atributo)** : Obrigatório. Um id único para o criador desta CRL.

**(conteúdo da entidade)** : Obrigatório. Uma Lista de Revogação de Certificado (CRL) padrão codificada em base 64 com quebras de linha, começando com a linha '-----BEGIN X509 CRL-----' e terminando com a linha '-----END X509 CRL-----'. Consulte [RFC 5280](https://tools.ietf.org/html/rfc5280) para mais informações sobre CRLs.

### Detalhes do Atom i2p:blocklist

Esta entidade é opcional e existe no máximo uma entidade `<i2p:blocklist>` no feed. Esta funcionalidade está programada para implementação na versão 0.9.28.

A entidade `<i2p:blocklist>` contém uma ou mais entidades `<i2p:block>` ou `<i2p:unblock>`, uma entidade "updated", e atributos "signer" e "sig":

**signer (atributo)** : Obrigatório. Um id único (UTF-8) para a chave pública usada para assinar esta lista de bloqueio.

**sig (atributo)** : Obrigatório. Uma assinatura no formato code:b64sig, onde code é o número ASCII do tipo de assinatura, e b64sig é a assinatura codificada em base 64 (alfabeto I2P). Veja abaixo a especificação dos dados a serem assinados.

**`<updated>`** : Obrigatório. Timestamp para a blocklist (em conformidade com [RFC 4287](https://tools.ietf.org/html/rfc4287) seção 3.3 e [RFC 3339](https://tools.ietf.org/html/rfc3339)). A data também pode estar em formato truncado yyyy-mm-dd (sem o 'T'); este é o formato "full-date" no RFC 3339. Neste formato, a hora é assumida como 00:00:00 UTC para qualquer processamento.

**`<i2p:block>`** : Opcional, múltiplas entidades são permitidas. Uma única entrada, seja um endereço IPv4 ou IPv6 literal, ou um hash de router base 64 de 44 caracteres (alfabeto I2P). Endereços IPv6 podem estar em formato abreviado (contendo "::"). O suporte para entradas com máscara de rede, ex. x.y.0.0/16, é opcional. O suporte para nomes de host é opcional.

**`<i2p:unblock>`** : Opcional, múltiplas entidades são permitidas. Mesmo formato que `<i2p:block>`.

**Especificação da assinatura:** Para gerar os dados a serem assinados ou verificados, concatene os seguintes dados em codificação ASCII: A string atualizada seguida de uma nova linha (ASCII 0x0a), então cada entrada de bloco na ordem recebida com uma nova linha após cada uma, depois cada entrada de desbloqueio na ordem recebida com uma nova linha após cada uma.

## Especificação do Arquivo de Lista de Bloqueio

A definir, não implementado, veja a proposta 130. As atualizações da blocklist são entregues no arquivo de notícias, veja acima.

## Trabalho Futuro

- O mecanismo de atualização do router faz parte do console web do router. Atualmente não há provisão para atualizações de um router incorporado que não possui o console do router.

## Referências

- **[CRYPTO-SIG]** [Criptografia - Assinaturas](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [Código Fonte I2P](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Especificação de Plugin](/docs/specs/plugin)
- **[Python]** [Assinaturas RSA Raw em Python](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Data e Hora](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Formato de Sindicação Atom](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Listas de Revogação de Certificados](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Tipo Signature](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [Tipo SigningPublicKey](/docs/specs/common-structures#signingpublickey)
