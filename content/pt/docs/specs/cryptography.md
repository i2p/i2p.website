---
title: "Criptografia de baixo nível"
description: "Resumo das primitivas criptográficas simétricas, assimétricas e de assinatura utilizadas em todo o I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Status:** Esta página condensa a especificação legada "Low-level Cryptography Specification". As versões modernas do I2P (2.10.0, outubro de 2025) concluíram a migração para novas primitivas criptográficas. Use especificações especializadas como [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), e [Tunnel Creation (ECIES)](/docs/specs/implementation/) para detalhes de implementação.

## Instantâneo do Evolution

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## Criptografia assimétrica

### X25519 (algoritmo de acordo de chaves de curva elíptica baseado na Curve25519)

- Usado para NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 e criação de tunnel baseada em X25519.  
- Fornece chaves compactas, operações em tempo constante e sigilo futuro por meio do Noise protocol framework (estrutura do protocolo Noise).  
- Oferece segurança de 128 bits com chaves de 32 bytes e troca de chaves eficiente.

### ElGamal (Legado)

- Mantido para compatibilidade com versões anteriores com routers mais antigos.  
- Opera sobre o primo de 2048 bits do Oakley Group 14 (RFC 3526) com gerador 2.  
- Cifra as chaves de sessão AES mais os IVs (vetores de inicialização) em textos cifrados de 514 bytes.  
- Não possui criptografia autenticada nem sigilo de encaminhamento; todos os pontos finais modernos migraram para ECIES.

## Criptografia simétrica

### ChaCha20/Poly1305

- Primitiva de criptografia autenticada padrão usada em NTCP2, SSU2 e ECIES.  
- Fornece segurança AEAD (Criptografia Autenticada com Dados Associados) e alto desempenho sem suporte de hardware para AES.  
- Implementado conforme a RFC 7539 (chave de 256 bits, nonce (número usado uma vez) de 96 bits, tag de 128 bits).

### AES‑256/CBC (Legado)

- Ainda é utilizado para a criptografia da camada de tunnel, em que sua estrutura de cifra de bloco se encaixa no modelo de criptografia em camadas do I2P.  
- Usa preenchimento PKCS#5 e transformações de IV (vetor de inicialização) por salto.  
- Programado para revisão de longo prazo, mas permanece criptograficamente sólido.

## Assinaturas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## Hash e Derivação de Chaves

- **SHA‑256:** Usado para chaves DHT, HKDF e assinaturas legadas.  
- **SHA‑512:** Usado por EdDSA/RedDSA e em derivações HKDF do Noise.  
- **HKDF‑SHA256:** Deriva chaves de sessão em ECIES, NTCP2 e SSU2.  
- Derivações de SHA‑256 com rotação diária protegem os locais de armazenamento de RouterInfo e LeaseSet na netDb.

## Resumo da Camada de Transporte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
Ambos os transportes oferecem forward secrecy (sigilo direto) e proteção contra repetição em nível de enlace, usando o padrão de handshake Noise_XK.

## Criptografia na Camada de Tunnel

- Continua a usar AES‑256/CBC para criptografia em camadas por salto.  
- Gateways de saída realizam descriptografia AES iterativa; cada salto volta a criptografar usando sua chave de camada e sua chave de IV.  
- A criptografia com IV duplo mitiga ataques de correlação e de confirmação.  
- A migração para AEAD está em estudo, mas não está planejada no momento.

## Criptografia Pós‑Quântica

- I2P 2.10.0 introduz **criptografia pós‑quântica híbrida experimental**.  
- Ativado manualmente via Hidden Service Manager (gerenciador de serviços ocultos) para testes.  
- Combina X25519 com um KEM resistente a ataques quânticos (modo híbrido).  
- Não é o padrão; destinado a pesquisa e avaliação de desempenho.

## Framework de Extensibilidade

- Os *identificadores de tipo* de criptografia e de assinatura permitem suporte paralelo a múltiplas primitivas.  
- Os mapeamentos atuais incluem:  
  - **Tipos de criptografia:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Tipos de assinatura:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Esta estrutura permite atualizações futuras, incluindo esquemas pós‑quânticos, sem divisão da rede.

## Composição Criptográfica

- **Camada de transporte:** X25519 + ChaCha20/Poly1305 (Noise framework).  
- **Camada de Tunnel:** Criptografia em camadas AES‑256/CBC para anonimato.  
- **Fim‑a‑fim:** ECIES‑X25519‑AEAD‑Ratchet para confidencialidade e sigilo futuro.  
- **Camada de banco de dados:** Assinaturas EdDSA/RedDSA para autenticidade.

Essas camadas se combinam para oferecer defesa em profundidade: mesmo que uma camada seja comprometida, as outras mantêm a confidencialidade e a não vinculabilidade.

## Resumo

A pilha criptográfica do I2P 2.10.0 concentra-se em:

- **Curve25519 (X25519)** para troca de chaves  
- **ChaCha20/Poly1305** para criptografia simétrica  
- **EdDSA / RedDSA** para assinaturas  
- **SHA‑256 / SHA‑512** para hash e derivação  
- **Modos híbridos pós‑quânticos experimentais** para compatibilidade futura

As versões legadas de ElGamal, AES‑CBC e DSA permanecem para compatibilidade com versões anteriores, mas não são mais utilizadas nos transportes ativos ou nos caminhos de criptografia.
