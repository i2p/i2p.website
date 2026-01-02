---
title: "Registros de Serviço em LS2"
number: "167"
author: "zzz, orignal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Fechado"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## Status
Aprovado na 2ª revisão em 2025-04-01; especificações são atualizadas; ainda não implementado.


## Visão Geral

O I2P não possui um sistema DNS centralizado.
No entanto, o livro de endereços, juntamente com o sistema de nome de host b32, permite
que o roteador busque destinos completos e busque conjuntos de leasing, que contêm
uma lista de gateways e chaves para que os clientes possam se conectar a esse destino.

Portanto, os conjuntos de leasing são um pouco como um registro DNS. Mas atualmente não há como
saber se esse host suporta algum serviço, seja nesse destino ou em outro,
de maneira semelhante aos registros DNS SRV [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

A primeira aplicação para isso pode ser email peer-to-peer.
Outras possíveis aplicações: DNS, GNS, servidores de chaves, autoridades de certificação, servidores de tempo,
bittorrent, criptomoedas, outras aplicações peer-to-peer.


## Propostas e Alternativas Relacionadas

### Listas de Serviço

A proposta LS2 123 [Prop123](/proposals/123-new-netdb-entries/) definiu 'registros de serviço' que indicavam que um destino
estava participando de um serviço global. Os floodfills agregariam esses registros
em 'listas de serviço' globais.
Isso nunca foi implementado devido à complexidade, falta de autenticação,
preocupações de segurança e spamming.

Essa proposta é diferente no sentido de que ela oferece busca por um serviço para um destino específico,
não um pool global de destinos para algum serviço global.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) propõe que todos rodem seu próprio servidor DNS.
Esta proposta é complementar, pois poderíamos usar registros de serviço para especificar
que o GNS (ou DNS) é suportado, com um nome de serviço padrão de "domínio" na porta 53.

### Dot well-known

Em [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) é proposto que os serviços sejam buscados via uma solicitação HTTP para
/.well-known/i2pmail.key. Isso requer que cada serviço tenha um site relacionado para
hospedar a chave. A maioria dos usuários não administra sites.

Uma solução alternativa é presumirmos que um serviço para um endereço b32 está realmente
executando nesse endereço b32. Assim, procurar o serviço para example.i2p requer
a busca HTTP de http://example.i2p/.well-known/i2pmail.key, mas
um serviço para aaa...aaa.b32.i2p não requer essa busca, ele pode apenas conectar diretamente.

Mas há uma ambiguidade aí, porque example.i2p também pode ser endereçado por seu b32.

### Registros MX

Registros SRV são simplesmente uma versão genérica de registros MX para qualquer serviço.
"_smtp._tcp" é o registro "MX".
Não há necessidade de registros MX se tivermos registros SRV, e registros MX
sozinhos não fornecem um registro genérico para qualquer serviço.


## Design

Os registros de serviço são colocados na seção de opções no LS2 [LS2](/docs/specs/common-structures/).
A seção de opções do LS2 atualmente não é utilizada.
Não suportado para LS1.
Isso é semelhante à proposta de largura de banda de túnel [Prop168](/proposals/168-tunnel-bandwidth/),
que define opções para registros de construção de túnel.

Para buscar um endereço de serviço para um hostname específico ou b32, o roteador busca o
conjunto de leasing e procura o registro de serviço nas propriedades.

O serviço pode ser hospedado no mesmo destino que o próprio LS, ou pode referenciar
um hostname/b32 diferente.

Se o destino alvo para o serviço for diferente, o LS alvo deve também
incluir um registro de serviço, apontando para si mesmo, indicando que suporta o serviço.

O design não requer suporte especial ou cache ou quaisquer alterações nos floodfills.
Apenas o editor do conjunto de leasing e o cliente que busca um registro de serviço
devem suportar essas alterações.

Extensões menores de I2CP e SAM são propostas para facilitar a recuperação de
registros de serviço pelos clientes.


