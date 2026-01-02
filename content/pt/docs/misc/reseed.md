---
title: "Hosts de Reseed (inicialização da rede)"
description: "Operando serviços de reseed (semeadura inicial da rede) e métodos alternativos de bootstrap (inicialização)"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Sobre os hosts de reseed

Novos routers precisam de um pequeno número de pares para entrar na rede I2P. Os hosts de reseed (reseed: processo de obter um conjunto inicial de pares para iniciar ou recuperar a participação na rede) fornecem esse conjunto inicial por meio de downloads HTTPS criptografados. Cada pacote de reseed é assinado pelo host, evitando adulterações por partes não autenticadas. Routers já estabelecidos podem, ocasionalmente, fazer reseed se seu conjunto de pares ficar desatualizado.

### Processo de Inicialização da Rede

Quando um router I2P é iniciado pela primeira vez ou fica offline por um período prolongado, ele precisa de dados RouterInfo para se conectar à rede. Como o router não tem pares existentes, ele não pode obter essas informações a partir da própria rede I2P. O mecanismo de reseed (mecanismo de inicialização) resolve esse problema de inicialização ao fornecer arquivos RouterInfo provenientes de servidores HTTPS externos confiáveis.

O processo de reseed (inicialização da rede) entrega de 75 a 100 arquivos RouterInfo em um único pacote assinado criptograficamente. Isso garante que novos routers possam estabelecer conexões rapidamente sem expô-los a ataques man-in-the-middle que poderiam isolá-los em partições de rede separadas e não confiáveis.

### Estado atual da rede

Em outubro de 2025, a rede I2P opera com a versão 2.10.0 do router (versão da API 0.9.67). O protocolo de reseed (processo de obtenção inicial de pares) introduzido na versão 0.9.14 permanece estável e inalterado em sua funcionalidade central. A rede mantém múltiplos servidores de reseed independentes distribuídos globalmente para garantir disponibilidade e resistência à censura.

