---
title: "Novas entradas no netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Aberto"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Status

Partes desta proposta estão completas e implementadas nas versões 0.9.38 e 0.9.39.
As Estruturas Comuns, I2CP, I2NP e outras especificações
agora estão atualizadas para refletir as mudanças que são suportadas atualmente.

As partes concluídas ainda estão sujeitas a pequenas revisões.
Outras partes desta proposta ainda estão em desenvolvimento
e sujeitas a revisões substanciais.

A busca de Serviços (tipos 9 e 11) são de baixa prioridade e
não estão previstas, podendo ser divididas em uma proposta separada.

## Visão Geral

Esta é uma atualização e agregação das seguintes 4 propostas:

- 110 LS2
- 120 Meta LS2 para multihoming massivo
- 121 LS2 Criptografado
- 122 Pesquisa de serviço não autenticado (anycasting)

Essas propostas são em grande parte independentes, mas para sanidade, definimos e usamos um
formato comum para vários delas.

As seguintes propostas são um pouco relacionadas:

- 140 Multihoming Invisível (incompatível com esta proposta)
- 142 Novo Modelo de Criptografia (para nova criptografia simétrica)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 para LS2 Criptografado
- 150 Protocolo Garlic Farm
- 151 ECDSA Blinding

## Proposta

Esta proposta define 5 novos tipos de DatabaseEntry e o processo para
armazená-los e recuperá-los do banco de dados da rede,
bem como o método para assiná-los e verificar essas assinaturas.

### Objetivos

- Compatível com versões anteriores
- LS2 Usável com multihoming no estilo antigo
- Nenhuma nova criptografia ou primitivas necessárias para suporte
- Manter a desacoplamento da criptografia e a assinatura; suporte a todas as versões atuais e futuras
- Permitir chaves de assinatura offline opcionais
- Reduzir a precisão dos timestamps para reduzir a impressão digital
- Permitir nova criptografia para destinos
- Permitir multihoming massivo
- Corrigir vários problemas com a LS criptografada existente
- Ofuscamento opcional para reduzir a visibilidade por floodfills
- Criptografado suporta tanto chave única quanto múltiplas chaves revogáveis
- Pesquisa de serviços para facilitar a busca de proxies externos, bootstrap de aplicação DHT,
  e outros usos
- Não quebrar nada que dependa de hashes de destino binários de 32 bytes, por exemplo, bittorrent
- Adicionar flexibilidade aos leasesets via propriedades, como temos em routerinfos.
- Colocar o timestamp publicado e a expiração variável no cabeçalho, para que funcione mesmo
  se o conteúdo estiver criptografado (não derivar timestamp do aluguel mais antigo)
- Todos os novos tipos vivem no mesmo espaço DHT e nas mesmas localizações que os leasesets existentes,
  para que os usuários possam migrar do LS antigo para LS2,
  ou mudar entre LS2, Meta, e Criptografado,
  sem alterar o Destino ou o hash.
- Um destino existente pode ser convertido para usar chaves offline,
  ou voltar para chaves online, sem alterar o Destino ou o hash.

### Objetivos não-meta / Fora do escopo

- Novo algoritmo de rotação DHT ou geração aleatória compartilhada
- O tipo específico de nova criptografia e o esquema de criptografia de ponta a ponta
  para usar o novo tipo seria em uma proposta separada.
  Nenhuma nova criptografia é especificada ou discutida aqui.
- Nova criptografia para RIs ou construção de túneis.
  Isso estaria em uma proposta separada.
- Métodos de criptografia, transmissão e recepção de mensagens I2NP DLM / DSM / DSRM.
  Não mudando.
- Como gerar e suportar Meta, incluindo comunicação entre roteadores, gerenciamento, failover e coordenação de backend.
  O suporte pode ser adicionado ao I2CP, ou i2pcontrol, ou um novo protocolo.
  Isso pode ou não ser padronizado.
- Como implementar e gerenciar túneis com expiração mais longa, ou cancelar túneis existentes.
  Isso é extremamente difícil, e sem isso, você não pode ter uma interrupção graciosa razoável.
- Mudanças no modelo de ameaça
- Formato de armazenamento offline, ou métodos para armazenar/recuperar/compartilhar os dados.
- Detalhes da implementação não são discutidos aqui e são deixados para cada projeto.

### Justificativa

LS2 adiciona campos para mudar o tipo de criptografia e para futuras alterações de protocolo.

LS2 Criptografado corrige vários problemas de segurança com o LS criptografado existente através do uso de criptografia assimétrica de todo o conjunto de leases.

Meta LS2 proporciona multihoming flexível, eficiente, eficaz e em larga escala.

Registro de Serviço e Lista de Serviço fornecem serviços anycast como pesquisa de nomeação e bootstrap DHT.

### Tipos de Dados NetDB

Os números de tipo são usados nas Mensagens de Pesquisa/Armazenamento de Banco de Dados I2NP.

A coluna de ponta a ponta refere-se a se consultas/respostas são enviadas a um Destino em uma Mensagem Garlic.

Tipos existentes:

            Dados NetDB             Tipo Pesquisa Tipo Armaz.
qualquer tipo                             0         qualquer   
LS                                        1           1      
RI                                        2           0      
exploratório                              3          DSRM    

Novos tipos:

            Dados NetDB           Tipo Pesquisa   Tipo Armaz.   Cabeçalho LS2 Padrão? Enviado ponta a ponta?
LS2                                       1            3             sim                 sim
LS2 Criptografado                         1            5             não                  não
Meta LS2                                  1            7             sim                 não
Registro de Serviço                      n/a           9             sim                 não
Lista de Serviço                          4           11             não                  não

Notas
`````
- Os tipos de pesquisa atualmente são bits 3-2 na Mensagem de Pesquisa de Banco de Dados.
  Tipos adicionais exigiriam o uso do bit 4.

- Todos os tipos de armazenamento são ímpares, pois os bits superiores no campo de tipo de Mensagem de Armazenamento de Banco de Dados
  são ignorados por roteadores antigos.
  Preferimos que a análise falhe como um LS do que como um RI comprimido.

- O tipo deve ser explícito ou implícito ou nenhum dos dois nos dados cobertos pela assinatura?

### Processo de Pesquisa/Armazenamento

Os tipos 3, 5 e 7 podem ser retornados em resposta a uma pesquisa de leaseset padrão (tipo 1).
O tipo 9 nunca é retornado em resposta a uma pesquisa.
Os tipos 11 são retornados em resposta a um novo tipo de pesquisa de serviço (tipo 11).

Apenas o tipo 3 pode ser enviado em uma mensagem Garlic cliente para cliente.

### Formato

Os tipos 3, 7 e 9 têm um formato comum::

  Cabeçalho LS2 Padrão
  - conforme definido abaixo

  Parte Específica do Tipo
  - conforme definido abaixo em cada parte

  Assinatura LS2 Padrão:
  - Comprimento conforme indicado pelo tipo de assinatura da chave de assinatura

O tipo 5 (Criptografado) não começa com um Destino e tem um
formato diferente. Veja abaixo.

O tipo 11 (Lista de Serviço) é uma agregação de vários Registros de Serviço e possui um
formato diferente. Veja abaixo.

### Considerações de Privacidade/Segurança

A definir

## Cabeçalho LS2 Padrão

Os tipos 3, 7 e 9 usam o cabeçalho LS2 padrão, especificado abaixo:

### Formato
::

  Cabeçalho LS2 Padrão:
  - Tipo (1 byte)
    Não faz parte do cabeçalho, mas faz parte dos dados cobertos pela assinatura.
    Tire do campo na Mensagem de Armazenamento de Banco de Dados.
  - Destino (387+ bytes)
  - Timestamp publicado (4 bytes, big endian, segundos desde a época, zera em 2106)
  - Expira (2 bytes, big endian) (deslocamento do timestamp publicado em segundos, máximo de 18,2 horas)
  - Flags (2 bytes)
    Ordem dos bits: 15 14 ... 3 2 1 0
    Bit 0: Se 0, sem chaves offline; se 1, chaves offline
    Bit 1: Se 0, um leaseset publicado padrão.
           Se 1, um leaseset não publicado. Não deve ser inundado, publicado ou
           enviado em resposta a uma consulta. Se este leaseset expirar, não consulte o
           netdb para um novo, a menos que o bit 2 esteja definido.
    Bit 2: Se 0, um leaseset publicado padrão.
           Se 1, este leaseset não criptografado será ofuscado e criptografado quando publicado.
           Se este leaseset expirar, consulte a localização ofuscada no netdb para um novo.
           Se este bit estiver definido como 1, defina também o bit 1 como 1.
           A partir da versão 0.9.42.
    Bits 3-15: definidos como 0 para compatibilidade com usos futuros
  - Se o flag indicar chaves offline, a seção de assinatura offline:
    Timestamp de expiração (4 bytes, big endian, segundos desde a época, zera em 2106)
    Tipo de assinatura transitória (2 bytes, big endian)
    Chave pública de assinatura transitória (comprimento conforme indicado pelo tipo de assinatura)
    Assinatura do timestamp de expiração, tipo de assinatura transitória e chave pública,
    pela chave pública do destino,
    comprimento conforme indicado pelo tipo de assinatura da chave pública do destino.
    Esta seção pode, e deve, ser gerada offline.

Justificação
```````````

