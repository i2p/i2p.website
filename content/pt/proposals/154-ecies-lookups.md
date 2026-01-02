---
title: "Consultas ao Banco de Dados de Destinos ECIES"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Closed"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Nota
ECIES para ElG está implementado na versão 0.9.46 e a fase de propostas está encerrada.
Veja [I2NP](/docs/specs/i2np/) para a especificação oficial.
Esta proposta ainda pode ser referenciada como informação de fundo.
ECIES para ECIES com chaves inclusas está implementado a partir da versão 0.9.48.
A seção ECIES-to-ECIES (chaves derivadas) pode ser reaberta ou incorporada
a uma proposta futura.


## Visão Geral

### Definições

- AEAD: ChaCha20/Poly1305
- DLM: Mensagem de Consulta ao Banco de Dados I2NP
- DSM: Mensagem de Armazenamento de Banco de Dados I2NP
- DSRM: Mensagem de Resposta de Pesquisa de Banco de Dados I2NP
- ECIES: ECIES-X25519-AEAD-Ratchet (proposta 144)
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): Conforme definido em [ECIES](/docs/specs/ecies/)
- LS: Leaseset
- lookup: DLM I2NP
- reply: DSM ou DSRM I2NP


### Resumo

Ao enviar um DLM para um LS para um floodfill, o DLM geralmente especifica
que a resposta deve ser marcada, criptografada com AES e enviada por um túnel até o destino.
O suporte para respostas criptografadas com AES foi adicionado na versão 0.9.7.

Respostas criptografadas com AES foram especificadas na versão 0.9.7 para minimizar a grande sobrecarga criptográfica do ElG, e porque reutilizava a facilidade de tags/AES
em ElGamal/AES+SessionTags. No entanto, respostas AES podem ser adulteradas no IBEP, pois não há autenticação, e as respostas não são secretas para o futuro.

Com destinos [ECIES](/docs/specs/ecies/), a intenção da proposta 144 é que
os destinos não suportem mais tags de 32 bytes e decriptação AES.
Os detalhes não foram intencionalmente incluídos nessa proposta.

Esta proposta documenta uma nova opção no DLM para solicitar respostas criptografadas com ECIES.


### Objetivos

- Novas flags para o DLM quando uma resposta criptografada é solicitada através de um túnel para um destino ECIES
- Para a resposta, adicionar segredo futuro e autenticação do remetente resistente à
  personificação por comprometimento de chave do solicitante (destino) (KCI).
- Manter o anonimato do solicitante
- Minimizar a sobrecarga criptográfica

### Não Objetivos

- Nenhuma mudança na criptografia ou propriedades de segurança da consulta (DLM).
  A consulta tem segredo futuro somente para comprometimento de chave do solicitante.
  A criptografia é feita para a chave estática do floodfill.
- Nenhum segredo futuro ou problemas de autenticação do remetente resistentes à
  personificação por comprometimento de chave do respondente (floodfill) (KCI).
  O floodfill é um banco público e responderá a consultas
  de qualquer um.
- Não projetar roteadores ECIES nesta proposta.
  A localização da chave pública X25519 de um roteador ainda será definida.


## Alternativas

Na ausência de uma maneira definida de criptografar respostas para destinos ECIES, há
várias alternativas:

1) Não solicitar respostas criptografadas. As respostas serão não criptografadas.
Java I2P atualmente usa essa abordagem.

2) Adicionar suporte para tags de 32 bytes e respostas criptografadas com AES para destinos somente ECIES, e solicitar respostas criptografadas com AES como de costume. i2pd atualmente usa essa abordagem.

3) Solicitar respostas criptografadas com AES como de costume, mas roteá-las de volta através de
túneis exploratórios para o roteador.
Java I2P atualmente usa essa abordagem em alguns casos.

4) Para destinos duplos ElG e ECIES,
solicitar respostas criptografadas com AES como de costume. Java I2P atualmente usa essa abordagem.
i2pd ainda não implementou destinos de criptografia dupla.


## Design

- Novo formato DLM adicionará um bit ao campo de flags para especificar respostas criptografadas com ECIES.
  Respostas criptografadas com ECIES usarão o formato de mensagem de Sessão Existente [ECIES](/docs/specs/ecies/),
  com uma tag anteposta e um payload e MAC ChaCha/Poly.

- Definir duas variantes. Uma para roteadores ElG, onde uma operação DH não é possível,
  e outra para futuros roteadores ECIES, onde uma operação DH é possível e pode fornecer
  segurança adicional. Para estudos futuros.

