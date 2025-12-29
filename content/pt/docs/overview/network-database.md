---
title: "Banco de dados da rede"
description: "Compreendendo o banco de dados de rede distribuído (netDb) do I2P - um DHT especializado para informações de contato de router e consultas de destinos"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Visão geral

O **netDb** é um banco de dados distribuído especializado que contém apenas dois tipos de dados: - **RouterInfos** – informações de contato do router - **LeaseSets** – informações de contato do destino

Todos os dados são assinados criptograficamente e verificáveis. Cada entrada inclui informações de liveness (indicadores de atividade) para descartar entradas obsoletas e substituir as desatualizadas, protegendo contra certas classes de ataque.

A distribuição usa um mecanismo de **floodfill** (método de armazenamento e propagação da base de dados distribuída no I2P), no qual um subconjunto de routers mantém essa base de dados.

---

## 2. RouterInfo

Quando routers precisam se comunicar com outros routers, eles trocam pacotes **RouterInfo** contendo:

- **Identidade do router** – chave de criptografia, chave de assinatura, certificado
- **Endereços de contato** – como alcançar o router
- **Carimbo de data e hora da publicação** – quando esta informação foi publicada
- **Opções de texto arbitrárias** – sinalizadores de capacidade e configurações
- **Assinatura criptográfica** – comprova a autenticidade

### 2.1 Sinalizadores de Capacidade

Os Routers anunciam capacidades por meio de códigos de letras em seu RouterInfo:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Classificações de largura de banda

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Valores de ID de Rede

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 Estatísticas do RouterInfo

Routers publicam estatísticas opcionais de saúde para análise da rede: - Taxas de sucesso/rejeição/tempo limite na construção de tunnel exploratório - Média de 1 hora do número de tunnel participantes

As estatísticas seguem o formato `stat_(statname).(statperiod)` com valores separados por ponto e vírgula.

**Estatísticas de exemplo:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Os Floodfill routers também podem publicar: `netdb.knownLeaseSets` e `netdb.knownRouters`

### 2.5 Opções da Família

A partir da versão 0.9.24, routers podem declarar que pertencem a uma família (mesmo operador):

- **family**: Nome da família
- **family.key**: Código do tipo de assinatura concatenado com a chave pública de assinatura codificada em base64
- **family.sig**: Assinatura do nome da família e do hash do router de 32 bytes

Múltiplos routers da mesma família não serão utilizados em tunnels individuais.

### 2.6 Expiração do RouterInfo (informações do router)

- Sem expiração durante a primeira hora de tempo de atividade
- Sem expiração com 25 ou menos RouterInfos (informações de router) armazenados
- A expiração diminui conforme a contagem local cresce (72 horas em <120 routers; ~30 horas em 300 routers)
- Os SSU introducers (nós de introdução) expiram em ~1 hora
- Floodfills usam expiração de 1 hora para todos os RouterInfos locais

---

## 3. LeaseSet

Os **LeaseSets** descrevem os pontos de entrada de tunnel para destinos específicos, especificando:

- **Identidade do router gateway do Tunnel**
- **ID do tunnel de 4 bytes**
- **Tempo de expiração do Tunnel**

LeaseSets incluem: - **Destino** – chave de criptografia, chave de assinatura, certificado - **Chave pública de criptografia adicional** – para garlic encryption de ponta a ponta (técnica do I2P que agrupa múltiplas mensagens criptografadas em um único pacote) - **Chave pública de assinatura adicional** – destinada à revogação (atualmente não utilizada) - **Assinatura criptográfica**

### 3.1 Variantes de LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 Expiração do LeaseSet

LeaseSets regulares expiram quando ocorre a expiração do lease (alocação de túnel) mais tardio. A expiração do LeaseSet2 é especificada no cabeçalho. As expirações de EncryptedLeaseSet e MetaLeaseSet podem variar, com possível imposição de um limite máximo.

---

## 4. Inicialização

A netDb descentralizada requer pelo menos uma referência de par para se integrar. **Reseeding** (processo de obtenção inicial de referências de pares) recupera arquivos RouterInfo (`routerInfo-$hash.dat`) a partir dos diretórios netDb de voluntários. Na primeira inicialização, obtém automaticamente a partir de URLs embutidas no código, selecionadas aleatoriamente.

