---
title: "Transporte SSU2"
date: 2022-10-11
author: "zzz"
description: "Transporte SSU2"
categories: ["development"]
---

## Visão geral

O I2P tem usado um protocolo de transporte UDP resistente à censura "SSU" desde 2005. Tivemos poucos, se é que tivemos algum, relatos de bloqueio do SSU em 17 anos. No entanto, pelos padrões atuais de segurança, resistência a bloqueios e desempenho, podemos fazer melhor. Muito melhor.

É por isso que, juntamente com o [projeto i2pd](https://i2pd.xyz/), criamos e implementamos o "SSU2", um protocolo UDP moderno projetado segundo os mais altos padrões de segurança e resistência a bloqueios. Este protocolo substituirá o SSU.

Combinamos a criptografia padrão do setor com os melhores recursos dos protocolos UDP WireGuard e QUIC, juntamente com os recursos de resistência à censura do nosso protocolo TCP "NTCP2". SSU2 pode ser um dos protocolos de transporte mais seguros já concebidos.

As equipes do Java I2P e do i2pd estão finalizando o transporte SSU2 e nós o habilitaremos para todos os routers na próxima versão. Isso conclui nosso plano de uma década de atualizar toda a criptografia da implementação original do Java I2P que remonta a 2003. O SSU2 substituirá o SSU, nosso único uso restante de criptografia ElGamal.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

Após a transição para SSU2, teremos migrado todos os nossos protocolos autenticados e criptografados para handshakes padrão do [Noise Protocol](https://noiseprotocol.org/):

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Todos os protocolos Noise do I2P usam os seguintes algoritmos criptográficos padrão:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Objetivos


- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Projeto

I2P usa múltiplas camadas de criptografia para proteger o tráfego contra atacantes. A camada mais baixa é a camada de protocolo de transporte, usada para ligações ponto a ponto entre dois routers. Atualmente temos dois protocolos de transporte: NTCP2, um protocolo TCP moderno introduzido em 2018, e SSU, um protocolo UDP desenvolvido em 2005.

SSU2, assim como os protocolos de transporte do I2P anteriores, não é um canal de uso geral para dados. Sua tarefa principal é entregar com segurança as mensagens I2NP de baixo nível do I2P de um router ao próximo. Cada uma dessas conexões ponto a ponto constitui um salto em um I2P tunnel. Protocolos I2P de camadas superiores operam sobre essas conexões ponto a ponto para entregar mensagens garlic (mensagens agregadas do I2P) de ponta a ponta entre os destinos do I2P.

Projetar um transporte UDP apresenta desafios únicos e complexos que não estão presentes em protocolos TCP. Um protocolo UDP deve lidar com questões de segurança causadas por falsificação de endereço e deve implementar seu próprio controle de congestionamento. Além disso, todas as mensagens devem ser fragmentadas para se ajustarem ao tamanho máximo de pacote (MTU) do caminho de rede e recompostas pelo receptor.

Primeiro, nos baseamos fortemente em nossa experiência anterior com nossos NTCP2, SSU e protocolos de streaming. Em seguida, analisamos cuidadosamente e nos baseamos amplamente em dois protocolos UDP desenvolvidos recentemente:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

A classificação e o bloqueio de protocolos por adversários no caminho (on-path), como firewalls de estados-nação, não fazem parte explicitamente do modelo de ameaça desses protocolos. No entanto, é uma parte importante do modelo de ameaça do I2P, pois nossa missão é fornecer um sistema de comunicações anônimo e resistente à censura para usuários em risco em todo o mundo. Portanto, grande parte do nosso trabalho de projeto envolveu combinar as lições aprendidas com o NTCP2 e o SSU com os recursos e a segurança suportados pelo QUIC e pelo WireGuard.

## Desempenho

A rede I2P é uma combinação complexa de routers diversos. Existem duas implementações principais em execução em todo o mundo, em hardware que vai desde computadores de centros de dados de alto desempenho até Raspberry Pi e telefones Android. Routers usam tanto TCP quanto UDP como transportes. Embora as melhorias do SSU2 sejam significativas, não esperamos que elas sejam aparentes para o usuário, seja localmente ou nas velocidades de transferência de ponta a ponta.

Aqui estão alguns destaques das melhorias estimadas do SSU2 em comparação com o SSU:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Plano de Transição

O I2P se esforça para manter a compatibilidade com versões anteriores, tanto para garantir a estabilidade da rede quanto para permitir que routers mais antigos continuem a ser úteis e seguros. No entanto, há limites, pois a compatibilidade aumenta a complexidade do código e os requisitos de manutenção.

Os projetos Java I2P e i2pd ativarão o SSU2 por padrão em seus próximos lançamentos (2.0.0 e 2.44.0) no final de novembro de 2022. No entanto, eles têm planos diferentes para desativar o SSU. O i2pd desativará o SSU imediatamente, porque o SSU2 é uma grande melhoria em relação à sua implementação de SSU. O Java I2P planeja desativar o SSU em meados de 2023, para permitir uma transição gradual e dar tempo para que routers mais antigos atualizem.

## Resumo

Os fundadores do I2P tiveram que fazer várias escolhas de algoritmos e protocolos criptográficos. Algumas dessas escolhas foram melhores do que outras, mas, vinte anos depois, a maioria já mostra sua idade. É claro que sabíamos que isso viria, e passamos a última década planejando e implementando atualizações criptográficas.

SSU2 foi o último e mais complexo protocolo a ser desenvolvido em nosso longo processo de atualização. UDP apresenta um conjunto de pressupostos e um modelo de ameaça muito desafiadores. Primeiro projetamos e lançamos três outras variantes de protocolos Noise e adquirimos experiência e uma compreensão mais profunda das questões de segurança e do projeto de protocolo.

Espera-se que o SSU2 seja ativado nas versões do i2pd e do Java I2P agendadas para o final de novembro de 2022. Se a atualização correr bem, ninguém vai notar absolutamente nada de diferente. Os benefícios de desempenho, embora significativos, provavelmente não serão mensuráveis para a maioria das pessoas.

Como de costume, recomendamos que você atualize para a nova versão quando estiver disponível. A melhor maneira de manter a segurança e ajudar a rede é executar a versão mais recente.
