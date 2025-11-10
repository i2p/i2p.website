---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Open"
thread: "http://zzz.i2p/topics/2689"
---

## Visão Geral

Esta proposta adiciona um novo tipo de assinatura utilizando BLAKE2b-512 com cadeias de personalização e sais, para substituir SHA-512. Isso eliminará três classes de ataques possíveis.

## Motivação

Durante discussões e o design do NTCP2 (proposta 111) e LS2 (proposta 123), consideramos brevemente vários ataques que eram possíveis, e como preveni-los. Três desses ataques são Ataques de Extensão de Comprimento, Ataques entre Protocolos, e Identificação de Mensagem Duplicada.

Para ambos NTCP2 e LS2, decidimos que esses ataques não eram diretamente relevantes para as propostas em questão, e quaisquer soluções conflitavam com o objetivo de minimizar novas primitivas. Também determinamos que a velocidade das funções hash nesses protocolos não era um fator importante em nossas decisões. Portanto, adiamos a solução para uma proposta separada. Enquanto adicionamos algumas características de personalização à especificação LS2, não exigimos quaisquer novas funções hash.

Muitos projetos, como o ZCash [ZCASH]_, estão utilizando funções hash e algoritmos de assinatura baseados em novos algoritmos que não são vulneráveis aos seguintes ataques.

### Ataques de Extensão de Comprimento

SHA-256 e SHA-512 são vulneráveis a Ataques de Extensão de Comprimento (LEA) [LEA]_. Isso ocorre quando dados reais são assinados, não o hash dos dados. Na maioria dos protocolos I2P (streaming, datagramas, netdb, e outros), os dados reais são assinados. Uma exceção são os arquivos SU3, onde o hash é assinado. A outra exceção são os datagramas assinados para DSA (tipo de assinatura 0) apenas, onde o hash é assinado. Para outros tipos de assinatura de datagrama assinados, os dados são assinados.

### Ataques entre Protocolos

Dados assinados em protocolos I2P podem ser vulneráveis a Ataques entre Protocolos (CPA) devido à falta de separação de domínio. Isso permite que um atacante use dados recebidos em um contexto (como um datagrama assinado) e os apresente como dados assinados válidos em outro contexto (como streaming ou banco de dados de rede). Embora seja improvável que os dados assinados de um contexto sejam interpretados como dados válidos em outro contexto, é difícil ou impossível analisar todas as situações para ter certeza. Adicionalmente, em algum contexto, pode ser possível para um atacante induzir uma vítima a assinar dados especialmente elaborados que poderiam ser dados válidos em outro contexto. Novamente, é difícil ou impossível analisar todas as situações para ter certeza.

### Identificação de Mensagem Duplicada

Protocolos I2P podem ser vulneráveis à Identificação de Mensagem Duplicada (DMI). Isso pode permitir que um atacante identifique que duas mensagens assinadas têm o mesmo conteúdo, mesmo se essas mensagens e suas assinaturas estiverem criptografadas. Embora seja improvável devido aos métodos de criptografia utilizados no I2P, é difícil ou impossível analisar todas as situações para ter certeza. Usando uma função hash que fornece um método para adicionar um sal aleatório, todas as assinaturas serão diferentes, mesmo ao assinar os mesmos dados. Embora o Red25519, conforme definido na proposta 123, adicione um sal aleatório à função hash, isso não resolve o problema para conjuntos de locação não criptografados.

### Velocidade

Embora não seja uma motivação primária para esta proposta, o SHA-512 é relativamente lento, e funções hash mais rápidas estão disponíveis.

## Objetivos

- Prevenir os ataques mencionados
- Minimizar o uso de novas primitivas criptográficas
- Usar primitivas criptográficas comprovadas e padrões
- Usar curvas padrão
- Usar primitivas mais rápidas, se disponíveis

## Design

Modificar o tipo de assinatura RedDSA_SHA512_Ed25519 existente para usar BLAKE2b-512 em vez de SHA-512. Adicionar cadeias de personalização únicas para cada caso de uso. O novo tipo de assinatura pode ser usado para conjuntos de locação cegos e não cegos.

## Justificativa

- BLAKE2b não é vulnerável a LEA [BLAKE2]_.
- BLAKE2b fornece um método padrão para adicionar cadeias de personalização para separação de domínio.
- BLAKE2b fornece um método padrão para adicionar um sal aleatório para prevenir DMI.
- BLAKE2b é mais rápido que SHA-256 e SHA-512 (e MD5) em hardware moderno, de acordo com [BLAKE2]_.
- Ed25519 ainda é nosso tipo de assinatura mais rápido, muito mais rápido que ECDSA, pelo menos em Java.
- Ed25519 [ED25519-REFS]_ requer uma função hash criptográfica de 512 bits. Não especifica SHA-512. BLAKE2b é igualmente adequado para a função hash.
- BLAKE2b está amplamente disponível em bibliotecas para muitas linguagens de programação, como o Noise.

## Especificação

Usar BLAKE2b-512 não autenticado como em [BLAKE2]_ com sal e personalização. Todos os usos de assinaturas BLAKE2b usarão uma cadeia de personalização de 16 caracteres.