---

## 5. Mecanismo de Floodfill

O netDb floodfill usa armazenamento distribuído simples: envia os dados para o par floodfill mais próximo. Quando pares não-floodfill enviam store (mensagens de armazenamento), os floodfills encaminham para um subconjunto de pares floodfill mais próximos da chave específica.

A participação em floodfill é indicada como uma flag de capacidade (`f`) no RouterInfo.

### 5.1 Requisitos para participação no Floodfill

Ao contrário dos servidores de diretório confiáveis pré-definidos no código do Tor, o conjunto de floodfill do I2P é **não confiável** e muda ao longo do tempo.

Floodfill é ativado automaticamente apenas em routers de alta largura de banda que atendem a estes requisitos: - Largura de banda compartilhada mínima de 128 KBytes/sec (configurada manualmente) - Deve passar em testes de integridade adicionais (tempo da fila de mensagens de saída, atraso de tarefas)

O opt-in automático atual resulta em aproximadamente **6% de participação floodfill na rede**.

Floodfills configurados manualmente coexistem com voluntários automáticos. Quando o número de floodfills cai abaixo do limiar, routers de alta largura de banda voluntariam-se automaticamente. Quando há floodfills em excesso, eles deixam de atuar como floodfill.

### 5.2 Papéis do floodfill

Além de aceitar armazenamentos do netDb e responder a consultas, os floodfills desempenham funções padrão de router. A maior largura de banda deles normalmente significa mais participação em tunnel, mas isso não está diretamente relacionado aos serviços de banco de dados.

---

## 6. Métrica de proximidade do Kademlia

O netDb usa medição de distância baseada em XOR **ao estilo Kademlia**. O hash SHA256 de RouterIdentity ou Destination cria a chave Kademlia (exceto para LS2 Encrypted LeaseSets, que usam SHA256 do byte de tipo 3 mais a chave pública cegada).

### 6.1 Rotação do Espaço de Chaves

Para aumentar os custos de um ataque Sybil, em vez de usar `SHA256(key)`, o sistema usa:

```
SHA256(key + yyyyMMdd)
```
onde a data é uma data UTC em ASCII de 8 bytes. Isso cria a **chave de roteamento**, que muda diariamente à meia-noite UTC—processo chamado **rotação do espaço de chaves**.

As chaves de roteamento nunca são transmitidas em mensagens I2NP; são usadas apenas para determinação de distância local.

---

## 7. Segmentação do Banco de Dados da Rede

As Kademlia DHTs (tabelas de hash distribuídas Kademlia) tradicionais não preservam a desvinculabilidade das informações armazenadas. O I2P previne ataques que associam tunnels de cliente a routers ao implementar **segmentação**.

### 7.1 Estratégia de Segmentação

Routers acompanham: - Se as entradas chegaram via tunnels do cliente ou diretamente - Se via tunnel, qual tunnel do cliente/destino - Múltiplas chegadas via tunnel são acompanhadas - Respostas de armazenamento vs. de consulta são diferenciadas

Ambas as implementações em Java e C++ utilizam: - Uma **"Main" netDb** para consultas diretas/operações de floodfill no contexto do router - **"Client Network Databases"** (Bancos de Dados de Rede do Cliente) ou **"Sub-Databases"** (Sub-bancos de dados) em contextos de cliente, capturando entradas enviadas para client tunnels

As netDbs do cliente existem apenas durante a vida útil do cliente, contendo apenas entradas de tunnel do cliente. Entradas provenientes de tunnels do cliente não podem se sobrepor a chegadas diretas.

Cada netDb rastreia se as entradas chegaram como armazenamentos (respondem a solicitações de consulta) ou como respostas de consulta (só respondem se previamente armazenadas para o mesmo destino). Os clientes nunca respondem a consultas com entradas do netDb principal, apenas com entradas do banco de dados de rede do cliente.

Estratégias combinadas **segmentam** a netDb (base de dados da rede do I2P) contra ataques de associação cliente-router.

---

## 8. Armazenamento, Verificação e Consulta

