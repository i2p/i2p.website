---
title: "Túneis ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Fechado"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Nota
Implantação e teste na rede em andamento.
Sujeito a revisões menores.
Veja [SPEC](/en/docs/spec/) para a especificação oficial.


## Visão Geral

Este documento propõe mudanças na criptografia de mensagem de Construção de Túneis
usando primitivas criptográficas introduzidas por [ECIES-X25519](/en/docs/spec/ecies/).
É uma parte da proposta geral
[Prop156](/en/proposals/156-ecies-routers/) para converter roteadores de chaves ElGamal para ECIES-X25519.

Para os propósitos de transição da rede de ElGamal + AES256 para ECIES + ChaCha20,
são necessários túneis com roteadores ElGamal e ECIES mistos.
Especificações para lidar com saltos de túneis mistos são fornecidas.
Nenhuma alteração será feita no formato, processamento ou criptografia de saltos ElGamal.

Criadores de túneis ElGamal precisarão criar pares de chaves X25519 efêmeras por salto e
seguir esta especificação para criar túneis contendo saltos ECIES.

Esta proposta especifica as mudanças necessárias para Construção de Túneis ECIES-X25519.
Para uma visão geral de todas as mudanças necessárias para roteadores ECIES, veja a proposta 156 [Prop156](/en/proposals/156-ecies-routers/).

Esta proposta mantém o mesmo tamanho para registros de construção de túneis,
como exigido para compatibilidade. Registros e mensagens de construção menores serão
implementados mais tarde - veja [Prop157](/en/proposals/157-new-tbm/).


### Primitivas Criptográficas

Não são introduzidas novas primitivas criptográficas. As primitivas necessárias para implementar esta proposta são:

