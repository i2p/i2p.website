---
title: "Roteadores ECIES"
number: "156"
author: "zzz, orignal"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Fechado"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
---

## Nota
Implantação de rede e testes em andamento.
Sujeito a revisões.
Status:

- Implementação de Roteadores ECIES a partir da versão 0.9.48, veja [Common](/en/docs/spec/common-structures/).
- Implementação de criação de túneis a partir da versão 0.9.48, veja [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).
- Implementação de mensagens criptografadas para roteadores ECIES a partir da versão 0.9.49, veja [ECIES-ROUTERS](/en/docs/spec/ecies-routers/).
- Implementação de novas mensagens de construção de túneis a partir da versão 0.9.51.




## Visão Geral


### Resumo

As identidades dos roteadores atualmente contêm uma chave de criptografia ElGamal.
Este tem sido o padrão desde o início do I2P.
ElGamal é lento e precisa ser substituído em todos os locais em que é usado.

As propostas para LS2 [Prop123](/en/proposals/123-new-netdb-entries/) e ECIES-X25519-AEAD-Ratchet [Prop144](/en/proposals/144-ecies-x25519-aead-ratchet/)
(agora especificadas em [ECIES](/en/docs/spec/ecies/)) definiram a substituição do ElGamal por ECIES
para Destinos.

Esta proposta define a substituição do ElGamal por ECIES-X25519 para roteadores.
Esta proposta fornece uma visão geral das mudanças necessárias.
A maioria dos detalhes está em outras propostas e especificações.
Veja a seção de referências para links.


### Objetivos

Veja [Prop152](/en/proposals/152-ecies-tunnels/) para objetivos adicionais.

- Substituir ElGamal por ECIES-X25519 nas Identidades de Roteadores
- Reutilizar primitivas criptográficas existentes
- Melhorar a segurança da mensagem de construção de túnel onde possível, mantendo a compatibilidade
- Suportar túneis com pares ElGamal/ECIES mistos
- Maximizar a compatibilidade com a rede atual
- Não requerer uma atualização completa da rede
- Implementação gradual para minimizar riscos
- Nova mensagem de construção de túnel, menor


### Não-Objetivos

Veja [Prop152](/en/proposals/152-ecies-tunnels/) para não-objetivos adicionais.

- Não há necessidade de roteadores com chave dupla
- Mudanças na camada de criptografia, para isso veja [Prop153](/en/proposals/153-chacha20-layer-encryption/)


## Design


### Localização da Chave e Tipo de Criptografia

Para Destinos, a chave está no conjunto de arrendamentos, não no Destino, e
suportamos múltiplos tipos de criptografia no mesmo conjunto de arrendamentos.

Nada disso é necessário para roteadores. A chave de criptografia do roteador
está na sua Identidade de Roteador. Veja a especificação das estruturas comuns [Common](/en/docs/spec/common-structures/).

Para roteadores, substituiremos a chave ElGamal de 256 bytes na Identidade de Roteador
por uma chave X25519 de 32 bytes e 224 bytes de preenchimento.
Isso será indicado pelo tipo de criptografia no certificado da chave.
O tipo de criptografia (mesmo usado no LS2) é 4.
Isso indica uma chave pública X25519 de 32 bytes em little-endian.
Esta é a construção padrão, conforme definido na especificação de estruturas comuns [Common](/en/docs/spec/common-structures/).

Isso é idêntico ao método proposto para ECIES-P256
para tipos de criptografia 1-3 na proposta 145 [Prop145](/en/proposals/145-ecies/).
Embora esta proposta nunca tenha sido adotada, os desenvolvedores de implementação Java prepararam
para tipos de criptografia nos certificados de chave de Identidade de Roteador, adicionando verificações em vários
locais na base de código. A maior parte deste trabalho foi feita em meados de 2019.


### Mensagem de Construção de Túnel

Várias mudanças na especificação de criação de túneis [Tunnel-Creation](/en/docs/spec/tunnel-creation/)
são necessárias para usar ECIES em vez de ElGamal.
Além disso, faremos melhorias na mensagem de construção de túneis
para aumentar a segurança.

Na fase 1, mudaremos o formato e a criptografia do
Registro de Solicitação de Construção e do Registro de Resposta de Construção para saltos ECIES.
Essas mudanças serão compatíveis com os roteadores ElGamal existentes.
Essas mudanças estão definidas na proposta 152 [Prop152](/en/proposals/152-ecies-tunnels/).