- Não publicado/publicado: Para uso ao enviar um armazenamento de banco de dados de ponta a ponta,
  o roteador de envio pode desejar indicar que este leaseset não deve ser
  enviado para outros. Atualmente, usamos heurísticas para manter este estado.

- Publicado: Substitui a lógica complexa necessária para determinar a 'versão' do
  leaseset. Atualmente, a versão é a expiração do aluguel que expira por último,
  e um roteador de publicação deve incrementar essa expiração em pelo menos 1ms ao
  publicar um leaseset que apenas remove um aluguel mais antigo.

- Expira: Permite que uma entrada no netdb expire antes do seu último
  leaseset a expirar. Pode não ser útil para LS2, onde os leasesets
  devem permanecer com uma expiração máxima de 11 minutos, mas
  para outros novos tipos, é necessário (veja Meta LS e Registro de Serviço abaixo).

- Chaves offline são opcionais, para reduzir a complexidade inicial/necessária de implementação.

### Problemas

- Poderíamos reduzir ainda mais a precisão do timestamp (10 minutos?), mas teríamos que adicionar
  número de versão. Isso pode quebrar o multihoming, a menos que tenhamos criptografia
  de preservação de ordem? Provavelmente não podemos ficar sem timestamps.

- Alternativa: timestamp de 3 bytes (época / 10 minutos), número de versão de 1 byte, expira de 2 bytes

- O tipo é explícito ou implícito nos dados / assinatura? Constantes de "Domínio"
  para assinatura?

Notas
`````

- Roteadores não devem publicar um LS mais de uma vez por segundo.
  Se fizerem, devem incrementar artificialmente o timestamp publicado em 1
  sobre o LS publicado anteriormente.

- Implementações de roteadores poderiam armazenar em cache as chaves transitórias e assinatura para
  evitar verificação a cada vez. Em particular, floodfills e roteadores em
  ambas as extremidades de conexões de longa duração poderiam se beneficiar disso.

- Chaves offline e assinatura são apropriadas apenas para destinos de longa duração,
  ou seja, servidores, não clientes.

## Novos tipos de DatabaseEntry

### LeaseSet 2

Mudanças do LeaseSet existente:

- Adicionar timestamp publicado, timestamp expira, flags e propriedades
- Adicionar tipo de criptografia
- Remover chave de revogação

Pesquise com
    Flag LS padrão (1)
Armazene com
    Tipo LS2 padrão (3)
Armazene em
    Hash do destino
    Este hash é então usado para gerar a "chave de roteamento" diária, como em LS1
Expiração típica
    10 minutos, como em um LS regular.
Publicado por
    Destino

Formato
``````
::

  Cabeçalho LS2 Padrão conforme especificado acima

  Parte Específica do Tipo LS2 Padrão
  - Propriedades (mapeamento conforme especificado na especificação de estruturas comuns, 2 bytes zero se não houver)
  - Número de seções de chave a seguir (1 byte, máx. TBD)
  - Seções de chave:
    - Tipo de criptografia (2 bytes, big endian)
    - Comprimento da chave de criptografia (2 bytes, big endian)
      Isso é explícito, para que os floodfills possam analisar LS2 com tipos de criptografia desconhecidos.
    - Chave de criptografia (número de bytes especificado)
  - Número de lease2s (1 byte)
  - Lease2s (40 bytes cada)
    Estes são aluguéis, mas com uma expiração de 4 bytes em vez de 8 bytes,
    segundos desde a época (zeram em 2106).

  Assinatura LS2 Padrão:
  - Assinatura
    Se o flag indicar chaves offline, assinado pela chave pública transitória,
    caso contrário, pela chave pública do destino
    Comprimento conforme indicado pelo tipo de assinatura da chave de assinatura
    A assinatura é de tudo acima.

Justificação
```````````

- Propriedades: Expansão futura e flexibilidade.
  Colocadas primeiro caso sejam necessárias para análise dos dados restantes.

- Vários pares de tipo de criptografia/chave pública são usados para facilitar a transição para novos tipos de criptografia.
  A outra maneira de fazer isso é publicar múltiplos leasesets, possivelmente usando os mesmos túneis,
  como fazemos agora para destinos DSA e EdDSA.
  A identificação do tipo de criptografia de entrada em um túnel
  pode ser feita com o mecanismo de tag de sessão existente,
  e/ou decriptando experimentalmente usando cada chave. Os comprimentos das
  mensagens de entrada também podem fornecer uma pista.

Discussão
````````

Esta proposta continua a usar a chave pública no leaseset para a
chave de criptografia de ponta-a-ponta, e deixa o campo da chave pública no
Destino sem uso, como está agora. O tipo de criptografia não é especificado
no certificado de chave do Destiono, permanecerá 0.

Uma alternativa rejeitada é especificar o tipo de criptografia no
certificado de chave do Destino, usar a chave pública no Destino e não
usar a chave pública no leaseset. Não planejamos fazer isso.

Benefícios do LS2:
- A localização da chave pública real não muda.
- O tipo de criptografia ou chave pública pode mudar sem mudar o Destino.
- Remove o campo de revogação não utilizado
- Compatibilidade básica com outros tipos de DatabaseEntry nesta proposta
- Permite múltiplos tipos de criptografia

Desvantagens do LS2:
- Localização da chave pública e tipo de criptografia difere de RouterInfo
- Mantém chave pública não utilizada no leaseset
- Requer implementação em toda a rede; na alternativa, tipos de criptografia experimental podem
  ser usados, se permitidos por floodfills (mas veja as propostas 136 e 137 sobre suporte para tipos
  de assinaturas experimentais). A proposta alternativa poderia ser mais fácil de implementar e testar
  para tipos de criptografia experimentais.

