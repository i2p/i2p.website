---
title: "Parâmetros de Largura de Banda do Túnel"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Fechado"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## NOTA

Esta proposta foi aprovada e agora está na
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) a partir da API 0.9.65.
Ainda não há implementações conhecidas; datas de implementação / versões da API ainda serão definidas.


## Visão Geral

À medida que aumentamos o desempenho da rede nos últimos anos
com novos protocolos, tipos de criptografia e melhorias no controle de congestionamento,
aplicações mais rápidas, como streaming de vídeo, estão se tornando possíveis.
Essas aplicações exigem alta largura de banda em cada salto nos seus túneis de clientes.

Os roteadores participantes, no entanto, não têm informações sobre quanto
de largura de banda um túnel usará quando recebem uma mensagem de construção de túnel.
Eles só podem aceitar ou rejeitar um túnel com base no total de largura de banda
atualmente usado por todos os túneis participantes e no limite total de largura de banda para túneis participantes.

Roteadores requisitantes também não têm informações sobre quanta largura de banda
está disponível em cada salto.

Além disso, os roteadores atualmente não têm como limitar o tráfego de entrada em um túnel.
Isso seria muito útil durante momentos de sobrecarga ou DDoS de um serviço.

Esta proposta aborda essas questões adicionando parâmetros de largura de banda às
mensagens de solicitação e resposta de construção de túnel.


## Design

Adicione parâmetros de largura de banda aos registros em mensagens de construção de túnel ECIES (ver [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies))
no campo de mapeamento de opções de construção de túnel. Use nomes de parâmetros curtos, uma vez que o espaço disponível
para o campo de opções é limitado.
As mensagens de construção de túnel são de tamanho fixo, assim não aumenta o
tamanho das mensagens.


## Especificação

Atualize a [especificação da mensagem de construção de túnel ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
da seguinte forma:

Para registros de construção ECIES longos e curtos:

### Opções de Solicitação de Construção

As seguintes três opções podem ser definidas no campo de mapeamento de opções de construção de túnel do registro:
Um roteador requisitante pode incluir qualquer uma, todas ou nenhuma delas.

- m := largura de banda mínima requerida para este túnel (inteiro positivo de KBps como uma string)
- r := largura de banda solicitada para este túnel (inteiro positivo de KBps como uma string)
- l := limite de largura de banda para este túnel; somente enviado para IBGW (inteiro positivo de KBps como uma string)

Restrição: m <= r <= l

O roteador participante deve rejeitar o túnel se "m" for especificado e ele não puder
fornecer pelo menos essa largura de banda.

As opções de solicitação são enviadas para cada participante no registro de solicitação de construção criptografado correspondente,
e não são visíveis para outros participantes.


### Opção de Resposta de Construção

A seguinte opção pode ser definida no campo de mapeamento de opções de resposta de construção de túnel do registro,
quando a resposta é ACCEPTED:

- b := largura de banda disponível para este túnel (inteiro positivo de KBps como uma string)

O roteador participante deve incluir isso se "m" ou "r" foram especificados
na solicitação de construção. O valor deve ser pelo menos igual ao valor "m" se especificado,
mas pode ser menos ou mais que o valor "r" se especificado.

O roteador participante deve tentar reservar e fornecer pelo menos esta
largura de banda para o túnel, porém isso não é garantido.
Os roteadores não podem prever as condições 10 minutos no futuro, e
o tráfego participante tem prioridade inferior ao tráfego e túneis próprios de um roteador.

Os roteadores podem também superalocar a largura de banda disponível se necessário, e isso é
provavelmente desejável, pois outros saltos no túnel podem rejeitá-lo.

Por esses motivos, a resposta do roteador participante deve ser tratada
como um compromisso de melhor esforço, mas não uma garantia.

Opções de resposta são enviadas para o roteador requisitante no registro de resposta de construção criptografado correspondente,
e não são visíveis para outros participantes.


## Notas de Implementação

Os parâmetros de largura de banda são vistos nos roteadores participantes na camada de túnel,
ou seja, o número de mensagens de túnel de 1 KB de tamanho fixo por segundo.
A sobrecarga de transporte (NTCP2 ou SSU2) não está incluída.

Esta largura de banda pode ser muito mais ou menos do que a largura de banda vista no cliente.
Mensagens de túnel contêm uma sobrecarga substancial, incluindo sobrecarga de camadas superiores
como catraca e streaming. Mensagens pequenas intermitentes como reconhecimentos de streaming
serão expandidas para 1 KB cada uma.
No entanto, a compressão gzip na camada I2CP pode reduzir substancialmente a largura de banda.

A implementação mais simples no roteador requisitante é usar
as larguras de banda média, mínima e/ou máxima dos túneis atuais no pool
para calcular os valores a serem colocados na solicitação.
Algoritmos mais complexos são possíveis e ficam a critério do implementador.

Atualmente não há opções I2CP ou SAM definidas para o cliente informar ao
roteador quanta largura de banda é necessária, e nenhuma nova opção é proposta aqui.
As opções podem ser definidas em uma data posterior, se necessário.

As implementações podem usar a largura de banda disponível ou qualquer outro dado, algoritmo, política local,
ou configuração local para calcular o valor de largura de banda retornado na
resposta de construção. Não especificado por esta proposta.

Esta proposta requer que os gateways de entrada implementem
limitação por túnel se solicitado pela opção "l".
Não requer que outros saltos participantes implementem limitação por túnel ou
global de qualquer tipo, nem especificam um algoritmo ou implementação em particular, se houver.

Esta proposta também não requer que os roteadores clientes limitem o tráfego
para o valor "b" retornado pelo salto participante, e dependendo da aplicação,
isso pode não ser possível, especialmente para túneis de entrada.

Esta proposta afeta apenas túneis criados pelo originador. Não há
método definido para solicitar ou alocar largura de banda para túneis de "extremidade distante" criados
pelo proprietário da outra extremidade de uma conexão fim a fim.


## Análise de Segurança

A impressão digital ou correlação do cliente pode ser possível com base em solicitações.
O roteador cliente (originador) pode querer randomizar os valores "m" e "r" em vez de enviar
o mesmo valor para cada salto; ou enviar um conjunto limitado de valores que representam "baldes" de largura de banda,
ou alguma combinação de ambos.

DDoS por Superalocação: Embora possa ser possível atualmente fazer um DDoS em um roteador construindo e
usando um grande número de túneis através dele, esta proposta, sem dúvida, torna isso muito mais fácil,
bastando solicitar um ou mais túneis com grandes solicitações de largura de banda.

As implementações podem e deveriam usar uma ou mais das seguintes estratégias
para mitigar esse risco:

- Superalocação da largura de banda disponível
- Limitar a alocação por túnel para uma certa porcentagem da largura de banda disponível
- Limitar a taxa de aumento na largura de banda alocada
- Limitar a taxa de aumento na largura de banda utilizada
- Limitar a largura de banda alocada para um túnel se não for utilizada cedo na vida útil do túnel (use ou perca)
- Rastrear largura de banda média por túnel
- Rastrear largura de banda solicitada vs. largura de banda realmente utilizada por túnel


## Compatibilidade

Sem problemas. Todas as implementações conhecidas atualmente ignoram o campo de mapeamento em mensagens de construção,
e corretamente ignoram um campo de opções não vazio.


## Migração

As implementações podem adicionar suporte a qualquer momento, sem necessidade de coordenação.

Como atualmente não há versão de API definida onde o suporte para esta proposta seja obrigatório,
os roteadores devem verificar uma resposta "b" para confirmar o suporte.


