---
title: "B32 para LS2 Criptografado"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Fechado"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
---

## Nota
Implementação e testes na rede em progresso.
Sujeito a revisões menores.
Consulte [SPEC](/docs/specs/b32-for-encrypted-leasesets/) para a especificação oficial.


## Visão Geral

Endereços padrão Base 32 ("b32") contêm o hash do destino.
Isso não funcionará para ls2 criptografado (proposta 123).

Você não pode usar um endereço tradicional base 32 para um LS2 criptografado (proposta 123),
pois ele contém apenas o hash do destino. Não fornece a chave pública não-desofuscada.
Clientes devem conhecer a chave pública do destino, tipo de assinatura,
tipo de assinatura ofuscada e uma chave secreta ou privada opcional
para buscar e descriptografar o leaseset.
Portanto, somente um endereço base 32 é insuficiente.
O cliente precisa ou do destino completo (que contém a chave pública),
ou da chave pública por si só.
Se o cliente tiver o destino completo em um livro de endereços, e o livro de endereços
suporta consulta reversa por hash, então a chave pública pode ser recuperada.

Portanto, precisamos de um novo formato que coloque a chave pública em vez do hash em
um endereço base32. Este formato deve também conter o tipo de assinatura da
chave pública e o tipo de assinatura do esquema de ofuscação.

Esta proposta documenta um novo formato b32 para esses endereços.
Embora tenhamos nos referido a esse novo formato durante as discussões
como um endereço "b33", o formato real mantém o sufixo usual ".b32.i2p".

## Objetivos

- Incluir tanto tipos de assinatura não-ofuscados quanto ofuscados para suportar esquemas de ofuscação futuros
- Suportar chaves públicas maiores que 32 bytes
- Garantir que os caracteres b32 sejam todos ou em sua maioria aleatórios, especialmente no início
  (não queremos que todos os endereços comecem com os mesmos caracteres)
- Analisável
- Indicar que é necessário um segredo de ofuscação e/ou chave por cliente
- Adicionar soma de verificação para detectar erros de digitação
- Minimizar o comprimento, manter o comprimento do rótulo DNS inferior a 63 caracteres para uso normal
- Continuar usando base 32 para insensibilidade a maiúsculas
- Manter o sufixo usual ".b32.i2p".

## Não-Objetivos

- Não suportar links "privados" que incluem segredo de ofuscação e/ou chave por cliente;
  isso seria inseguro.


## Design

- O novo formato conterá a chave pública não-ofuscada, tipo de assinatura não-ofuscada,
  e tipo de assinatura ofuscada.
- Opcionalmente conter um segredo e/ou chave privada, apenas para links privados
- Usar o sufixo existente ".b32.i2p", mas com um comprimento maior.
- Adicionar uma soma de verificação.
- Endereços para leasesets criptografados são identificados por 56 ou mais caracteres codificados
  (35 ou mais bytes decodificados), em comparação com 52 caracteres (32 bytes) para endereços tradicionais base 32.


## Especificação

### Criação e codificação

Construa um nome de host de {56+ chars}.b32.i2p (35+ chars em binário) como segue:

```text
flag (1 byte)
    bit 0: 0 para tipos de assinatura de um byte, 1 para tipos de assinatura de dois bytes
    bit 1: 0 se não houver segredo, 1 se segredo for requerido
    bit 2: 0 se não houver autenticação por cliente,
           1 se a chave privada do cliente for requerida
    bits 7-3: Não utilizados, definir como 0

  tipo de assinatura da chave pública (1 ou 2 bytes conforme indicado nas flags)
    Se 1 byte, assume-se que o byte superior é zero

  tipo de assinatura da chave ofuscada (1 ou 2 bytes conforme indicado nas flags)
    Se 1 byte, assume-se que o byte superior é zero

  chave pública
    Número de bytes conforme indicado pelo tipo de assinatura

```

Pós-processamento e soma de verificação:

