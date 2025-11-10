---
title: "Processo de Resposta a Vulnerabilidades"
description: "Processo de Relato e Resposta a Vulnerabilidades de Segurança do I2P"
layout: "security-response"
aliases:
  - /en/research/vrp
---

<div id="contact"></div>

## Relatar uma Vulnerabilidade

Descobriu um problema de segurança? Relate para **security@i2p.net** (PGP recomendado)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">Baixar Chave PGP</a> | Impressão digital da chave GPG: `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Diretrizes de Pesquisa

**Por favor, NÃO:**
- Explore a rede I2P ao vivo
- Conduza engenharia social ou ataque a infraestrutura do I2P
- Interrompa serviços para outros usuários

**Por favor, FAÇA:**
- Use redes de teste isoladas sempre que possível
- Siga práticas de divulgação coordenada
- Entre em contato conosco antes de testar na rede ao vivo

<div id="process"></div>

## Processo de Resposta

### 1. Relato Recebido
- Resposta dentro de **3 dias úteis**
- Gerente de Resposta designado
- Classificação de severidade (ALTA/MÉDIA/BAIXA)

### 2. Investigação e Desenvolvimento
- Desenvolvimento de correção privado via canais criptografados
- Teste em rede isolada
- **Severidade ALTA:** Notificação pública em 3 dias (sem detalhes do exploit)

### 3. Lançamento e Divulgação
- Atualização de segurança implantada
- Prazo máximo de **90 dias** para divulgação completa
- Crédito opcional ao pesquisador nos anúncios

### Níveis de Severidade

**ALTA** - Impacto em toda a rede, atenção imediata necessária  
**MÉDIA** - Roteadores individuais, exploração direcionada  
**BAIXA** - Impacto limitado, cenários teóricos  

<div id="communication"></div>

## Comunicação Segura

Use criptografia PGP/GPG para todos os relatórios de segurança:

```
Impressão digital: 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

Inclua no seu relatório:
- Descrição técnica detalhada
- Passos para reproduzir
- Código de prova de conceito (se aplicável)

<div id="timeline"></div>

## Cronograma

| Fase | Prazo |
|------|-------|
| Resposta Inicial | 0-3 dias |
| Investigação | 1-2 semanas |
| Desenvolvimento e Teste | 2-6 semanas |
| Lançamento | 6-12 semanas |
| Divulgação Completa | 90 dias máx |

<div id="faq"></div>

## FAQ

**Vou ter problemas por relatar?**
Não. A divulgação responsável é apreciada e protegida.

**Posso testar na rede ao vivo?**
Não. Use apenas redes de teste isoladas.

**Posso permanecer anônimo?**
Sim, embora isso possa complicar a comunicação.

**Vocês têm um programa de recompensas por bugs?**
Não atualmente. O I2P é movido por voluntários com recursos limitados.

<div id="examples"></div>

## O Que Relatar

**Dentro do Escopo:**
- Vulnerabilidades do roteador I2P
- Falhas de protocolo ou criptografia
- Ataques a nível de rede
- Técnicas de desanonimização
- Problemas de negação de serviço

**Fora do Escopo:**
- Aplicações de terceiros (entre em contato com os desenvolvedores)
- Engenharia social ou ataques físicos
- Vulnerabilidades conhecidas/divulgadas
- Questões puramente teóricas

---

**Obrigado por ajudar a manter o I2P seguro!**
