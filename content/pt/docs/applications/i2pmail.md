---
title: "I2P Mail (Email Anônimo sobre I2P)"
description: "Uma visão geral dos sistemas de email dentro da rede I2P — histórico, opções e status atual"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Introdução

O I2P fornece mensagens privadas no estilo e-mail através do **serviço Postman's Mail.i2p** combinado com o **SusiMail**, um cliente de webmail integrado. Este sistema permite que os usuários enviem e recebam e-mails tanto dentro da rede I2P quanto de/para a internet regular (clearnet) através de uma ponte gateway.

---

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um título ou pareça incompleto, traduza-o como está.

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** é um provedor de e-mail hospedado dentro do I2P, operado pelo "Postman"
- **SusiMail** é o cliente webmail integrado no console do router I2P. Ele foi projetado para evitar vazamento de metadados (por exemplo, hostname) para servidores SMTP externos.
- Através dessa configuração, os usuários do I2P podem enviar/receber mensagens tanto dentro do I2P quanto de/para a clearnet (por exemplo, Gmail) via ponte Postman.

### How Addressing Works

O email I2P usa um sistema de endereço duplo:

- **Dentro da rede I2P**: `username@mail.i2p` (por exemplo, `idk@mail.i2p`)
- **Da clearnet**: `username@i2pmail.org` (por exemplo, `idk@i2pmail.org`)

O gateway `i2pmail.org` permite que usuários regulares da internet enviem e-mails para endereços I2P, e usuários I2P enviem para endereços da clearnet. E-mails da internet são roteados através do gateway antes de serem encaminhados através do I2P para sua caixa de entrada do SusiMail.

**Quota de envio para clearnet**: 20 emails por dia ao enviar para endereços de internet regulares.

### O que é

**Para registar uma conta mail.i2p:**

1. Certifique-se de que seu roteador I2P está em execução
2. Visite **[http://hq.postman.i2p](http://hq.postman.i2p)** dentro do I2P
3. Siga o processo de registro
4. Acesse seu e-mail através do **SusiMail** no console do roteador

> **Nota**: `hq.postman.i2p` é um endereço de rede I2P (eepsite) e só pode ser acessado enquanto conectado ao I2P. Para mais informações sobre configuração de email, segurança e uso, visite o Postman HQ.

### Como o Endereçamento Funciona

- Remoção automática de cabeçalhos identificadores (`User-Agent:`, `X-Mailer:`) para privacidade
- Sanitização de metadados para prevenir vazamentos para servidores SMTP externos
- Criptografia ponta a ponta para emails internos I2P-para-I2P

### Primeiros Passos

- Interoperabilidade com email "normal" (SMTP/POP) via ponte Postman
- Experiência de usuário simples (webmail integrado ao console do roteador)
- Integrado com a distribuição principal do I2P (SusiMail incluído no I2P Java)
- Remoção de cabeçalhos para proteção de privacidade

### Recursos de Privacidade

- A ponte para email externo requer confiança na infraestrutura do Postman
- A ponte para clearnet reduz a privacidade comparada à comunicação puramente interna do I2P
- Dependente da disponibilidade e segurança do servidor de email Postman

---

## Technical Details

**Serviço SMTP**: `localhost:7659` (fornecido pelo Postman) **Serviço POP3**: `localhost:7660` **Acesso ao Webmail**: Integrado no console do roteador em `http://127.0.0.1:7657/susimail/`

> **Importante**: O SusiMail é apenas para ler e enviar emails. A criação e gestão de contas devem ser feitas em **hq.postman.i2p**.

---

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um cabeçalho ou pareça incompleto, traduza-o como está.

## Best Practices

- **Altere sua senha** após registrar sua conta mail.i2p
- **Use e-mail I2P-para-I2P** sempre que possível para máxima privacidade (sem ponte para clearnet)
- **Esteja atento ao limite de 20/dia** ao enviar para endereços clearnet
- **Compreenda as compensações**: A ponte para clearnet oferece conveniência, mas reduz o anonimato em comparação com comunicações puramente internas do I2P
- **Mantenha o I2P atualizado** para beneficiar-se das melhorias de segurança no SusiMail

---

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um cabeçalho ou pareça incompleto, traduza-o como está.