### 8.1 Armazenamento de RouterInfo (informações do router) para pares

I2NP `DatabaseStoreMessage` contendo a troca local de RouterInfo (informações do router) durante a inicialização da conexão de transporte NTCP ou SSU.

### 8.2 Armazenamento de LeaseSet para pares

Mensagens I2NP `DatabaseStoreMessage` que contêm o LeaseSet local são trocadas periodicamente por meio de mensagens cifradas com garlic encryption, agrupadas com o tráfego da Destination (destino no I2P), permitindo respostas sem consultas ao LeaseSet.

### 8.3 Seleção de Floodfill

`DatabaseStoreMessage` envia para o floodfill mais próximo da chave de roteamento atual. O floodfill mais próximo é encontrado via busca no banco de dados local. Mesmo que não seja de fato o mais próximo, o flooding (difusão por inundação) o propaga "mais perto" ao enviá-lo para vários floodfills.

O Kademlia tradicional usa uma pesquisa "find-closest" (encontrar os mais próximos) antes da inserção. Embora o I2NP careça de tais mensagens, routers podem realizar uma pesquisa iterativa com o bit menos significativo invertido (`key ^ 0x01`) para garantir a descoberta do par realmente mais próximo.

### 8.4 Armazenamento de RouterInfo nos Floodfills

Routers publicam RouterInfo (informações do router) conectando-se diretamente a um floodfill, enviando I2NP `DatabaseStoreMessage` com Reply Token (token de resposta) diferente de zero. A mensagem não é end-to-end garlic encrypted (conexão direta, sem intermediários). O floodfill responde com `DeliveryStatusMessage` usando o Reply Token como ID da mensagem.

Routers também podem enviar RouterInfo (informações do router) via tunnel exploratório (limites de conexão, incompatibilidade, ocultação de IP). Floodfills podem rejeitar tais operações de armazenamento durante sobrecarga.

### 8.5 Armazenamento de LeaseSet nos Floodfills

O armazenamento de LeaseSet é mais sensível do que o RouterInfo (informações do roteador). Routers devem impedir a associação de LeaseSet a si próprios.

Routers publicam LeaseSet via tunnel de cliente de saída `DatabaseStoreMessage` com Reply Token (token de resposta) diferente de zero. A mensagem é criptografada de ponta a ponta com garlic encryption usando o Session Key Manager (gerenciador de chaves de sessão) da Destination (destino), ocultando-a do endpoint de saída do tunnel. O floodfill responde com `DeliveryStatusMessage` retornado via tunnel de entrada.

### 8.6 Processo de inundação

Floodfills validam RouterInfo/LeaseSet antes de armazená-los localmente, usando critérios adaptativos dependentes da carga, do tamanho do netdb e de outros fatores.

Após receberem dados mais recentes válidos, os floodfills (nós especiais na I2P que mantêm e propagam dados da netDb) "flood" esses dados procurando os 3 floodfill routers mais próximos da chave de roteamento. Conexões diretas enviam um I2NP `DatabaseStoreMessage` com Reply Token igual a zero. Outros routers não respondem nem fazem re-flood.

**Restrições importantes:** - Floodfills não devem propagar via tunnels; apenas conexões diretas - Floodfills nunca propagam LeaseSet expirado ou RouterInfo (informações do router) publicado há mais de uma hora

### 8.7 Consulta de RouterInfo (informações do router) e LeaseSet

I2NP `DatabaseLookupMessage` solicita entradas do netDb aos routers floodfill. As consultas são enviadas via tunnel exploratório de saída; as respostas especificam o retorno pelo tunnel exploratório de entrada.

As consultas geralmente são enviadas para dois floodfill routers "bons" mais próximos da chave solicitada, em paralelo.

- **Correspondência local**: recebe uma resposta I2NP `DatabaseStoreMessage`
- **Sem correspondência local**: recebe uma I2NP `DatabaseSearchReplyMessage` com referências a outros floodfill routers próximos à chave

Consultas de LeaseSet usam garlic encryption de ponta a ponta (a partir da versão 0.9.5). Consultas de RouterInfo (registro de informações do router) não são criptografadas devido ao custo computacional do ElGamal, o que as torna vulneráveis à espionagem no ponto de saída.

