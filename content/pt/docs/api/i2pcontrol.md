---
title: "I2PControl JSON-RPC"
description: "API de gerenciamento remoto de router via webapp I2PControl"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# Documentação da API I2PControl

-------------verificar adicionar coisas--------------

I2PControl é uma API **JSON-RPC 2.0** incluída com o router I2P (desde a versão 0.9.39). Ela permite monitoramento autenticado e controle do router através de requisições JSON estruturadas.

> **Senha padrão:** `itoopie` — esta é a senha padrão de fábrica e **deve ser alterada** imediatamente por segurança.

## 1. Visão Geral e Acesso

| Implementação              | Endpoint Padrão                  | Protocolo | Habilitado por Padrão                          | Observações            |
|----------------------------|----------------------------------|-----------|------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/` | HTTP      | ❌ Deve ser habilitado via WebApps (Console do Roteador) | Aplicativo web incluso |
| i2pd (implementação C++)   | `https://127.0.0.1:7650/`        | HTTPS     | ✅ Habilitado por padrão                         | Comportamento de plugin legado |
---

No caso do Java I2P, você deve ir para **Router Console → WebApps → I2PControl** e habilitá-lo (configurar para iniciar automaticamente). Uma vez ativo, todos os métodos exigem que você primeiro se autentique e receba um token de sessão.

## 2. Formato JSON-RPC

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
Todas as requisições seguem a estrutura JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Uma resposta bem-sucedida inclui um campo `result`; em caso de falha, um objeto `error` é retornado:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
ou

## 3. Fluxo de Autenticação

### Solicitação (Autenticar)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### Resposta Bem-sucedida

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| Campo      | Direção   | Tipo   | Descrição                                                  |
|------------|-----------|--------|------------------------------------------------------------|
| `API`      | Solicitação | long   | Versão da API I2PControl solicitada pelo cliente. Use `1`. |
| `Password` | Solicitação | String | Senha usada para autenticar com o I2PControl.              |
| `API`      | Resposta  | long   | Versão principal da API implementada pelo servidor.        |
| `Token`    | Resposta  | String | Token de autenticação usado em solicitações subsequentes.  |
---

Você deve incluir esse `Token` em todas as solicitações subsequentes nos `params`.

## 4. Métodos e Endpoints

### 4.1 RouterInfo

---

Obtém telemetria chave sobre o router.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemplo de Requisição**

#### Enumeração de Código de Status (`i2p.router.net.status`)

| Chave                                    | Tipo   | Descrição                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | String | Status do roteador em formato livre e traduzido, destinado à exibição.             |
| `i2p.router.uptime`                    | long   | Tempo de atividade do roteador em milissegundos. Versões mais antigas do i2pd podem retornar uma string. |
| `i2p.router.version`                   | String | Versão completa do roteador.                                                    |
| `i2p.router.net.status`                | long   | Código de status da rede; veja a tabela abaixo.                               |
| `i2p.router.net.bw.inbound.1s`         | double | Largura de banda de entrada atual em bytes por segundo.                          |
| `i2p.router.net.bw.inbound.15s`        | double | Média de largura de banda de entrada nos últimos 15 segundos em bytes por segundo.                |
| `i2p.router.net.bw.outbound.1s`        | double | Largura de banda de saída atual em bytes por segundo.                         |
| `i2p.router.net.bw.outbound.15s`       | double | Média de largura de banda de saída nos últimos 15 segundos em bytes por segundo.               |
| `i2p.router.net.tunnels.participating` | long   | Número de túneis nos quais este roteador está participando.                |
#### Enumeração de Código de Status (`i2p.router.net.status`)

| Código | Significado                                          |
|--------|-----------------------------------------------------|
| 0      | OK                                                  |
| 1      | TESTANDO                                            |
| 2      | BLOQUEADO POR FIREWALL                              |
| 3      | OCULTO                                              |
| 4      | AVISO_BLOQUEADO_POR_FIREWALL_E_RÁPIDO               |
| 5      | AVISO_BLOQUEADO_POR_FIREWALL_E_FLOODFILL            |
| 6      | AVISO_BLOQUEADO_POR_FIREWALL_COM_TCP_DE_ENTRADA     |
| 7      | AVISO_BLOQUEADO_POR_FIREWALL_COM_UDP_DESATIVADO     |
| 8      | ERRO_I2CP                                           |
| 9      | ERRO_DESINCRONIA_DE_RELOGIO                         |
| 10     | ERRO_ENDEREÇO_TCP_PRIVADO                           |
| 11     | ERRO_NAT_SIMÉTRICO                                  |
| 12     | ERRO_PORTA_UDP_EM_USO                               |
| 13     | ERRO_SEM_PARES_ATIVOS_VERIFIQUE_CONEXÃO_E_FIREWALL  |
| 14     | ERRO_UDP_DESATIVADO_E_TCP_NÃO_CONFIGURADO           |
#### Campos do NetDB e do Par

