---
title: "Ofuscação NTCP"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Rejeitado"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Visão Geral

Esta proposta é sobre a reformulação do transporte NTCP para melhorar sua resistência à identificação automatizada.

## Motivação

Os dados NTCP são criptografados após a primeira mensagem (e a primeira mensagem parece ser dados aleatórios), prevenindo assim a identificação de protocolo através da "análise de carga útil". Ainda é vulnerável à identificação de protocolo através da "análise de fluxo". Isso ocorre porque as primeiras 4 mensagens (ou seja, o handshake) têm comprimento fixo (288, 304, 448 e 48 bytes).

Ao adicionar quantidades aleatórias de dados aleatórios a cada uma das mensagens, podemos tornar isso muito mais difícil.

## Modificações no NTCP

Isso é bastante pesado, mas previne qualquer detecção por equipamentos DPI.

Os seguintes dados serão adicionados ao final da mensagem de 288 bytes:

- Um bloco criptografado ElGamal de 514 bytes
- Preenchimento aleatório

O bloco ElG é criptografado com a chave pública de Bob. Quando descriptografado para 222 bytes, contém:
- 214 bytes de preenchimento aleatório
- 4 bytes 0 reservados
- 2 bytes indicando o comprimento do preenchimento a seguir
- 2 bytes para versão do protocolo e bandeiras

Nas mensagens 2-4, os últimos dois bytes do preenchimento agora indicarão o comprimento de mais preenchimento a seguir.

Observe que o bloco ElG não tem segredo a diante totalmente perfeito, mas não há nada interessante lá dentro.

Poderíamos modificar nossa biblioteca ElG para criptografar tamanhos menores de dados se acharmos que 514 bytes é demais? A criptografia ElG para cada configuração NTCP é demais?

O suporte para isso seria anunciado no endereço do roteador netdb com a opção "version=2". Se apenas 288 bytes forem recebidos na Mensagem 1, assume-se que Alice é de versão 1 e nenhum preenchimento é enviado nas mensagens subsequentes. Observe que a comunicação poderia ser bloqueada se um MITM fragmentasse o IP para 288 bytes (muito improvável segundo Brandon).