A partir da versão 0.9.7, as respostas de consulta incluem a chave de sessão e a tag, ocultando as respostas do inbound gateway (gateway de entrada).

### 8.8 Consultas Iterativas

Pré-0.8.9: Duas consultas redundantes em paralelo, sem roteamento recursivo ou iterativo.

A partir da versão 0.8.9: **Consultas iterativas** implementadas sem redundância — mais eficientes, confiáveis e adequadas a um conhecimento de floodfill incompleto. À medida que as redes crescem e os routers conhecem menos floodfills, as consultas se aproximam da complexidade O(log n).

Buscas iterativas continuam mesmo sem referências a pares mais próximos, prevenindo black-holing (descartar silenciosamente o tráfego) malicioso. Aplicam-se a contagem máxima de consultas e o tempo limite atuais.

### 8.9 Verificação

**Verificação de RouterInfo**: Desativada a partir da versão 0.9.7.1 para impedir ataques descritos no artigo "Practical Attacks Against the I2P Network".

**Verificação do LeaseSet**: Routers aguardam ~10 segundos e então consultam um floodfill diferente via tunnel de cliente de saída. A garlic encryption de ponta a ponta oculta as informações do ponto final de saída. As respostas retornam via tunnels de entrada.

A partir da versão 0.9.7, as respostas são criptografadas de forma a ocultar a chave/tag de sessão do gateway de entrada.

### 8.10 Exploração

**Exploração** envolve uma consulta ao netdb (banco de dados da rede) com chaves aleatórias para descobrir novos routers (roteadores). Floodfills (roteadores especiais que mantêm o netdb) respondem com `DatabaseSearchReplyMessage` contendo hashes de routers não-floodfill próximos da chave solicitada. As consultas de exploração definem um sinalizador especial em `DatabaseLookupMessage`.

---

## 9. MultiHoming (múltiplas conexões a provedores/redes)

Destinations (destinos do I2P) que utilizam o mesmo par de chaves privada/pública (tradicional `eepPriv.dat`) podem hospedar em múltiplos routers simultaneamente. Cada instância publica periodicamente LeaseSets assinados; o LeaseSet publicado mais recentemente é retornado aos solicitantes de consulta. Com tempos de vida de LeaseSet de até 10 minutos, as interrupções duram no máximo ~10 minutos.

A partir da versão 0.9.38, **Meta LeaseSets** oferecem suporte a serviços multihomed em grande escala usando Destinations (endereços I2P) separados que fornecem serviços comuns. As entradas de Meta LeaseSet são Destinations ou outros Meta LeaseSets com expiração de até 18,2 horas, permitindo que centenas/milhares de Destinations hospedem serviços comuns.

---

## 10. Análise de Ameaças

Aproximadamente 1700 floodfill routers (um tipo especial de router no I2P) operam atualmente. O crescimento da rede dificulta a maioria dos ataques ou reduz seu impacto.

### 10.1 Mitigações Gerais

- **Crescimento**: Mais floodfills tornam os ataques mais difíceis ou menos impactantes
- **Redundância**: Todas as entradas do netdb são armazenadas em 3 routers floodfill mais próximos da chave via flooding (difusão em massa)
- **Assinaturas**: Todas as entradas são assinadas pelo criador; falsificações são impossíveis

### 10.2 Routers lentos ou sem resposta

Routers mantêm estatísticas ampliadas do perfil dos pares para floodfills: - Tempo médio de resposta - Percentual de respostas a consultas - Percentual de sucesso na verificação de armazenamento - Último armazenamento bem-sucedido - Última consulta bem-sucedida - Última resposta

Os routers usam essas métricas ao determinar a "qualidade" para selecionar o floodfill mais próximo. Routers que não respondem de forma alguma são rapidamente identificados e evitados; routers parcialmente maliciosos representam um desafio maior.

### 10.3 Ataque Sybil (Espaço de Chaves Completo)

Atacantes podem criar numerosos floodfill routers distribuídos por todo o espaço de chaves como um ataque de negação de serviço (DoS) eficaz.

