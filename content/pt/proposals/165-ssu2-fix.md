---
title: "Proposta I2P #165: Correção do SSU2"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Aberto"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Proposta por weko, orignal, the Anonymous e zzz.

### Visão Geral

Este documento sugere alterações no SSU2 após um ataque ao I2P que explorou vulnerabilidades no SSU2. O objetivo principal é aprimorar a segurança e prevenir ataques de negação de serviço distribuído (DDoS) e tentativas de desanonimização.

### Modelo de Ameaça

Um atacante cria novos RIs falsos (o roteador não existe): é um RI regular, mas ele coloca endereço, porta, chaves s e i do roteador real de Bob, e então inunda a rede. Quando tentamos nos conectar a esse roteador (que pensamos ser real), nós, como Alice, podemos nos conectar a esse endereço, mas não podemos ter certeza de que isso foi feito com o RI real de Bob. Isso é possível e foi usado para um ataque de negação de serviço distribuído (criar uma grande quantidade de tais RIs e inundar a rede), além disso, isso pode facilitar ataques de desanonimização ao incriminar bons roteadores e não os do atacante, se banirmos IPs com muitos RIs (em vez de melhor distribuir a construção do túnel para esses RIs como para um único roteador).

### Possíveis Correções

#### 1. Correção com suporte para roteadores antigos (antes da mudança)

.. _overview-1:

Visão Geral
^^^^^^^^

Um paliativo para suportar conexões SSU2 com roteadores antigos.

Comportamento
^^^^^^^^^

O perfil do roteador de Bob deve ter a flag 'verificado', que é falsa por padrão para todos os novos roteadores (sem perfil ainda). Quando a flag 'verificado' é falsa, nunca fazemos conexões com SSU2 como Alice para Bob - não podemos ter certeza do RI. Se Bob se conectar a nós (Alice) com NTCP2 ou SSU2 ou se nós (Alice) nos conectarmos a Bob com NTCP2 uma vez (podemos verificar o RouterIdent de Bob nesses casos) - a flag é definida como verdadeira.

Problemas
^^^^^^^^

Há um problema com a inundação de RIs falsos apenas SSU2: não podemos verificá-lo por nós mesmos e somos forçados a esperar que o roteador real faça conexões conosco.

#### 2. Verificar RouterIdent durante a criação da conexão

.. _overview-2:

Visão Geral
^^^^^^^^

Adicionar bloco “RouterIdent” para SessionRequest e SessionCreated.

Formato possível do bloco RouterIdent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 byte flags, 32 bytes RouterIdent. Flag_0: 0 se RouterIdent do receptor; 1 se RouterIdent do remetente

Comportamento
^^^^^^^^

Alice (deveria(1), pode(2)) envia no payload o bloco RouterIdent com Flag_0 = 0 e o RouterIdent de Bob. Bob (deveria(3), pode(4)) verifica se é o seu RouterIdent, e se não for: encerra a sessão com a razão "RouterIdent Errado", se for seu RouterIdent: envia o bloco RI com 1 em Flag_0 e o RouterIdent de Bob.

Com (1) Bob não suporta roteadores antigos. Com (2) Bob suporta roteadores antigos, mas pode ser vítima de DDoS de roteadores que estão tentando fazer conexão com RIs falsos. Com (3) Alice não suporta roteadores antigos. Com (4) Alice suporta roteadores antigos e está usando um esquema híbrido: Correção 1 para roteadores antigos e Correção 2 para novos roteadores. Se o RI diz a versão nova, mas durante a conexão não recebemos o bloco RouterIdent - terminar e remover o RI.

.. _problems-1:

Problemas
^^^^^^^^

Um atacante pode mascarar seus roteadores falsos como antigos, e com (4) ainda estamos esperando pelo 'verificado' como na correção 1.

Notas
^^^^^

Em vez de 32 bytes para RouterIdent, podemos provavelmente usar 4 bytes
siphash-do-hash, algum HKDF ou algo mais, que deve ser suficiente.

#### 3. Bob define i = RouterIdent

.. _overview-3:

Visão Geral
^^^^^^^^

Bob usa seu RouterIdent como chave i.

.. _behavior-1:

Comportamento
^^^^^^^^

Bob (deveria(1), pode(2)) usa seu próprio RouterIdent como chave i para SSU2.

Alice com (1) conecta-se apenas se i = RouterIdent de Bob. Alice com (2) usa o esquema híbrido (correção 3 e 1): se i = RouterIdent de Bob, podemos fazer a conexão, caso contrário devemos verificá-lo primeiro (ver correção 1).

Com (1) Alice não suporta roteadores antigos. Com (2) Alice suporta roteadores antigos.

.. _problems-2:

Problemas
^^^^^^^^

Um atacante pode mascarar seus roteadores falsos como antigos, e com (2) ainda estamos esperando pelo 'verificado' como na correção 1.

.. _notes-1:

Notas
^^^^^

Para economizar no tamanho do RI, é melhor adicionar um tratamento se a chave i não for especificada. Se for, então i = RouterIdent. Nesse caso, Bob não suporta roteadores antigos.

#### 4. Adicionar mais um MixHash ao KDF do SessionRequest

.. _overview-4:

Visão Geral
^^^^^^^^

Adicionar MixHash(hash do ident de Bob) ao estado NOISE da mensagem "SessionRequest", por exemplo, h = SHA256(h || hash do ident de Bob).
Deve ser o último MixHash usado como ad para ENCRYPT ou DECRYPT.
Deve-se introduzir a flag de cabeçalho adicional do SSU2 "Verificar ident de Bob" = 0x02.

.. _behavior-4:

Comportamento
^^^^^^^^

- Alice adiciona MixHash com o hash do ident de Bob do RouterInfo de Bob e o usa como ad para ENCRYPT e define a flag "Verificar ident de Bob"
- Bob verifica a flag "Verificar ident de Bob" e adiciona MixHash com seu próprio hash ident e o usa como ad para DECRYPT. Se AEAD/Chacha20/Poly1305 falhar, Bob fecha a sessão.

Compatibilidade com roteadores antigos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice deve verificar a versão do roteador de Bob e, se satisfizer a versão mínima que suporta esta proposta, adicionar este MixHash e definir a flag "Verificar ident de Bob". Se o roteador for mais antigo, Alice não adiciona MixHash e não define a flag "Verificar ident de Bob".
- Bob verifica a flag "Verificar ident de Bob" e adiciona este MixHash se estiver definido. Roteadores mais antigos não definem esta flag e este MixHash não deve ser adicionado.

.. _problems-4:

Problemas
^^^^^^^^

- Um atacante pode alegar roteadores falsos com versão mais antiga. Em algum momento, roteadores mais antigos devem ser usados com precaução e após serem verificados por outros meios.

### Compatibilidade Retroativa

Descrita nas correções.

### Status Atual

i2pd: Correção 1.