## Especificação

### Especificação de Opção LS2

As opções LS2 DEVEM ser ordenadas por chave, portanto, a assinatura é invariável.

Definido da seguinte forma:

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := O nome simbólico do serviço desejado. Deve ser em minúsculas. Exemplo: "smtp".
  Os caracteres permitidos são [a-z0-9-] e não devem começar ou terminar com um '-'.
  Identificadores padrão de [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) ou Linux /etc/services devem ser usados se estiverem definidos lá.
- proto := O protocolo de transporte do serviço desejado. Deve ser em minúsculas, "tcp" ou "udp".
  "tcp" significa streaming e "udp" significa datagramas replicáveis.
  Indicadores de protocolo para datagramas brutos e datagrama2 podem ser definidos mais tarde.
  Os caracteres permitidos são [a-z0-9-] e não devem começar ou terminar com um '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := tempo de vida, em segundos inteiros. Inteiro positivo. Exemplo: "86400".
  Um mínimo de 86400 (um dia) é recomendado, veja a seção de Recomendações abaixo para detalhes.
- priority := A prioridade do host alvo, valor mais baixo significa mais preferido. Inteiro não negativo. Exemplo: "0"
  Útil apenas se houver mais de um registro, mas exigido mesmo que haja apenas um registro.
- weight := Um peso relativo para registros com a mesma prioridade. Valor mais alto significa mais chance de ser escolhido. Inteiro não negativo. Exemplo: "0"
  Útil apenas se houver mais de um registro, mas exigido mesmo que haja apenas um registro.
- port := A porta I2CP na qual o serviço deve ser encontrado. Inteiro não negativo. Exemplo: "25"
  Porta 0 é suportada, mas não recomendada.
- target := O hostname ou b32 do destino que fornece o serviço. Um hostname válido conforme [NAMING](/docs/overview/naming/). Deve ser em minúsculas.
  Exemplo: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" ou "example.i2p".
  b32 é recomendado, a menos que o hostname seja "bem conhecido", ou seja, em livros de endereços oficiais ou padrão.
- appoptions := texto arbitrário específico para a aplicação, não deve conter " " ou ",". A codificação é UTF-8.

### Exemplos


No LS2 para aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, apontando para um servidor SMTP:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

No LS2 para aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, apontando para dois servidores SMTP:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

No LS2 para bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, apontando para ele mesmo como um servidor SMTP:

    "_smtp._tcp" "0 999999 25"

Formato possível para redirecionamento de email (veja abaixo):

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Limites


O formato da estrutura de dados Mapping usado para opções LS2 limita as chaves e valores a 255 bytes (não caracteres) no máximo.
Com um alvo b32, o valor da opção é de cerca de 67 bytes, portanto, apenas 3 registros caberiam.
Talvez apenas um ou dois com um campo appoptions longo, ou até quatro ou cinco com um hostname curto.
Isso deve ser suficiente; múltiplos registros devem ser raros.


### Diferenças de [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)


- Sem pontos finais
- Sem nome após o proto
- Minúsculas requeridas
- Em formato de texto com registros separados por vírgulas, não em formato binário DNS
- Indicadores de tipo de registro diferentes
- Campo appoptions adicional


### Notas


Não é permitido curinga como (asterisco), (asterisco)._tcp, ou _tcp.
Cada serviço suportado deve ter seu próprio registro.


### Registro de Nome de Serviço

Identificadores não padrão que não estão listados em [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) ou Linux /etc/services
podem ser solicitados e adicionados à especificação de estruturas comuns [LS2](/docs/specs/common-structures/).

Formatos de appoptions específicos para serviços também podem ser adicionados lá.


### Especificação I2CP

O protocolo [I2CP](/docs/specs/i2cp/) deve ser estendido para suportar buscas de serviço.
Códigos de erro adicionais MessageStatusMessage e/ou HostReplyMessage relacionados à busca de serviço
são necessários.
Para tornar a funcionalidade de busca geral, não apenas específica de registro de serviço,
o design é para suportar a recuperação de todas as opções LS2.