Na fase 2, adicionaremos uma nova versão do
Registro de Solicitação de Construção, Registro de Resposta de Construção.
O tamanho será reduzido para eficiência.
Essas mudanças devem ser suportadas por todos os saltos em um túnel, e todos os saltos devem ser ECIES.
Essas mudanças estão definidas na proposta 157 [Prop157](/en/proposals/157-new-tbm/).



### Criptografia de Ponta-a-Ponta

Histórico
```````````

No design original do Java I2P, havia um único Gerenciador de Chaves de Sessão ElGamal (SKM)
compartilhado pelo roteador e todos os seus Destinos locais.
Como um SKM compartilhado poderia vazar informações e permitir correlação por atacantes,
o design foi alterado para suportar SKMs ElGamal separados para o roteador e cada Destino.
O design ElGamal suportava apenas remetentes anônimos;
o remetente enviava apenas chaves efêmeras, não uma chave estática.
A mensagem não estava ligada à identidade do remetente.

Então, projetamos o ECIES Ratchet SKM em
ECIES-X25519-AEAD-Ratchet [Prop144](/en/proposals/144-ecies-x25519-aead-ratchet/), agora especificado em [ECIES](/en/docs/spec/ecies/).
Este design foi especificado usando o padrão Noise "IK", que incluiu a chave
estática do remetente na primeira mensagem. Este protocolo é usado para Destinos ECIES (tipo 4).
O padrão IK não permite remetentes anônimos.

Portanto, incluímos na proposta uma maneira de também enviar mensagens anônimas
a um Ratchet SKM, usando uma chave estática preenchida com zeros. Isso simulava um padrão Noise "N",
mas de uma forma compatível, para que um SKM ECIES pudesse receber tanto mensagens anônimas quanto não-anônimas.
A intenção era usar chave zero para roteadores ECIES.


Casos de Uso e Modelos de Ameaça
```````````````````````````````

O caso de uso e modelo de ameaça para mensagens enviadas a roteadores é muito diferente daquele
para mensagens de ponta a ponta entre Destinos.


Caso de uso e modelo de ameaça de Destino:

- Não-anônimas de/para destinos (remetente inclui chave estática)
- Apoiar eficientemente tráfego sustentado entre destinos (handshake completo, streaming e tags)
- Sempre enviadas através de túneis de saída e entrada
- Esconder todas as características de identificação de OBEP e IBGW, exigindo codificação Elligator2 de chaves efêmeras.
- Ambos os participantes devem usar o mesmo tipo de criptografia


Caso de uso e modelo de ameaça de Roteador:

- Mensagens anônimas de roteadores ou destinos (remetente não inclui chave estática)
- Para Consultas e Armazenamentos de Banco de Dados criptografados apenas, geralmente para flooding
- Mensagens ocasionais
- Múltiplas mensagens não devem ser correlacionadas
- Sempre enviadas através do túnel de saída diretamente para um roteador. Nenhum túnel de entrada usado
- OBEP sabe que está encaminhando a mensagem para um roteador e conhece seu tipo de criptografia
- Os dois participantes podem ter diferentes tipos de criptografia
- Respostas a consultas de banco de dados são mensagens únicas usando a chave de resposta e tag na mensagem de Consulta de Banco de Dados
- Confirmações de Armazenamento de Banco de Dados são mensagens únicas usando uma mensagem de Status de Entrega integrada


Não-objetivos do caso de uso de Roteador:

- Não há necessidade de mensagens não-anônimas
- Não há necessidade de enviar mensagens através de túneis exploratórios de entrada (um roteador não publica conjuntos de arrendamentos exploratórios)
- Não há necessidade de tráfego de mensagens sustentado usando tags
- Não há necessidade de executar Gerenciadores de Chave de Sessão "de chave dupla" conforme descrito em [ECIES](/en/docs/spec/ecies/) para Destinos. Roteadores têm apenas uma chave pública.


