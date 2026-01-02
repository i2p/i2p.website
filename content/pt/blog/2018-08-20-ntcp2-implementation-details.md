---
title: "Detalhes de Implementação do NTCP2"
date: 2018-08-20
author: "villain"
description: "Detalhes de implementação e especificações técnicas do novo protocolo de transporte do I2P"
categories: ["development"]
---

Os protocolos de transporte do I2P foram originalmente desenvolvidos há cerca de 15 anos. Na época, o principal objetivo era ocultar os dados transferidos, não ocultar o fato de que se estava usando o próprio protocolo. Ninguém pensava seriamente em proteger contra DPI (inspeção profunda de pacotes) e censura de protocolos. Os tempos mudam e, embora os protocolos de transporte originais ainda forneçam segurança robusta, surgiu demanda por um novo protocolo de transporte. NTCP2 foi projetado para resistir às ameaças de censura atuais. Principalmente, à análise por DPI do comprimento dos pacotes. Além disso, o novo protocolo usa os desenvolvimentos mais modernos em criptografia. NTCP2 é baseado no [Noise Protocol Framework](https://noiseprotocol.org/noise.html), com SHA256 como função de hash e x25519 como um mecanismo de troca de chaves Diffie-Hellman (DH) de curva elíptica.

A especificação completa do protocolo NTCP2 pode ser [encontrada aqui](/docs/specs/ntcp2/).

## Nova criptografia

NTCP2 requer a adição dos seguintes algoritmos criptográficos a uma implementação do I2P:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

Compared to our original protocol, NTCP, NTCP2 uses x25519 instead of ElGamal for DH function, AEAD/Chaha20/Poly1305 instead of AES-256-CBC/Adler32, and uses SipHash for obfuscating the packet's length information. The key derivation function used in NTCP2 is more complex, now using many HMAC-SHA256 calls.

*Nota sobre a implementação do i2pd (C++): Todos os algoritmos mencionados acima, exceto o SipHash, estão implementados no OpenSSL 1.1.0. O SipHash será adicionado à próxima versão do OpenSSL 1.1.1. Para compatibilidade com o OpenSSL 1.0.2, que é usado na maioria dos sistemas atuais, o desenvolvedor principal do i2pd [Jeff Becker](https://github.com/majestrate) contribuiu com implementações independentes dos algoritmos criptográficos ausentes.*

## Alterações no RouterInfo

O NTCP2 requer a existência de uma terceira chave (x25519), além das duas já existentes (as chaves de criptografia e de assinatura). Ela é chamada de chave estática e deve ser adicionada a qualquer um dos endereços RouterInfo como parâmetro "s". Ela é obrigatória tanto para o iniciador do NTCP2 (Alice) quanto para o respondente (Bob). Se mais de um endereço suportar NTCP2, por exemplo, IPv4 e IPv6, o "s" deve ser o mesmo para todos. O endereço de Alice pode ter apenas o parâmetro "s" sem "host" e "port" definidos. Além disso, é necessário um parâmetro "v", que atualmente é sempre definido como "2".

O endereço NTCP2 pode ser declarado como um endereço NTCP2 separado ou como um endereço NTCP de estilo antigo com parâmetros adicionais; nesse caso, ele aceitará conexões NTCP e NTCP2. A implementação do I2P em Java usa a segunda abordagem, o i2pd (implementação em C++) usa a primeira.

Se um nó aceita conexões NTCP2, ele deve publicar seu RouterInfo com o parâmetro "i", que é usado como um vetor de inicialização (IV) para a chave pública de criptografia quando esse nó estabelece novas conexões.

## Estabelecendo uma conexão

Para estabelecer uma conexão, ambos os lados precisam gerar pares de chaves efêmeras x25519. Com base nessas chaves e em chaves "estáticas", eles derivam um conjunto de chaves para a transferência de dados. Ambas as partes devem verificar que o outro lado de fato possui uma chave privada correspondente àquela chave "estática" e que essa chave "estática" é a mesma que consta no RouterInfo.

Três mensagens estão sendo enviadas para estabelecer uma conexão:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Uma chave x25519 comum, chamada «input key material» (material de chave de entrada), é computada para cada mensagem, após o que a chave de criptografia da mensagem é gerada com uma função MixKey. Um valor ck (chave de encadeamento) é mantido enquanto as mensagens estão sendo trocadas. Esse valor é usado como entrada final ao gerar chaves para transferência de dados.

A função MixKey se parece com algo assim na implementação em C++ do I2P:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
A mensagem **SessionRequest** é composta por uma chave pública x25519 de Alice (32 bytes), um bloco de dados criptografado com AEAD/Chacha20/Poly1305 (16 bytes), um hash (16 bytes) e alguns dados aleatórios no final (preenchimento (padding)). O comprimento do preenchimento é definido no bloco de dados criptografado. O bloco criptografado também contém o comprimento da segunda parte da mensagem **SessionConfirmed**. Um bloco de dados é criptografado e assinado com uma chave derivada da chave efêmera de Alice e da chave estática de Bob. O valor inicial de ck para a função MixKey é definido como SHA256 (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Como 32 bytes da chave pública x25519 podem ser detectados por DPI (inspeção profunda de pacotes), ela é cifrada com o algoritmo AES-256-CBC, usando o hash do endereço de Bob como chave e o parâmetro "i" do RouterInfo como vetor de inicialização (IV).

A mensagem **SessionCreated** tem a mesma estrutura que **SessionRequest**, exceto que a chave é calculada com base nas chaves efêmeras de ambas as partes. O IV (vetor de inicialização) gerado após criptografar/descriptografar a chave pública da mensagem **SessionRequest** é usado como IV para criptografar/descriptografar a chave pública efêmera.

A mensagem **SessionConfirmed** tem 2 partes: chave pública estática e o RouterInfo de Alice. A diferença em relação às mensagens anteriores é que a chave pública efêmera é criptografada com AEAD/Chaha20/Poly1305 usando a mesma chave de **SessionCreated**. Isso faz com que a primeira parte da mensagem aumente de 32 para 48 bytes. A segunda parte também é criptografada com AEAD/Chaha20/Poly1305, mas usando uma nova chave, derivada a partir da chave efêmera de Bob e da chave estática de Alice. A parte RouterInfo também pode ser complementada com padding (preenchimento) de dados aleatórios, mas isso não é obrigatório, pois o RouterInfo normalmente tem comprimentos variados.

## Geração de Chaves de Transferência de Dados

Se todas as verificações de hash e de chave tiverem sido bem-sucedidas, um valor ck comum deve estar presente após a última operação MixKey em ambos os lados. Este valor é usado para gerar dois conjuntos de chaves <k, sipk, sipiv> para cada lado de uma conexão. "k" é uma chave AEAD/Chaha20/Poly1305, "sipk" é uma chave SipHash, "sipiv" é um valor inicial para o SipHash IV, que é alterado após cada uso.

O código usado para gerar chaves se parece com isto na implementação em C++ do I2P:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*nota de implementação do i2pd (C++): Os primeiros 16 bytes do array "sipkeys" são uma chave SipHash; os últimos 8 bytes são o IV (vetor de inicialização). O SipHash requer duas chaves de 8 bytes, mas o i2pd as trata como uma única chave de 16 bytes.*

## Transferência de Dados

Os dados são transferidos em quadros, cada quadro possui 3 partes:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

O tamanho máximo dos dados transferidos em um quadro é 65519 bytes.

O tamanho da mensagem é ofuscado por meio da aplicação da operação XOR com os dois primeiros bytes do IV atual do SipHash.

A parte de dados criptografados contém blocos de dados. Cada bloco é precedido por um cabeçalho de 3 bytes, que define o tipo e o comprimento do bloco. Em geral, são transferidos blocos do tipo I2NP, que são mensagens I2NP com um cabeçalho alterado. Um único quadro NTCP2 pode transferir múltiplos blocos I2NP.

O outro tipo importante de bloco de dados é o bloco de dados aleatório. Recomenda-se adicionar um bloco de dados aleatório a cada quadro NTCP2. Apenas um bloco de dados aleatório pode ser adicionado e deve ser o último bloco.

Estes são outros blocos de dados usados na implementação atual do NTCP2:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Resumo


O novo protocolo de transporte do I2P, NTCP2, oferece resistência eficaz à censura por DPI. Ele também reduz a carga de CPU devido à criptografia mais rápida e moderna utilizada. Isso torna mais provável que o I2P seja executado em dispositivos de baixo desempenho, como smartphones e routers domésticos. As duas principais implementações do I2P têm suporte completo ao NTCP2 e o disponibilizam para uso a partir da versão 0.9.36 (Java) e 2.20 (i2pd, C++).
