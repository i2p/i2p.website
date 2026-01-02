---
title: "Formato do filtro de acesso"
description: "Sintaxe dos arquivos de filtro de controle de acesso do tunnel"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Filtros de acesso permitem aos operadores de servidores I2PTunnel autorizar, negar ou limitar conexões de entrada com base na Destination (identificador de destino no I2P) de origem e na taxa recente de conexões. O filtro é um arquivo de texto simples com regras. O arquivo é lido de cima para baixo e a **primeira regra correspondente prevalece**.

> Alterações na definição do filtro entram em vigor **na reinicialização do tunnel**. Algumas compilações podem reler listas baseadas em arquivos em tempo de execução, mas planeje uma reinicialização para garantir que as alterações sejam aplicadas.

## Formato de arquivo

- Uma regra por linha.  
- Linhas em branco são ignoradas.  
- `#` inicia um comentário que vai até o fim da linha.  
- As regras são avaliadas em ordem; a primeira correspondência é usada.

## Limiares

Um **limiar** define quantas tentativas de conexão de uma única Destination (identificador de destino no I2P) são permitidas em uma janela de tempo móvel.

- **Numérico:** `N/S` significa permitir `N` conexões a cada `S` segundos. Exemplo: `15/5` permite até 15 conexões a cada 5 segundos. A tentativa `N+1` dentro da janela é rejeitada.  
- **Palavras-chave:** `allow` significa sem limite. `deny` significa sempre rejeitar.

## Sintaxe de regras

As regras têm o seguinte formato:

```
<threshold> <scope> <target>
```
Onde:

- `<threshold>` é `N/S`, `allow` ou `deny`  
- `<scope>` é um dentre `default`, `explicit`, `file` ou `record` (veja abaixo)  
- `<target>` depende do escopo

### Regra padrão

Aplica-se quando nenhuma outra regra corresponde. Apenas **uma** regra padrão é permitida. Se omitida, Destinos desconhecidos são permitidos sem restrições.

```
15/5 default
allow default
deny default
```
### Regra explícita

Aponta para um Destino específico pelo endereço Base32 (por exemplo `example1.b32.i2p`) ou pela chave completa.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Regra baseada em arquivo

Aplica-se a **todos** os Destinos listados em um arquivo externo. Cada linha contém um Destino; comentários iniciados por `#` e linhas em branco são permitidos.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> Nota operacional: Algumas implementações releem listas de arquivos periodicamente. Se você editar uma lista enquanto o tunnel estiver em execução, espere um pequeno atraso até que as alterações sejam detectadas. Reinicie para aplicar imediatamente.

### Gravador (controle progressivo)

Um **recorder** (registrador) monitora tentativas de conexão e grava em um arquivo os Destinos que excedem um limite. Você pode então referenciar esse arquivo em uma regra `file` para aplicar limitações ou bloqueios a tentativas futuras.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Verifique o suporte ao gravador no seu build antes de depender dele. Use listas `file` para um comportamento garantido.

## Ordem de avaliação

Coloque as regras específicas primeiro, depois as gerais. Um padrão comum:

1. Permissões explícitas para pares confiáveis  
2. Negações explícitas para abusadores conhecidos  
3. Listas de permissão/bloqueio baseadas em arquivos
4. Registradores para limitação progressiva
5. Regra padrão para cobrir todos os casos

## Exemplo completo

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Notas de implementação

- O filtro de acesso opera na camada de tunnel, antes do tratamento pela aplicação, para que o tráfego abusivo possa ser rejeitado logo no início.  
- Coloque o arquivo de filtro no seu diretório de configuração do I2PTunnel e reinicie o tunnel para aplicar as alterações.  
- Compartilhe listas baseadas em arquivo entre vários tunnels se quiser uma política consistente entre serviços.