```text
Construa os dados binários como acima.
  Trate a soma de verificação como little-endian.
  Calcule a soma de verificação = CRC-32(data[3:end])
  data[0] ^= (byte) soma de verificação
  data[1] ^= (byte) (soma de verificação >> 8)
  data[2] ^= (byte) (soma de verificação >> 16)

  hostname = Base32.encode(data) || ".b32.i2p"
```

Quaisquer bits não utilizados no final do b32 devem ser 0.
Não há bits não utilizados para um endereço padrão de 56 caracteres (35 bytes).


### Decodificação e Verificação

```text
retire o ".b32.i2p" do nome do host
  data = Base32.decode(hostname)
  Calcule a soma de verificação = CRC-32(data[3:end])
  Trate a soma de verificação como little-endian.
  flags = data[0] ^ (byte) soma de verificação
  se tipos de assinatura de 1 byte:
    tipo de assinatura da chave pública = data[1] ^ (byte) (soma de verificação >> 8)
    tipo de assinatura ofuscada = data[2] ^ (byte) (soma de verificação >> 16)
  senão (tipos de assinatura de 2 bytes):
    tipo de assinatura da chave pública = data[1] ^ ((byte) (soma de verificação >> 8)) || data[2] ^ ((byte) (soma de verificação >> 16))
    tipo de assinatura ofuscada = data[3] || data[4]
  analise o restante com base nas flags para obter a chave pública
```


### Bits de Segredo e Chave Privada

Os bits de segredo e chave privada são usados para indicar aos clientes, proxies, ou outro
código no lado do cliente que o segredo e/ou chave privada serão necessários para descriptografar o
leaseset. Implementações específicas podem solicitar ao usuário para fornecer os
dados necessários, ou rejeitar tentativas de conexão se os dados necessários estiverem ausentes.


## Justificativa

- XORing os primeiros 3 bytes com o hash fornece uma capacidade limitada de soma de verificação,
  e garante que todos os caracteres base32 no início sejam aleatórios.
  Apenas algumas combinações de flags e tipos de assinatura são válidas, de modo que qualquer erro de digitação provavelmente criará uma combinação inválida que será rejeitada.
- No caso usual (tipos de assinatura de 1 byte, sem segredo, sem autenticação por cliente),
  o nome do host será {56 chars}.b32.i2p, decodificando para 35 bytes, o mesmo que o Tor.
- A soma de verificação de 2 bytes do Tor tem uma taxa de falso negativo de 1/64K. Com 3 bytes, menos alguns bytes ignorados,
  a nossa aproxima de 1 em um milhão, já que a maioria das combinações de flags/tipos de assinatura são inválidas.
- Adler-32 é uma escolha ruim para entradas pequenas, e para detectar pequenas alterações .
  Usar CRC-32 em vez disso. CRC-32 é rápido e amplamente disponível.

## Cache

Embora fora do escopo desta proposta, roteadores e/ou clientes devem lembrar e salvar em cache
(provavelmente de forma persistente) o mapeamento de chave pública para destino, e vice-versa.



## Notas

- Diferenciar sabores antigos de novos pelo comprimento. Endereços b32 antigos são sempre {52 chars}.b32.i2p. Novos são {56+ chars}.b32.i2p
- Tópico de discussão do Tor: https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- Não espere que tipos de assinatura de 2 bytes aconteçam alguma vez, estamos apenas até 13. Não há necessidade de implementar agora.
- O novo formato pode ser usado em links de salto (e servido por servidores de salto) se desejado, assim como o b32.


## Problemas

- Qualquer segredo, chave privada ou chave pública mais longa que 32 bytes
  excederia o comprimento máximo do rótulo DNS de 63 caracteres. Navegadores provavelmente não se importarão.


## Migração

Sem problemas de compatibilidade retroativa. Endereços b32 mais longos falharão ao serem convertidos
para hashes de 32 bytes em software antigo.
