---
title: "Especificação do Blockfile"
description: "Formato de armazenamento em disco do tipo blockfile (arquivo em blocos) usado pelo I2P para resolução de nomes de host"
slug: "blockfile"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Visão geral

Este documento especifica o **formato de arquivo blockfile do I2P** e as tabelas no `hostsdb.blockfile` usadas pelo **Blockfile Naming Service (serviço de nomes Blockfile)**.   Para contexto, consulte [Nomes no I2P e Livro de Endereços](/docs/overview/naming).

O blockfile (arquivo em blocos) possibilita **consultas rápidas de destinos** em um formato binário compacto.   Em comparação com o sistema legado `hosts.txt`:

- Destinos são armazenados em binário, não em Base64.  
- Metadados arbitrários (por exemplo, data de adição, origem, comentários) podem ser anexados.  
- Os tempos de consulta são aproximadamente **10× mais rápidos**.  
- O uso de disco aumenta modestamente.

Um blockfile (arquivo de blocos) é uma coleção em disco de mapas ordenados (pares chave-valor) implementada como **skiplists** (listas de salto).   Foi derivado do [Metanotion Blockfile Database](http://www.metanotion.net/software/sandbox/block.html).   Esta especificação primeiro define a estrutura do arquivo, depois descreve como ela é usada pelo `BlockfileNamingService`.

> O Blockfile Naming Service (serviço de nomes Blockfile) substituiu a implementação antiga de `hosts.txt` no **I2P 0.8.8**.   > Na inicialização, ele importa entradas de `privatehosts.txt`, `userhosts.txt` e `hosts.txt`.

---

## Formato do Blockfile (arquivo de blocos)

O formato é composto por **páginas de 1024 bytes**, cada uma prefixada por um **número mágico** para integridade.   As páginas são numeradas a partir de 1:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Page</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Superblock (starts at byte 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Metaindex skiplist (starts at byte 1024)</td>
    </tr>
  </tbody>
</table>
Todos os inteiros usam **ordem de bytes de rede (big-endian, byte mais significativo primeiro)**.   Os valores de 2 bytes são sem sinal; os valores de 4 bytes (números de página) são com sinal e devem ser positivos.

> **Uso de threads:** O banco de dados é projetado para **acesso por uma única thread**; `BlockfileNamingService` fornece sincronização.

---

### Formato do Superbloco

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number <code>0x3141de493250</code> (<code>"1A"</code> <code>0xde</code> <code>"I2P"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Major version <code>0x01</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version <code>0x02</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File length (in bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag (<code>0x01</code> = yes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (max key/value pairs per span, 16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Page size (as of v1.2; 1024 before that)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Formato da página de bloco de lista de saltos

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x536b69704c697374</code> (<code>"SkipList"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (total keys, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Spans (total spans, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Levels (total levels, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (as of v1.2; used for new spans)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Formato da Página de Bloqueio de Skip Level (pular nível)

Todo nível tem um intervalo, mas nem todos os intervalos têm níveis.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x42534c6576656c73</code> (<code>"BSLevels"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages (<code>current height</code> × 4 bytes, lowest first)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Remaining bytes unused</td>
    </tr>
  </tbody>
</table>
---

### Formato da Página do Bloco Skip Span

Pares chave/valor são ordenados pela chave entre spans (segmentos).   Spans não iniciais não podem estar vazios.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x5370616e</code> (<code>"Span"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys (16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (current keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Formato de Página do Bloco de Continuação de Span (elemento HTML span)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x434f4e54</code> (<code>"CONT"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Formato da Estrutura Chave/Valor

Os campos de comprimento de chave e de valor **não podem atravessar páginas** (todos os 4 bytes devem caber). Se não restar espaço suficiente, preencha com até 3 bytes de padding e continue no deslocamento 8 da próxima página.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Value length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key data → Value data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max length = 65535 bytes each</td>
    </tr>
  </tbody>
</table>
---

### Formato da Página de Blocos da Lista Livre

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x2366724c69737423</code> (<code>"#frList#"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages (0 – 252)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Free page numbers (4 bytes each)</td>
    </tr>
  </tbody>
</table>
---

### Formato do Bloco de Página Livre

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x7e2146524545217e</code> (<code>"~!FREE!~"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Metaíndice

Localizado na página 2.   Mapeia **strings US-ASCII** → **inteiros de 4 bytes**.   A chave é o nome do skiplist (lista de salto); o valor é o índice da página.

---

## Tabelas do Blockfile Naming Service (serviço de nomes baseado em arquivo de blocos)

O serviço define várias skiplists (listas de salto). Cada span (intervalo) suporta até 16 elementos.

---

### Lista de salto de propriedades

`%%__INFO__%%` contém uma entrada:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>info</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A Properties object (UTF-8 String / String map) serialized as a Mapping</td>
    </tr>
  </tbody>
</table>
Campos típicos:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>version</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"4"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>created</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>upgraded</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch, since DB v2)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>lists</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma-separated host DBs (e.g. <code>privatehosts.txt,userhosts.txt,hosts.txt</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>listversion_*</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version of each DB (used to detect partial upgrades, since v4)</td>
    </tr>
  </tbody>
</table>
---

### Skiplist de Consulta Reversa (lista de saltos)

`%%__REVERSE__%%` contém entradas do tipo **Inteiro → Propriedades** (desde o DB v2).

- **Chave:** Primeiros 4 bytes do hash SHA-256 da Destination (identificador criptográfico do serviço no I2P).  
- **Valor:** objeto Properties (mapeamento serializado).  
- Várias entradas tratam colisões e Destinations com múltiplos nomes de host.  
- Cada chave de propriedade = hostname; valor = string vazia.

---

### Skiplists (listas de salto) do banco de dados de hosts

Cada um de `hosts.txt`, `userhosts.txt` e `privatehosts.txt` mapeia nomes de host → Destinos.

A versão 4 oferece suporte a vários Destinos por nome de host (introduzido no **I2P 0.9.26**).   Os bancos de dados da versão 3 são migrados automaticamente.

#### Chave

string UTF-8 (nome de host, em minúsculas, terminando em `.i2p`)

#### Valor

- **Versão 4:**  
  - 1 byte contendo a contagem de pares Propriedade/Destino  
  - Para cada par: Propriedades → Destino (binário)
- **Versão 3:**  
  - Propriedades → Destino (binário)

#### Propriedades de DestEntry

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>a</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Time added (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>m</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Last modified (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>notes</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User comments</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>s</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Source (file or subscription URL)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>v</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verified (<code>true</code>/<code>false</code>)</td>
    </tr>
  </tbody>
</table>
---

## Notas de Implementação

A classe Java `BlockfileNamingService` implementa esta especificação.

- Fora do contexto do router, o banco de dados abre como **somente leitura** a menos que `i2p.naming.blockfile.writeInAppContext=true`.  
- Não é destinado a acesso por múltiplas instâncias ou múltiplas JVMs.  
- Mantém três mapas principais (`privatehosts`, `userhosts`, `hosts`) e um mapa reverso para buscas rápidas.

---

## Referências

- [Documentação de Nomes e Livro de Endereços do I2P](/docs/overview/naming/)  
- [Especificação de Estruturas Comuns](/docs/specs/common-structures/)  
- [Banco de dados Blockfile da Metanotion](http://www.metanotion.net/software/sandbox/block.html)  
- [JavaDoc de BlockfileNamingService](https://geti2p.net/javadoc/i2p/naming/BlockfileNamingService.html)