Se o comportamento inadequado não for suficiente para a designação "bad", as possíveis respostas incluem: - Compilação de listas de hash/IP de router "bad" anunciadas via notícias do console, site, fórum - Habilitação de floodfill em toda a rede ("combater Sybil com mais Sybil") - Novas versões de software com listas "bad" hardcoded (fixas no código) - Métricas e limiares de perfis de pares aprimorados para identificação automática - Qualificação por bloco de IP, desqualificando múltiplos floodfills em um único bloco de IP - Lista de bloqueio automática baseada em subscrição (semelhante ao consenso do Tor)

Redes maiores tornam isso mais difícil.

### 10.4 Ataque Sybil (Espaço de chaves parcial)

Atacantes podem criar 8–15 floodfill routers agrupados de forma próxima no espaço de chaves. Todas as consultas/armazenamentos desse espaço de chaves são encaminhadas para os routers do atacante, possibilitando DOS (negação de serviço) em determinados sites I2P.

Como o espaço de chaves indexa hashes criptográficos SHA256, os atacantes precisam usar força bruta para gerar routers com proximidade suficiente.

**Defesa**: O algoritmo de proximidade do Kademlia varia ao longo do tempo usando `SHA256(key + YYYYMMDD)`, mudando diariamente à meia-noite UTC. Essa **rotação do espaço de chaves (keyspace)** exige a regeneração diária do ataque.

> **Observação**: Pesquisas recentes mostram que a rotação do espaço de chaves não é particularmente eficaz — atacantes podem pré-calcular hashes de router, sendo necessários apenas alguns routers para eclipsar porções do espaço de chaves em até meia hora após a rotação.

Consequência da rotação diária: o netDb distribuído fica instável por alguns minutos após a rotação—consultas falham antes que o novo router mais próximo receba as inserções.

### 10.5 Ataques de Inicialização

Atacantes poderiam assumir o controle de sites de reseed (sites que fornecem os dados iniciais da rede) ou enganar desenvolvedores a adicionar sites de reseed hostis, fazendo com que novos routers sejam inicializados em redes isoladas/controladas pela maioria.

**Defesas Implementadas:** - Obter subconjuntos de RouterInfo de múltiplos sites de reseed (processo de inicialização da rede) em vez de um único site - Monitoramento de reseed fora da rede consultando periodicamente os sites - A partir da versão 0.9.14, pacotes de dados de reseed como arquivos zip assinados, com verificação da assinatura baixada (veja [especificação su3](/docs/specs/updates))

### 10.6 Captura de Consultas

Floodfill routers podem "direcionar" pares para routers controlados pelo atacante por meio de referências retornadas.

Improvável via exploração devido à baixa frequência; routers adquirem referências de pares principalmente por meio da construção normal de tunnel.

A partir da 0.8.9, foram implementadas pesquisas iterativas. Referências de floodfill em `DatabaseSearchReplyMessage` são seguidas se estiverem mais próximas da chave da consulta. Os routers solicitantes não confiam na proximidade das referências. As consultas continuam mesmo sem chaves mais próximas até o tempo limite/número máximo de consultas, evitando black-holing malicioso (descartar silenciosamente o tráfego).

### 10.7 Vazamentos de Informação

O vazamento de informações da DHT (tabela hash distribuída) no I2P requer investigação adicional. Os floodfill routers observam consultas, coletando informações. Com 20% de nós maliciosos, as ameaças Sybil descritas anteriormente tornam-se problemáticas por vários motivos.

---

## 11. Trabalhos futuros

- Criptografia de ponta a ponta para consultas adicionais ao netDb e suas respostas
- Melhores métodos de rastreamento de respostas de consulta
- Métodos de mitigação para problemas de confiabilidade na rotação do espaço de chaves

---

## 12. Referências

- [Especificação de Estruturas Comuns](/docs/specs/common-structures/) – Estruturas RouterInfo e LeaseSet
- [Especificação do I2NP](/docs/specs/i2np/) – Tipos de mensagens de banco de dados
- [Proposta 123: Novas entradas do netDb](/proposals/123-new-netdb-entries) – Especificação do LeaseSet2
- [Discussão histórica do netDb](/docs/netdb/) – Histórico de desenvolvimento e discussões arquivadas
