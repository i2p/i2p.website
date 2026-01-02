---
title: "Nomenclatura e Livro de Endereços"
description: "Como o I2P mapeia nomes de host legíveis para destinos"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Os endereços I2P são longas chaves criptográficas. O sistema de nomenclatura fornece uma camada mais amigável sobre essas chaves **sem introduzir uma autoridade central**. Todos os nomes são **locais**—cada router decide independentemente a qual destino um nome de host se refere.

> **Precisa de contexto?** A [discussão sobre nomenclatura](/docs/legacy/naming/) documenta os debates originais de design, propostas alternativas e fundamentos filosóficos por trás da nomenclatura descentralizada do I2P.

---

## 1. Componentes

A camada de nomenclatura do I2P é composta por vários subsistemas independentes mas cooperantes:

1. **Serviço de nomes** – resolve nomes de host para destinos e trata [nomes de host Base32](#base32-hostnames).
2. **Proxy HTTP** – repassa consultas `.i2p` para o router e sugere serviços jump quando um nome é desconhecido.
3. **Serviços host-add** – formulários estilo CGI que adicionam novas entradas no catálogo de endereços local.
4. **Serviços jump** – auxiliares remotos que retornam o destino para um nome de host fornecido.
5. **Catálogo de endereços** – busca e mescla periodicamente listas de hosts remotas usando uma "rede de confiança" (web of trust) localmente confiável.
6. **SusiDNS** – uma interface web para gerenciar catálogos de endereços, assinaturas e substituições locais.

Este design modular permite que os usuários definam seus próprios limites de confiança e automatizem o quanto quiserem do processo de nomenclatura.

---

## 2. Serviços de Nomenclatura

A API de nomenclatura do router (`net.i2p.client.naming`) suporta múltiplos backends através da propriedade configurável `i2p.naming.impl=<class>`. Cada implementação pode oferecer diferentes estratégias de busca, mas todas compartilham o mesmo modelo de confiança e resolução.

### 2.1 Hosts.txt (legacy format)

O modelo legado usava três arquivos de texto simples verificados em ordem:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Cada linha armazena um mapeamento `hostname=base64-destination`. Este formato de texto simples permanece totalmente suportado para importação/exportação, mas não é mais o padrão devido ao baixo desempenho quando a lista de hosts excede algumas milhares de entradas.

---

### 2.2 Blockfile Naming Service (default backend)

Introduzido na **versão 0.8.8**, o Blockfile Naming Service é agora o backend padrão. Ele substitui arquivos planos por uma skiplist de alto desempenho baseada em armazenamento chave/valor em disco (`hostsdb.blockfile`) que oferece buscas aproximadamente **10× mais rápidas**.

**Características principais:** - Armazena múltiplos catálogos de endereços lógicos (privado, usuário e hosts) em um único banco de dados binário. - Mantém compatibilidade com importação/exportação do formato legado hosts.txt. - Suporta buscas reversas, metadados (data de adição, origem, comentários) e cache eficiente. - Usa a mesma ordem de busca em três níveis: privado → usuário → hosts.

Esta abordagem preserva a compatibilidade com versões anteriores enquanto melhora drasticamente a velocidade de resolução e a escalabilidade.

---

### 2.1 Hosts.txt (formato legado)

Os desenvolvedores podem implementar backends personalizados como: - **Meta** – agrega múltiplos sistemas de nomenclatura. - **PetName** – suporta petnames armazenados em um `petnames.txt`. - **AddressDB**, **Exec**, **Eepget** e **Dummy** – para resolução externa ou alternativa.

A implementação blockfile permanece como o backend **recomendado** para uso geral devido ao desempenho e confiabilidade.

---

## 3. Base32 Hostnames

Nomes de host Base32 (`*.b32.i2p`) funcionam de forma semelhante aos endereços `.onion` do Tor. Quando você acessa um endereço `.b32.i2p`:

1. O router decodifica o payload Base32.
2. Ele reconstrói o destino diretamente a partir da chave—**nenhuma consulta ao address-book é necessária**.

Isso garante a acessibilidade mesmo se não existir um nome de host legível por humanos. Os nomes Base32 estendidos introduzidos na **versão 0.9.40** suportam **LeaseSet2** e destinos criptografados.

---

## 4. Address Book & Subscriptions

A aplicação de livro de endereços recupera listas de hosts remotos via HTTP e as mescla localmente de acordo com as regras de confiança configuradas pelo usuário.

### 2.2 Serviço de Nomeação Blockfile (backend padrão)

- As subscrições são URLs `.i2p` padrão que apontam para `hosts.txt` ou feeds de atualização incremental.
- As atualizações são obtidas periodicamente (por hora, por padrão) e validadas antes da mesclagem.
- Os conflitos são resolvidos **por ordem de chegada**, seguindo a ordem de prioridade:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Desde **I2P 2.3.0 (junho de 2023)**, dois provedores de subscrição padrão estão incluídos: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Esta redundância melhora a confiabilidade enquanto preserva o modelo de confiança local. Os usuários podem adicionar ou remover assinaturas através do SusiDNS.

#### Incremental Updates

Atualizações incrementais são obtidas via `newhosts.txt` (substituindo o conceito mais antigo de `recenthosts.cgi`). Este endpoint fornece atualizações delta eficientes **baseadas em ETag**—retornando apenas novas entradas desde a última requisição ou `304 Not Modified` quando não houver alterações.

---

### 2.3 Backends Alternativos e Plug-ins

- **Serviços Host-add** (`add*.cgi`) permitem o envio manual de mapeamentos nome-para-destino. Sempre verifique o destino antes de aceitar.  
- **Serviços Jump** respondem com a chave apropriada e podem redirecionar através do proxy HTTP com um parâmetro `?i2paddresshelper=`.  
  Exemplos comuns: `stats.i2p`, `identiguy.i2p`, e `notbob.i2p`.  
  Estes serviços **não são autoridades confiáveis**—os usuários devem decidir quais usar.

---

## 5. Managing Entries Locally (SusiDNS)

O SusiDNS está disponível em:   `http://127.0.0.1:7657/susidns/`

Você pode: - Visualizar e editar catálogos de endereços locais. - Gerenciar e priorizar assinaturas. - Importar/exportar listas de hosts. - Configurar agendamentos de busca.

**Novidades no I2P 2.8.1 (Março de 2025):** - Adicionado recurso "ordenar por mais recente". - Melhoria no tratamento de assinaturas (correção para inconsistências de ETag).

Todas as alterações permanecem **locais**—o livro de endereços de cada router é único.

---

## 3. Nomes de host Base32

Seguindo a RFC 9476, o I2P registrou **`.i2p.alt`** junto à GNUnet Assigned Numbers Authority (GANA) em **março de 2025 (I2P 2.8.1)**.

**Propósito:** Prevenir vazamentos acidentais de DNS de software mal configurado.

- Resolvedores DNS compatíveis com RFC 9476 **não encaminharão** domínios `.alt` para o DNS público.
- O software I2P trata `.i2p.alt` como equivalente a `.i2p`, removendo o sufixo `.alt` durante a resolução.
- `.i2p.alt` **não** se destina a substituir `.i2p`; é uma proteção técnica, não uma mudança de marca.

---

## 4. Livro de Endereços & Assinaturas

- **Chaves de destino:** 516–616 bytes (Base64)  
- **Hostnames:** Máximo 67 caracteres (incluindo `.i2p`)  
- **Caracteres permitidos:** a–z, 0–9, `-`, `.` (sem pontos duplos, sem maiúsculas)  
- **Reservado:** `*.b32.i2p`  
- **ETag e Last-Modified:** utilizados ativamente para minimizar largura de banda  
- **Tamanho médio de hosts.txt:** ~400 KB para ~800 hosts (valor de exemplo)  
- **Uso de largura de banda:** ~10 bytes/seg se obtido a cada 12 horas

---

## 8. Security Model and Philosophy

O I2P intencionalmente sacrifica a unicidade global em troca de descentralização e segurança—uma aplicação direta do **Triângulo de Zooko**.

**Princípios fundamentais:** - **Sem autoridade central:** todas as consultas são locais.   - **Resistência ao sequestro de DNS:** as consultas são criptografadas para chaves públicas de destino.   - **Prevenção de ataques Sybil:** sem votação ou nomenclatura baseada em consenso.   - **Mapeamentos imutáveis:** uma vez que existe uma associação local, ela não pode ser sobrescrita remotamente.

Sistemas de nomenclatura baseados em blockchain (por exemplo, Namecoin, ENS) têm explorado a resolução dos três lados do triângulo de Zooko, mas o I2P intencionalmente os evita devido à latência, complexidade e incompatibilidade filosófica com seu modelo de confiança local.

---

## 9. Compatibility and Stability

- Nenhum recurso de nomenclatura foi descontinuado entre 2023–2025.
- O formato hosts.txt, serviços de salto, assinaturas e todas as implementações de API de nomenclatura permanecem funcionais.
- O Projeto I2P mantém **compatibilidade retroativa** rigorosa ao mesmo tempo que introduz melhorias de desempenho e segurança (isolamento NetDB, separação Sub-DB, etc.).

---

## 10. Best Practices

- Mantenha apenas assinaturas confiáveis; evite listas de hosts grandes e desconhecidas.
- Faça backup de `hostsdb.blockfile` e `privatehosts.txt` antes de atualizar ou reinstalar.
- Revise regularmente os serviços de jump e desative qualquer um em que você não confie mais.
- Lembre-se: seu catálogo de endereços define sua versão do mundo I2P—**cada hostname é local**.

---

### Further Reading

- [Discussão sobre Nomenclatura](/docs/legacy/naming/)  
- [Especificação de Blockfile](/docs/specs/blockfile/)  
- [Formato de Arquivo de Configuração](/docs/specs/configuration/)  
- [Javadoc do Serviço de Nomenclatura](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
