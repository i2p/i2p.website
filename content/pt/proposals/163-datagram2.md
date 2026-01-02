---
title: "Protocolo Datagram2"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Fechado"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Status

Aprovado na revisão em 2025-04-15.
Alterações incorporadas nas especificações.
Implementado em Java I2P a partir da API 0.9.66.
Verifique a documentação de implementação para status.


## Visão Geral

Extraído de [Prop123](/proposals/123-new-netdb-entries/) como uma proposta separada.

Assinaturas offline não podem ser verificadas no processamento de datagramas repliáveis.
Necessita de uma bandeira para indicar assinaturas offline, mas não há lugar para colocar uma bandeira.

Será necessário um número e formato de protocolo I2CP completamente novo,
a serem adicionados à especificação [DATAGRAMS](/docs/api/datagrams/).
Vamos chamá-lo de "Datagram2".


## Objetivos

- Adicionar suporte para assinaturas offline
- Adicionar resistência a replay
- Adicionar versão sem assinaturas
- Adicionar campos de bandeiras e opções para extensibilidade


## Não-Objetivos

Suporte completo de protocolo de ponta a ponta para controle de congestionamento, etc.
Isso seria construído sobre, ou como uma alternativa a, Datagram2, que é um protocolo de baixo nível.
Não faria sentido projetar um protocolo de alto desempenho apenas sobre o
Datagram2, por causa do campo "from" e da sobrecarga de assinatura.
Qualquer protocolo desse tipo deve realizar um handshake inicial com Datagram2 e, em seguida,
alternar para datagramas RAW.


## Motivação

Remanescente do trabalho LS2, concluído em 2019.

A primeira aplicação a usar o Datagram2 deve ser
anúncios UDP de bittorrent, conforme implementado em i2psnark e zzzot,
veja [Prop160](/proposals/160-udp-trackers/).


## Especificação de Datagramas Repliáveis

Para referência,
segue uma revisão da especificação para datagramas repliáveis,
copiada de [Datagrams](/docs/api/datagrams/).
O número padrão de protocolo I2CP para datagramas repliáveis é PROTO_DATAGRAM (17).

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: um `Destination`
          comprimento: 387+ bytes
          O originador e assinante do datagrama

  signature :: uma `Signature`
               O tipo de assinatura deve corresponder ao tipo de chave pública de assinatura de $from
               comprimento: 40+ bytes, conforme implícito pelo tipo de assinatura.
               Para o tipo de chave DSA_SHA1 padrão:
                  A `Signature` DSA do hash SHA-256 do payload.
               Para outros tipos de chave:
                  A `Signature` do payload.
               A assinatura pode ser verificada pela chave pública de assinatura de $from

  payload ::  Os dados
              Comprimento: 0 até cerca de 31,5 KB (veja notas)

  Comprimento total: Comprimento do payload + 423+
```


## Design

- Definir novo protocolo 19 - Datagramas repliáveis com opções.
- Definir novo protocolo 20 - Datagramas repliáveis sem assinatura.
- Adicionar campo de bandeiras para assinaturas offline e expansão futura
- Mover assinatura após o payload para processamento mais fácil
- Nova especificação de assinatura diferente de datagrama repliável ou streaming, de modo que
  a verificação da assinatura falhará se interpretada como datagrama repliável ou streaming.
  Isso é conseguido movendo a assinatura após o payload,
  e incluindo o hash do destino na função de assinatura.
- Adicionar prevenção de replay para datagramas, como foi feito em [Prop164](/proposals/164-streaming/) para streaming.
- Adicionar seção para opções arbitrárias
- Reutilizar formato de assinatura offline de [Common](/docs/specs/common-structures/) e [Streaming](/docs/specs/streaming/).
- A seção de assinatura offline deve ser antes das seções de
  payload e assinatura de comprimento variável, pois especifica o comprimento
  da assinatura.


## Especificação

### Protocolo

O novo número de protocolo I2CP para Datagram2 é 19. Adicione-o como PROTO_DATAGRAM2 a [I2CP](/docs/specs/i2cp/).

O novo número de protocolo I2CP para Datagram3 é 20. Adicione-o como PROTO_DATAGRAM2 a [I2CP](/docs/specs/i2cp/).


### Formato Datagram2

Adicione Datagram2 a [DATAGRAMS](/docs/api/datagrams/) como segue:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: um `Destination`
          comprimento: 387+ bytes
          O originador e (a menos que assinado offline) assinante do datagrama

  flags :: (2 bytes)
           Ordem dos bits: 15 14 ... 3 2 1 0
           Bits 3-0: Versão: 0x02 (0 0 1 0)
           Bit 4: Se 0, sem opções; se 1, mapeamento de opções incluído
           Bit 5: Se 0, sem assinatura offline; se 1, assinado offline
           Bits 15-6: não usados, configurar para 0 para compatibilidade com usos futuros

  options :: (2+ bytes se presentes)
           Se a bandeira indicar que opções estão presentes, um `Mapping`
           contendo opções de texto arbitrárias

  offline_signature ::
               Se a bandeira indicar chaves offline, a seção de assinatura offline,
               conforme especificado na Especificação de Estruturas Comuns,
               com os seguintes 4 campos. Comprimento: varia conforme os tipos de assinatura
               online e offline, tipicamente 102 bytes para Ed25519
               Esta seção pode e deve ser gerada offline.

    expires :: Timestamp de expiração
               (4 bytes, big endian, segundos desde a época, gira em 2106)

    sigtype :: Tipo de assinatura transitória (2 bytes, big endian)

    pubkey :: Chave pública de assinatura transitória (comprimento conforme implicado pelo tipo de assinatura),
              tipicamente 32 bytes para o tipo de assinatura Ed25519.

    offsig :: uma `Signature`
              Assinatura de timestamp de expiração, tipo de assinatura transitória,
              e chave pública, pela chave pública de destino,
              comprimento: 40+ bytes, conforme implícito pelo tipo de assinatura, tipicamente
              64 bytes para o tipo de assinatura Ed25519.

  payload ::  Os dados
              Comprimento: 0 até cerca de 61 KB (veja notas)

  signature :: uma `Signature`
               O tipo de assinatura deve corresponder ao tipo de chave pública de assinatura de $from
               (se não assinado offline) ou o tipo de assinatura transitória
               (se assinado offline)
               comprimento: 40+ bytes, conforme implícito pelo tipo de assinatura, tipicamente
               64 bytes para o tipo de assinatura Ed25519.
               A `Signature` do payload e outros campos especificados abaixo.
               A assinatura é verificada pela chave pública de assinatura de $from
               (se não assinado offline) ou a chave pública transitória
               (se assinado offline)

```