Implementação: Estender HostLookupMessage para adicionar pedido de
opções LS2 para hash, hostname e destino (tipos de pedido 2-4).
Estender HostReplyMessage para adicionar o mapeamento de opções, se solicitado.
Estender HostReplyMessage com códigos de erro adicionais.

Mapeamentos de opções podem ser armazenados em cache ou negativamente armazenados em cache por um curto período de tempo tanto no cliente quanto no roteador,
dependendo da implementação. O tempo máximo recomendado é de uma hora, a menos que o TTL do registro de serviço seja menor.
Registros de serviço podem ser armazenados em cache até o TTL especificado pela aplicação, cliente ou roteador.

Estender a especificação da seguinte forma:

### Opções de Configuração

Adicionar o seguinte a [I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

Opções a serem colocadas no conjunto de leasing. Disponível apenas para LS2.
nnn começa com 0. Valor da opção contém "chave=valor".
(não incluir aspas)

Exemplo:

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p


### Mensagem de Busca de Host


- Tipo de busca 2: Busca de hash, solicitar mapeamento de opções
- Tipo de busca 3: Busca de hostname, solicitar mapeamento de opções
- Tipo de busca 4: Busca de destino, solicitar mapeamento de opções

Para o tipo de busca 4, o item 5 é um Destination.


### Mensagem de Resposta de Host


Para tipos de busca 2-4, o roteador deve buscar o conjunto de leasing,
mesmo que a chave de busca esteja no livro de endereços.

Se bem-sucedido, a Resposta de Host conterá o Mapeamento de opções
do conjunto de leasing e o inclui como item 5 após o destino.
Se não houver opções no Mapeamento, ou o conjunto de leasing era versão 1,
ainda será incluído como um Mapeamento vazio (dois bytes: 0 0).
Todas as opções do conjunto de leasing serão incluídas, não apenas as opções de registro de serviço.
Por exemplo, opções para parâmetros definidos no futuro podem estar presentes.

Em caso de falha na busca do conjunto de leasing, a resposta conterá um novo código de erro 6 (Falha na busca do conjunto de leasing)
e não incluirá um mapeamento.
Quando o código de erro 6 é retornado, o campo Destination pode ou não estar presente.
Estará presente se uma busca de nome de host no livro de endereços teve sucesso,
ou se uma busca anterior teve sucesso e o resultado foi armazenado em cache,
ou se o Destination estava presente na mensagem de busca (tipo de busca 4).

Se um tipo de busca não for suportado,
a resposta conterá um novo código de erro 7 (tipo de busca não suportado).


### Especificação SAM

O protocolo [SAMv3](/docs/api/samv3/) deve ser estendido para suportar buscas de serviço.

Estender NAMING LOOKUP da seguinte forma:

NAMING LOOKUP NAME=example.i2p OPTIONS=true solicita o mapeamento de opções na resposta.

NAME pode ser um destino base64 completo quando OPTIONS=true.

Se a busca do destino teve sucesso e opções estavam presentes no conjunto de leasing,
então na resposta, após o destino,
haverá uma ou mais opções na forma OPTION:key=value.
Cada opção terá um prefixo OPTION: separado.
Todas as opções do conjunto de leasing serão incluídas, não apenas as opções de registro de serviço.
Por exemplo, opções para parâmetros definidos no futuro podem estar presentes.
Exemplo:

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Chaves contendo '=', e chaves ou valores contendo uma nova linha,
são considerados inválidos e o par chave/valor será removido da resposta.

Se não forem encontradas opções no conjunto de leasing, ou se o conjunto de leasing era versão 1,
então a resposta não incluirá nenhuma opção.

Se OPTIONS=true estava na busca, e o conjunto de leasing não é encontrado, um novo valor de resultado LEASESET_NOT_FOUND será retornado.


## Alternativa de Busca por Nome

Um design alternativo foi considerado, para suportar buscas de serviços
como um hostname completo, por exemplo _smtp._tcp.example.i2p,
atualizando [NAMING](/docs/overview/naming/) para especificar o manuseio de hostnames começando com '_'.
Isso foi rejeitado por duas razões:

- Alterações no I2CP e SAM ainda seriam necessárias para passar as informações de TTL e porta para o cliente.
- Não seria uma funcionalidade geral que poderia ser usada para recuperar outras opções LS2
  que poderiam ser definidas no futuro.


## Recomendações

Os servidores devem especificar um TTL de pelo menos 86400, e a porta padrão para a aplicação.


## Recursos Avançados

### Busca Recursiva

Pode ser desejável suportar buscas recursivas, onde cada conjunto de leasing sucessivo
é verificado para um registro de serviço apontando para outro conjunto de leasing, no estilo DNS.
Provavelmente isso não é necessário, pelo menos em uma implementação inicial.

TODO


### Campos específicos para a aplicação

Pode ser desejável ter dados específicos da aplicação no registro de serviço.
Por exemplo, o operador do exemplo.i2p pode querer indicar que email deve
ser encaminhado para example@mail.i2p. A parte "example@" precisaria estar em um campo separado
do registro de serviço, ou ser retirada do alvo.

Mesmo se o operador executar seu próprio serviço de email, ele pode querer indicar que
o email deve ser enviado para example@example.i2p. A maioria dos serviços I2P são executados por uma única pessoa.
Portanto, um campo separado pode ser útil aqui também.

TODO como fazer isso de maneira genérica


### Alterações necessárias para Email

Fora do escopo desta proposta. Veja [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) para uma discussão.


## Notas de Implementação

O cache de registros de serviço até o TTL pode ser feito pelo roteador ou pela aplicação,
dependendo da implementação. Se deve ser armazenado em cache de forma persistente também é dependente da implementação.

As buscas devem também procurar o conjunto de leasing alvo e verificar se ele contém um registro "self"
antes de retornar o destino alvo para o cliente.


## Análise de Segurança

Como o conjunto de leasing é assinado, quaisquer registros de serviço dentro dele são autenticados pela chave de assinatura do destino.

Os registros de serviço são públicos e visíveis para os floodfills, a menos que o conjunto de leasing esteja criptografado.
Qualquer roteador que solicitar o conjunto de leasing poderá ver os registros de serviço.

Um registro SRV diferente de "self" (ou seja, um que aponta para um alvo de hostname/b32 diferente)
não requer o consentimento do hostname/b32 alvo.
Não está claro se um redirecionamento de um serviço para um destino arbitrário poderia facilitar algum
tipo de ataque, ou qual seria o propósito de tal ataque.
No entanto, esta proposta atenua tal ataque exigindo que o alvo
também publique um registro SRV "self". Os implementadores devem verificar por um registro "self"
no conjunto de leasing do alvo.


## Compatibilidade

LS2: Sem problemas. Todas as implementações conhecidas atualmente ignoram o campo de opções no LS2,
e corretamente pulam por um campo de opções não vazio.
Isso foi verificado em testes tanto pelo Java I2P quanto pelo i2pd durante o desenvolvimento do LS2.
LS2 foi implementado em 0.9.38 em 2016 e é bem suportado por todas as implementações de roteadores.
O design não requer suporte especial ou cache ou quaisquer alterações nos floodfills.

Nomeação: '_' não é um caractere válido em hostnames i2p.

I2CP: Os tipos de busca 2-4 não devem ser enviados para roteadores abaixo da versão mínima da API
em que é suportado (TBD).

SAM: Servidor SAM Java ignora chaves/valores adicionais como OPTIONS=true.
i2pd deve fazer o mesmo, a ser verificado.
Clientes SAM não receberão os valores adicionais na resposta a menos que solicitados com OPTIONS=true.
Não deve ser necessário nenhum aumento de versão.