DH não é possível para respostas de roteadores ElG porque eles não publicam
uma chave pública X25519.


## Especificação

Na especificação [I2NP](/docs/specs/i2np/) DLM (Consulta ao Banco de Dados), faça as seguintes alterações.


Adicione o bit de flag 4 "ECIESFlag" para as novas opções de criptografia.

```text
flags ::
       bit 4: ECIESFlag
               antes da versão 0.9.46 ignorado
               a partir da versão 0.9.46:
               0  => enviar resposta não criptografada ou ElGamal
               1  => enviar resposta criptografada ChaCha/Poly usando chave incluída
                     (se a tag está incluída depende do bit 1)
```

O bit de flag 4 é usado em combinação com o bit 1 para determinar o modo de criptografia da resposta.
O bit de flag 4 deve ser definido somente ao enviar para roteadores com versão 0.9.46 ou superior.


Na tabela abaixo,
"DH n/a" significa que a resposta não é criptografada.
"DH não" significa que as chaves de resposta estão incluídas na solicitação.
"DH sim" significa que as chaves de resposta são derivadas da operação DH.


| Flag bits 4,1 | Do Dest | Para Router | Resposta | DH? | notas |
|---------------|---------|-------------|----------|-----|-------|
| 0 0            | Qualquer| Qualquer    | sem cripto| n/a | atual |
| 0 1            | ElG     | ElG         | AES      | não | atual |
| 0 1            | ECIES   | ElG         | AES      | não | i2pd solução alternativa |
| 1 0            | ECIES   | ElG         | AEAD     | não | esta proposta |
| 1 0            | ECIES   | ECIES       | AEAD     | não | 0.9.49 |
| 1 1            | ECIES   | ECIES       | AEAD     | sim | futuro |


### ElG para ElG

O destino ElG envia uma consulta para um roteador ElG.

Pequenas alterações na especificação para verificar o novo bit 4.
Nenhuma mudança no formato binário existente.


Geração de chave do solicitante (esclarecimento):

```text
reply_key :: CSRNG(32) 32 bytes de dados aleatórios
  reply_tags :: Cada um é CSRNG(32) 32 bytes de dados aleatórios
```

Formato da mensagem (adicionar verificação para ECIESFlag):

```text
reply_key ::
       32 byte `SessionKey` big-endian
       somente incluído se encryptionFlag == 1 E ECIESFlag == 0, somente a partir da versão 0.9.7

  tags ::
       1 byte `Integer`
       faixa válida: 1-32 (normalmente 1)
       o número de tags de resposta que seguem
       somente incluído se encryptionFlag == 1 E ECIESFlag == 0, somente a partir da versão 0.9.7

  reply_tags ::
       uma ou mais 32 bytes `SessionTag`s (normalmente um)
       somente incluído se encryptionFlag == 1 E ECIESFlag == 0, somente a partir da versão 0.9.7
```


### ECIES para ElG

O destino ECIES envia uma consulta para um roteador ElG.
Suportado a partir da versão 0.9.46.

Os campos reply_key e reply_tags são redefinidos para uma resposta criptografada com ECIES.

Geração de chave do solicitante:

```text
reply_key :: CSRNG(32) 32 bytes de dados aleatórios
  reply_tags :: Cada um é CSRNG(8) 8 bytes de dados aleatórios
```

Formato da mensagem:
Redefina os campos reply_key e reply_tags da seguinte forma:

```text
reply_key ::
       32 byte ECIES `SessionKey` big-endian
       somente incluído se encryptionFlag == 0 E ECIESFlag == 1, somente a partir da versão 0.9.46

  tags ::
       1 byte `Integer`
       valor requerido: 1
       o número de tags de resposta que seguem
       somente incluído se encryptionFlag == 0 E ECIESFlag == 1, somente a partir da versão 0.9.46

  reply_tags ::
       uma 8 byte ECIES `SessionTag`
       somente incluído se encryptionFlag == 0 E ECIESFlag == 1, somente a partir da versão 0.9.46
```


A resposta é uma mensagem de Sessão Existente ECIES, conforme definido em [ECIES](/docs/specs/ecies/).