| Chave                                  | Tipo    | Descrição                                        |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | Número de pares conhecidos, excluindo o roteador local. |
| `i2p.router.netdb.activepeers`       | long    | Número de pares ativos.                            |
| `i2p.router.netdb.fastpeers`         | long    | Número de pares classificados como rápidos.                |
| `i2p.router.netdb.highcapacitypeers` | long    | Número de pares classificados como alta capacidade.       |
| `i2p.router.netdb.isreseeding`       | boolean | Indica se um reseed está em andamento.                   |
**Campos de Resposta (result)**   De acordo com a documentação oficial (GetI2P):   - `i2p.router.status` (String) — um status legível para humanos   - `i2p.router.uptime` (long) — milissegundos (ou string para i2pd mais antigo) :contentReference[oaicite:0]{index=0}   - `i2p.router.version` (String) — string de versão :contentReference[oaicite:1]{index=1}   - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — largura de banda de entrada em B/s :contentReference[oaicite:2]{index=2}   - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — largura de banda de saída em B/s :contentReference[oaicite:3]{index=3}   - `i2p.router.net.status` (long) — código de status numérico (ver enum abaixo) :contentReference[oaicite:4]{index=4}   - `i2p.router.net.tunnels.participating` (long) — número de tunnels participantes :contentReference[oaicite:5]{index=5}   - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — estatísticas de peers do netDB :contentReference[oaicite:6]{index=6}   - `i2p.router.netdb.isreseeding` (boolean) — se o reseed está ativo :contentReference[oaicite:7]{index=7}   - `i2p.router.netdb.knownpeers` (long) — total de peers conhecidos :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Parâmetro | Tipo   | Descrição                     |
|-----------|--------|-------------------------------|
| `Stat`    | String | Nome do RateStat do roteador. |
| `Period`  | long   | Período de taxa em milissegundos. |
Usado para buscar métricas de taxa (por exemplo, largura de banda, sucesso do tunnel) ao longo de uma janela de tempo determinada.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemplo de Solicitação**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Resposta de Exemplo**

### 4.3 RouterManager

---

| Parâmetro          | Resultado           | Descrição                                                           |
|--------------------|---------------------|---------------------------------------------------------------------|
| `Restart`          | null                | Inicia uma reinicialização imediata do roteador.                   |
| `RestartGraceful`  | null                | Reinicia após os túneis participantes expirarem.                   |
| `Shutdown`         | null                | Inicia uma desativação imediata do roteador.                       |
| `ShutdownGraceful` | null                | Desativa após os túneis participantes expirarem.                   |
| `Reseed`           | null                | Inicia um reseed do roteador.                                      |
| `FindUpdates`      | boolean ou String   | Bloqueante. Procura por uma atualização assinada do roteador.      |
| `Update`           | String              | Bloqueante. Inicia uma atualização assinada do roteador e retorna seu status final. |
Executar ações administrativas.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Parâmetros / métodos permitidos**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**Exemplo de Solicitação**

### 4.4 NetworkSetting

**Resposta de Sucesso**

---