Questões sobre Nova Criptografia
`````````````````````````````````
Alguns destes estão fora do escopo para esta proposta,
mas colocando notas aqui por enquanto, pois ainda não temos
uma proposta de criptografia separada.
Veja também as propostas ECIES 144 e 145.

- O tipo de criptografia representa a combinação de curva, comprimento da chave, e esquema de ponta-a-ponta,
  incluindo KDF e MAC, se houver.

- Incluímos um campo de comprimento de chave, para que o LS2 seja
  parseável e verificável pelo floodfill, mesmo para tipos de criptografia desconhecidos.

- O primeiro novo tipo de criptografia a ser proposto provavelmente será ECIES/X25519.
  Como será usado de ponta-a-ponta (ou uma versão levemente modificada de ElGamal/AES+SessionTag
  ou algo completamente novo, por exemplo, ChaCha/Poly) será especificado
  em uma ou mais propostas separadas.
  Veja também as propostas ECIES 144 e 145.

Notas
`````
- Expiração em leases alterada de 8 bytes para 4 bytes.

- Se decidirmos implementar revogação, poderemos fazê-lo com um campo de expiração zero,
  ou leases zero, ou ambos. Não há necessidade de uma chave de revogação separada.

- As chaves de criptografia estão na ordem de preferência do servidor, sendo a mais preferida primeiro.
  O comportamento padrão do cliente é selecionar a primeira chave com
  um tipo de criptografia suportado. Clientes podem usar outros algoritmos de seleção
  com base no suporte à criptografia, desempenho relativo, e outros fatores.

### LS2 Criptografado

Objetivos:

- Adicionar ofuscamento
- Permitir múltiplos tipos de assinatura
- Não exigir novos primitivos criptográficos
- Opcionalmente criptografar para cada destinatário, revogável
- Suportar criptografia de LS2 Padrão e Meta LS2 apenas

O LS2 Criptografado nunca é enviado em uma mensagem garlic de ponta-a-ponta.
Use o LS2 padrão como acima.

Mudanças do LeaseSet criptografado existente:

- Criptografe tudo para garantir segurança
- Criptografe de forma segura, não apenas com AES.
- Criptografe para cada destinatário

Pesquise com
    Flag LS padrão (1)
Armazene com
    Tipo LS2 criptografado (5)
Armazene em
    Hash do tipo de assinatura ofuscada e chave pública ofuscada
    Dois bytes tipo de assinatura (big endian, por exemplo, 0x000b) || chave pública ofuscada
    Este hash é então usado para gerar a "chave de roteamento" diária, como em LS1
Expiração típica
    10 minutos, como em um LS normal, ou horas, como em um meta LS.
Publicado por
    Destino

Definições
``````````
Definimos as seguintes funções correspondentes aos blocos de construção criptográficos usados
para o LS2 criptografado:

CSRNG(n)
    Saída de n bytes de um gerador de números aleatórios criptograficamente seguro.

    Além do requisito de CSRNG ser criptograficamente seguro (e
    assim apropriado para gerar material de chave), deve ser seguro para uma
    saída de n bytes ser usada como material de chave quando as
    sequências de bytes imediatamente anteriores e posteriores
    forem expostas na rede (como em um sal, ou padding criptografado). Implementações
    que dependem de uma fonte potencialmente não confiável devem
    hashear qualquer saída que for exposta na rede [PRNG-REFS]_.

H(p, d)
    Função hash SHA-256 que recebe uma string de personalização p e
    dados d, e produz uma saída de tamanho 32 bytes.

    Use SHA-256 da seguinte forma::

        H(p, d) := SHA-256(p || d)

STREAM
    O cifrador de fluxo ChaCha20, conforme especificado em [RFC-7539-S2.4]_, com o contador
    inicial definido para 1. S_KEY_LEN = 32 e S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Criptografa plaintext usando a chave de cifra k, e nonce iv, que DEVE ser único para
        a chave k. Retorna um ciphertext que é do mesmo tamanho que o plaintext.

        Todo o ciphertext deve ser indistinguível de aleatório, se a chave for secreta.

    DECRYPT(k, iv, ciphertext)
        Decripta ciphertext usando a chave de cifra k, e nonce iv. Retorna o plaintext.

SIG
    O esquema de assinatura RedDSA (correspondente ao tipo de assinatura 11) com ofuscamento de chave.
    Tem as seguintes funções:

    DERIVE_PUBLIC(privkey)
        Retorna a chave pública correspondente à chave privada dada.

    SIGN(privkey, m)
        Retorna uma assinatura pela chave privada privkey sobre a mensagem dada m.

    VERIFY(pubkey, m, sig)
        Verifica a assinatura sig contra a chave pública pubkey e a mensagem m. Retorna
        true se a assinatura for válida, false caso contrário.

    Também deve suportar as seguintes operações de ofuscamento de chave:

    GENERATE_ALPHA(data, secret)
        Gere alpha para aqueles que conhecem os dados e um segredo opcional.
        O resultado deve ser distribuído de forma idêntica às chaves privadas.

    BLIND_PRIVKEY(privkey, alpha)
        Ofusca uma chave privada, usando um segredo alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Ofusca uma chave pública, usando um segredo alpha.
        Para um dado par de chaves (privkey, pubkey), a seguinte relação é válida::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH
    Sistema de acordo de chaves públicas X25519. Chaves privadas de 32 bytes, chaves públicas de
    32 bytes, produz saídas de 32 bytes. Tem as seguintes
    funções:

    GENERATE_PRIVATE()
        Gera uma nova chave privada.

    DERIVE_PUBLIC(privkey)
        Retorna a chave pública correspondente à chave privada dada.

    DH(privkey, pubkey)
        Gera um segredo compartilhado a partir das chaves privada e pública dadas.

HKDF(salt, ikm, info, n)
    Uma função de derivação criptográfica de chave que recebe algum material de chave de entrada
    ikm (que deve ter boa entropia, mas não é necessário ser uma string aleatória uniforme),
    um sal de comprimento 32 bytes, e um valor 'info' específico de contexto, e produz uma saída
    de n bytes adequada para uso como material de chave.

    Use HKDF conforme especificado em [RFC-5869]_, usando a função hash HMAC SHA-256
    conforme especificado em [RFC-2104]_. Isso significa que SALT_LEN tem 32 bytes máx.

Formato
``````
O formato do LS2 criptografado consiste em três camadas aninhadas:

- Uma camada externa contendo as informações necessárias em texto claro para armazenamento e recuperação.
- Uma camada do meio que trata da autenticação do cliente.
- Uma camada interna que contém os dados reais do LS2.

O formato geral se parece com::

    Dados da Camada 0 + Enc(dados da camada 1 + Enc(dados da camada 2)) + Assinatura

Observe que o LS2 criptografado é ofuscado. O Destino não está no cabeçalho.
O local de armazenamento do DHT é SHA-256(sig type || chave pública ofuscada), e é rotacionado diariamente.

NÃO usa o cabeçalho LS2 padrão especificado acima.

#### Camada 0 (externa)
Tipo
    1 byte

    Não faz parte do cabeçalho, mas faz parte dos dados cobertos pela assinatura.
    Tire do campo na Mensagem de Armazenamento de Banco de Dados.

Tipo de Assinatura da Chave Pública Ofuscada
    2 bytes, big endian
    Isto será sempre do tipo 11, identificando uma chave ofuscada Red25519.

Chave Pública Ofuscada
    Comprimento conforme indicado pelo tipo de assinatura

Timestamp publicado
    4 bytes, big endian

    Segundos desde a época, zera em 2106

Expira
    2 bytes, big endian

    Deslocamento do timestamp publicado em segundos, máximo de 18,2 horas

Flags
    2 bytes

    Ordem dos bits: 15 14 ... 3 2 1 0

    Bit 0: Se 0, sem chaves offline; se 1, chaves offline

    Outros bits: definidos para 0 para compatibilidade com usos futuros