```text
tag :: 8 byte reply_tag

  k :: 32 byte session key
     A chave de resposta.

  n :: 0

  ad :: A 8 byte reply_tag

  payload :: Dados em texto simples, o DSM ou DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### ECIES para ECIES (0.9.49)

Destino ou roteador ECIES envia uma consulta para um roteador ECIES, com chaves de resposta incluídas.
Suportado a partir da versão 0.9.49.

Roteadores ECIES foram introduzidos na versão 0.9.48, veja [Prop156](/proposals/156-ecies-routers/).
A partir da versão 0.9.49, destinos e roteadores ECIES podem usar o mesmo formato da seção
"ECIES para ElG" acima, com chaves de resposta incluídas na solicitação.
A consulta usará o "formato de uma vez" em [ECIES](/docs/specs/ecies/)
já que o solicitante é anônimo.

Para um novo método com chaves derivadas, veja a próxima seção.


### ECIES para ECIES (futuro)

Destino ou roteador ECIES envia uma consulta para um roteador ECIES, e as chaves de resposta são derivadas do DH.
Não totalmente definido ou suportado, implementação ainda será feita.

A consulta usará o "formato de uma vez" em [ECIES](/docs/specs/ecies/)
já que o solicitante é anônimo.

Redefina o campo reply_key como segue. Não há tags associadas.
As tags serão geradas no KDF abaixo.

Esta seção está incompleta e requer estudo adicional.


```text
reply_key ::
       32 byte X25519 efêmero `PublicKey` do solicitante, little-endian
       somente incluído se encryptionFlag == 1 E ECIESFlag == 1, somente a partir da versão 0.9.TBD
```

A resposta é uma mensagem de Sessão Existente ECIES, conforme definido em [ECIES](/docs/specs/ecies/).
Veja [ECIES](/docs/specs/ecies/) para todas as definições.


```text
// Chaves efêmeras X25519 de Alice
  // aesk = chave privada efêmera de Alice
  aesk = GENERATE_PRIVATE()
  // aepk = chave pública efêmera de Alice
  aepk = DERIVE_PUBLIC(aesk)
  // Chaves estáticas X25519 de Bob
  // bsk = chave privada estática de Bob
  bsk = GENERATE_PRIVATE()
  // bpk = chave pública estática de Bob
  // bpk está ou na parte de RouterIdentity, ou publicada no RouterInfo (será definido)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey de ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = chainKey da Seção de Payload
  2) k do KDF ou split() da Nova Sessão

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Saída 1: não utilizada
  unused = keydata[0:31]
  // Saída 2: A chain key para inicializar o novo
  // ciclos de tag e chave simétrica
  // para transmissões de Alice para Bob
  ck = keydata[32:63]

  // ciclos de tag e chave simétrica
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: 8 byte tag como gerado por RATCHET_TAG() em [ECIES](/docs/specs/ecies/)

  k :: 32 byte key como gerado por RATCHET_KEY() em [ECIES](/docs/specs/ecies/)

  n :: O índice da tag. Normalmente 0.

  ad :: A 8 byte tag

  payload :: Dados em texto simples, o DSM ou DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### Formato de resposta

Esta é a mensagem de sessão existente,
mesma de [ECIES](/docs/specs/ecies/), copiada abaixo para referência.

```text
+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Payload            +
  |       Dados criptografados com ChaCha20     |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticação de Mensagem Poly1305 |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, texto claro

  Dados criptografados da seção de payload :: dados restantes menos 16 bytes

  MAC :: Código de autenticação de mensagem Poly1305, 16 bytes
```


## Justificação

Os parâmetros de criptografia de resposta na consulta, introduzidos pela primeira vez na versão 0.9.7,
são de certa forma uma violação de camada. Isso é feito desta forma por eficiência.
Mas também porque a consulta é anônima.

Poderíamos tornar o formato de consulta genérico, como com um campo de tipo de criptografia,
mas isso provavelmente daria mais problemas do que vale a pena.

A proposta acima é a mais fácil e minimiza a mudança no formato da consulta.


## Notas

Consultas e armazenamento no banco de dados para roteadores ElG devem ser criptografados com ElGamal/AESSessionTag
como de costume.


## Questões

Análise adicional é necessária sobre a segurança das duas opções de resposta ECIES.


## Migração

Nenhum problema de compatibilidade com versões anteriores. Roteadores que anunciam uma router.version de 0.9.46 ou superior
em seu RouterInfo devem suportar este recurso.
Roteadores não devem enviar um DatabaseLookup com as novas flags para roteadores com uma versão inferior a 0.9.46.
Se uma mensagem de consulta ao banco de dados for enviada erroneamente com o bit 4 definido e o bit 1 não definido para
um roteador sem suporte, provavelmente ignorará a chave e a tag fornecidas, e
enviará a resposta não criptografada.