| Chave                             | Valor Aceito                                      | Descrição                                                  |
|---------------------------------|---------------------------------------------------|------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | String, 1–65535                                   | Porta NTCP; uma alteração exige reinicialização.          |
| `i2p.router.net.ntcp.hostname`  | String                                            | Nome de host NTCP; uma alteração exige reinicialização.   |
| `i2p.router.net.ntcp.autoip`    | `always`, `true` ou `false`                       | Seleção automática de endereço NTCP.                      |
| `i2p.router.net.ssu.port`       | String, 1–65535                                   | Porta SSU; uma alteração exige reinicialização.           |
| `i2p.router.net.ssu.hostname`   | String                                            | Nome de host externo SSU; uma alteração exige reinicialização. |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu` ou `local,upnp,ssu` | Fontes de descoberta de endereço SSU.                     |
| `i2p.router.net.ssu.detectedip` | null                                              | Endereço SSU detectado (somente leitura).                 |
| `i2p.router.net.upnp`           | String                                            | Configuração UPnP.                                        |
| `i2p.router.net.bw.share`       | String, 0–100                                     | Porcentagem de largura de banda disponível para túneis participantes. |
| `i2p.router.net.bw.in`          | String de inteiro não negativo                   | Limite de largura de banda de entrada em KiB/s.           |
| `i2p.router.net.bw.out`         | String de inteiro não negativo                   | Limite de largura de banda de saída em KiB/s.             |
| `i2p.router.net.laptopmode`     | String                                            | Configuração de modo laptop.                              |
Obter ou definir parâmetros de configuração da rede (portas, upnp, compartilhamento de largura de banda, etc.)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemplo de Requisição (obter valores atuais)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**Resposta de Exemplo**

> Nota: versões do i2pd anteriores à 2.41 podem retornar tipos numéricos em vez de strings — os clientes devem lidar com ambos. :contentReference[oaicite:11]{index=11}

### 4.5 Configurações Avançadas

---

| Parâmetro | Tipo                | Descrição                                                           |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | String              | Retorna uma configuração dentro de um objeto resultado `get`.       |
| `getAll`  | n/a                 | Retorna o mapa completo de configurações dentro de `getAll`.         |
| `set`     | Map<String, String> | Atualiza as configurações fornecidas sem remover outras chaves.     |
| `setAll`  | Map<String, String> | **Destrutivo:** substitui todas as configurações e remove chaves não fornecidas. |
Permite manipular parâmetros internos do router.

**Exemplo de Solicitação**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemplo de Resposta**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Códigos de Erro Padrão JSON-RPC2

---

| Parâmetro | Tipo   | Descrição                      |
|-----------|--------|----------------------------------|
| `Echo`    | String | Valor retornado como `Result`. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### Códigos de Erro Específicos do I2PControl

Gerencia o próprio I2PControl. O manipulador Java atual suporta alterações de senha.

| Parâmetro             | Tipo   | Descrição                                                                |
|-----------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password` | String | Define uma nova senha I2PControl e revoga tokens de autenticação existentes. |
O resultado contém `SettingsSaved`. Se a senha foi alterada, o resultado também contém `"i2pcontrol.password": null`. As configurações de endereço e porta de escuta do plugin autônomo legado não estão ativas no manipulador Java atual.

> **Senha padrão:** `itoopie` — esta é a senha padrão de fábrica e **deve ser alterada** imediatamente por segurança.

## 5. Códigos de Erro

### Códigos de Erro Padrão JSON-RPC2

| Código | Significado           |
|--------|-----------------------|
| -32700 | Erro de análise JSON |
| -32600 | Solicitação inválida  |
| -32601 | Método não encontrado |
| -32602 | Parâmetros inválidos  |
| -32603 | Erro interno          |
### Códigos de erro específicos do I2PControl

| Código   | Significado                                                                                  |
|----------|----------------------------------------------------------------------------------------------|
| -32001   | Senha inválida fornecida                                                                     |
| -32002   | Nenhum token de autenticação apresentado                                                      |
| -32003   | O token de autenticação não existe                                                            |
| -32004   | O token de autenticação fornecido expirou e será removido                                    |
| -32005   | A versão da API I2PControl usada não foi especificada, mas é obrigatória                      |
| -32006   | A versão da API I2PControl especificada não é suportada pelo I2PControl                       |
> **Senha padrão:** `itoopie` — esta é a senha padrão de fábrica e **deve ser alterada** imediatamente por segurança.

## 6. Uso e Melhores Práticas

- Sempre inclua o parâmetro `Token` (exceto ao autenticar).  
- Altere a senha padrão (`itoopie`) no primeiro uso.  
- Para Java I2P, certifique-se de que o webapp I2PControl esteja habilitado via WebApps.  
- Esteja preparado para pequenas variações: alguns campos podem ser números ou strings, dependendo da versão do I2P.  
- Quebre strings de status longas para uma saída amigável à exibição.

> **Senha padrão:** `itoopie` — esta é a senha padrão de fábrica e **deve ser alterada** imediatamente por segurança.