Dados de chave transitória
    Presente se o flag indicar chaves offline

    Timestamp de expiração
        4 bytes, big endian

        Segundos desde a época, zera em 2106

    Tipo de assinatura transitório
        2 bytes, big endian

    Chave pública de assinatura transitória
        Comprimento conforme indicado pelo tipo de assinatura

    Assinatura
        Comprimento conforme indicado pelo tipo de assinatura da chave pública ofuscada

        Sobre timestamp de expiração, tipo de assinatura transitório e chave pública.

        Verificado com a chave pública ofuscada.

lenOuterCiphertext
    2 bytes, big endian

outerCiphertext
    lenOuterCiphertext bytes

    Dados da camada 1 criptografados. Veja abaixo os algoritmos de derivação de chave e criptografia.

Assinatura
    Comprimento conforme indicado pelo tipo de assinatura da chave usada

    A assinatura é de tudo acima.

    Se o flag indicar chaves offline, a assinatura é verificada com a chave pública
    transitória. Caso contrário, a assinatura é verificada com a chave pública ofuscada.

#### Camada 1 (meio)
Flags
    1 byte
    
    Ordem dos bits: 76543210

    Bit 0: 0 para todos, 1 para por-cliente, seção de autorização a seguir

    Bits 3-1: Esquema de autenticação, apenas se o bit 0 estiver definido como 1 para por-cliente, caso contrário 000
              000: Autenticação de cliente DH (ou nenhuma autenticação por-cliente)
              001: Autenticação de cliente PSK

    Bits 7-4: Não utilizados, definidos como 0 para compatibilidade futura

Dados de autenticação de cliente DH
    Presente se o flag bit 0 estiver definido como 1 e os bits 3-1 do flag estiverem definidos como 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Número de entradas authClient a seguir, 40 bytes cada

    authClient
        Dados de autorização para um único cliente.
        Veja abaixo o algoritmo de autorização de cliente por cliente.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Dados de autenticação de cliente PSK
    Presente se o flag bit 0 estiver definido como 1 e os bits 3-1 do flag estiverem definidos como 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Número de entradas authClient a seguir, 40 bytes cada

    authClient
        Dados de autorização para um único cliente.
        Veja abaixo o algoritmo de autorização de cliente por cliente.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

innerCiphertext
    Comprimento implícito pelo lenOuterCiphertext (qualquer dado restante)

    Dados da camada 2 criptografados. Veja abaixo os algoritmos de derivação de chave e criptografia.

#### Camada 2 (interna)
Tipo
    1 byte

    Ou 3 (LS2) ou 7 (Meta LS2)

Data
    Dados LeaseSet2 para o tipo dado.

    Inclui o cabeçalho e assinatura.

Derivação de Chave Ofuscante
`````````````````````````````

Usamos o seguinte esquema para ofuscamento de chaves,
baseado em Ed25519 e ZCash RedDSA [ZCASH]_.
As assinaturas Re25519 são sobre a curva Ed25519, usando SHA-512 para o hash.

Não usamos o apêndice A.2 do rend-spec-v3.txt do Tor [TOR-REND-SPEC-V3]_,
que tem objetivos de design semelhantes, porque suas chaves públicas
ofuscadas podem estar fora do subgrupo de ordem primo, com implicações de segurança desconhecidas.

#### Objetivos

- A chave pública de assinatura no destino não ofuscado deve ser
  Ed25519 (tipo de assinatura 7) ou Red25519 (tipo de assinatura 11);
  Nenhum outro tipo de assinatura é suportado
- Se a chave pública de assinatura está offline, a chave pública de assinatura transitória também deve ser Ed25519
- A ofuscamento deve ser computacionalmente simples
- Usar primitivas criptográficas existentes
- As chaves públicas ofuscadas não podem ser desofuscadas
- As chaves públicas ofuscadas devem estar na curva Ed25519 e no subgrupo de ordem primo
- Deve-se conhecer a chave pública de assinatura do destino
  (o destino completo não é necessário) para derivar a chave pública ofuscada
- Opcionalmente fornecer um segredo adicional necessário para derivar a chave pública ofuscada

#### Segurança

A segurança de um esquema de ofuscamento requer que
a distribuição de alfa seja a mesma que a das chaves privadas não ofuscadas.
No entanto, quando ofuscamos uma chave privada Ed25519 (tipo de assinatura 7)
para uma chave privada Red25519 (tipo de assinatura 11), a distribuição é diferente.
Para atender aos requisitos da seção 4.1.6.1 do zcash [ZCASH]_,
deve-se usar Red25519 (tipo de assinatura 11) para as chaves não ofuscadas também, para que
"a combinação de uma chave pública re-randomizada e assinaturas(s)
sob essa chave não revele a chave da qual foi re-randomizada."
Permitimos o tipo 7 para destinos existentes, mas recomendamos o
tipo 11 para novos destinos que serão criptografados.

#### Definições

B
    O ponto base (gerador) Ed25519 2^255 - 19 como em [ED25519-REFS]_

L
    A ordem Ed25519 2^252 + 27742317777372353535851937790883648493
    conforme em [ED25519-REFS]_

DERIVE_PUBLIC(a)
    Converta uma chave privada para pública, como em Ed25519 (multiplicação por G)

alpha
    Um número aleatório de 32 bytes conhecido para aqueles que conhecem o destino.

GENERATE_ALPHA(destination, date, secret)
    Gerar alfa para a data atual, para aqueles que conhecem o destino e o segredo.
    O resultado deve ter a mesma distribuição das chaves privadas Ed25519.

a
    A chave privada de assinatura de 32 bytes não ofuscada EdDSA ou RedDSA usada para assinar o destino

A
    A chave pública de assinatura de 32 bytes não ofuscada EdDSA ou RedDSA no destino,
    = DERIVE_PUBLIC(a), como em Ed25519

a'
    A chave privada de assinatura de 32 bytes ofuscada EdDSA usada para assinar o leaseset criptografado
    Esta é uma chave privada EdDSA válida.

A'
    A chave pública de assinatura de 32 bytes ofuscada EdDSA no Destino,
    pode ser gerada com DERIVE_PUBLIC(a'), ou de A e alpha.
    Esta é uma chave pública EdDSA válida, na curva e no subgrupo de ordem primo.

LEOS2IP(x)
    Inverter a ordem dos bytes de entrada para little-endian

H*(x)
    32 bytes = (LEOS2IP(SHA512(x))) mod B, o mesmo que no hash-e-reduzir Ed25519

#### Cálculos de Ofuscamento

Uma nova alfa secreta e chaves ofuscadas devem ser geradas a cada dia (UTC).
O alfa secreto e as chaves ofuscadas são calculados da seguinte forma.

GENERATE_ALPHA(destination, date, secret), para todas as partes:

  ```text
  // GENERATE_ALPHA(destination, date, secret)

  // secret é opcional, caso contrário, comprimento zero
  A = chave pública de assinatura do destino
  stA = tipo de assinatura de A, 2 bytes big endian (0x0007 ou 0x000b)
  stA' = tipo de assinatura de chave pública ofuscada A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD da data atual UTC
  secret = string codificada em UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // tratar seed como um valor de 64 bytes little-endian
  alpha = seed mod L
```

BLIND_PRIVKEY(), para o proprietário que publica o leaseset:

  ```text
  // BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // Se para uma chave privada Ed25519 (tipo 7)
  seed = chave privada de assinatura do destino
  a = metade esquerda de SHA512(seed) e fixada como de costume para Ed25519
  // caso contrário, para uma chave privada Red25519 (tipo 11)
  a = chave privada de assinatura do destino
  // Adição usando aritmética de escalar
  chave de assinatura ofuscada a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  chave pública de assinatura ofuscada = A' = DERIVE_PUBLIC(a')
