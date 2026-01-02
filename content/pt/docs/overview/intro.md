---
title: "Introdução ao I2P"
description: "Uma introdução menos técnica à rede anônima I2P"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## O que é o I2P?

O Invisible Internet Project (I2P) é uma camada de rede anônima que permite comunicação peer-to-peer resistente à censura. Conexões anônimas são alcançadas através da criptografia do tráfego do usuário e seu envio através de uma rede distribuída operada por voluntários ao redor do mundo.

## Funcionalidades Principais

### Anonymity

O I2P oculta tanto o remetente quanto o destinatário das mensagens. Ao contrário das conexões tradicionais de internet onde seu endereço IP fica visível para sites e serviços, o I2P usa múltiplas camadas de criptografia e roteamento para manter sua identidade privada.

### Decentralization

Não há autoridade central no I2P. A rede é mantida por voluntários que doam largura de banda e recursos computacionais. Isso a torna resistente à censura e a pontos únicos de falha.

### Anonimato

Todo o tráfego dentro do I2P é criptografado ponta a ponta. As mensagens são criptografadas múltiplas vezes conforme passam pela rede, semelhante a como o Tor funciona, mas com diferenças importantes na implementação.

## How It Works

### Descentralização

O I2P usa "tunnels" para rotear o tráfego. Quando você envia ou recebe dados:

1. Seu roteador cria um túnel de saída (para envio)
2. Seu roteador cria um túnel de entrada (para recebimento)
3. Mensagens são criptografadas e enviadas através de múltiplos roteadores
4. Cada roteador conhece apenas o salto anterior e o próximo, não o caminho completo

### Criptografia Ponta a Ponta

I2P aprimora o roteamento em cebola tradicional com "garlic routing":

- Múltiplas mensagens podem ser agrupadas juntas (como dentes em um bulbo de alho)
- Isso proporciona melhor desempenho e anonimato adicional
- Torna a análise de tráfego mais difícil

### Network Database

I2P mantém uma base de dados de rede distribuída contendo:

- Informações do roteador
- Endereços de destino (semelhante aos websites .i2p)
- Dados de roteamento criptografados

## Common Use Cases

### Túneis

Hospede ou visite sites que terminam em `.i2p` - estes são acessíveis apenas dentro da rede I2P e fornecem fortes garantias de anonimato tanto para os anfitriões quanto para os visitantes.

### Roteamento Garlic

Compartilhe arquivos anonimamente usando BitTorrent sobre I2P. Muitos aplicativos de torrent têm suporte I2P integrado.

### Base de Dados da Rede

Envie e receba e-mails anônimos usando I2P-Bote ou outras aplicações de e-mail projetadas para I2P.

### Messaging

Use IRC, mensagens instantâneas ou outras ferramentas de comunicação de forma privada através da rede I2P.

## Getting Started

Pronto para experimentar o I2P? Confira nossa [página de downloads](/downloads) para instalar o I2P no seu sistema.

Para mais detalhes técnicos, consulte a [Introdução Técnica](/docs/overview/tech-intro) ou explore a [documentação](/docs) completa.

## Como Funciona

- [Introdução Técnica](/docs/overview/tech-intro) - Conceitos técnicos mais profundos
- [Modelo de Ameaças](/docs/overview/threat-model) - Compreendendo o modelo de segurança do I2P
- [Comparação com Tor](/docs/overview/comparison) - Como o I2P difere do Tor
- [Criptografia](/docs/specs/cryptography) - Detalhes sobre os algoritmos criptográficos do I2P