Conclusões de Design
```````````````````````

O Router SKM ECIES não precisa de um Ratchet SKM completo conforme especificado em [ECIES](/en/docs/spec/ecies/) para Destinos.
Não há requisito para mensagens não-anônimas usando o padrão IK.
O modelo de ameaça não requer chaves efêmeras codificadas em Elligator2.

Portanto, o router SKM usará o padrão Noise "N", mesmo conforme especificado
em [Prop152](/en/proposals/152-ecies-tunnels/) para construção de túneis.
Usará o mesmo formato de payload conforme especificado em [ECIES](/en/docs/spec/ecies/) para Destinos.
O modo de chave estática zero (sem ligação ou sessão) de IKT especificado em [ECIES](/en/docs/spec/ecies/) não será usado.

Respostas a consultas serão criptografadas com uma tag de ratchet se solicitado na consulta.
Isso é conforme documentado em [Prop154](/en/proposals/154-ecies-lookups/), agora especificado em [I2NP](/en/docs/spec/i2np/).

O design permite que o roteador tenha um único Gerenciador de Chaves de Sessão ECIES.
Não há necessidade de executar Gerenciadores de Chave de Sessão "de chave dupla" conforme
descritos em [ECIES](/en/docs/spec/ecies/) para Destinos.
Roteadores têm apenas uma chave pública.

Um roteador ECIES não tem uma chave estática ElGamal.
O roteador ainda precisa de uma implementação de ElGamal para construir túneis
através de roteadores ElGamal e enviar mensagens criptografadas para roteadores ElGamal.

Um roteador ECIES PODE exigir um Gerenciador de Chave de Sessão ElGamal parcial para
receber mensagens etiquetadas com ElGamal recebidas como respostas a consultas de NetDB
de roteadores floodfill pré-0.9.46, uma vez que esses roteadores não têm uma implementação de respostas etiquetadas por ECIES conforme especificado em [Prop152](/en/proposals/152-ecies-tunnels/).
Se não, um roteador ECIES pode não solicitar uma resposta criptografada de um
roteador floodfill pré-0.9.46.

Isso é opcional. A decisão pode variar em várias implementações do I2P
e pode depender da quantidade da rede que foi atualizada para
0.9.46 ou superior.
Até esta data, aproximadamente 85% da rede é 0.9.46 ou superior.



## Especificação

X25519: Veja [ECIES](/en/docs/spec/ecies/).

Identidade do Roteador e Certificado de Chave: Veja [Common](/en/docs/spec/common-structures/).

Construção de Túneis: Veja [Prop152](/en/proposals/152-ecies-tunnels/).

Nova Mensagem de Construção de Túnel: Veja [Prop157](/en/proposals/157-new-tbm/).


### Criptografia de Solicitação

A criptografia de solicitação é a mesma daquela especificada em [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) e [Prop152](/en/proposals/152-ecies-tunnels/),
usando o padrão Noise "N".

Respostas a consultas serão criptografadas com uma tag de ratchet se solicitadas na consulta.
Mensagens de solicitação de Consulta de Banco de Dados contêm a chave de resposta de 32 bytes e a tag de resposta de 8 bytes
conforme especificado em [I2NP](/en/docs/spec/i2np/) e [Prop154](/en/proposals/154-ecies-lookups/). A chave e a tag são usadas para criptografar a resposta.

Não são criados conjuntos de tags.
O esquema de chave estática zero especificado em
ECIES-X25519-AEAD-Ratchet [Prop144](/en/proposals/144-ecies-x25519-aead-ratchet/) e [ECIES](/en/docs/spec/ecies/) não será usado.
Chaves efêmeras não serão codificadas como Elligator2.

Geralmente, estas serão mensagens de Nova Sessão e serão enviadas com uma chave estática zero
(sem ligação ou sessão), pois o remetente da mensagem é anônimo.


KDF para ck e h Inicial
````````````````````````

Isso é padrão [NOISE](https://noiseprotocol.org/noise.html) para o padrão "N" com um nome de protocolo padrão.
Isso é o mesmo que especificado em [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) e [Prop152](/en/proposals/152-ecies-tunnels/) para mensagens de construção de túnel.


  ```text

Este é o padrão de mensagem "e":

  // Defina protocol_name.
  Defina protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, codificado em US-ASCII, sem terminação NULL).

  // Defina Hash h = 32 bytes
  // Preencha para 32 bytes. NÃO o hash, porque não tem mais que 32 bytes.
  h = protocol_name || 0

  Defina ck = chave de encadeamento de 32 bytes. Copie os dados de h para ck.
  Defina chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // até aqui, todos os roteadores podem pré-calcular.





  ```


KDF para Mensagem
````````````````````````

Criadores de mensagens geram um par de chaves efêmeros X25519 para cada mensagem.
Chaves efêmeras devem ser únicas por mensagem.
Isso é o mesmo que especificado em [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) e [Prop152](/en/proposals/152-ecies-tunnels/) para mensagens de construção de túnel.


  ```dataspec