```

BLIND_PUBKEY(), para os clientes que recuperam o leaseset:

  ```text
  // BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = chave pública de assinatura do destino
  // Adição usando elementos do grupo (pontos na curva)
  chave pública ofuscada = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```

Ambos os métodos de cálculo de A' fornecem o mesmo resultado, conforme necessário.

#### Assinatura

O leaseset não ofuscado é assinado pela chave privada de assinatura Ed25519 ou Red25519 não ofuscada
e verificado com a chave pública de assinatura Ed25519 ou Red25519 não ofuscada (tipos de assinatura 7 ou 11) como de costume.

Se a chave pública de assinatura estiver offline,
o leaseset não ofuscado é assinado pela chave privada de assinatura transitória Ed25519 ou Red25519 não ofuscada
e verificado com a chave pública de assinatura transitória Ed25519 ou Red25519 não ofuscada (tipos de assinatura 7 ou 11) como de costume.
Veja abaixo notas adicionais sobre chaves offline para leasesets criptografados.

Para assinatura do leaseset criptografado, usamos Red25519, baseado no RedDSA [ZCASH]_
para assinar e verificar com chaves ofuscadas.
As assinaturas Red25519 são sobre a curva Ed25519, usando SHA-512 para o hash.

Red25519 é idêntico ao Ed25519 exceto conforme especificado abaixo.

#### Cálculos de Assinatura/Verificação

A parte exterior do leaseset criptografado usa chaves e assinaturas Red25519.

Red25519 é quase idêntico ao Ed25519. Há duas diferenças:

As chaves privadas Red25519 são geradas a partir de números aleatórios e depois devem ser reduzidas mod L, onde L é definido acima.
As chaves privadas Ed25519 são geradas a partir de números aleatórios e depois "fixadas" usando
mascaramento de bits para bytes 0 e 31. Isso não é feito para Red25519.
As funções GENERATE_ALPHA() e BLIND_PRIVKEY() definidas acima geram chaves privadas Red25519 apropriadas usando mod L.

No Red25519, o cálculo de r para assinatura usa dados aleatórios adicionais,
e usa o valor da chave pública em vez do hash da chave privada.
Devido aos dados aleatórios, cada assinatura Red25519 é diferente, mesmo
quando assinando os mesmos dados com a mesma chave.

Assinatura:

  ```text
  T = 80 bytes aleatórios
  r = H*(T || chave pública || mensagem)
  // resto é o mesmo que no Ed25519
```

Verificação:

  ```text
  // igual ao Ed25519
```

Processamento e Criptografia
```````````````````````````
#### Derivação de subcredenciais
Como parte do processo de ofuscamento, precisamos garantir que um LS2 criptografado só possa ser
decriptografado por alguém que conheça a chave pública de assinatura correspondente do Destino.
O Destino completo não é necessário.
Para alcançar isso, derivamos uma credencial da chave pública de assinatura:

  ```text
  A = chave pública de assinatura do destino
  stA = tipo de assinatura de A, 2 bytes big endian (0x0007 ou 0x000b)
  stA' = tipo de assinatura de A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```

A string de personalização garante que a credencial não colida com qualquer hash usado
como uma chave de pesquisa DHT, como o hash de Destino simples.

Para uma chave ofuscada dada, então podemos derivar uma subcredencial:

  ```text
  subcredential = H("subcredential", credential || chavePublicaOfuscada)
```

A subcredencial é incluída nos processos de derivação de chave abaixo, que vincula essas
chaves ao conhecimento da chave pública de assinatura do Destino.

#### Criptografia de Camada 1
Primeiro, a entrada para o processo de derivação de chave é preparada:

  ```text
  outerInput = subcredential || publishedTimestamp
```

Em seguida, um sal aleatório é gerado:

  ```text
  outerSalt = CSRNG(32)
```

Então a chave usada para criptografar a camada 1 é derivada:

  ```text
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Finalmente, o plaintext da camada 1 é criptografado e serializado:

  ```text
  outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```

#### Decriptação de Camada 1
O sal é analisado do ciphertext da camada 1:

  ```text
  outerSalt = outerCiphertext[0:31]
```

Então a chave usada para criptografar a camada 1 é derivada:

  ```text
  outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Finalmente, o ciphertext da camada 1 é decriptografado:

  ```text
  outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```

#### Criptografia de Camada 2
Quando a autenticação cliente está ativada, ``authCookie`` é calculado conforme descrito abaixo.
Quando a autenticação de cliente está desativada, ``authCookie`` é a matriz de bytes de comprimento zero.

A criptografia prossegue de uma maneira semelhante à camada 1:

  ```text
  innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```

#### Decriptação de Camada 2
Quando a autenticação de cliente está ativada, ``authCookie`` é calculado conforme descrito abaixo.
Quando a autenticação de cliente está desativada, ``authCookie`` é a matriz de bytes de comprimento zero.

A decriptação prossegue de uma forma semelhante à camada 1:

  ```text
  innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```

Autorização por cliente
```````````````````````
Quando a autorização por cliente está ativada para um Destino, o servidor mantém uma lista de
clientes que autoriza para decriptografar os dados do LS2 criptografado. Os dados armazenados por cliente
dependem do mecanismo de autorização, e incluem algum tipo de material de chave que cada
cliente gera e envia para o servidor via um mecanismo seguro fora de banda.

Existem duas alternativas para implementar a autorização por cliente:

#### Autorização de cliente DH
Cada cliente gera um par de chaves DH ``[csk_i, cpk_i]`` e envia a chave pública ``cpk_i``
para o servidor.

Processamento no servidor
^^^^^^^^^^^^^^^^^^^^^^^^
O servidor gera um novo ``authCookie`` e um par de chaves DH efêmero:

  ```text
  authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```

Então, para cada cliente autorizado, o servidor criptografa ``authCookie`` para sua chave pública:

  ```text
  sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

O servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` na camada 1 do
LS2 criptografado, junto com ``epk``.

Processamento no cliente
^^^^^^^^^^^^^^^^^^^^^^^^^
O cliente usa sua chave privada para derivar seu identificador esperado `clientID_i`,
chave de criptografia ``clientKey_i`` e IV de criptografia ``clientIV_i``:

  ```text
  sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Então o cliente procura nos dados de autorização da camada 1 por uma entrada que contenha
``clientID_i``. Se uma entrada correspondente existir, o cliente a decripta para obter
``authCookie``:

  ```text
  authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Autorização de cliente com chave pré-compartilhada (PSK)
Cada cliente gera uma chave secreta de 32 bytes ``psk_i`` e a envia para o servidor.
Alternativamente, o servidor pode gerar a chave secreta e enviá-la para um ou mais clientes.

Processamento no servidor
^^^^^^^^^^^^^^^^^^^^^^^^
O servidor gera um novo ``authCookie`` e sal:

  ```text
  authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```

Então, para cada cliente autorizado, o servidor criptografa ``authCookie`` para sua chave pré-compartilhada:

  ```text
  authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

O servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` na camada 1 do
LS2 criptografado, junto com ``authSalt``.

Processamento no cliente
^^^^^^^^^^^^^^^^^^^^^^^^
O cliente usa sua chave pré-compartilhada para derivar seu identificador esperado `clientID_i`,
chave de criptografia ``clientKey_i`` e IV de criptografia ``clientIV_i``:

  ```text
  authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Então o cliente procura nos dados de autorização da camada 1 por uma entrada que contenha
