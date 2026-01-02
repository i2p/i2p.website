---
title: "RI e Preenchimento de Destino"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Open"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Status

Implementado na versão 0.9.57. 
Deixando esta proposta aberta para que possamos aprimorar e discutir as ideias na seção "Planejamento Futuro".


## Visão Geral


### Resumo

A chave pública ElGamal em Destinos não tem sido usada desde a versão 0.6 (2005).
Enquanto nossas especificações dizem que ela não é usada, NÃO dizem que as implementações podem evitar
gerar um par de chaves ElGamal e simplesmente preencher o campo com dados aleatórios.

Propomos a alteração das especificações para dizer que
o campo é ignorado e que as implementações PODEM preenchê-lo com dados aleatórios.
Esta mudança é compatível com versões anteriores. Não há nenhuma implementação conhecida que valide
a chave pública ElGamal.

Além disso, esta proposta oferece orientação aos implementadores sobre como gerar os
dados aleatórios para o preenchimento de Destino E Identidade de Roteador, de forma que sejam compressíveis enquanto
ainda sejam seguros, e sem que as representações em Base 64 pareçam ser corrompidas ou inseguras.
Isto fornece a maioria dos benefícios de remover os campos de preenchimento sem quaisquer
mudanças disruptivas no protocolo.
Destinos compressíveis reduzem o tamanho do SYN de streaming e datagramas respondíveis;
Identidades de Roteador compressíveis reduzem Mensagens de Armazenamento de Banco de Dados, mensagens SSU2 Confirmadas por Sessão,
e arquivos su3 de re-sementação.

Finalmente, a proposta discute possibilidades para novos formatos de Destino e Identidade de Roteador
que eliminariam o preenchimento por completo. Há também uma breve discussão sobre criptografia pós-quântica
e como isso pode afetar o planejamento futuro.


### Objetivos

- Eliminar a exigência de gerar par de chaves ElGamal para Destinos
- Recomendar as melhores práticas para que os Destinos e Identidades de Roteador sejam altamente compressíveis,
  mas não exibam padrões óbvios em representações Base 64.
- Incentivar a adoção das melhores práticas por todas as implementações para
  que os campos não sejam distinguíveis
- Reduzir o tamanho do SYN de streaming
- Reduzir o tamanho do datagrama respondível
- Reduzir o tamanho do bloco RI do SSU2
- Reduzir o tamanho e a frequência de fragmentação da Sessão Confirmada SSU2
- Reduzir o tamanho da Mensagem de Armazenamento de Banco de Dados (com RI)
- Reduzir o tamanho do arquivo de re-sementação
- Manter compatibilidade em todos os protocolos e APIs
- Atualizar especificações
- Discutir alternativas para novos formatos de Destino e Identidade de Roteador

Ao eliminar a exigência de gerar chaves ElGamal, as implementações podem
ser capazes de remover completamente o código ElGamal, sujeitas às considerações de compatibilidade
com versões anteriores em outros protocolos.


## Design

Estritamente falando, a chave pública de assinatura de 32 bytes sozinha (em ambos os Destinos e Identidades de Roteador)
e a chave pública de criptografia de 32 bytes (somente em Identidades de Roteador) é um número aleatório
que fornece toda a entropia necessária para as hashes SHA-256 dessas estruturas
serem criptograficamente fortes e distribuídas aleatoriamente na base de dados de rede DHT.

No entanto, por excesso de cautela, recomendamos um mínimo de 32 bytes de dados aleatórios
a serem usados no campo da chave pública ElG e preenchimento. Além disso, se os campos fossem todos zeros,
os destinos em Base 64 conteriam longas sequências de caracteres AAAA, o que poderia causar alarme
ou confusão aos usuários.

Para o tipo de assinatura Ed25519 e tipo de criptografia X25519:
Os Destinos conterão 11 cópias (352 bytes) dos dados aleatórios.
As Identidades de Roteador conterão 10 cópias (320 bytes) dos dados aleatórios.


### Estimativa de Economia

Os Destinos estão incluídos em cada SYN de streaming
e datagrama respondível.
Infos de Roteador (contendo Identidades de Roteador) estão incluídos em Mensagens de Armazenamento de Banco de Dados
e nas mensagens Sessão Confirmada em NTCP2 e SSU2.

NTCP2 não comprime a Info de Roteador.
RIs em Mensagens de Armazenamento de Banco de Dados e mensagens Sessão Confirmada SSU2 são compactados com gzip.
Infos de Roteador são compactadas em arquivos SU3 de re-sementação.

Destinos em Mensagens de Armazenamento de Banco de Dados não são comprimidos.
Mensagens SYN de streaming são compactadas com gzip na camada I2CP.

Para o tipo de assinatura Ed25519 e tipo de criptografia X25519,
economias estimadas:

| Tipo de Dado | Tamanho Total | Chaves e Cert | Preenchimento Não Comprimido | Preenchimento Comprimido | Tamanho | Economia |
|--------------|---------------|---------------|------------------------------|--------------------------|---------|----------|
| Destino | 391 | 39 | 352 | 32 | 71 | 320 bytes (82%) |
| Identidade do Roteador | 391 | 71 | 320 | 32 | 103 | 288 bytes (74%) |
| Info do Roteador | 1000 tip. | 71 | 320 | 32 | 722 tip. | 288 bytes (29%) |

Notas: Assume que o certificado de 7 bytes não é compressível, sem sobrecarga adicional do gzip.
Nenhum dos dois é verdade, mas os efeitos serão pequenos.
Ignora outras partes compressíveis da Info de Roteador.


## Especificação

As mudanças propostas para nossas especificações atuais estão documentadas abaixo.


