---
title: "Ofuscação de chave ECDSA"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Open"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Motivação

Algumas pessoas não gostam de EdDSA ou RedDSA. Devemos oferecer algumas alternativas e permitir que elas ofusquem assinaturas ECDSA.

## Visão geral

Esta proposta descreve a ofuscação de chave para tipos de assinatura ECDSA 1, 2, 3.

## Proposta

Funciona da mesma forma que RedDSA, mas tudo está em Big Endian. 
Apenas os mesmos tipos de assinatura são permitidos, por exemplo, 1->1, 2->2, 3->3.

### Definições

B
    Ponto base da curva

L
   Ordem do grupo da curva elíptica. Propriedade da curva.

DERIVE_PUBLIC(a)
    Converter uma chave privada para pública, multiplicando B sobre uma curva elíptica

alpha
    Um número aleatório de 32 bytes conhecido por aqueles que conhecem o destino.

GENERATE_ALPHA(destination, date, secret)
    Gerar alpha para a data atual, para aqueles que conhecem o destino e o segredo.

a
    A chave privada de assinatura de 32 bytes não ofuscada usada para assinar o destino

A
    A chave pública de assinatura de 32 bytes não ofuscada no destino,
    = DERIVE_PUBLIC(a), na curva correspondente

a'
    A chave privada de assinatura de 32 bytes ofuscada usada para assinar o leaseset criptografado
    Esta é uma chave privada ECDSA válida.

A'
    A chave pública de assinatura ECDSA de 32 bytes ofuscada no destino,
    pode ser gerada com DERIVE_PUBLIC(a'), ou de A e alpha.
    Esta é uma chave pública ECDSA válida na curva

H(p, d)
    Função hash SHA-256 que recebe uma string de personalização p e dados d, e
    produz uma saída de comprimento 32 bytes.

    Use SHA-256 da seguinte forma::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    Uma função de derivação de chave criptográfica que recebe algum material chave de entrada ikm (que
    deve ter boa entropia, mas não é necessário que seja uma string aleatória uniforme), um salt
    de comprimento 32 bytes, e um valor 'info' específico do contexto, e produz uma saída
    de n bytes adequada para uso como material chave.

    Use HKDF conforme especificado em [RFC-5869](https://tools.ietf.org/html/rfc5869), usando a função hash HMAC SHA-256
    conforme especificado em [RFC-2104](https://tools.ietf.org/html/rfc2104). Isso significa que SALT_LEN é 32 bytes máx.


### Cálculos de Ofuscação

Um novo segredo alpha e chaves ofuscadas devem ser gerados a cada dia (UTC).
O segredo alpha e as chaves ofuscadas são calculados da seguinte forma.

GENERATE_ALPHA(destination, date, secret), para todas as partes:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret é opcional, caso contrário, comprimento zero
  A = chave pública de assinatura do destino
  stA = tipo de assinatura de A, 2 bytes em big endian (0x0001, 0x0002 ou 0x0003)
  stA' = tipo de assinatura da chave pública ofuscada A', 2 bytes em big endian, sempre o mesmo que stA
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD da data atual UTC
  secret = string codificada em UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // trate o seed como um valor de 64 bytes em big-endian
  alpha = seed mod L
```


BLIND_PRIVKEY(), para o proprietário publicando o leaseset:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = chave privada de assinatura do destino
  // Adição usando aritmética escalar
  chave privada de assinatura ofuscada = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  chave pública de assinatura ofuscada = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY(), para os clientes recuperando o leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = chave pública de assinatura do destino
  // Adição usando elementos do grupo (pontos na curva)
  chave pública ofuscada = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


Ambos os métodos de calcular A' produzem o mesmo resultado, conforme exigido.

## endereço b33

A chave pública do ECDSA é o par (X, Y), então para P256, por exemplo, são 64 bytes, ao invés de 32 como para RedDSA. 
Ou o endereço b33 será maior, ou a chave pública pode ser armazenada em formato comprimido, como em carteiras de bitcoin.


## Referências

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