Quando usado em assinatura RedDSA_BLAKE2b_Ed25519, um sal aleatório é permitido, no entanto, não é necessário, pois o algoritmo de assinatura adiciona 80 bytes de dados aleatórios (ver proposta 123). Se desejado, ao fazer o hash dos dados para calcular r, defina um novo sal aleatório de 16 bytes BLAKE2b para cada assinatura. Ao calcular S, redefina o sal para o padrão de todos zeros.

Quando usado em verificação RedDSA_BLAKE2b_Ed25519, não use um sal aleatório, use o padrão de todos zeros.

As características de sal e personalização não são especificadas em [RFC-7693]_; use essas características conforme especificado em [BLAKE2]_.

### Tipo de Assinatura

Para RedDSA_BLAKE2b_Ed25519, substitua a função hash SHA-512 em RedDSA_SHA512_Ed25519 (tipo de assinatura 11, conforme definido na proposta 123) por BLAKE2b-512. Nenhuma outra alteração.

Não precisamos de um substituto para EdDSA_SHA512_Ed25519ph (tipo de assinatura 8) para arquivos su3, porque a versão pre-hash de EdDSA não é vulnerável ao LEA. EdDSA_SHA512_Ed25519 (tipo de assinatura 7) não é suportado para arquivos su3.

=======================  ===========  ======  =====
        Tipo             Código Tipo  Desde   Uso
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        TBD    Apenas para Identidades de Roteador, Destinos e conjuntos de locação criptografados; nunca usado para Identidades de Roteador
=======================  ===========  ======  =====

### Comprimentos Comuns de Estrutura de Dados

O seguinte se aplica ao novo tipo de assinatura.

==================================  =============
            Tipo de Dados              Comprimento    
==================================  =============
Hash                                     64      
Chave Privada                            32      
Chave Pública                            32      
Assinatura                                64      
==================================  =============

### Personalizações

Para fornecer separação de domínio para os vários usos de assinaturas, usaremos a característica de personalização BLAKE2b.

Todos os usos de assinaturas BLAKE2b usarão uma cadeia de personalização de 16 caracteres. Quaisquer novos usos devem ser adicionados à tabela aqui, com uma personalização única.

Os usos de handshake NTCP 1 e SSU abaixo são para os dados assinados definidos no próprio handshake. RouterInfos assinados em Mensagens DatabaseStore usarão a personalização de Entrada NetDb, assim como se armazenados no NetDB.

==================================  ==========================
         Uso                      Personalização de 16 Bytes
==================================  ==========================
Configuração da Sessão I2CP        "I2CP_SessionConf"
Entradas NetDB (RI, LS, LS2)       "network_database"
Handshake NTCP 1                   "NTCP_1_handshake"
Datagramas Assinados               "sign_datagramI2P"
Streaming                          "streaming_i2psig"
Handshake SSU                      "SSUHandshakeSign"
Arquivos SU3                       n/a, não suportado
Testes unitários                   "test1234test5678"
==================================  ==========================

## Notas

## Questões

- Alternativa 1: Proposta 146; 
  Fornece resistência ao LEA
- Alternativa 2: Ed25519ctx no RFC 8032; 
  Fornece resistência ao LEA e personalização. 
  Padronizado, mas alguém o utiliza? Veja [RFC-8032]_ e [ED25519CTX]_.
- Hashing "chaveado" é útil para nós?

## Migração

Igual ao rollout para os tipos de assinatura anteriores.

Planejamos mudar novos roteadores do tipo 7 para tipo 12 como padrão. Planejamos eventualmente migrar roteadores existentes do tipo 7 para tipo 12, usando o processo de "rekeying" usado após a introdução do tipo 7. Planejamos mudar novos destinos do tipo 7 para tipo 12 como padrão. Planejamos mudar novos destinos criptografados do tipo 11 para tipo 13 como padrão.

Suportaremos ofuscação de tipos 7, 11 e 12 para tipo 12. Não suportaremos ofuscação do tipo 12 para tipo 11.

Novos roteadores poderiam começar a usar o novo tipo de assinatura por padrão após alguns meses. Novos destinos poderiam começar a usar o novo tipo de assinatura por padrão após talvez um ano.

Para a versão mínima do roteador 0.9.TBD, os roteadores devem garantir:

- Não armazenar (ou propagar) um RI ou LS com o novo tipo de assinatura para roteadores com versão inferior a 0.9.TBD.
- Ao verificar um store netdb, não buscar um RI ou LS com o novo tipo de assinatura de roteadores com versão inferior a 0.9.TBD.
- Roteadores com um novo tipo de assinatura em seu RI não podem se conectar a roteadores com versão inferior a 0.9.TBD, seja por NTCP, NTCP2, ou SSU.
- Conexões de streaming e datagramas assinados não funcionarão para roteadores com versão inferior a 0.9.TBD, mas não há como saber isso, então o novo tipo de assinatura não deve ser usado por padrão por um período de meses ou anos após o lançamento do 0.9.TBD.

## Referências

.. [BLAKE2]
   https://blake2.net/blake2.pdf

.. [ED25519CTX]
   https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS]
    "High-speed high-security signatures" por Daniel
    J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, e
    Bo-Yin Yang. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS]
   https://news.ycombinator.com/item?id=15414760

.. [LEA]
   https://en.wikipedia.org/wiki/Length_extension_attack

.. [RFC-7693]
   https://tools.ietf.org/html/rfc7693

.. [RFC-8032]
   https://tools.ietf.org/html/rfc8032

.. [ZCASH]
   https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
