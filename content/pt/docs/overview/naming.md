---
title: "Nomenclatura e Livro de Endereços"
description: "Como o I2P mapeia nomes de host legíveis para destinos"
slug: "naming"
aliases:
  - "/pt/docs/specs/naming"
  - "/pt/docs/specs/naming/"
  - "/pt/docs/naming"
  - "/pt/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Visão Geral

O I2P vem com uma biblioteca de nomeação genérica e uma implementação base projetada para funcionar a partir de um mapeamento local de nome para destino, bem como uma aplicação adicional chamada [catálogo de endereços](#address-book). O I2P também suporta [nomes de host Base32](#base32-names) similares aos endereços .onion do Tor.

O livro de endereços é um sistema de nomenclatura seguro, distribuído e legível por humanos baseado em web-of-trust, sacrificando apenas a exigência de que todos os nomes legíveis por humanos sejam globalmente únicos ao exigir apenas unicidade local. Embora todas as mensagens no I2P sejam endereçadas criptograficamente pelo seu destino, pessoas diferentes podem ter entradas no livro de endereços local para "Alice" que se referem a destinos diferentes. As pessoas ainda podem descobrir novos nomes importando livros de endereços publicados de pares especificados em sua web of trust, adicionando as entradas fornecidas através de terceiros, ou (se algumas pessoas organizarem uma série de livros de endereços publicados usando um sistema de registro por ordem de chegada) as pessoas podem optar por tratar esses livros de endereços como servidores de nomes, emulando o DNS tradicional.

NOTA: Para o raciocínio por trás do sistema de nomenclatura do I2P, argumentos comuns contra ele e possíveis alternativas, consulte a página de [discussão sobre nomenclatura](/docs/legacy/naming/).

---

## Componentes do Sistema de Nomenclatura

Não há autoridade central de nomenclatura no I2P. Todos os nomes de host são locais.

O sistema de nomenclatura é bastante simples e a maior parte dele é implementada em aplicações externas ao router, mas incluídas na distribuição do I2P. Os componentes são:

1. O [serviço de nomeação](#naming-services) local que faz consultas e também lida com [nomes de host Base32](#base32-names).
2. O [proxy HTTP](#http-proxy) que solicita consultas ao router e direciona o usuário para serviços de salto remotos para auxiliar com consultas falhadas.
3. [Formulários de adição de host](#host-add-services) HTTP que permitem aos usuários adicionar hosts ao seu hosts.txt local.
4. [Serviços de salto](#jump-services) HTTP que fornecem suas próprias consultas e redirecionamento.
5. A aplicação [livro de endereços](#address-book) que mescla listas de host externas, recuperadas via HTTP, com a lista local.
6. A aplicação [SusiDNS](#susidns) que é uma interface web simples para configuração do livro de endereços e visualização das listas de host locais.

---

## Serviços de Nomenclatura

Todos os destinos no I2P são chaves de 516 bytes (ou mais). (Para ser mais preciso, é uma chave pública de 256 bytes mais uma chave de assinatura de 128 bytes mais um certificado de 3 ou mais bytes, que na representação Base64 tem 516 ou mais bytes. [Certificados](/docs/legacy/naming/#certificates) não-nulos estão em uso agora para indicação do tipo de assinatura. Portanto, certificados em destinos gerados recentemente têm mais de 3 bytes.

Se uma aplicação (i2ptunnel ou o proxy HTTP) deseja acessar um destino por nome, o router faz uma busca local muito simples para resolver esse nome.

### Serviço de Nomenclatura Hosts.txt

O Serviço de Nomes hosts.txt faz uma busca linear simples através de arquivos de texto. Este serviço de nomes foi o padrão até a versão 0.8.8 quando foi substituído pelo Serviço de Nomes Blockfile. O formato hosts.txt havia se tornado muito lento após o arquivo crescer para milhares de entradas.

Ele faz uma busca linear através de três arquivos locais, em ordem, para procurar nomes de host e convertê-los em uma chave de destino de 516 bytes. Cada arquivo está em um [formato de arquivo de configuração](/docs/specs/configuration/) simples, com hostname=base64, um por linha. Os arquivos são:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Serviço de Nomenclatura Blockfile

O Blockfile Naming Service armazena múltiplos "livros de endereços" em um único arquivo de banco de dados chamado hostsdb.blockfile. Este Naming Service é o padrão desde a versão 0.8.8.

Um blockfile é simplesmente armazenamento em disco de múltiplos mapas ordenados (pares chave-valor), implementados como skiplists. O formato blockfile está especificado na [página Blockfile](/docs/specs/blockfile/). Ele fornece pesquisa rápida de Destination em um formato compacto. Embora a sobrecarga do blockfile seja substancial, os destinations são armazenados em binário em vez de Base 64 como no formato hosts.txt. Além disso, o blockfile oferece a capacidade de armazenamento arbitrário de metadados (como data de adição, fonte e comentários) para cada entrada, permitindo implementar recursos avançados do livro de endereços. O requisito de armazenamento do blockfile é um aumento modesto em relação ao formato hosts.txt, e o blockfile oferece aproximadamente 10x de redução nos tempos de pesquisa.

Na criação, o serviço de nomeação importa entradas dos três arquivos usados pelo Serviço de Nomeação hosts.txt. O blockfile imita a implementação anterior mantendo três mapas que são pesquisados em ordem, nomeados privatehosts.txt, userhosts.txt, e hosts.txt. Ele também mantém um mapa de busca reversa para implementar buscas reversas rápidas.

### Outras Facilidades de Serviço de Nomeação

A busca não diferencia maiúsculas de minúsculas. A primeira correspondência é usada, e conflitos não são detectados. Não há aplicação de regras de nomenclatura nas buscas. As buscas são armazenadas em cache por alguns minutos. A resolução Base 32 é [descrita abaixo](#base32-names). Para uma descrição completa da API do Naming Service, consulte o [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). Esta API foi significativamente expandida na versão 0.8.7 para fornecer adições e remoções, armazenamento de propriedades arbitrárias com o hostname, e outras funcionalidades.

### Serviços de Nomenclatura Alternativos e Experimentais

O serviço de nomeação é especificado com a propriedade de configuração `i2p.naming.impl=class`. Outras implementações são possíveis. Por exemplo, existe uma funcionalidade experimental para consultas em tempo real (similar ao DNS) pela rede dentro do router. Para mais informações, consulte as [alternativas na página de discussão](/docs/legacy/naming/#alternatives).

O proxy HTTP faz uma consulta através do router para todos os nomes de host que terminam em '.i2p'. Caso contrário, encaminha a solicitação para um outproxy HTTP configurado. Assim, na prática, todos os nomes de host HTTP (I2P Site) devem terminar no pseudo-Domínio de Nível Superior '.i2p'.

Se o router falhar em resolver o nome do host, o proxy HTTP retorna uma página de erro ao usuário com links para vários serviços de "jump". Veja os detalhes abaixo.

---

## Domínio .i2p.alt

Anteriormente [solicitamos a reserva do TLD .i2p](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) seguindo os procedimentos especificados na [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html). No entanto, esta solicitação e todas as outras foram rejeitadas, e a RFC 6761 foi declarada um "erro".

Após muitos anos de trabalho da equipe GNUnet e outros, o domínio .alt foi reservado como um TLD de uso especial na [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) no final de 2023. Embora não existam registradores oficiais sancionados pela IANA, registramos o domínio .i2p.alt com o principal registrador não oficial [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). Isso não impede que outros usem o domínio, mas deve ajudar a desencorajá-lo.

Uma vantagem do domínio .alt é que, em teoria, os resolvedores DNS não encaminharão solicitações .alt uma vez que sejam atualizados para cumprir com a RFC 9476, e isso impedirá vazamentos de DNS. Para compatibilidade com nomes de host .i2p.alt, o software e serviços I2P devem ser atualizados para lidar com esses nomes de host removendo o TLD .alt. Essas atualizações estão programadas para a primeira metade de 2024.

No momento, não há planos para tornar .i2p.alt a forma preferida para exibição e intercâmbio de nomes de host I2P. Este é um tópico para pesquisa e discussão futuras.

---

## Catálogo de Endereços

### Subscrições de Entrada e Fusão

A aplicação de livro de endereços recupera periodicamente os arquivos hosts.txt de outros usuários e os mescla com o hosts.txt local, após várias verificações. Conflitos de nomenclatura são resolvidos por ordem de chegada.

Subscrever o arquivo hosts.txt de outro usuário envolve depositar nele uma certa quantidade de confiança. Você não quer que ele, por exemplo, "sequestre" um novo site inserindo rapidamente sua própria chave para um novo site antes de passar a nova entrada host/chave para você.

Por esta razão, a única subscrição configurada por padrão é `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, que contém uma cópia do hosts.txt incluído na versão do I2P. Os usuários devem configurar subscrições adicionais na sua aplicação de livro de endereços local (via subscriptions.txt ou [SusiDNS](#susidns)).

Alguns outros links de subscrição de livro de endereços público:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Os operadores destes serviços podem ter várias políticas para listar hosts. A presença nesta lista não implica endosso.

### Regras de Nomenclatura

Embora esperançosamente não existam limitações técnicas dentro do I2P para nomes de host, o livro de endereços impõe várias restrições aos nomes de host importados de assinaturas. Isso é feito para sanidade tipográfica básica e compatibilidade com navegadores, além de segurança. As regras são essencialmente as mesmas daquelas na RFC2396 Seção 3.2.2. Quaisquer nomes de host que violem essas regras podem não ser propagados para outros routers.

Regras de Nomenclatura:

- Os nomes são convertidos para minúsculas na importação.
- Os nomes são verificados quanto a conflitos com nomes existentes no userhosts.txt e hosts.txt existentes (mas não no privatehosts.txt) após conversão para minúsculas.
- Deve conter apenas [a-z] [0-9] '.' e '-' após conversão para minúsculas.
- Não deve começar com '.' ou '-'.
- Deve terminar com '.i2p'.
- Máximo de 67 caracteres, incluindo o '.i2p'.
- Não deve conter '..'.
- Não deve conter '.-' ou '-.' (a partir da versão 0.6.1.33).
- Não deve conter '--' exceto em 'xn--' para IDN.
- Hostnames Base32 (*.b32.i2p) são reservados para uso base 32 e portanto não são permitidos para importação.
- Certos hostnames reservados para uso do projeto não são permitidos (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p, e outros)
- Hostnames começando com 'www.' são desencorajados e são rejeitados por alguns serviços de registro. Algumas implementações de addressbook automaticamente removem prefixos 'www.' das consultas. Então registrar 'www.example.i2p' é desnecessário, e registrar um destino diferente para 'www.example.i2p' e 'example.i2p' tornará 'www.example.i2p' inacessível para alguns usuários.
- As chaves são verificadas quanto à validade base64.
- As chaves são verificadas quanto a conflitos com chaves existentes no hosts.txt (mas não no privatehosts.txt).
- Comprimento mínimo da chave: 516 bytes.
- Comprimento máximo da chave: 616 bytes (para acomodar certificados de até 100 bytes).

Qualquer nome recebido via subscrição que passe em todas as verificações é adicionado através do serviço de nomenclatura local.

Note que os símbolos '.' em um nome de host não têm significado, e não denotam qualquer hierarquia real de nomeação ou confiança. Se o nome 'host.i2p' já existir, não há nada que impeça qualquer pessoa de adicionar um nome 'a.host.i2p' ao seu hosts.txt, e esse nome pode ser importado pelo catálogo de endereços de outros. Métodos para negar subdomínios a não 'proprietários' de domínio (certificados?), e a desejabilidade e viabilidade desses métodos, são tópicos para discussão futura.

Nomes de Domínio Internacionais (IDN) também funcionam no i2p (usando a forma punycode 'xn--'). Para ver os nomes de domínio IDN .i2p renderizados corretamente na barra de endereços do Firefox, adicione 'network.IDN.whitelist.i2p (boolean) = true' em about:config.

Como a aplicação do catálogo de endereços não utiliza o privatehosts.txt de forma alguma, na prática este arquivo é o único local onde é apropriado colocar aliases privados ou "nomes de estimação" para sites já presentes no hosts.txt.

### Formato Avançado de Feed de Subscrição

A partir da versão 0.9.26, sites de subscrição e clientes podem suportar um protocolo avançado de feed hosts.txt que inclui metadados incluindo assinaturas. Este formato é compatível com versões anteriores do formato padrão hosts.txt hostname=base64destination. Veja [a especificação](/docs/specs/subscription/) para detalhes.

### Subscrições de Saída

O Address Book publicará o hosts.txt mesclado em um local (tradicionalmente hosts.txt no diretório home do I2P Site local) para ser acessado por outros para suas subscrições. Esta etapa é opcional e está desabilitada por padrão.

### Problemas de Hospedagem e Transporte HTTP

A aplicação de catálogo de endereços, juntamente com o eepget, salva as informações Etag e/ou Last-Modified retornadas pelo servidor web da subscrição. Isso reduz significativamente a largura de banda necessária, pois o servidor web retornará um '304 Not Modified' na próxima busca se nada tiver mudado.

No entanto, todo o arquivo hosts.txt é baixado se ele tiver sido alterado. Veja abaixo a discussão sobre esta questão.

Hosts que servem um arquivo hosts.txt estático ou uma aplicação CGI equivalente são fortemente encorajados a fornecer um cabeçalho Content-Length, e um cabeçalho Etag ou Last-Modified. Também certifique-se de que o servidor entregue um '304 Not Modified' quando apropriado. Isso reduzirá drasticamente a largura de banda da rede e reduzirá as chances de corrupção.

---

## Adicionar Serviços do Host

Um serviço de adição de host é uma aplicação CGI simples que recebe um nome de host e uma chave Base64 como parâmetros e adiciona isso ao seu hosts.txt local. Se outros routers se inscreverem nesse hosts.txt, o novo nome de host/chave será propagado através da rede.

É recomendado que os serviços de adição de hosts imponham, no mínimo, as restrições impostas pela aplicação de livro de endereços listada acima. Os serviços de adição de hosts podem impor restrições adicionais em nomes de hosts e chaves, por exemplo:

- Um limite no número de 'subdomínios'.
- Autorização para 'subdomínios' através de vários métodos.
- Hashcash ou certificados assinados.
- Revisão editorial de nomes de host e/ou conteúdo.
- Categorização de hosts por conteúdo.
- Reserva ou rejeição de determinados nomes de host.
- Restrições no número de nomes registrados em um determinado período de tempo.
- Atrasos entre registro e publicação.
- Exigência de que o host esteja ativo para verificação.
- Expiração e/ou revogação.
- Rejeição de spoofing IDN.

---

## Serviços de Jump

Um serviço de salto é uma aplicação CGI simples que recebe um hostname como parâmetro e retorna um redirecionamento 301 para a URL adequada com uma string `?i2paddresshelper=key` anexada. O proxy HTTP interpretará a string anexada e usará essa chave como o destino real. Além disso, o proxy armazenará essa chave em cache para que o auxiliar de endereço não seja necessário até reiniciar.

Note que, assim como com as assinaturas, usar um serviço de salto implica uma certa quantidade de confiança, já que um serviço de salto poderia redirecionar maliciosamente um usuário para um destino incorreto.

Para fornecer o melhor serviço, um serviço de salto deve estar inscrito em vários provedores de hosts.txt para que sua lista local de hosts esteja atualizada.

---

## SusiDNS

O SusiDNS é simplesmente uma interface web front-end para configurar assinaturas de livro de endereços e acessar os quatro arquivos de livro de endereços. Todo o trabalho real é feito pela aplicação 'address book'.

Atualmente, há pouca aplicação das regras de nomenclatura do livro de endereços dentro do SusiDNS, então um usuário pode inserir nomes de host localmente que seriam rejeitados pelas regras de assinatura do livro de endereços.

---

## Nomes Base32

O I2P suporta hostnames Base32 similares aos endereços .onion do Tor. Endereços Base32 são muito mais curtos e fáceis de manusear do que os Destinations Base64 completos de 516 caracteres ou addresshelpers. Exemplo: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

No Tor, o endereço tem 16 caracteres (80 bits), ou metade do hash SHA-1. O I2P usa 52 caracteres (256 bits) para representar o hash SHA-256 completo. O formato é {52 chars}.b32.i2p. O Tor tem uma [proposta](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) para converter para um formato idêntico de {52 chars}.onion para seus serviços ocultos. Base32 é implementado no serviço de nomenclatura, que consulta o router através do I2CP para buscar o leaseSet e obter o Destination completo. As buscas Base32 só serão bem-sucedidas quando o Destination estiver ativo e publicando um leaseSet. Como a resolução pode exigir uma busca na base de dados da rede, pode demorar significativamente mais do que uma busca no catálogo de endereços local.

Endereços Base32 podem ser usados na maioria dos lugares onde hostnames ou destinos completos são utilizados, porém há algumas exceções onde podem falhar se o nome não resolver imediatamente. I2PTunnel falhará, por exemplo, se o nome não resolver para um destino.

---

## Nomes Base32 Estendidos

Os nomes base 32 estendidos foram introduzidos na versão 0.9.40 para suportar leasesets criptografados. Endereços para leasesets criptografados são identificados por 56 ou mais caracteres codificados, não incluindo o ".b32.i2p" (35 ou mais bytes decodificados), comparado a 52 caracteres (32 bytes) para endereços base 32 tradicionais. Veja as propostas 123 e 149 para informações adicionais.

Endereços Base 32 padrão ("b32") contêm o hash do destino. Isso não funcionará para ls2 criptografado (proposta 123).

Você não pode usar um endereço base 32 tradicional para um LS2 criptografado (proposta 123), pois ele contém apenas o hash do destino. Ele não fornece a chave pública não-ofuscada. Os clientes devem conhecer a chave pública do destino, tipo de assinatura, o tipo de assinatura ofuscada e uma chave secreta ou privada opcional para buscar e descriptografar o leaseset. Portanto, um endereço base 32 sozinho é insuficiente. O cliente precisa do destino completo (que contém a chave pública) ou da própria chave pública. Se o cliente tiver o destino completo em um catálogo de endereços, e o catálogo de endereços suportar busca reversa por hash, então a chave pública pode ser recuperada.

Então precisamos de um novo formato que coloque a chave pública em vez do hash em um endereço base32. Este formato também deve conter o tipo de assinatura da chave pública e o tipo de assinatura do esquema de ocultação.

Esta seção documenta um novo formato b32 para esses endereços. Embora tenhamos nos referido a este novo formato durante as discussões como um endereço "b33", o formato novo atual mantém o sufixo usual ".b32.i2p".

### Criação e codificação

Construa um hostname de {56+ chars}.b32.i2p (35+ chars em binário) da seguinte forma. Primeiro, construa os dados binários a serem codificados em base 32:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Pós-processamento e checksum:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Quaisquer bits não utilizados no final do b32 devem ser 0. Não há bits não utilizados para um endereço padrão de 56 caracteres (35 bytes).

### Decodificação e Verificação

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits de Chave Secreta e Privada

Os bits de chave secreta e privada são usados para indicar a clientes, proxies ou outro código do lado do cliente que a chave secreta e/ou privada será necessária para descriptografar o leaseset. Implementações específicas podem solicitar ao usuário que forneça os dados necessários, ou rejeitar tentativas de conexão se os dados necessários estiverem ausentes.

### Notas

- Fazer XOR dos primeiros 3 bytes com o hash fornece uma capacidade limitada de checksum e garante que todos os caracteres base32 no início sejam aleatorizados. Apenas algumas combinações de flag e sigtype são válidas, então qualquer erro de digitação provavelmente criará uma combinação inválida e será rejeitada.
- No caso usual (sigtypes de 1 byte, sem segredo, sem autenticação por cliente), o hostname será {56 chars}.b32.i2p, decodificando para 35 bytes, mesmo que o Tor.
- O checksum de 2 bytes do Tor tem uma taxa de falso negativo de 1/64K. Com 3 bytes, menos alguns bytes ignorados, o nosso está se aproximando de 1 em um milhão, já que a maioria das combinações flag/sigtype são inválidas.
- Adler-32 é uma má escolha para entradas pequenas e para detectar pequenas mudanças. Usamos CRC-32 em vez disso. CRC-32 é rápido e amplamente disponível.
- Embora fora do escopo desta especificação, routers e/ou clientes devem lembrar e armazenar em cache (provavelmente de forma persistente) o mapeamento de chave pública para destino, e vice-versa.
- Distinguir versões antigas das novas pelo comprimento. Endereços b32 antigos são sempre {52 chars}.b32.i2p. Os novos são {56+ chars}.b32.i2p
- Thread de discussão do Tor [está aqui](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Não espere que sigtypes de 2 bytes aconteçam, estamos apenas no 13. Não há necessidade de implementar agora.
- O novo formato pode ser usado em jump links (e servido por jump servers) se desejado, assim como b32.
- Qualquer segredo, chave privada ou chave pública maior que 32 bytes excederia o comprimento máximo de label DNS de 63 caracteres. Navegadores provavelmente não se importam.
- Nenhum problema de compatibilidade com versões anteriores. Endereços b32 mais longos falharão ao serem convertidos para hashes de 32 bytes em software antigo.
