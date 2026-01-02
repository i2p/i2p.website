---
title: "IRC sobre I2P"
description: "Guia completo de redes IRC I2P, clientes, túneis e configuração de servidor (atualizado 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão Geral

**Pontos-chave**

- O I2P fornece **criptografia ponta a ponta** para o tráfego IRC através de seus túneis. **Desative SSL/TLS** nos clientes IRC, a menos que você esteja usando outproxy para a clearnet.
- O túnel cliente **Irc2P** pré-configurado escuta em **127.0.0.1:6668** por padrão. Conecte seu cliente IRC a esse endereço e porta.
- Não use o termo "TLS fornecido pelo router." Use "criptografia nativa do I2P" ou "criptografia ponta a ponta."

## Início rápido (Java I2P)

1. Abra o **Hidden Services Manager** em `http://127.0.0.1:7657/i2ptunnel/` e certifique-se de que o túnel **Irc2P** está **em execução**.
2. No seu cliente IRC, defina **servidor** = `127.0.0.1`, **porta** = `6668`, **SSL/TLS** = **desativado**.
3. Conecte-se e entre em canais como `#i2p`, `#i2p-dev`, `#i2p-help`.

Para usuários do **i2pd** (router em C++), crie um túnel cliente no `tunnels.conf` (veja os exemplos abaixo).

## Redes e servidores

### IRC2P (main community network)

- Servidores federados: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- O túnel **Irc2P** em `127.0.0.1:6668` conecta-se automaticamente a um destes.
- Canais típicos: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Servidores: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Idiomas principais: Russo e Inglês. Interfaces web existem em alguns hosts.

## Client setup

### Recommended, actively maintained

- **WeeChat (terminal)** — forte suporte a SOCKS; fácil de programar.
- **Pidgin (desktop)** — ainda mantido; funciona bem no Windows/Linux.
- **Thunderbird Chat (desktop)** — suportado no ESR 128+.
- **The Lounge (auto-hospedado web)** — cliente web moderno.

### IRC2P (rede comunitária principal)

- **LimeChat** (gratuito, código aberto).
- **Textual** (pago na App Store; código-fonte disponível para compilação).

### Rede Ilita

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Protocolo: **IRC**
- Servidor: **127.0.0.1**
- Porta: **6668**
- Criptografia: **desativada**
- Nome de usuário/apelido: qualquer

#### Thunderbird Chat

- Tipo de conta: **IRC**
- Servidor: **127.0.0.1**
- Porta: **6668**
- SSL/TLS: **desativado**
- Opcional: entrar automaticamente em canais ao conectar

#### Dispatch (SAM v3)

Exemplo de valores padrão do `config.toml`:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Túnel cliente Irc2P: **127.0.0.1:6668** → servidor upstream na **porta 6667**.
- Gerenciador de Serviços Ocultos: `http://127.0.0.1:7657/i2ptunnel/`.

### Recomendado, mantido ativamente

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Túnel separado para Ilita (exemplo):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### Opções para macOS

- **Ative o SAM** no I2P Java (desativado por padrão) em `/configclients` ou `clients.config`.
- Padrões: **127.0.0.1:7656/TCP** e **127.0.0.1:7655/UDP**.
- Criptografia recomendada: `SIGNATURE_TYPE=7` (Ed25519) e `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 com fallback ElGamal) ou apenas `4` para somente modernos.

### Configurações de exemplo

- Padrão do Java I2P: **2 de entrada / 2 de saída**.
- Padrão do i2pd: **5 de entrada / 5 de saída**.
- Para IRC: **2–3 de cada** é suficiente; configure explicitamente para comportamento consistente entre routers.

## Configuração do cliente

- **Não ative SSL/TLS** para conexões IRC internas do I2P. O I2P já fornece criptografia ponta a ponta. TLS adicional aumenta sobrecarga sem ganhos de anonimato.
- Use **chaves persistentes** para identidade estável; evite regenerar chaves a cada reinicialização, a menos que esteja testando.
- Se múltiplas aplicações usam IRC, prefira **tunnels separados** (não compartilhados) para reduzir correlação entre serviços.
- Se você precisar permitir controle remoto (SAM/I2CP), vincule ao localhost e proteja o acesso com tunnels SSH ou proxies reversos autenticados.

## Alternative connection method: SOCKS5

Alguns clientes podem conectar via proxy SOCKS5 do I2P: **127.0.0.1:4447**. Para melhores resultados, prefira um túnel IRC dedicado na porta 6668; SOCKS não consegue sanitizar identificadores da camada de aplicação e pode vazar informações se o cliente não foi projetado para anonimato.

## Troubleshooting

- **Não consegue conectar** — certifique-se de que o túnel Irc2P está em execução e o router está totalmente bootstrapped.
- **Trava em resolve/join** — verifique novamente se SSL está **desabilitado** e o cliente aponta para **127.0.0.1:6668**.
- **Alta latência** — I2P tem latência mais alta por design. Mantenha as quantidades de túneis modestas (2–3) e evite loops de reconexão rápida.
- **Usando aplicativos SAM** — confirme que SAM está habilitado (Java) ou não está bloqueado por firewall (i2pd). Sessões de longa duração são recomendadas.

## Appendix: Ports and naming

- Portas comuns de túnel IRC: **6668** (padrão do Irc2P), **6667** e **6669** como alternativas.
- Nomes de host `.b32.i2p`: forma padrão de 52 caracteres; formas estendidas de 56+ caracteres existem para LS2/certificados avançados. Use nomes de host `.i2p` a menos que você explicitamente precise de endereços b32.
