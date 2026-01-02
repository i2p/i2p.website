---
title: "Especificação de Atualização de Software"
description: "Mecanismo seguro de atualização assinada e estrutura de feed para I2P routers"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão geral

Routers verificam automaticamente a existência de atualizações consultando periodicamente um feed de notícias assinado distribuído pela rede I2P. Quando uma versão mais recente é anunciada, o router baixa um arquivo de atualização assinado criptograficamente (`.su3`) e o prepara para instalação.   Este sistema garante distribuição **autenticada, resistente à adulteração** e **multicanal** de versões oficiais.

A partir da versão 2.10.0 do I2P, o sistema de atualização utiliza: - **RSA-4096 / SHA-512** assinaturas - **formato de contêiner SU3** (substituindo os legados SUD/SU2) - **Espelhos redundantes:** HTTP na rede, HTTPS na clearnet e BitTorrent

---

## 1. Feed de Notícias

Routers verificam o feed Atom assinado a cada algumas horas para descobrir novas versões e avisos de segurança.   O feed é assinado e distribuído como um arquivo `.su3`, que pode incluir:

- `<i2p:version>` — novo número de versão  
- `<i2p:minVersion>` — versão mínima do router suportada  
- `<i2p:minJavaVersion>` — ambiente de execução Java mínimo obrigatório  
- `<i2p:update>` — lista vários espelhos de download (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — dados de revogação de certificados  
- `<i2p:blocklist>` — listas de bloqueio no nível da rede para pares comprometidos

### Distribuição do feed

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Os routers preferem o feed via I2P, mas podem recorrer à distribuição via clearnet ou via torrent, se necessário.

---

## 2. Formatos de Arquivo

### SU3 (Padrão atual)

Introduzido na versão 0.9.9, o SU3 substituiu os formatos legados SUD e SU2. Cada arquivo contém um cabeçalho, uma carga útil e uma assinatura final.

**Estrutura do Cabeçalho** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Etapas de verificação da assinatura** 1. Analisar o cabeçalho e identificar o algoritmo de assinatura.   2. Verificar o hash e a assinatura usando o certificado do signatário armazenado.   3. Confirmar que o certificado do signatário não foi revogado.   4. Comparar a string de versão incorporada com os metadados da carga útil.

Routers vêm com certificados de assinadores confiáveis (atualmente **zzz** e **str4d**) e rejeitam quaisquer fontes não assinadas ou revogadas.

### SU2 (Obsoleto)

- Usava a extensão `.su2` com JARs comprimidos com Pack200.  
- Removido após o Java 14 ter marcado o Pack200 como obsoleto (JEP 367).  
- Desativado no I2P 0.9.48+; agora totalmente substituído por compressão ZIP.

### SUD (Legado)

- Formato ZIP inicial assinado com DSA-SHA1 (pré-0.9.9).  
- Sem ID do signatário nem cabeçalho, integridade limitada.  
- Substituído devido a criptografia fraca e falta de imposição de versão.

---

## 3. Fluxo de trabalho de atualização

### 3.1 Verificação do Cabeçalho

Os routers obtêm apenas o **cabeçalho SU3** para verificar a string de versão antes de baixar os arquivos completos. Isso evita desperdiçar largura de banda com espelhos desatualizados ou versões antigas.

### 3.2 Download completo

Após verificar o cabeçalho, o router baixa o arquivo `.su3` completo de: - Espelhos de eepsite na rede (preferencial)   - Espelhos HTTPS na clearnet (alternativa)   - BitTorrent (distribuição opcional assistida por pares)

As transferências usam clientes HTTP padrão do I2PTunnel, com novas tentativas, tratamento de tempo limite e recurso a espelhos.

### 3.3 Verificação de Assinatura

Cada arquivo baixado passa por: - **Verificação de assinatura:** verificação RSA-4096/SHA512   - **Correspondência de versões:** verificação da versão do cabeçalho vs. da carga útil   - **Prevenção de downgrade:** garante que a atualização seja mais recente do que a versão instalada

Arquivos inválidos ou incompatíveis são descartados imediatamente.

### 3.4 Preparação da Instalação

Uma vez verificado: 1. Extraia o conteúdo do ZIP para um diretório temporário   2. Remova os arquivos listados em `deletelist.txt`   3. Substitua as bibliotecas nativas se `lib/jbigi.jar` estiver incluído   4. Copie os certificados do signatário para `~/.i2p/certificates/`   5. Mova a atualização para `i2pupdate.zip` para aplicação na próxima reinicialização

A atualização é instalada automaticamente na próxima inicialização ou quando “Install update now” é acionado manualmente.

---

## 4. Gerenciamento de arquivos

### deletelist.txt

Uma lista em texto simples de arquivos obsoletos para remover antes de descompactar os novos conteúdos.

**Regras:** - Um caminho por linha (apenas caminhos relativos) - Linhas que começam com `#` são ignoradas - `..` e caminhos absolutos rejeitados

### Bibliotecas Nativas

Para evitar binários nativos obsoletos ou incompatíveis: - Se `lib/jbigi.jar` existir, arquivos `.so` ou `.dll` antigos são excluídos   - Garante que as bibliotecas específicas da plataforma sejam extraídas novamente

---

## 5. Gerenciamento de Certificados

Routers podem receber **novos certificados de assinante** por meio de atualizações ou revogações do feed de notícias.

- Novos arquivos `.crt` são copiados para o diretório de certificados.  
- Certificados revogados são excluídos antes de futuras verificações.  
- Suporta rotação de chaves sem exigir intervenção manual do usuário.

Todas as atualizações são assinadas offline usando **air-gapped signing systems** (sistemas de assinatura isolados fisicamente).   As chaves privadas nunca são armazenadas nos servidores de compilação.

---

## 6. Diretrizes para Desenvolvedores

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Versões futuras explorarão a integração de assinaturas pós-quânticas (consulte a Proposal 169) e compilações reprodutíveis.

---

## 7. Visão geral de segurança

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Versionamento

- Router: **2.10.0 (API 0.9.67)**  
- Versionamento semântico com `Major.Minor.Patch`.  
- A imposição de versão mínima evita atualizações inseguras.  
- Java com suporte: **Java 8–17**. No futuro, as versões 2.11.0 e superiores exigirão Java 17+.

---