``clientID_i``. Se uma entrada correspondente existir, o cliente a decripta para obter
``authCookie``:

  ```text
  authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Considerações de segurança
Ambos os mecanismos de autorização de clientes acima proporcionam privacidade para a associação de clientes.
Uma entidade que só conhece o Destino pode ver quantos clientes estão inscritos a qualquer
momento, mas não pode rastrear quais clientes estão sendo adicionados ou revogados.

Os servidores DEVEM randomizar a ordem dos clientes sempre que gerarem um LS2 criptografado,
para evitar que os clientes aprendam sua posição na lista e inferem quando outros clientes foram
adicionados ou revogados.

Um servidor PODE escolher ocultar o número de clientes que estão inscritos, inserindo entradas
aleatórias na lista de dados de autorização.

Vantagens da autorização de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A segurança do esquema não depende exclusivamente da troca fora de banda de material de chave
  do cliente. A chave privada do cliente nunca precisa sair do dispositivo, e assim um
  adversário que seja capaz de interceptar a troca fora de banda, mas não quebrar o algoritmo DH,
  não pode decriptar o LS2 criptografado, nem determinar por quanto tempo o cliente tem acesso.

Desvantagens da autorização de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Requer N + 1 operações DH do lado do servidor para N clientes.
- Exige uma operação DH no lado do cliente.
- Requer que o cliente gere a chave secreta.

Vantagens da autorização de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Não requer operações DH.
- Permite que o servidor gere a chave secreta.
- Permite que o servidor compartilhe a mesma chave com vários clientes, se desejado.

Desvantagens da autorização de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- A segurança do esquema depende criticamente da troca fora de banda de material de chave
  de cliente. Um adversário que intercepte a troca para um cliente particular pode
  decriptar qualquer LS2 criptografado subsequente para o qual esse cliente esteja autorizado, bem como determinar
  quando o acesso do cliente é revogado.

LS Criptografado com Endereços Base 32
``````````````````````````````````````

Veja a proposta 149.

Você não pode usar um LS2 criptografado para bittorrent, por causa das respostas de anúncio compactas que são 32 bytes.
Os 32 bytes contêm apenas o hash. Não há espaço para uma indicação de que o
leaseset é criptografado ou os tipos de assinatura.

LS Criptografado com Chaves Offline
```````````````````````````````````
Para leasesets criptografados com chaves offline, as chaves privadas ofuscadas devem também ser geradas offline,
uma para cada dia.

Como o bloco de assinatura offline opcional está na parte não criptografada do leaseset criptografado,
qualquer pessoa vasculhando os floodfills poderia usar isso para rastrear o leaseset (mas não decriptá-lo)
durante vários dias.
Para evitar isso, o proprietário das chaves deve gerar novas chaves transitórias
para cada dia também.
Tanto as chaves transitórias quanto as ofuscadas podem ser geradas antecipadamente, e entregues ao roteador
em lote.

Não há formato de arquivo definido nesta proposta para empacotar várias chaves transitórias e
ofuscadas e fornecê-las ao cliente ou roteador.
Não há aprimoramento no protocolo I2CP definido nesta proposta para suportar
leasesets criptografados com chaves offline.

Notas
`````

- Um serviço usando leasesets criptografados publicaria a versão criptografada para os
  floodfills. No entanto, para eficiência, enviaria leasesets não criptografados para
  clientes na mensagem garlic, uma vez autenticados (via whitelist, por
  exemplo).

- Floodfills podem limitar o tamanho máximo para um valor razoável para evitar abuso.

- Após a decriptação, várias verificações devem ser feitas, incluindo se
  o timestamp interno e a expiração correspondem aos do nível superior.

- ChaCha20 foi selecionado em vez de AES. Embora as velocidades sejam semelhantes caso o
  suporte de hardware AES esteja disponível, ChaCha20 é 2,5-3x mais rápido quando
  o suporte de hardware AES não está disponível, como em dispositivos ARM de menor capacidade.

- Não nos importamos o suficiente com a velocidade para usar BLAKE2b com chaveamento. Tem um tamanho
  de saída grande o suficiente para acomodar o maior n que precisamos (ou podemos chamá-lo uma vez por
  chave desejada com um argumento contador). BLAKE2b é muito mais rápido que SHA-256,
  e BLAKE2b com chaveamento reduziria o número total de chamadas de funções de hash.
  No entanto, veja a proposta 148, onde é proposto que mudemos para BLAKE2b por outras razões.
  [UNSCIENTIFIC-KDF-SPEEDS]_

### Meta LS2

Isso é usado para substituir o multihoming. Como qualquer leaseset, isso é assinado pelo
criador. Esta é uma lista autenticada de hashes de destino.

O Meta LS2 é o topo, e possivelmente nós intermediários,
de uma estrutura de árvore.
Contém vários registros, cada um apontando para um LS, LS2, ou outro Meta LS2
para suportar multihoming massivo.
Um Meta LS2 pode conter uma mistura de registros LS, LS2 e Meta LS2.
As folhas da árvore são sempre um LS ou LS2.
A árvore é um DAG; loops são proibidos; clientes fazendo pesquisas devem detectar e
recusar-se a seguir loops.

Um Meta LS2 pode ter uma expiração muito mais longa que um LS ou LS2 padrão.
O nível superior pode ter uma expiração de várias horas após a data de publicação.
O tempo máximo de expiração será imposto por floodfills e clientes, e está por definir.

O caso de uso para Meta LS2 é multihoming massivo, mas sem mais
proteção para correlação de roteadores a leasesets (no momento de reinício do roteador) do que
é fornecido agora com LS ou LS2.
Isso é equivalente ao caso de uso "facebook", que provavelmente não precisa de
proteção de correlação. Este caso de uso provavelmente precisa de chaves offline,
que são fornecidas no cabeçalho padrão em cada nó da árvore.

O protocolo de backend para coordenação entre os roteadores das folhas, intermediários e mestres dos Metas LS
não é especificado aqui. Os requisitos são extremamente simples - apenas verificar se o colega está ativo,
e publicar um novo LS a cada poucas horas. A única complexidade é para escolher novos
publicadores para o LS Meta de nível superior ou intermediário em caso de falha.

Leasesets mistos e combinados, onde leases de vários roteadores são combinados, assinados e publicados
em um único leaseset, está documentado na proposta 140, "multihoming invisível".
Esta proposta é inviável conforme escrita, porque conexões de streaming não seriam
"grudadas" em um único roteador, veja http://zzz.i2p/topics/2335.

O protocolo de backend, e a interação com o roteador e clientes internos, seria
bastante complexo para multihoming invisível.

Para evitar sobrecarregar o floodfill para o LS Meta de nível superior, a expiração deve
ser de várias horas pelo menos. Clientes devem armazenar em cache o LS Meta nível superior, e persistí-lo
através de reinícios se não estiver expirado.

Precisamos definir algum algoritmo para os clientes percorrerem a árvore, incluindo fallback,
para que o uso seja disperso. Alguma função de distância de hash, custo, e aleatoriedade.
Se um nó tem ambos LS ou LS2 e Meta LS, precisamos saber quando está permitido
usar esses leasesets, e quando continuar percorrendo a árvore.

Pesquise com
    Flag LS padrão (1)
Armazene com
    Tipo Meta LS2 (7)
Armazene em
    Hash do destino
    Este hash é então usado para gerar a "chave de roteamento" diária, como em LS1
Expiração típica
    Horas. Máximo de 18,2 horas (65535 segundos)
Publicado por
    Destino "mestre" ou coordenador, ou coordenadores intermediários

Formato
``````
::

  Cabeçalho LS2 Padrão conforme especificado acima

  Parte Específica do Tipo Meta LS2
  - Propriedades (mapeamento conforme especificado na especificação de estruturas comuns, 2 bytes zero se não houver)
  - Número de entradas (1 byte) Máximo TBD
  - Entradas. Cada entrada contém: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Defina todos como zero para compatibilidade com usos futuros.
    - Tipo (1 byte) O tipo de LS ao qual está se referindo;
      1 para LS, 3 para LS2, 5 para criptografado, 7 para meta, 0 para desconhecido.
    - Custo (prioridade) (1 byte)
    - Expira (4 bytes) (4 bytes, big endian, segundos desde a época, zera em 2106)
  - Número de revogações (1 byte) Máximo TBD
  - Revogações: Cada revogação contém: (32 bytes)
    - Hash (32 bytes)

  Assinatura LS2 Padrão:
  - Assinatura (40+ bytes)
    A assinatura é de tudo acima.

Flags e propriedades: para uso futuro

Notas
`````
- Um serviço distribuído usando isso teria um ou mais "mestres" com a
  chave privada do destino do serviço. Eles (fora de banda) determinariam a
  lista atual de destinos ativos e publicariam o Meta LS2. Para
  redundância, vários mestres poderiam usar multihoming (ou seja, publicar simultaneamente) o
  Meta LS2.