Comprimento total: mínimo 433 + comprimento do payload;
comprimento típico para remetentes X25519 e sem assinaturas offline:
457 + comprimento do payload.
Observe que a mensagem será tipicamente comprimida com gzip na camada I2CP,
o que resultará em economias significativas se o destino "from" for compressível.

Nota: O formato de assinatura offline é o mesmo que na especificação de Estruturas Comuns [Common](/docs/specs/common-structures/) e [Streaming](/docs/specs/streaming/).

### Assinaturas

A assinatura é sobre os seguintes campos.

- Prelúdio: O hash de 32 bytes do destino alvo (não incluído no datagrama)
- flags
- options (se presentes)
- offline_signature (se presente)
- payload

No datagrama repliável, para o tipo de chave DSA_SHA1, a assinatura era sobre o
hash SHA-256 do payload, não o payload em si; aqui, a assinatura é
sempre sobre os campos acima (NÃO o hash), independentemente do tipo de chave.


### Verificação de ToHash

Os receptores devem verificar a assinatura (usando seu hash de destino)
e descartar o datagrama em caso de falha, para prevenção de replay.


### Formato Datagram3

Adicione Datagram3 a [DATAGRAMS](/docs/api/datagrams/) como segue:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: um `Hash`
              comprimento: 32 bytes
              O originador do datagrama

  flags :: (2 bytes)
           Ordem dos bits: 15 14 ... 3 2 1 0
           Bits 3-0: Versão: 0x03 (0 0 1 1)
           Bit 4: Se 0, sem opções; se 1, mapeamento de opções incluído
           Bits 15-5: não usados, configurar para 0 para compatibilidade com usos futuros

  options :: (2+ bytes se presentes)
           Se a bandeira indicar que opções estão presentes, um `Mapping`
           contendo opções de texto arbitrárias

  payload ::  Os dados
              Comprimento: 0 até cerca de 61 KB (veja notas)

```

Comprimento total: mínimo 34 + comprimento do payload.


### SAM

Adicione STYLE=DATAGRAM2 e STYLE=DATAGRAM3 à especificação SAMv3.
Atualize as informações sobre assinaturas offline.


### Sobrecarga

Este design adiciona 2 bytes de sobrecarga para datagramas repliáveis para bandeiras.
Isso é aceitável.


## Análise de Segurança

Incluir o hash alvo na assinatura deve ser efetivo em prevenir ataques de replay.

O formato Datagram3 não possui assinaturas, então o remetente não pode ser verificado,
e ataques de replay são possíveis. Qualquer validação necessária deve ser feita na camada de aplicação,
ou pelo roteador na camada de ratchet.


## Notas

- O comprimento prático é limitado pelas camadas inferiores dos protocolos - a especificação de mensagem de túnel [TUNMSG](/docs/specs/implementation/#notes) limita as mensagens a cerca de 61,2 KB e os transportes
  [TRANSPORT](/docs/overview/transport/) atualmente limitam as mensagens a cerca de 64 KB, então o comprimento dos dados aqui
  é limitado a cerca de 61 KB.
- Veja notas importantes sobre a confiabilidade de datagramas grandes [API](/docs/api/datagrams/). Para
  melhores resultados, limite o payload a cerca de 10 KB ou menos.


## Compatibilidade

Nenhuma. As aplicações devem ser reescritas para rotear mensagens I2CP Datagram2
com base no protocolo e/ou porta.
Mensagens Datagram2 que são mal roteadas e interpretadas como
mensagens de datagrama repliáveis ou de streaming falharão com base na assinatura, formato, ou ambos.


## Migração

Cada aplicação UDP deve detectar suporte e migrar separadamente.
A aplicação UDP mais proeminente é o bittorrent.

### Bittorrent

DHT de Bittorrent: Provavelmente precisa de bandeira de extensão,
por exemplo, i2p_dg2, coordenar com BiglyBT

Anúncios UDP de Bittorrent [Prop160](/proposals/160-udp-trackers/): Design desde o início.
Coordenar com BiglyBT, i2psnark, zzzot

### Outros

Bote: Improvável de migrar, não mantido ativamente

Streamr: Ninguém está usando, nenhuma migração planejada

Aplicativos UDP SAM: Nenhum conhecido


## Referências

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/overview/transport/)
* [TUNMSG](/docs/specs/implementation/#notes)