### Estruturas Comuns
Alterar a especificação das estruturas comuns
para especificar que o campo de chave pública de Destino de 256 bytes é ignorado e pode
conter dados aleatórios.

Adicionar uma seção à especificação das estruturas comuns
recomendando a melhor prática para o campo de chave pública de Destino e os
campos de preenchimento do Destino e Identidade de Roteador, conforme segue:

Gerar 32 bytes de dados aleatórios usando um gerador de números pseudo-aleatórios criptograficamente forte (PRNG)
e repetir esses 32 bytes conforme necessário para preencher o campo de chave pública (para Destinos)
e o campo de preenchimento (para Destinos e Identidades de Roteador).

### Arquivo de Chave Privada
O formato do arquivo de chave privada (eepPriv.dat) não é uma parte oficial de nossas especificações
mas está documentado nos [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html)
e outras implementações o suportam.
Isso permite a portabilidade de chaves privadas entre diferentes implementações.
Adicionar uma nota a esse javadoc de que a chave pública de criptografia pode ser um preenchimento aleatório
e a chave privada de criptografia pode ser toda de zeros ou dados aleatórios.

### SAM
Nota na especificação SAM que a chave privada de criptografia não é usada e pode ser ignorada.
Qualquer dado aleatório pode ser retornado pelo cliente.
A SAM Bridge pode enviar dados aleatórios na criação (com DEST GENERATE ou SESSION CREATE DESTINATION=TRANSIENT)
ao invés de todos zeros, para que a representação em Base 64 não tenha uma sequência de caracteres AAAA
e pareça quebrada.


### I2CP
Nenhuma mudança necessária para o I2CP. A chave privada para a chave pública de criptografia no Destino
não é enviada para o roteador.


## Planejamento Futuro


### Mudanças de Protocolo

A um custo de mudanças no protocolo e uma falta de compatibilidade com versões anteriores, poderíamos
mudar nossos protocolos e especificações para eliminar o campo de preenchimento no
Destino, Identidade de Roteador, ou ambos.

Esta proposta apresenta alguma semelhança com o formato de leaseset criptografado "b33",
contendo apenas uma chave e um campo de tipo.

Para manter alguma compatibilidade, certas camadas de protocolo poderiam "expandir" o campo de preenchimento
com todos zeros para apresentar a outras camadas de protocolo.

Para Destinos, também poderíamos remover o campo de tipo de criptografia no certificado de chave,
economizando dois bytes.
Alternativamente, os Destinos poderiam obter um novo tipo de criptografia no certificado de chave,
indicando uma chave pública zero (e preenchimento).

Se a conversão de compatibilidade entre formatos antigos e novos não for incluída em alguma camada de protocolo,
as seguintes especificações, APIs, protocolos e aplicações seriam afetadas:

- Especificação de estruturas comuns
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Streaming
- SAM
- Bittorrent
- Re-sementação
- Arquivo de Chave Privada
- Núcleo Java e API do roteador
- API i2pd
- Bibliotecas SAM de terceiros
- Ferramentas integradas e de terceiros
- Vários plugins Java
- Interfaces de usuário
- Aplicações P2P, como MuWire, bitcoin, monero
- hosts.txt, catálogo de endereços e assinaturas

Se a conversão for especificada em alguma camada, a lista seria reduzida.

Os custos e benefícios dessas mudanças não são claros.

Propostas específicas a serem definidas (TBD):


### Chaves PQ

Chaves públicas de criptografia pós-quântica (PQ), para qualquer algoritmo antecipado,
são maiores que 256 bytes. Isso eliminaria qualquer preenchimento e quaisquer economias das mudanças propostas acima, para Identidades de Roteador.

Em uma abordagem "híbrida" PQ, como o que o SSL está fazendo, as chaves PQ seriam apenas efêmeras,
e não apareceriam na Identidade de Roteador.

Chaves de assinatura PQ não são viáveis,
e os Destinos não contêm chaves públicas de criptografia.
Chaves estáticas para ratchet estão no Lease Set, não no Destino.
portanto, podemos eliminar os Destinos da seguinte discussão.

Assim, o PQ só afeta Infos de Roteador, e apenas para chaves estáticas PQ (não efêmeras), não para híbridas PQ.
Isso seria para um novo tipo de criptografia e afetaria NTCP2, SSU2 e
Mensagens de Pesquisa de Banco de Dados criptografadas e respostas.
Prazo estimado para projeto, desenvolvimento e implantação disso seria ????????
Mas seria após híbrido ou ratchet ????????????

Para mais discussões, veja [this topic](http://zzz.i2p/topics/3294).


## Questões

Pode ser desejável renovar as chaves da rede em uma taxa lenta, para fornecer proteção para novos roteadores.
"Renovar chaves" poderia significar simplesmente mudar o preenchimento, não realmente mudar as chaves.

Não é possível renovar chaves de Destinos existentes.

Devem as Identidades de Roteador com preenchimento no campo de chave pública serem identificadas com um tipo de criptografia diferente no certificado de chave? Isso causaria problemas de compatibilidade.


## Migração

Nenhum problema de compatibilidade com versões anteriores para substituir a chave ElGamal por preenchimento.

Renovação de chaves, se implementada, seria semelhante à realizada
em três transições anteriores de identidade de roteador:
De assinaturas DSA-SHA1 para ECDSA, depois para
assinaturas EdDSA, depois para criptografia X25519.

Sujeito a questões de compatibilidade com versões anteriores, e após desabilitação do SSU,
as implementações podem remover completamente o código ElGamal.
Aproximadamente 14% dos roteadores na rede são do tipo de criptografia ElGamal, incluindo muitos floodfills.

Uma solicitação de mesclagem preliminar para I2P em Java está em [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66).