- Um serviço distribuído poderia começar com um único destino ou usar multihoming no estilo antigo,
  então, fazer a transição para um Meta LS2. Uma pesquisa de LS padrão poderia retornar
  qualquer um de um LS, LS2 ou Meta LS2.

- Quando um serviço usa um Meta LS2, ele não tem túneis (leases).

### Registro de Serviço

Este é um registro individual que indica que um destino está participando de um
serviço. É enviado do participante para o floodfill. Nunca é enviado
individualmente por um floodfill, mas apenas como parte de uma Lista de Serviço. O Registro de
Serviço também é usado para revogar a participação em um serviço, definindo a
expiração para zero.

Este não é um LS2, mas usa o formato de cabeçalho e assinatura LS2 padrão.

Pesquise com
    n/a, veja Lista de Serviço
Armazene com
    Tipo Registro de Serviço (9)
Armazene em
    Hash do nome do serviço
    Este hash é então usado para gerar a "chave de roteamento" diária, como em LS1
Expiração típica
    Horas. Máximo de 18,2 horas (65535 segundos)
Publicado por
    Destino

Formato
``````
::

  Cabeçalho LS2 Padrão conforme especificado acima

  Parte Específica do Tipo Registro de Serviço
  - Porta (2 bytes, big endian) (0 se não especificado)
  - Hash do nome do serviço (32 bytes)

  Assinatura LS2 Padrão:
  - Assinatura (40+ bytes)
    A assinatura é de tudo acima.

Notas
`````
- Se expirar for tudo zero, o floodfill deve revogar o registro e não mais
  incluí-lo na lista de serviço.

- Armazenamento: O floodfill pode limitar estritamente o armazenamento desses registros e
  limitar o número de registros armazenados por hash e sua expiração. Uma lista
  branca de hashes também pode ser usada.

- Qualquer outro tipo netdb no mesmo hash tem prioridade, portanto, um registro de serviço jamais pode
  sobrescrever um LS/RI, mas um LS/RI sobrescreverá todos os registros de serviço naquele hash.

### Lista de Serviço

Isso não é nada como um LS2 e usa um formato diferente.

A lista de serviços é criada e assinada pelo floodfill. É não autenticada
no sentido de que qualquer um pode se juntar a um serviço publicando um Registro de Serviço para um
floodfill.

Uma Lista de Serviço contém Registros de Serviço Curto, não Registros de Serviço completos. Estes
contêm assinaturas, mas apenas hashes, não destinos completos, por isso não podem ser
verificados sem o destino completo.

A segurança, se houver, e a desejabilidade das listas de serviços é TBD.
Floodfills poderiam limitar a publicação e as pesquisas a uma lista branca de serviços,
mas essa lista branca pode variar com base na implementação, ou preferência do operador.
Pode não ser possível alcançar consenso sobre uma lista branca comum, base
entre implementações.

Se o nome do serviço for incluído no registro de serviço acima,
então os operadores de floodfill podem se opor; se apenas o hash for incluído,
não há verificação, e um registro de serviço poderia "entrar" antes de
qualquer outro tipo netdb e ser armazenado no floodfill.

Pesquise com
    Tipo de pesquisa Lista de Serviço (11)
Armazene com
    Tipo de armazenamento Lista de Serviço (11)
Armazene em
    Hash do nome do serviço
    Este hash é então usado para gerar a "chave de roteamento" diária, como em LS1
Expiração típica
    Horas, não especificada na lista em si, até política local
Publicado por
    Ninguém, nunca enviado ao floodfill, nunca inundado.

Formato
``````
NÃO usa o cabeçalho LS2 padrão especificado acima.

::

  - Tipo (1 byte)
    Não está realmente no cabeçalho, mas faz parte dos dados cobertos pela assinatura.
    Tire do campo na Mensagem de Armazenamento de Banco de Dados.
  - Hash do nome do serviço (implícito, na mensagem Store Database)
  - Hash do Criador (floodfill) (32 bytes)
  - Timestamp publicado (8 bytes, big endian)

  - Número de Registros de Serviço Curto (1 byte)
  - Lista de Registros de Serviço Curto:
    Cada Registro de Serviço Curto contém (90+ bytes)
    - Hash do Dest a (32 bytes)
    - Timestamp publicado (8 bytes, big endian)
    - Expira (4 bytes, big endian) (offset de publicado em ms)
    - Flags (2 bytes)
    - Porta (2 bytes, big endian)
    - Comprimento da assinatura (2 bytes, big endian)
    - Assinatura do dest (40+ bytes)

  - Número de Registros de Revogação (1 byte)
  - Lista de Registros de Revogação:
    Cada Registro de Revogação contém (86+ bytes)
    - Hash do Dest a (32 bytes)
    - Timestamp publicado (8 bytes, big endian)
    - Flags (2 bytes)
    - Porta (2 bytes, big endian)
    - Comprimento da assinatura (2 bytes, big endian)
    - Assinatura do dest (40+ bytes)

  - Assinatura do floodfill (40+ bytes)
    A assinatura é de tudo acima.

Para verificar a assinatura da Lista de Serviço:

- prepend o hash do nome do serviço
- remover o hash do criador
- Verificar assinatura do conteúdo modificado

Para verificar a assinatura de cada Registro de Serviço Curto:

- Buscar destino
- Verificar assinatura de (timestamp publicado + expira + flags + porta + Hash do
  nome do serviço)

Para verificar a assinatura de cada Registro de Revogação:

- Buscar destino
- Verificar assinatura de (timestamp publicado + 4 bytes zero + flags + porta + Hash
  do nome do serviço)

Notas
`````
- Usamos comprimento de assinatura em vez de tipo de assinatura para que possamos suportar tipos de assinaturas desconhecidos.

- Não há expiração de uma lista de serviço, destinatários podem tomar suas próprias
  decisões com base em políticas ou na expiração dos registros individuais.

- Listas de Serviço não são inundadas, apenas Registros de Serviço individuais são. Cada
  floodfill cria, assina e armazena em cache uma Lista de Serviço. O floodfill usa sua
  própria política para o tempo em cache e o número máximo de registros de serviço e de revogação.

## Alterações requeridas na especificação de Estruturas Comuns

### Certificados de Chave

Fora do escopo para esta proposta.
Adicione às propostas ECIES 144 e 145.

### Novas Estruturas Intermediárias

Adicione novas estruturas para Lease2, MetaLease, LeaseSet2Header e OfflineSignature.
Efeito a partir da versão 0.9.38.

### Novos tipos NetDB

Adicione estruturas para cada novo tipo de leaseset, incorporado do acima.
Para LeaseSet2, EncryptedLeaseSet e MetaLeaseSet,
efeito a partir da versão 0.9.38.
Para Registro de Serviço e Lista de Serviço,
preliminar e sem previsão.

### Novo Tipo de Assinatura