O serviço [checki2p](https://checki2p.com/reseed) monitora todos os servidores de reseed do I2P a cada 4 horas, fornecendo verificações de status em tempo real e métricas de disponibilidade para a infraestrutura de reseed.

## Especificação do Formato de Arquivo SU3

O formato de arquivo SU3 é a base do protocolo de reseed (inicialização de pares da rede) do I2P, proporcionando entrega de conteúdo assinada criptograficamente. Compreender este formato é essencial para implementar servidores e clientes de reseed.

### Estrutura de arquivos

O formato SU3 consiste em três componentes principais: cabeçalho (40+ bytes), conteúdo (tamanho variável) e assinatura (tamanho especificado no cabeçalho).

#### Formato do cabeçalho (mínimo: Bytes 0-39)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Parâmetros SU3 Específicos de Reseed

Para pacotes de reseed (inicialização/obtenção inicial de pares), o arquivo SU3 deve ter as seguintes características:

- **Nome do arquivo**: Deve ser exatamente `i2pseeds.su3`
- **Tipo de Conteúdo** (byte 27): 0x03 (RESEED)
- **Tipo de Arquivo** (byte 25): 0x00 (ZIP)
- **Tipo de Assinatura** (bytes 8-9): 0x0006 (RSA-4096-SHA512)
- **String de Versão**: Carimbo de data/hora Unix em ASCII (segundos desde a época, formato date +%s)
- **ID do Signatário**: Identificador no estilo de e-mail correspondente ao CN do certificado X.509

#### Parâmetro de consulta do ID da rede

Desde a versão 0.9.42, routers acrescentam `?netid=2` às solicitações de reseed (processo de inicialização/obtenção inicial de pares). Isso impede conexões entre redes, pois redes de teste usam IDs de rede diferentes. A rede de produção atual do I2P usa o ID de rede 2.

Exemplo de solicitação: `https://reseed.example.com/i2pseeds.su3?netid=2`

### Estrutura do conteúdo do ZIP

A seção de conteúdo (após o cabeçalho, antes da assinatura) contém um arquivo ZIP padrão com os seguintes requisitos:

- **Compressão**: Compressão ZIP padrão (DEFLATE)
- **Contagem de arquivos**: Normalmente 75-100 arquivos RouterInfo (informações do router)
- **Estrutura de diretórios**: Todos os arquivos devem estar no nível superior (sem subdiretórios)
- **Nomenclatura de arquivos**: `routerInfo-{44-character-base64-hash}.dat`
- **Alfabeto Base64**: Deve usar o alfabeto base64 modificado do I2P

O alfabeto base64 do I2P difere do base64 padrão ao usar `-` e `~` em vez de `+` e `/` para garantir compatibilidade com sistemas de arquivos e URLs.

### Assinatura criptográfica

A assinatura abrange o arquivo inteiro, do byte 0 até o final da seção de conteúdo. A própria assinatura é anexada após o conteúdo.

#### Algoritmo de Assinatura (RSA-4096-SHA512)

1. Calcule o hash SHA-512 dos bytes 0 até o final do conteúdo
2. Assine o hash usando RSA "raw" (NONEwithRSA na terminologia do Java)
3. Preencha a assinatura com zeros à esquerda, se necessário, até atingir 512 bytes
4. Anexe a assinatura de 512 bytes ao arquivo

#### Processo de Verificação de Assinatura

Os clientes devem:

1. Ler os bytes 0-11 para determinar o tipo e o tamanho da assinatura
2. Ler todo o cabeçalho para localizar os limites do conteúdo
3. Fazer streaming do conteúdo enquanto calcula o hash SHA-512
4. Extrair a assinatura do final do arquivo
5. Verificar a assinatura usando a chave pública RSA-4096 do signatário
6. Rejeitar o arquivo se a verificação da assinatura falhar

### Modelo de Confiança de Certificados

As chaves de assinatura de reseed (processo de bootstrap para obter peers iniciais) são distribuídas na forma de certificados X.509 autoassinados com chaves RSA-4096. Esses certificados estão incluídos nos pacotes do router I2P no diretório `certificates/reseed/`.

Formato do certificado: - **Tipo de chave**: RSA-4096 - **Assinatura**: autossinada - **CN do Sujeito**: Deve corresponder ao ID do signatário no cabeçalho SU3 - **Datas de validade**: Os clientes devem respeitar os períodos de validade do certificado

## Operando um servidor Reseed (servidor de bootstrap da rede I2P)

Operar um serviço de reseed (processo de bootstrap para novos routers) exige atenção cuidadosa à segurança, confiabilidade e requisitos de diversidade da rede. Mais hosts de reseed independentes aumentam a resiliência e dificultam que atacantes ou censores bloqueiem a entrada de novos routers.

### Requisitos técnicos

#### Especificações do Servidor

- **Sistema Operacional**: Unix/Linux (Ubuntu, Debian, FreeBSD testados e recomendados)
- **Conectividade**: Endereço IPv4 estático obrigatório, IPv6 recomendado mas opcional
- **CPU**: No mínimo 2 núcleos
- **RAM**: No mínimo 2 GB
- **Largura de banda**: Aproximadamente 15 GB por mês
- **Tempo de atividade**: Operação 24/7 requerida
- **I2P Router**: I2P router bem integrado em execução contínua

#### Requisitos de Software

- **Java**: JDK 8 ou posterior (Java 17+ será obrigatório a partir do I2P 2.11.0)
- **Servidor Web**: nginx ou Apache com suporte a proxy reverso (Lighttpd não é mais suportado devido a limitações do cabeçalho X-Forwarded-For)
- **TLS/SSL**: Certificado TLS válido (Let's Encrypt, autoassinado ou autoridade certificadora comercial)
- **Proteção contra DDoS**: fail2ban ou equivalente (obrigatório, não opcional)
- **Ferramentas de Reseed (processo de bootstrap da rede)**: reseed-tools oficiais de https://i2pgit.org/idk/reseed-tools

### Requisitos de Segurança

#### Configuração de HTTPS/TLS

- **Protocolo**: Somente HTTPS, sem fallback para HTTP
- **Versão do TLS**: No mínimo TLS 1.2
- **Suítes de cifras**: Devem suportar cifras fortes compatíveis com Java 8+
- **CN/SAN do certificado**: Deve corresponder ao nome do host da URL servida
- **Tipo de certificado**: Pode ser autoassinado se comunicado à equipe de desenvolvimento, ou emitido por uma autoridade certificadora reconhecida (CA)

#### Gerenciamento de Certificados

Certificados de assinatura SU3 e certificados TLS têm finalidades diferentes:

- **Certificado TLS** (`certificates/ssl/`): Protege o transporte HTTPS
- **Certificado de Assinatura SU3** (`certificates/reseed/`): Assina pacotes de reseed

Ambos os certificados devem ser fornecidos ao reseed coordinator (zzz@mail.i2p) (coordenador do processo de inicialização da rede) para inclusão nos pacotes do router.

#### Proteção contra DDoS e raspagem de dados

Servidores Reseed (servidores de provisionamento inicial) enfrentam ataques periódicos provenientes de implementações com bugs, botnets e atores maliciosos que tentam raspar o netDb (banco de dados da rede). As medidas de proteção incluem:

- **fail2ban**: Necessário para limitação de taxa e mitigação de ataques
- **Diversidade de Conjuntos**: Entregar conjuntos diferentes de RouterInfo a solicitantes diferentes
- **Consistência do Conjunto**: Entregar o mesmo conjunto para solicitações repetidas do mesmo IP dentro de uma janela de tempo configurável
- **Restrições de registro de IP**: Não divulgar logs ou endereços IP (requisito da política de privacidade)

### Métodos de Implementação

#### Método 1: reseed-tools oficial (Recomendado)

A implementação canônica mantida pelo projeto I2P. Repositório: https://i2pgit.org/idk/reseed-tools

**Instalação**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
Na primeira execução, a ferramenta gerará: - `your-email@mail.i2p.crt` (certificado de assinatura SU3) - `your-email@mail.i2p.pem` (chave privada de assinatura SU3) - `your-email@mail.i2p.crl` (lista de revogação de certificados) - arquivos de certificado e chave TLS

**Recursos**: - Geração automática de pacotes SU3 (350 variações, 77 RouterInfos (objetos de informação do router) cada) - Servidor HTTPS integrado - Reconstrói o cache a cada 9 horas via cron - Suporte ao cabeçalho X-Forwarded-For com a flag `--trustProxy` - Compatível com configurações de proxy reverso

**Implantação em Produção**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Método 2: Implementação em Python (pyseeder)

Implementação alternativa do projeto PurpleI2P: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Método 3: Implantação com Docker

Para ambientes em contêineres, existem várias implementações prontas para Docker:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Adiciona serviço onion do Tor e suporte a IPFS

### Configuração de proxy reverso

#### Configuração do nginx

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Configuração do Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Registro e Coordenação

Para incluir seu servidor de reseed (processo de inicialização da rede) no pacote oficial do I2P:

1. Conclua a configuração e os testes
2. Envie ambos os certificados (SU3 signing (assinatura SU3) e TLS) ao reseed coordinator (coordenador de reseed)
3. Contato: zzz@mail.i2p ou zzz@i2pmail.org
4. Junte-se a #i2p-dev no IRC2P para coordenação com outros operadores

### Melhores Práticas Operacionais

#### Monitoramento e Registro em Log

- Ativar o formato de log combinado do Apache/nginx para estatísticas
- Implementar rotação de logs (os logs crescem rapidamente)
- Monitorar o sucesso da geração de bundle (pacote) e os tempos de reconstrução
- Acompanhar o uso de largura de banda e os padrões de solicitações
- Nunca divulgar endereços IP ou logs de acesso detalhados

#### Cronograma de Manutenção

- **A cada 9 horas**: Reconstruir o cache de bundles SU3 (automatizado via cron)
- **Semanalmente**: Revisar os logs em busca de padrões de ataque
- **Mensalmente**: Atualizar o I2P router e reseed-tools (ferramentas de resemeadura)
- **Conforme necessário**: Renovar certificados TLS (automatizar com Let's Encrypt)

#### Seleção de portas

- Padrão: 8443 (recomendado)
- Alternativa: Qualquer porta entre 1024-49151
- Porta 443: Requer privilégios de root ou redirecionamento de portas (iptables redirect recomendado)

Exemplo de redirecionamento de portas:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Métodos alternativos de Reseed

Outras opções de bootstrap (inicialização) ajudam usuários em redes restritivas:

### Reseed Baseado em Arquivo

Introduzido na versão 0.9.16, o reseeding baseado em arquivos (procedimento de bootstrap/obtenção inicial de pares) permite que os usuários carreguem manualmente pacotes de RouterInfo. Esse método é particularmente útil para usuários em regiões censuradas onde os servidores de reseed HTTPS estão bloqueados.

**Processo**: 1. Um contato confiável gera um pacote SU3 usando seu router 2. O pacote é transferido por e-mail, unidade USB ou outro canal fora de banda 3. O usuário coloca `i2pseeds.su3` no diretório de configuração do I2P 4. O router detecta e processa automaticamente o pacote ao reiniciar

**Documentação**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Casos de uso**: - Usuários por trás de firewalls nacionais que bloqueiam reseed servers (servidores de bootstrap) - Redes isoladas que exigem inicialização manual - Ambientes de teste e desenvolvimento

### Reseeding (processo de inicialização para obter pares da rede) com proxy do Cloudflare

Encaminhar o tráfego de reseed (processo de inicialização da rede) pela CDN da Cloudflare oferece várias vantagens para operadores em regiões de alta censura.

**Benefícios**: - Endereço IP do servidor de origem oculto dos clientes - Proteção contra DDoS via infraestrutura da Cloudflare - Distribuição geográfica de carga via cache na borda - Desempenho aprimorado para clientes globais

**Requisitos de Implementação**: - parâmetro `--trustProxy` ativado no reseed-tools - proxy da Cloudflare ativado para o registro DNS - Tratamento adequado do cabeçalho X-Forwarded-For

**Considerações importantes**: - As restrições de portas da Cloudflare se aplicam (é necessário usar portas suportadas) - Same-client bundle consistency (consistência do agrupamento para o mesmo cliente) exige suporte a X-Forwarded-For - Configuração de SSL/TLS gerenciada pela Cloudflare

**Documentação**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Estratégias resistentes à censura

A pesquisa de Nguyen Phong Hoang (USENIX FOCI 2019) identifica métodos adicionais de inicialização para redes censuradas:

#### Provedores de Armazenamento em Nuvem

- **Box, Dropbox, Google Drive, OneDrive**: Hospedar arquivos SU3 em links públicos
- **Vantagem**: Difícil de bloquear sem interromper serviços legítimos
- **Limitação**: Requer distribuição manual de URLs para os usuários

#### Distribuição via IPFS

- Hospedar pacotes de reseed (obtenção inicial de pares para se conectar à rede) no InterPlanetary File System
- Armazenamento endereçado por conteúdo impede adulterações
- Resiliente a tentativas de remoção

#### Serviços Onion do Tor

- Reseed servers (servidores que fornecem pares iniciais para iniciar a participação na rede) acessíveis via endereços .onion
- Resistente ao bloqueio baseado em IP
- Requer cliente Tor no sistema do usuário

**Documentação de pesquisa**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Países com bloqueio conhecido do I2P

Em 2025, há confirmação de que os seguintes países bloqueiam I2P reseed servers (servidores usados para inicializar o I2P): - China - Irã - Omã - Catar - Kuwait

Os usuários nessas regiões devem utilizar métodos alternativos de bootstrap ou estratégias de reseed resistentes à censura.

## Detalhes do Protocolo para Implementadores

### Especificação da Solicitação de Reseed (processo de obtenção inicial de pares)

#### Comportamento do Cliente

1. **Seleção do servidor**: Router mantém uma lista codificada de forma fixa de URLs de reseed (processo de inicialização/obtenção de pares do I2P)
2. **Seleção aleatória**: O cliente seleciona aleatoriamente um servidor da lista disponível
3. **Formato da requisição**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Deve imitar navegadores comuns (por exemplo, "Wget/1.11.4")
5. **Lógica de nova tentativa**: Se a requisição SU3 falhar, usar como alternativa a análise da página índice
6. **Validação de certificado**: Verificar o certificado TLS contra o repositório de confiança do sistema
7. **Validação da assinatura SU3**: Verificar a assinatura em relação aos certificados de reseed conhecidos

#### Comportamento do Servidor

1. **Seleção do conjunto**: Selecionar subconjunto pseudoaleatório de RouterInfos (registros de metadados de router no I2P) do netDb
2. **Rastreamento do cliente**: Identificar solicitações pelo IP de origem (respeitando X-Forwarded-For)
3. **Consistência do conjunto**: Retornar o mesmo conjunto para solicitações repetidas dentro de uma janela de tempo (tipicamente 8-12 horas)
4. **Diversidade de conjuntos**: Retornar conjuntos diferentes para clientes diferentes para diversidade de rede
5. **Content-Type**: `application/octet-stream` ou `application/x-i2p-reseed`

### Formato do arquivo RouterInfo

Cada arquivo `.dat` no reseed bundle (pacote de reseed usado para inicialização) contém uma estrutura RouterInfo:

**Nomenclatura de arquivos**: `routerInfo-{base64-hash}.dat` - O hash tem 44 caracteres usando o alfabeto base64 do I2P - Exemplo: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Conteúdo do arquivo**: - RouterIdentity (hash do router, chave de criptografia, chave de assinatura) - Carimbo de data e hora da publicação - Endereços do router (IP, porta, tipo de transporte) - Capacidades e opções do router - Assinatura que cobre todos os dados acima

### Requisitos de Diversidade da Rede

Para evitar a centralização da rede e permitir a detecção de Sybil attack (ataque Sybil, em que um adversário cria múltiplas identidades falsas):

- **Sem dumps completos do NetDb**: Nunca forneça todas as RouterInfos (informações de roteadores) a um único cliente
- **Amostragem aleatória**: Cada lote contém um subconjunto diferente dos pares disponíveis
- **Tamanho mínimo do lote**: 75 RouterInfos (aumentado em relação aos 50 originais)
- **Tamanho máximo do lote**: 100 RouterInfos
- **Atualidade**: As RouterInfos devem ser recentes (em até 24 horas de sua geração)

### Considerações sobre IPv6

**Status atual** (2025): - Vários servidores de reseed não respondem via IPv6 - Os clientes devem preferir ou forçar IPv4 para maior confiabilidade - O suporte a IPv6 é recomendado para novas implantações, mas não é crítico

**Nota de Implementação**: Ao configurar servidores dual-stack (dupla pilha), garanta que os endereços de escuta IPv4 e IPv6 funcionem corretamente, ou desative o IPv6 se ele não puder ser suportado adequadamente.

## Considerações de Segurança

### Modelo de Ameaças

O protocolo de reseed protege contra:

1. **Ataques Man-in-the-Middle (ataque de intermediário)**: Assinaturas RSA-4096 impedem a adulteração do pacote
2. **Particionamento da rede**: Múltiplos servidores de reseed (servidores de inicialização) independentes evitam um único ponto de controle
3. **Ataques Sybil (múltiplas identidades falsas)**: A diversidade de pacotes limita a capacidade do atacante de isolar usuários
4. **Censura**: Múltiplos servidores e métodos alternativos fornecem redundância

O protocolo de reseed (processo de inicialização do netDb) NÃO defende contra:

1. **Reseed servers comprometidos (servidores de bootstrap da rede)**: Se o atacante controla as chaves privadas dos certificados de reseed
2. **Bloqueio completo da rede**: Se todos os métodos de reseed estiverem bloqueados em uma região
3. **Monitoramento de longo prazo**: Solicitações de reseed revelam o endereço IP que tenta ingressar no I2P

### Gerenciamento de Certificados

**Segurança de Chaves Privadas**: - Armazene as chaves de assinatura SU3 offline quando não estiverem em uso - Use senhas fortes para a criptografia das chaves - Mantenha backups seguros das chaves e certificados - Considere módulos de segurança de hardware (HSMs) para implantações de alto valor

**Revogação de Certificados**: - Listas de Revogação de Certificados (CRLs) distribuídas via feed de notícias - Certificados comprometidos podem ser revogados pelo coordenador - Routers atualizam automaticamente as CRLs com as atualizações de software

### Mitigação de Ataques

**Proteção contra DDoS**: - regras do fail2ban para solicitações excessivas - Limitação de taxa no nível do servidor web - Limites de conexão por endereço IP - Cloudflare ou CDN semelhante para camada adicional

**Prevenção de scraping (raspagem automatizada de dados)**: - Pacotes diferentes por IP solicitante - Armazenamento em cache de pacotes baseado no tempo por IP - Registro de padrões que indiquem tentativas de scraping - Coordenação com outros operadores sobre ataques detectados

## Testes e Validação

### Testando seu servidor de reseed (inicialização da rede)

#### Método 1: Instalação Limpa do Router

1. Instale o I2P em um sistema limpo
2. Adicione sua URL de reseed (obtenção inicial de pares da rede) à configuração
3. Remova ou desative outras URLs de reseed
4. Inicie o router e monitore os logs para confirmar o reseed bem-sucedido
5. Verifique a conexão com a rede em até 5-10 minutos

Saída de log esperada:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Método 2: Validação Manual de SU3

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Método 3: monitoramento do checki2p

O serviço em https://checki2p.com/reseed realiza verificações automatizadas a cada 4 horas em todos os servidores de reseed do I2P (processo de inicialização da rede para obter pares inicialmente). Isso fornece:

- Monitoramento de disponibilidade
- Métricas de tempo de resposta
- Validação de certificado TLS
- Verificação da assinatura SU3
- Dados históricos de tempo de atividade

Assim que o seu reseed (servidor de inicialização) for registrado junto ao projeto I2P, ele aparecerá automaticamente no checki2p dentro de 24 horas.

### Solução de problemas comuns

**Problema**: "Unable to read signing key" na primeira execução - **Solução**: Isso é esperado. Responda 'y' para gerar novas chaves.

**Problema**: router não consegue verificar a assinatura - **Causa**: certificado não está no repositório de confiança do router - **Solução**: coloque o certificado no diretório `~/.i2p/certificates/reseed/`

**Problema**: Mesmo bundle entregue a clientes diferentes - **Causa**: Cabeçalho X-Forwarded-For não encaminhado corretamente - **Solução**: Ative `--trustProxy` e configure os cabeçalhos do proxy reverso

**Problema**: erros "Connection refused" - **Causa**: porta não acessível a partir da Internet - **Solução**: verifique as regras do firewall, verifique o encaminhamento de portas

**Problema**: Uso elevado de CPU durante a reconstrução do bundle - **Causa**: Comportamento normal ao gerar mais de 350 variações de SU3 (formato de atualização assinado do I2P) - **Solução**: Garanta recursos de CPU adequados, considere reduzir a frequência de reconstrução

## Informações de referência

### Documentação Oficial

- **Guia de Contribuidores do Reseed (inicialização do netDb do I2P)**: /guides/creating-and-running-an-i2p-reseed-server/
- **Requisitos da Política de Reseed**: /guides/reseed-policy/
- **Especificação SU3**: /docs/specs/updates/
- **Repositório das Ferramentas de Reseed**: https://i2pgit.org/idk/reseed-tools
- **Documentação das Ferramentas de Reseed**: https://eyedeekay.github.io/reseed-tools/

### Implementações alternativas

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Reseeder WSGI em Python (servidor de distribuição inicial de pares)**: https://github.com/torbjo/i2p-reseeder

### Recursos da Comunidade

- **Fórum I2P**: https://i2pforum.net/
- **Repositório Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev no IRC2P
- **Monitoramento de Status**: https://checki2p.com/reseed

### Histórico de versões

- **0.9.14** (2014): Formato de reseed SU3 introduzido
- **0.9.16** (2014): Reseeding baseado em arquivos adicionado
- **0.9.42** (2019): Exigência do parâmetro de consulta Network ID
- **2.0.0** (2022): Protocolo de transporte SSU2 introduzido
- **2.4.0** (2024): Melhorias de isolamento e segurança do NetDB
- **2.6.0** (2024): Conexões I2P-over-Tor bloqueadas
- **2.10.0** (2025): Versão estável atual (em setembro de 2025)

### Referência dos Tipos de Assinatura

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Padrão de Reseed**: Tipo 6 (RSA-SHA512-4096) é obrigatório para pacotes de reseed.

## Apreço

Agradecemos a todos os reseed operators (operadores que fornecem os dados iniciais para a rede) por manterem a rede acessível e resiliente. Reconhecimento especial aos seguintes colaboradores e projetos:

- **zzz**: Desenvolvedor do I2P de longa data e coordenador de reseed (processo de inicialização do I2P para começar a se conectar à rede)
- **idk**: Mantenedor atual do reseed-tools e responsável pelos lançamentos
- **Nguyen Phong Hoang**: Pesquisa sobre estratégias de reseed resistentes à censura
- **Equipe PurpleI2P**: Implementações alternativas do I2P e ferramentas
- **checki2p**: Serviço automatizado de monitoramento da infraestrutura de reseed

A infraestrutura descentralizada de reseed (processo inicial de descoberta de pares) da rede I2P representa um esforço colaborativo de dezenas de operadores em todo o mundo, garantindo que novos usuários possam sempre encontrar um caminho para ingressar na rede, independentemente da censura local ou de barreiras técnicas.
