---
title: "Proxy SOCKS"
description: "Usando o tunnel SOCKS do I2P com segurança"
slug: "socks"
aliases:
  - "/pt/socks"
  - "/pt/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS e Proxies SOCKS {#overview}

O proxy SOCKS está funcionando a partir da versão 0.7.1. SOCKS 4/4a/5 são suportados. Habilite o SOCKS criando um tunnel cliente SOCKS no i2ptunnel. Tanto clientes compartilhados quanto não compartilhados são suportados. Não há outproxy SOCKS, então tem uso limitado.

Como diz na [FAQ](/docs/overview/faq#socks):

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
E citando de um email de 2005:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Esperar que possamos simplesmente conectar um cliente arbitrário em cima do I2P sem auditar tanto seu comportamento quanto os protocolos que ele expõe em termos de segurança e anonimato é ingênuo. Praticamente *toda* aplicação e protocolo viola o anonimato, a menos que tenha sido projetado especificamente para isso, e mesmo assim, a maioria deles também viola. Essa é a realidade. Os usuários finais são melhor atendidos com sistemas projetados para anonimato e segurança. Modificar sistemas existentes para funcionar em ambientes anônimos não é tarefa simples, é ordens de magnitude mais trabalho do que simplesmente usar as APIs existentes do I2P.

O proxy SOCKS suporta nomes padrão do livro de endereços, mas não destinos Base64. Hashes Base32 devem funcionar a partir da versão 0.7. Ele suporta apenas conexões de saída, ou seja, um cliente I2PTunnel. O suporte UDP está esboçado mas ainda não funciona. A seleção de outproxy por número de porta está esboçada.

## Veja Também {#see-also}

- As notas da Reunião 81 (16 de março de 2004) e Reunião 82 (23 de março de 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Se Você Conseguir Algo Funcionando {#working}

Por favor, nos informe. E por favor forneça avisos substanciais sobre os riscos dos proxies SOCKS.