Adicione RedDSA_SHA512_Ed25519 Tipo 11.
Chave pública é 32 bytes; chave privada é 32 bytes; hash é 64 bytes; assinatura é 64 bytes.

## Alterações na Especificação de Criptografia Requeridas

Fora do escopo para esta proposta.
Veja as propostas 144 e 145.

## Alterações necessárias no I2NP

Adicionar nota: LS2 só pode ser publicado para floodfills com uma versão mínima.

### Mensagem de Pesquisa de Banco de Dados

Adicione o tipo de pesquisa de lista de serviço.

Alterações
```````
::

  Byte Flags: campo de tipo de pesquisa, atualmente bits 3-2, expande para bits 4-2.
  Tipo de pesquisa 0x04 é definido como o tipo de pesquisa de lista de serviço.

  Adicione nota: A pesquisa de lista de serviço só pode ser enviada para floodfills com uma versão mínima.
  A versão mínima é 0.9.38.

### Mensagem de Armazenamento de Banco de Dados

Adicione todos os novos tipos de armazenamento.

Alterações
```````
::

  Byte de Tipo: campo de Tipo, atualmente bit 0, expande para bits 3-0.
  Tipo 3 é definido como um armazenamento LS2.
  Tipo 5 é definido como um armazenamento LS2 criptografado.
  Tipo 7 é definido como um armazenamento meta LS2.
  Tipo 9 é definido como um armazenamento de registro de serviço.
  Tipo 11 é definido como um armazenamento de lista de serviço.
  Outros tipos são indefinidos e inválidos.

  Adicione nota: Todos os novos tipos só podem ser publicados em floodfills com uma versão mínima.
  A versão mínima é 0.9.38.

## Alterações necessárias no I2CP

### Opções I2CP

Novas opções interpretadas pelo lado do roteador, enviadas no Mapeamento de Configuração de Sessão:

::

  i2cp.leaseSetType=nnn       O tipo de leaseset a ser enviado na Mensagem de Criação de Leaseset
                              O valor é o mesmo do tipo de armazenamento netdb na tabela acima.
                              Interpretado pelo lado do cliente, mas também passado para o roteador na
                              Configuração da Sessão, para declarar intenção e verificar suporte.

  i2cp.leaseSetEncType=nnn[,nnn]  Os tipos de criptografia a serem usados.
                                  Interpretado pelo lado do cliente, mas também passado para o roteador na
                                  Configuração da Sessão, para declarar intenção e verificar suporte.
                                  Veja as propostas 144 e 145.

  i2cp.leaseSetOfflineExpiration=nnn  A expiração da assinatura offline, ASCII,
                                      segundos desde a época.

  i2cp.leaseSetTransientPublicKey=[type:]b64  O base 64 da chave privada transitória,
                                              prefixado por um número de tipo de assinatura opcional
                                              ou nome, padrão DSA_SHA1.
                                              Comprimento conforme inferido pelo tipo de assinatura

  i2cp.leaseSetOfflineSignature=b64   O base 64 da assinatura offline.
                                      Comprimento conforme inferido pelo tipo de chave de assinatura do destino

  i2cp.leaseSetSecret=b64     O base 64 de um segredo utilizado para ofuscar o
                              endereço do leaseset, padrão ""

  i2cp.leaseSetAuthType=nnn   O tipo de autenticação para LS2 criptografado.
                              0 para nenhuma autenticação por cliente (o padrão)
                              1 para autenticação por cliente DH
                              2 para autenticação por cliente PSK

  i2cp.leaseSetPrivKey=b64    Uma chave privada base 64 para o roteador usar para
                              decriptar o LS2 criptografado,
                              apenas se a autenticação por cliente estiver habilitada

Novas opções interpretadas pelo lado do cliente:

::

  i2cp.leaseSetType=nnn     O tipo de leaseset a ser enviado na Mensagem de Criação de Leaseset
                            O valor é o mesmo do tipo de armazenamento netdb na tabela acima.
                            Interpretada pelo lado do cliente, mas também passada para o roteador na
                            Configuração da Sessão, para declarar intenção e verificar suporte.

  i2cp.leaseSetEncType=nnn[,nnn]  Os tipos de criptografia a serem usados.
                                  Interpretada pelo lado do cliente, mas também passada para o roteador na
                                  Configuração da Sessão, para declarar intenção e verificar suporte.
                                  Veja as propostas 144 e 145.

  i2cp.leaseSetSecret=b64     O base 64 de um segredo utilizado para ofuscar o
                              endereço do leaseset, padrão ""

  i2cp.leaseSetAuthType=nnn       O tipo de autenticação para LS2 criptografado.
                                  0 para nenhuma autenticação por cliente (o padrão)
                                  1 para autenticação por cliente DH
                                  2 para autenticação por cliente PSK

  i2cp.leaseSetBlindedType=nnn   O tipo de assinatura da chave ofuscada para LS2 criptografado.
                                 O padrão depende do tipo de assinatura do destino.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   O base 64 do nome do cliente (ignorado, uso somente UI),
                                                 seguido por ':', seguido pelo base 64 da chave pública
                                                 a ser usada para autenticação por cliente DH. nnn começa em 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   O base 64 do nome do cliente (ignorado, uso somente UI),
                                                   seguido por ':', seguido pelo base 64 da chave privada
                                                   a ser usada para autenticação por cliente PSK. nnn começa em 0

### Configuração da Sessão

Note que para assinaturas offline, as opções
i2cp.leaseSetOfflineExpiration,
i2cp.leaseSetTransientPublicKey, e
i2cp.leaseSetOfflineSignature são obrigatórias,
e a assinatura é pela chave privada de assinatura transitória.

### Mensagem de Solicitação de Leaseset

Roteador para cliente.
Sem mudanças.
Os leases são enviados com timestamps de 8 bytes, mesmo que o
leaseset retornado seja um LS2 com timestamps de 4 bytes.
Note que a resposta pode ser uma Mensagem Create Leaseset ou Create Leaseset2.

### Mensagem de Solicitação de Leaseset Variável

Roteador para cliente.
Sem mudanças.
Os leases são enviados com timestamps de 8 bytes, mesmo que o
leaseset retornado seja um LS2 com timestamps de 4 bytes.
Note que a resposta pode ser uma Mensagem Create Leaseset ou Create Leaseset2.

### Mensagem Create Leaseset2

Cliente para roteador.
Nova mensagem, para usar no lugar da Mensagem de Create Leaseset.

Justificação
`````````````

- Para que o roteador analise o tipo de armazenamento, o tipo deve estar na mensagem,
  a menos que seja passado para o roteador antes na config da sessão.
  Para facilitar a análise, é mais fácil ter na própria mensagem.

- Para que o roteador saiba o tipo e comprimento da chave privada,
  ela deve estar depois do lease set, a menos que o parser saiba o tipo antes na
  config da sessão.
  Para facilitar a análise, é mais fácil saber da própria mensagem.

- A chave privada de assinatura, previamente definida para revogação e não usada,
  não está presente no LS2.

Tipo de Mensagem
``````````````

O tipo de mensagem para a Mensagem Create Leaseset2 é 41.

Formato
``````

::

  ID de Sessão
  Byte Tipo: Tipo de lease set a seguir
             Tipo 1 é um LS
             Tipo 3 é um LS2
             Tipo 5 é um LS2 criptografado
             Tipo 7 é um meta LS2
  LeaseSet: tipo especificado acima
  Número de chaves privadas a seguir (1 byte)
  Chaves de criptografia privada: Para cada chave pública no lease set,
                           na mesma ordem
                           (Não presente para Meta LS2)
                           - Tipo de criptografia (2 bytes, big endian)
                           - Comprimento da chave de criptografia (2 bytes, big endian)
                           - Chave de criptografia (número de bytes especificado