- AES-256-CBC como em [Criptografia](/en/docs/spec/cryptography/)
- Funções STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) e DECRYPT(k, n, ciphertext, ad) - como em [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) e [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funções DH X25519 - como em [NTCP2](/en/docs/spec/ntcp2/) e [ECIES-X25519](/en/docs/spec/ecies/)
- HKDF(salt, ikm, info, n) - como em [NTCP2](/en/docs/spec/ntcp2/) e [ECIES-X25519](/en/docs/spec/ecies/)

Outras funções Noise definidas em outros lugares:

- MixHash(d) - como em [NTCP2](/en/docs/spec/ntcp2/) e [ECIES-X25519](/en/docs/spec/ecies/)
- MixKey(d) - como em [NTCP2](/en/docs/spec/ntcp2/) e [ECIES-X25519](/en/docs/spec/ecies/)


### Objetivos

- Aumentar a velocidade das operações criptográficas
- Substituir ElGamal + AES256/CBC por primitivas ECIES para BuildRequestRecords e BuildReplyRecords de túneis.
- Nenhuma alteração no tamanho de BuildRequestRecords e BuildReplyRecords criptografados (528 bytes) para compatibilidade
- Sem novas mensagens I2NP
- Manter o tamanho do registro de construção criptografado para compatibilidade
- Adicionar sigilo direto para Mensagens de Construção de Túnel.
- Adicionar criptografia autenticada
- Detectar reordenamento de saltos em BuildRequestRecords
- Aumentar a resolução do timestamp para que o tamanho do filtro de Bloom possa ser reduzido
- Adicionar campo para expiração do túnel para que sejam possíveis tempos de vida variáveis do túnel (apenas túneis totalmente ECIES)
- Adicionar campo de opções extensíveis para recursos futuros
- Reutilizar primitivas criptográficas existentes
- Melhorar a segurança da mensagem de construção de túnel onde possível enquanto mantém a compatibilidade
- Suporte a túneis com pares ElGamal/ECIES mistos
- Melhorar defesas contra ataques de "marcação" em mensagens de construção
- Saltos não precisam conhecer o tipo de criptografia do próximo salto antes de processar a mensagem de construção,
  pois podem não ter o RI do próximo salto naquele momento
- Maximizar compatibilidade com a rede atual
- Sem alterações na criptografia de solicitação/resposta AES de construção de túnel para roteadores ElGamal
- Sem alteração na criptografia "de camada" AES de túnel, para isso veja [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Continuar a suportar tanto TBM/TBRM de 8 registros quanto VTBM/VTBRM de tamanho variável
- Não exigir atualização de "dia da bandeira" para toda a rede


### Não-Objetivos

- Redesenho completo de mensagens de construção de túnel requerendo um "dia da bandeira".
- Encolhimento de mensagens de construção de túnel (requer todos os saltos ECIES e uma nova proposta)
- Uso de opções de construção de túnel como definido em [Prop143](/en/proposals/143-build-message-options/), só necessário para mensagens pequenas
- Túneis bidirecionais - para isso veja [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Mensagens de construção de túnel menores - para isso veja [Prop157](/en/proposals/157-new-tbm/)


## Modelo de Ameaças

### Objetivos de Design

- Nenhum salto é capaz de determinar o originador do túnel.

- Saltos intermediários não devem ser capazes de determinar a direção do túnel
  ou sua posição no túnel.

- Nenhum salto pode ler qualquer conteúdo de outros registros de solicitação ou resposta, exceto
  para hash do roteador truncado e chave efêmera para o próximo salto

- Nenhum membro do túnel de resposta para construção de saída pode ler qualquer registro de resposta.

- Nenhum membro do túnel de saída para construção de entrada pode ler qualquer registro de solicitação,
  exceto que OBEP pode ver o hash do roteador truncado e chave efêmera para IBGW




### Ataques de Marcação

Um dos principais objetivos do design de construção de túnel é dificultar
para roteadores coniventes X e Y saberem que estão em um único túnel.
Se o roteador X está no salto m e o roteador Y está no salto m+1, eles obviamente saberão.
Mas se o roteador X está no salto m e o roteador Y está no salto m+n para n>1, isso deve ser muito mais difícil.

Ataques de marcação são quando o roteador de salto intermediário X altera a mensagem de construção do túnel de forma que
o roteador Y possa detectar a alteração quando a mensagem de construção chegar lá.
O objetivo é que qualquer mensagem alterada seja descartada por um roteador entre X e Y antes de chegar ao roteador Y.
Para modificações que não são descartadas antes do roteador Y, o criador do túnel deve detectar a corrupção na resposta
e descartar o túnel.

Possíveis ataques:

- Alterar um registro de construção
- Substituir um registro de construção
- Adicionar ou remover um registro de construção
- Reordenar os registros de construção





TODO: O design atual previne todos esses ataques?






## Design

### Estrutura do Protocolo Noise

Esta proposta fornece os requisitos com base na Estrutura do Protocolo Noise
[NOISE](https://noiseprotocol.org/noise.html) (Revisão 34, 2018-07-11).
Na linguagem Noise, Alice é a iniciadora, e Bob é o respondedor.

Esta proposta baseia-se no protocolo Noise Noise_N_25519_ChaChaPoly_SHA256.
Este protocolo Noise usa as seguintes primitivas:

- Padrão de Handshake de Uma Via: N
  Alice não transmite sua chave estática para Bob (N)

- Função DH: X25519
  X25519 DH com um comprimento de chave de 32 bytes conforme especificado em [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Função de Cifra: ChaChaPoly
  AEAD_CHACHA20_POLY1305 conforme especificado em [RFC-7539](https://tools.ietf.org/html/rfc7539) seção 2.8.
  Nonce de 12 bytes, com os primeiros 4 bytes definidos como zero.
  Idêntico ao em [NTCP2](/en/docs/spec/ntcp2/).

- Função de Hash: SHA256
  Hash padrão de 32 bytes, já usado extensivamente no I2P.


Adições à Estrutura
```````````````````````````````````````````````````````

Nenhuma.


### Padrões de Handshake

Os handshakes usam padrões de handshake [Noise](https://noiseprotocol.org/noise.html).

A seguinte correspondência de letras é usada:

- e = chave efêmera única
- s = chave estática
- p = payload de mensagem

A solicitação de construção é idêntica ao padrão Noise N.
Isso também é idêntico à primeira mensagem (Solicitação de Sessão) no padrão XK usado em [NTCP2](/en/docs/spec/ntcp2/).


  ```dataspec

<- s
  ...
  e es p ->





  ```


### Criptografia de Solicitação

Registros de Solicitação de Construção são criados pelo criador do túnel e assimetricamente criptografados para o salto individual.
Esta criptografia assimétrica dos registros de solicitação atualmente é ElGamal conforme definido em [Criptografia](/en/docs/spec/cryptography/)
e contém um checksum SHA-256. Este design não é sigilo futuro.

O novo design usará o padrão One-Way "N" do Noise com ECIES-X25519 efêmero-estático DH, com um HKDF, e
ChaCha20/Poly1305 AEAD para sigilo futuro, integridade e autenticação.
Alice é a solicitante de construção de túnel. Cada salto no túnel é um Bob.


(Propriedades de Segurança do Payload)

  ```text

N:                      Autenticação   Confidencialidade
    -> e, es                  0                2

    Autenticação: Nenhuma (0).
    Este payload pode ter sido enviado por qualquer parte, incluindo um atacante ativo.

    Confidencialidade: 2.
    Criptografado para um destinatário conhecido, sigilo futuro apenas para comprometimento do remetente, vulnerável a repetição.
    Este payload é criptografado com base apenas nos DHs envolvendo o par de chaves estáticas do destinatário.
    Se a chave privada estática do destinatário for comprometida, mesmo em uma data posterior, este payload pode ser
    decriptografado. Esta mensagem também pode ser repetida, pois não há contribuição efêmera do destinatário.

    "e": Alice gera um novo par de chaves efêmeras e o armazena na variável e,
         escreve a chave pública efêmera como texto claro no buffer de mensagem e
         faz hash da chave pública junto com o antigo h para derivar um novo h.

    "es": Um DH é realizado entre o par de chaves efêmeras de Alice e o
          par de chaves estáticas de Bob. O resultado é calculado junto com o antigo ck para
          derivar um novo ck e k, e n é configurado para zero.





  ```



### Criptografia de Resposta

Registros de Resposta de Construção são criados pelo criador dos saltos e criptografados simetricamente ao criador.
Essa criptografia simétrica dos registros de resposta atualmente é AES com um checksum SHA-256 pré-pendente.
e contém um checksum SHA-256. Este design não é sigilo futuro.

O novo design usará ChaCha20/Poly1305 AEAD para integridade e autenticação.


### Justificação

A chave pública efêmera na solicitação não precisa ser ofuscada com AES
ou Elligator2. O salto anterior é o único que pode vê-la, e esse salto
sabe que o próximo salto é ECIES.

Registros de resposta não precisam de criptografia assimétrica completa com outro DH.



## Especificação



### Registros de Solicitação de Construção

BuildRequestRecords criptografados são 528 bytes para ambos ElGamal e ECIES, para compatibilidade.


Registro de Solicitação Não Criptografado (ElGamal)
``````````````````````````````````````````````````

Para referência, esta é a especificação atual do BuildRequestRecord de túnel para roteadores ElGamal, retirada de [I2NP](/en/docs/spec/i2np/).
Os dados não criptografados são precedidos por um byte não zero e o hash SHA-256 dos dados antes da criptografia,
conforme definido em [Criptografia](/en/docs/spec/cryptography/).

Todos os campos são em big-endian.

Tamanho não criptografado: 222 bytes

  ```dataspec


bytes     0-3: ID do túnel para receber mensagens, não zero
  bytes    4-35: hash da identidade do roteador local
  bytes   36-39: ID do próximo túnel, não zero
  bytes   40-71: hash da identidade do próximo roteador
  bytes  72-103: chave de camada de túnel AES-256
  bytes 104-135: chave IV de túnel AES-256
  bytes 136-167: chave de resposta AES-256
  bytes 168-183: IV de resposta AES-256
  byte      184: bandeiras
  bytes 185-188: hora da solicitação (em horas desde a época, arredondado para baixo)
  bytes 189-192: ID da próxima mensagem
  bytes 193-221: preenchimento aleatório / não interpretado




  ```


Registro de Solicitação Criptografado (ElGamal)
```````````````````````````````````````````````

Para referência, esta é a especificação atual do BuildRequestRecord de túnel para roteadores ElGamal, retirada de [I2NP](/en/docs/spec/i2np/).

Tamanho criptografado: 528 bytes

  ```dataspec


bytes    0-15: Hash truncado da identidade do salto
  bytes  16-528: BuildRequestRecord criptografado com ElGamal




  ```




Registro de Solicitação Não Criptografado (ECIES)
````````````````````````````````````````````````

Esta é a especificação proposta do BuildRequestRecord de túnel para roteadores ECIES-X25519.
Resumo das mudanças:

- Remover hash de roteador de 32 bytes não utilizado
- Alterar o tempo da solicitação de horas para minutos
- Adicionar campo de expiração para futuro tempo de túnel variável
- Adicionar mais espaço para bandeiras
- Adicionar Mapeamento para opções adicionais de construção
- Chave e IV de resposta AES-256 não são usados para o próprio registro de resposta do salto
- Registro não criptografado é mais longo porque há menos sobrecarga de criptografia

O registro de solicitação não contém nenhuma chave de resposta ChaCha.
Essas chaves são derivadas de um KDF. Veja abaixo.

Todos os campos são em big-endian.

Tamanho não criptografado: 464 bytes

  ```dataspec


bytes     0-3: ID do túnel para receber mensagens, não zero
  bytes     4-7: id do próximo túnel, não zero
  bytes    8-39: hash da identidade do próximo roteador
  bytes   40-71: chave de camada de túnel AES-256
  bytes  72-103: chave IV de túnel AES-256
  bytes 104-135: chave de resposta AES-256
  bytes 136-151: IV de resposta AES-256
  byte      152: bandeiras
  bytes 153-155: mais bandeiras, não usadas, definidas para 0 para compatibilidade
  bytes 156-159: hora da solicitação (em minutos desde a época, arredondado para baixo)
  bytes 160-163: expiração da solicitação (em segundos desde a criação)
  bytes 164-167: ID da próxima mensagem
  bytes   168-x: opções de construção de túnel (Mapeamento)
  bytes     x-x: outros dados conforme indicado por bandeiras ou opções
  bytes   x-463: preenchimento aleatório




  ```

O campo de bandeiras é o mesmo definido em [Tunnel-Creation](/en/docs/spec/tunnel-creation/) e contém o seguinte::

 Ordem de bits: 76543210 (bit 7 é o MSB)
 bit 7: se configurado, permitir mensagens de qualquer pessoa
 bit 6: se configurado, permitir mensagens a qualquer pessoa, e enviar a resposta ao
        próximo salto especificado em uma Mensagem de Resposta de Construção de Túnel
 bits 5-0: Não definido, deve ser configurado para 0 para compatibilidade com futuras opções

O bit 7 indica que o salto será um gateway de entrada (IBGW). O bit 6
indica que o salto será um ponto final de saída (OBEP). Se nenhum dos dois bits estiver
definido, o salto será um participante intermediário. Ambos não podem ser configurados ao mesmo tempo.

A expiração da solicitação é para futura duração variável do túnel.
Por enquanto, o único valor suportado é 600 (10 minutos).

As opções de construção de túnel são uma estrutura de Mapeamento conforme definido em [Common](/en/docs/spec/common-structures/).
Isso é para uso futuro. Nenhuma opção está atualmente definida.
Se a estrutura de Mapeamento estiver vazia, são dois bytes 0x00 0x00.
O tamanho máximo do Mapeamento (incluindo o campo de comprimento) é 296 bytes,
e o valor máximo do campo de comprimento do Mapeamento é 294.



Registro de Solicitação Criptografado (ECIES)
````````````````````````````````````````````

Todos os campos são em big-endian, exceto para a chave pública efêmera que é little-endian.

Tamanho criptografado: 528 bytes

  ```dataspec


bytes    0-15: Hash truncado da identidade do salto
  bytes   16-47: Chave pública efêmera X25519 do remetente
  bytes  48-511: BuildRequestRecord criptografado com ChaCha20
  bytes 512-527: MAC Poly1305




  ```



### Registros de Resposta de Construção

BuildReplyRecords criptografados são 528 bytes para ambos ElGamal e ECIES, para compatibilidade.


Registro de Resposta Não Criptografado (ElGamal)
```````````````````````````````````````````````
Respostas ElGamal são criptografadas com AES.

Todos os campos são em big-endian.

Tamanho não criptografado: 528 bytes

  ```dataspec


bytes   0-31: Hash SHA-256 dos bytes 32-527
  bytes 32-526: dados aleatórios
  byte     527: resposta

  comprimento total: 528




  ```


Registro de Resposta Não Criptografado (ECIES)
`````````````````````````````````````````````
Esta é a especificação proposta do BuildReplyRecord de túnel para roteadores ECIES-X25519.
Resumo das mudanças:

- Adicionar Mapeamento para opções de resposta de construção
- Registro não criptografado é mais longo porque há menos sobrecarga de criptografia

Respostas ECIES são criptografadas com ChaCha20/Poly1305.

Todos os campos são em big-endian.

Tamanho não criptografado: 512 bytes

  ```dataspec


bytes    0-x: Opções de Resposta de Construção de Túnel (Mapeamento)
  bytes    x-x: outros dados conforme indicado por opções
  bytes  x-510: Preenchimento aleatório
  byte     511: Byte de Resposta




  ```

O campo de opções de resposta de construção de túnel é uma estrutura de Mapeamento conforme definido em [Common](/en/docs/spec/common-structures/).
Isso é para uso futuro. Nenhuma opção está atualmente definida.
Se a estrutura de Mapeamento estiver vazia, são dois bytes 0x00 0x00.
O tamanho máximo do Mapeamento (incluindo o campo de comprimento) é 511 bytes,
e o valor máximo do campo de comprimento do Mapeamento é 509.

O byte de resposta é um dos seguintes valores
conforme definido em [Tunnel-Creation](/en/docs/spec/tunnel-creation/) para evitar impressão digital:

- 0x00 (aceitar)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Registro de Resposta Criptografado (ECIES)
`````````````````````````````````````````

Tamanho criptografado: 528 bytes

  ```dataspec


bytes   0-511: BuildReplyRecord criptografado com ChaCha20
  bytes 512-527: MAC Poly1305




  ```

Após transição completa para registros ECIES, as regras de preenchimento variado são as mesmas para registros de solicitação.


### Criptografia Simétrica de Registros

Túneis mistos são permitidos, e necessários, para a transição de ElGamal para ECIES.
Durante o período de transição, um número crescente de roteadores será chaveado sob chaves ECIES.

O pré-processamento criptográfico simétrico ocorrerá da mesma maneira:

- "criptografia":

  - cifra executada no modo de decriptação
  - registros de solicitação préemptivamente decriptografados no pré-processamento (ocultando registros de solicitação criptografados)

- "decriptação":

  - cifra executada no modo de criptografia
  - registros de solicitação criptografados (revelando próximo registro de solicitação em texto simples) por saltos participantes

- ChaCha20 não tem "modos", então é simplesmente executado três vezes:

  - uma vez no pré-processamento
  - uma vez pelo salto
  - uma vez no processamento final de resposta

Quando túneis mistos são usados, os criadores de túneis precisarão basear a criptografia simétrica
do BuildRequestRecord no tipo de criptografia do hop atual e do anterior.

Cada salto usará seu próprio tipo de criptografia para criptografar BuildReplyRecords e os outros
registros na VariableTunnelBuildMessage (VTBM).

No caminho de resposta, o endpoint (remetente) precisará desfazer a [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), usando a chave de resposta de cada salto.

Como exemplo esclarecedor, vamos observar um túnel de saída com ECIES cercado por ElGamal:

- Remetente (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Todos os BuildRequestRecords estão em seu estado criptografado (usando ElGamal ou ECIES).

O cifrador AES256/CBC, quando usado, ainda é usado para cada registro, sem encadeamento em múltiplos registros.

Da mesma forma, ChaCha20 será usado para criptografar cada registro, não transmitindo por todo o VTBM.

Os registros de solicitação são pré-processados pelo Remetente (OBGW):

- O registro de H3 é "criptografado" usando:

  - a chave de resposta de H2 (ChaCha20)
  - a chave de resposta de H1 (AES256/CBC)

- O registro de H2 é "criptografado" usando:

  - a chave de resposta de H1 (AES256/CBC)

- O registro de H1 sai sem criptografia simétrica

Apenas H2 verifica a bandeira de criptografia de resposta, e vê que sua seguida por AES256/CBC.

Após serem processados por cada salto, os registros estão em um estado "decriptografado":

- O registro de H3 é "decriptografado" usando:

  - a chave de resposta de H3 (AES256/CBC)

- O registro de H2 é "decriptografado" usando:

  - a chave de resposta de H3 (AES256/CBC)
  - a chave de resposta de H2 (ChaCha20-Poly1305)

- O registro de H1 é "decriptografado" usando:

  - a chave de resposta de H3 (AES256/CBC)
  - a chave de resposta de H2 (ChaCha20)
  - a chave de resposta de H1 (AES256/CBC)

O criador do túnel, também conhecido como Endpoint de Entrada (IBEP), pós-processa a resposta:

- O registro de H3 é "criptografado" usando:

  - a chave de resposta de H3 (AES256/CBC)

- O registro de H2 é "criptografado" usando:

  - a chave de resposta de H3 (AES256/CBC)
  - a chave de resposta de H2 (ChaCha20-Poly1305)

- O registro de H1 é "criptografado" usando:

  - a chave de resposta de H3 (AES256/CBC)
  - a chave de resposta de H2 (ChaCha20)
  - a chave de resposta de H1 (AES256/CBC)


### Chaves de Registro de Solicitação (ECIES)

Essas chaves estão explicitamente incluídas nos BuildRequestRecords ElGamal.
Para BuildRequestRecords ECIES, as chaves do túnel e chaves de resposta AES estão incluídas,
mas as chaves de resposta ChaCha são derivadas da troca DH.
Veja [Prop156](/en/proposals/156-ecies-routers/) para detalhes sobre as chaves estáticas do roteador ECIES.

Abaixo está uma descrição de como derivar as chaves anteriormente transmitidas em registros de solicitação.


KDF para ck e h Iniciais
````````````````````````

Isso é padrão [NOISE](https://noiseprotocol.org/noise.html) para o padrão "N" com um nome de protocolo padrão.

  ```text

Este é o padrão de mensagem "e":

  // Definir protocol_name.
  Definir protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, codificado em US-ASCII, sem terminação NULL).

  // Definir Hash h = 32 bytes
  // Preencher para 32 bytes. NÃO fazer hash, porque não é mais que 32 bytes.
  h = protocol_name || 0

  Definir ck = chave de encadeamento de 32 bytes. Copiar os dados de h para ck.
  Definir chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // até aqui, pode ser pré-calculado por todos os roteadores.




  ```


KDF para Registro de Solicitação
``````````````````````````````````````

Criadores de túneis ElGamal geram um par de chaves X25519 efêmeras para cada
salto ECIES no túnel, e usam o esquema acima para criptografar seu BuildRequestRecord.
Criadores de túnel ElGamal usarão o esquema anterior a esta especificação para criptografar saltos ElGamal.

Criadores de túneis ECIES precisarão criptografar para a chave pública de cada salto ElGamal usando o
esquema definido em [Tunnel-Creation](/en/docs/spec/tunnel-creation/). Criadores de túneis ECIES usarão o esquema acima para criptografar
saltos ECIES.

Isso significa que saltos de túnel verão apenas registros criptografados do mesmo tipo de criptografia.

Para criadores de túneis ElGamal e ECIES, eles gerarão pares de chaves X25519 efêmeras exclusivas
por salto para criptografar os saltos ECIES.

**IMPORTANTE**:
As chaves efêmeras devem ser exclusivas por salto ECIES e por registro de construção.
Falhar em usar chaves exclusivas abre um vetor de ataque para saltos coniventes confirmarem que estão no mesmo túnel.


  ```dataspec


// Cada par de chaves estáticas X25519 do salto (hesk, hepk) da Identidade do Roteador
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || abaixo significa anexar
  h = SHA256(h || hepk);

  // até aqui, pode ser pré-calculado por cada roteador
  // para todas as solicitações de construção recebidas

  // Remetente gera um par de chaves X25519 efêmeras por salto ECIES no VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Fim do padrão de mensagem "e".

  Este é o padrão de mensagem "es":

  // Noise es
  // Remetente realiza um DH X25519 com a chave pública estática do Salto.
  // Cada Salto encontra o registro com seu hash de identidade truncado,
  // e extrai a chave efêmera do Remetente precedendo o registro criptografado.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // parâmetros ChaChaPoly para criptografar/decriptografar
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Salvar para KDF de Registro de Resposta
  chainKey = keydata[0:31]

  // parâmetros AEAD
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte de registro de solicitação de construção
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Fim do padrão de mensagem "es".

  // MixHash(ciphertext)
  // Salvar para KDF de Registro de Resposta
  h = SHA256(h || ciphertext)





  ```

``replyKey``, ``layerKey`` e ``layerIV`` ainda devem ser incluídos dentro de registros ElGamal,
e podem ser gerados aleatoriamente.


### Criptografia de Registro de Solicitação (ElGamal)

Conforme definido em [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Não há alterações na criptografia para saltos ElGamal.




### Criptografia de Registro de Resposta (ECIES)

O registro de resposta é criptografado com ChaCha20/Poly1305.

  ```dataspec


// parâmetros AEAD
  k = chave de encadeamento do registro de solicitação
  n = 0
  plaintext = 512 byte de registro de resposta de construção
  ad = h do registro de solicitação

  ciphertext = ENCRYPT(k, n, plaintext, ad)




  ```



### Criptografia de Registro de Resposta (ElGamal)

Conforme definido em [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Não há alterações na criptografia para saltos ElGamal.



### Análise de Segurança

ElGamal não fornece sigilo futuro para Mensagens de Construção de Túnel.

AES256/CBC está em uma posição ligeiramente melhor, sendo vulnerável apenas a um enfraquecimento teórico de um
ataque `biclique` de texto conhecido.

O único ataque prático conhecido contra AES256/CBC é um ataque de oracle de preenchimento, quando o IV é conhecido pelo atacante.

Um atacante precisaria quebrar a criptografia ElGamal do próximo salto para obter as informações da chave AES256/CBC (chave de resposta e IV).

ElGamal é significativamente mais intensivo em CPU do que ECIES, levando a um potencial esgotamento de recursos.

ECIES, usado com novas chaves efêmeras por BuildRequestRecord ou VariableTunnelBuildMessage, fornece sigilo futuro.

ChaCha20Poly1305 fornece criptografia AEAD, permitindo que o destinatário verifique a integridade da mensagem antes de tentar decriptografar.


## Justificação

Este design maximiza a reutilização de primitivas criptográficas, protocolos e código existentes.
Este design minimiza o risco.




## Notas de Implementação

* Roteadores mais antigos não verificam o tipo de criptografia do salto e enviarão
  registros criptografados com ElGamal. Alguns roteadores recentes são buggy e enviarão vários tipos de registros
  mal formados. Implementadores devem detectar e rejeitar esses registros antes da operação DH
  se possível, para reduzir o uso de CPU.


## Questões



## Migração

Veja [Prop156](/en/proposals/156-ecies-routers/).