// Par de chaves estáticas X25519 do roteador de destino (hesk, hepk) da Identidade do Roteador
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || abaixo significa anexar
  h = SHA256(h || hepk);

  // até aqui, todos os roteadores podem pré-calcular
  // para todas as mensagens recebidas

  // Remetente gera um par de chaves efêmeras X25519
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Final do padrão de mensagem "e".

  Este é o padrão de mensagem "es":

  // Noise es
  // Remetente realiza um DH X25519 com a chave pública estática do receptor.
  // O roteador de destino
  // extrai a chave efêmera do remetente antes do registro criptografado.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parâmetros ChaChaPoly para encriptar/decriptar
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Chave de cadeia não é usada
  //chainKey = keydata[0:31]

  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  plaintext = Registro de solicitação de construção de 464 bytes
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Final do padrão de mensagem "es".

  // MixHash(ciphertext) não é necessário
  //h = SHA256(h || ciphertext)





  ```



Payload
````````````````````````

O payload é o mesmo formato de bloco definido em [ECIES](/en/docs/spec/ecies/) e [Prop144](/en/proposals/144-ecies-x25519-aead-ratchet/).
Todas as mensagens devem conter um bloco DateTime para prevenção de replay.


### Criptografia de Resposta

Respostas a mensagens de Consulta de Banco de Dados são mensagens de Armazenamento de Banco de Dados ou Resposta de Pesquisa de Banco de Dados.
Elas são criptografadas como mensagens de Sessão Existente com
a chave de resposta de 32 bytes e a tag de resposta de 8 bytes
conforme especificado em [I2NP](/en/docs/spec/i2np/) e [Prop154](/en/proposals/154-ecies-lookups/).


Não há respostas explícitas para mensagens de Armazenamento de Banco de Dados. O remetente pode incluir sua
própria resposta como uma Mensagem de Alho para si mesmo, contendo uma mensagem de Status de Entrega.




## Justificação

Este design maximiza a reutilização de primitivas criptográficas, protocolos e código existentes.

Este design minimiza riscos.




## Notas de Implementação

Roteadores mais antigos não verificam o tipo de criptografia do roteador e enviarão registros de construção ou mensagens netdb criptografados com ElGamal.
Alguns roteadores recentes estão com bugs e enviarão vários tipos de registros de construção malformados.
Alguns roteadores recentes podem enviar mensagens netdb não-anônimas (ratchet completo).
Os implementadores devem detectar e rejeitar esses registros e mensagens o mais cedo possível, para reduzir o uso da CPU.



## Questões

Proposta 145 [Prop145](/en/proposals/145-ecies/) pode ou não ser reescrita para ser principalmente compatível com
a Proposta 152 [Prop152](/en/proposals/152-ecies-tunnels/).



## Migração

A implementação, teste e implantação levarão várias versões
e aproximadamente um ano. As fases são as seguintes. Atribuição de
cada fase a uma versão específica está TBD e depende
do ritmo de desenvolvimento.

Os detalhes da implementação e migração podem variar para
cada implementação do I2P.



### Ponto-a-Ponto Básico

Roteadores ECIES podem se conectar e receber conexões de roteadores ElGamal.
Isso já deve ser possível agora, pois várias verificações foram adicionadas à base de código Java
em meados de 2019 em reação à proposta inacabada 145 [Prop145](/en/proposals/145-ecies/).
Garanta que não haja nada nas bases de código
que impeça conexões ponto-a-ponto para roteadores não-ElGamal.

Verificações de correção de código:

- Garanta que roteadores ElGamal não solicitem respostas criptografadas por AEAD para mensagens de Consulta de Banco de Dados
  (quando a resposta retorna através de um túnel exploratório para o roteador)
- Garanta que roteadores ECIES não solicitem respostas criptografadas por AES para mensagens de Consulta de Banco de Dados
  (quando a resposta retorna através de um túnel exploratório para o roteador)

Até fases posteriores, quando especificações e implementações estiverem completas:

- Garanta que construções de túneis não sejam tentadas por roteadores ElGamal através de roteadores ECIES.
- Garanta que mensagens criptografadas por ElGamal não sejam enviadas por roteadores ElGamal para roteadores de flooding ECIES.
  (Consultas de Banco de Dados e Armazenamentos de Banco de Dados)
- Garanta que mensagens criptografadas por ECIES não sejam enviadas por roteadores ECIES para roteadores de flooding ElGamal.
  (Consultas de Banco de Dados e Armazenamentos de Banco de Dados)
- Garanta que roteadores ECIES não se tornem automaticamente de flooding.

Nenhuma alteração deve ser necessária.
Versão alvo, se alterações necessárias: 0.9.48


### Compatibilidade NetDB

Garanta que as informações de roteadores ECIES possam ser armazenadas e recuperadas de sistemas ElGamal de flooding.
Isso já deveria ser possível, pois várias conclusões foram adicionadas à base de código Java
em meados de 2019 em reação à proposta inacabada 145 [Prop145](/en/proposals/145-ecies/).
Garanta que não haja nada nas bases de código
que impeça o armazenamento de Informações de Roteadores não-ElGamal no banco de dados da rede.

Nenhuma alteração deve ser necessária.
Versão alvo, se alterações necessárias: 0.9.48


### Construção de Túnel

Implemente a construção de túneis conforme definido na proposta 152 [Prop152](/en/proposals/152-ecies-tunnels/).
Comece com um roteador ECIES construindo túneis com todos os saltos ElGamal;
use seu próprio registro de solicitação de construção para um túnel de entrada para testar e depurar.

Depois, teste e suporte roteadores ECIES construindo túneis com uma mistura de
saltos ElGamal e ECIES.

Em seguida, possibilite a construção de túneis através de roteadores ECIES.
Nenhuma verificação de versão mínima deve ser necessária, a menos que mudanças incompatíveis
na proposta 152 sejam feitas após um lançamento.

Versão alvo: 0.9.48, final de 2020


### Mensagens Ratchet para floodfills ECIES

Implemente e teste o recebimento de mensagens ECIES (com chave estática zero) por floodfills ECIES,
conforme definido na proposta 144 [Prop144](/en/proposals/144-ecies-x25519-aead-ratchet/).
Implemente e teste o recebimento de respostas AEAD para mensagens de Consulta de Banco de Dados por roteadores ECIES.

Possibilite flooding automático por roteadores ECIES.
Então, possibilite o envio de mensagens ECIES para roteadores ECIES.
Nenhuma verificação de versão mínima deve ser necessária, a menos que mudanças incompatíveis
na proposta 152 sejam feitas após um lançamento.

Versão alvo: 0.9.49, início de 2021.
Roteadores ECIES podem se tornar automaticamente de flooding.


### Rekeying e Novas Instalações

Novas instalações padrão usarão ECIES a partir da versão 0.9.49.

Rechaveie gradualmente todos os roteadores para minimizar o risco e a interrupção da rede.
Utilize o código existente que realizou a troca de chaves para migração do tipo de assinatura anos atrás.
Este código dá a cada roteador uma pequena chance aleatória de re-chavear a cada reinício.
Após várias reinicializações, um roteador provavelmente terá re-chaveado para ECIES.

O critério para iniciar o re-chaveamento é que uma parte suficiente da rede,
talvez 50%, possa construir túneis através de roteadores ECIES (0.9.48 ou superior).

Antes de re-chavear agressivamente toda a rede, a vasta maioria
(talvez 90% ou mais) deve ser capaz de construir túneis através de roteadores ECIES (0.9.48 ou superior)
E enviar mensagens para floodfills ECIES (0.9.49 ou superior).
Este alvo provavelmente será alcançado para a versão 0.9.52.

O re-chaveamento levará várias versões.

Versão alvo:
0.9.49 para novos roteadores com padrão ECIES;
0.9.49 para começar lentamente o re-chaveamento;
0.9.50 - 0.9.52 para aumentar repetidamente a taxa de re-chaveamento;
final de 2021 para a maioria da rede ser re-chaveada.


### Nova Mensagem de Construção de Túnel (Fase 2)

Implemente e teste a nova Mensagem de Construção de Túnel conforme definido na proposta 157 [Prop157](/en/proposals/157-new-tbm/).
Lance o suporte na versão 0.9.51.
Faça testes adicionais, depois possibilite na versão 0.9.52.

Os testes serão difíceis.
Antes que isso possa ser amplamente testado, um bom subconjunto da rede deve suportá-lo.
Antes que seja amplamente útil, a maioria da rede deve suportá-lo.
Se mudanças na especificação ou implementação forem necessárias após o teste,
isso atrasaria a implementação por uma versão adicional.

Versão alvo: 0.9.52, final de 2021.


### Rekeying Completo

Neste ponto, roteadores mais antigos que alguma versão TBD não
poderão construir túneis através da maioria dos pares.

Versão alvo: 0.9.53, início de 2022.


