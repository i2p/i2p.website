---
title: "Tradução de Nome para GarliCat"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Dead"
thread: "http://zzz.i2p/topics/453"
---

## Visão Geral

Esta proposta é sobre adicionar suporte para consultas reversas de DNS ao I2P.


## Mecanismo de Tradução Atual

GarliCat (GC) executa a tradução de nomes para estabelecer conexões com outros nós GC. Esta tradução de nomes é apenas uma recodificação da representação binária de um endereço em forma codificada Base32. Assim, a tradução funciona nos dois sentidos.

Esses endereços são escolhidos para ter 80 bits de comprimento. Isso ocorre porque o Tor usa valores de 80 bits para endereçar seus serviços ocultos. Assim, OnionCat (que é o GC para Tor) funciona com Tor sem necessidade de intervenção adicional.

Infelizmente (em relação a este esquema de endereçamento), o I2P usa valores de 256 bits para endereçar seus serviços. Como já mencionado, o GC transcodifica entre a forma binária e a codificação Base32. Devido à natureza do GC ser uma VPN de camada 3, em sua representação binária, os endereços são definidos para serem endereços IPv6 que têm um comprimento total de 128 bits. Obviamente, endereços I2P de 256 bits não cabem.

Assim, um segundo passo de tradução de nomes se torna necessário:
Endereço IPv6 (binário) -1a-> Endereço Base32 (80 bits) -2a-> Endereço I2P (256 bits)
-1a- ... tradução GC
-2a- ... consulta I2P hosts.txt

A solução atual é deixar o roteador I2P fazer o trabalho. Isso é realizado pela inserção do endereço Base32 de 80 bits e seu destino (o endereço I2P) como um par nome/valor no arquivo hosts.txt ou privatehosts.txt do roteador I2P.

Isso basicamente funciona, mas depende de um serviço de nomes que (na minha opinião) está em um estado de desenvolvimento e não é maduro o suficiente (especialmente em relação à distribuição de nomes).


## Uma Solução Escalável

Sugiro mudar as etapas de endereçamento em relação ao I2P (e talvez também para Tor) de tal forma que o GC faça consultas reversas nos endereços IPv6 usando o protocolo DNS regular. A zona reversa deve conter diretamente o endereço I2P de 256 bits em sua forma codificada em Base32. Isso muda o mecanismo de consulta para um único passo, adicionando ainda mais vantagens.
Endereço IPv6 (binário) -1b-> Endereço I2P (256 bits)
-1b- ... consulta reversa DNS

Consultas DNS dentro da Internet são conhecidas por serem vazamentos de informação em relação ao anonimato. Assim, essas consultas devem ser realizadas dentro do I2P. Isso implica que vários serviços DNS devem estar disponíveis dentro do I2P. Como as consultas DNS são geralmente realizadas usando o protocolo UDP, o próprio GC é necessário para o transporte de dados porque carrega pacotes UDP que o I2P nativamente não faz.

Outras vantagens estão associadas ao DNS:
1) É um protocolo padrão bem conhecido, por isso é continuamente aprimorado e existem muitas ferramentas (clientes, servidores, bibliotecas,...).
2) É um sistema distribuído. Ele suporta o espaço de nomes sendo hospedado em vários servidores em paralelo por padrão.
3) Ele suporta criptografia (DNSSEC) que permite a autenticação de registros de recursos. Isso poderia ser diretamente vinculado às chaves de um destino.


## Oportunidades Futuras

Pode ser possível que este serviço de nomes também possa ser usado para fazer consultas diretas. Isso é traduzir nomes de host para endereços I2P e/ou endereços IPv6. Mas esse tipo de consulta precisa de investigação adicional porque essas consultas são geralmente feitas pela biblioteca de resolução localmente instalada, que utiliza servidores de nomes da Internet regulares (por exemplo, conforme especificado em /etc/resolv.conf em sistemas Unix-like). Isso é diferente das consultas reversas do GC que expliquei acima.
Uma oportunidade futura poderia ser que o endereço I2P (destino) seja registrado automaticamente ao criar um túnel de entrada GC. Isso melhoraria muito a usabilidade.
