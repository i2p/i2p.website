---
title: "Tipo de Assinatura GOST"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Open"
thread: "http://zzz.i2p/topics/2239"
---

## Visão Geral

Assinatura de curva elíptica GOST R 34.10 usada por autoridades e empresas na Rússia.
Apoiar isso poderia simplificar a integração de aplicativos existentes (geralmente baseados no CryptoPro).
A função hash é GOST R 34.11 de 32 ou 64 bytes.
Basicamente funciona da mesma maneira que o EcDSA, o tamanho da assinatura e da chave pública é de 64 ou 128 bytes.

## Motivação

A criptografia de curva elíptica nunca foi completamente confiável e gera muita especulação sobre possíveis backdoors. 
Portanto, não há um tipo de assinatura definitivo confiado por todos.
Adicionar mais um tipo de assinatura dará às pessoas mais opções sobre o que confiam mais.

## Design

O GOST R 34.10 usa curva elíptica padrão com seus próprios conjuntos de parâmetros.
A matemática dos grupos existentes pode ser reutilizada.
No entanto, a assinatura e a verificação são diferentes e devem ser implementadas.
Veja o RFC: https://www.rfc-editor.org/rfc/rfc7091.txt
O GOST R 34.10 deve funcionar junto com o hash GOST R 34.11.
Usaremos o GOST R 34.10-2012 (também conhecido como steebog) com 256 ou 512 bits.
Veja o RFC: https://tools.ietf.org/html/rfc6986

O GOST R 34.10 não especifica parâmetros, no entanto, há alguns bons conjuntos de parâmetros usados por todos.
O GOST R 34.10-2012 com 64 bytes de chaves públicas herda os conjuntos de parâmetros do CryptoPro do GOST R 34.10-2001.
Veja o RFC: https://tools.ietf.org/html/rfc4357

No entanto, novos conjuntos de parâmetros para chaves de 128 bytes foram criados por um comitê técnico especial tc26 (tc26.ru).
Veja o RFC: https://www.rfc-editor.org/rfc/rfc7836.txt

Implementação baseada em Openssl no i2pd demonstra que é mais rápido que o P256 e mais lento que o 25519.

## Especificação

Apenas GOST R 34.10-2012 e GOST R 34.11-2012 são suportados.
Dois novos tipos de assinatura:
9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A representa tipo de chave pública e assinatura de 64 bytes, tamanho de hash de 32 bytes e conjunto de parâmetros CryptoProA (também conhecido como CryptoProXchA)
10 - GOSTR3410_GOSTR3411_512_TC26_A representa tipo de chave pública e assinatura de 128 bytes, tamanho de hash de 64 bytes e conjunto de parâmetros A do TC26.

## Migração

Esses tipos de assinatura devem ser usados apenas como tipo de assinatura opcional.
Nenhuma migração é necessária. O i2pd já o suporta.
