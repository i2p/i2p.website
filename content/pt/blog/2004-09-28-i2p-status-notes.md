---
title: "Notas de status do I2P de 2004-09-28"
date: 2004-09-28
author: "jr"
description: "Atualização semanal de status do I2P abordando a implementação de um novo protocolo de transporte, a autodetecção de IP e o progresso do lançamento da versão 0.4.1"
categories: ["status"]
---

Oi, pessoal, é hora da atualização semanal

## Índice:

1. New transport
2. 0.4.1 status
3. ???

## 1) Novo transporte

O lançamento da versão 0.4.1 tem demorado mais do que o esperado, mas o novo protocolo de transporte e sua implementação já estão no ar com tudo o que foi planejado - detecção de IP, estabelecimento de conexão de baixo custo e uma interface mais simples para ajudar a depurar quando as conexões estão falhando. Isso foi feito descartando completamente o antigo protocolo de transporte e implementando um novo, embora ainda tenhamos os mesmos termos da moda (2048bit DH + STS, AES256/CBC/PKCS#5). Se você quiser examinar o protocolo, ele está na documentação. A nova implementação também está muito mais limpa, já que a versão antiga era apenas um amontoado de atualizações acumuladas ao longo do último ano.

De qualquer forma, há algumas coisas no novo código de detecção de IP que valem mencionar. O mais importante: é totalmente opcional - se você especificar um endereço IP na página de configuração (ou no próprio router.config), ele sempre usará esse endereço, não importa o que aconteça. Porém, se você deixar isso em branco, seu router permitirá que o primeiro par com quem entrar em contato lhe diga qual é o seu endereço IP e, então, passará a escutar nesse endereço (depois de adicionar isso ao seu próprio RouterInfo e colocá-lo na base de dados da rede). Bem, isso não é bem verdade - se você não tiver definido explicitamente um endereço IP, ele confiará em qualquer um para dizer em que endereço IP pode ser alcançado sempre que o par não tiver conexões. Portanto, se a sua conexão de internet reiniciar, talvez lhe atribuindo um novo endereço DHCP, seu router confiará no primeiro par que conseguir alcançar.

Sim, isso significa que não precisa mais de dyndns. Você ainda pode, é claro, continuar a usá-lo, mas não é necessário.

No entanto, isso não faz tudo o que você deseja - se você tiver um NAT ou firewall, saber seu endereço IP externo é apenas metade da batalha - você ainda precisa abrir a porta de entrada. Mas já é um começo.

(como observação, para pessoas que executam suas próprias redes I2P privadas ou simuladores, há um novo par de flags a ser definido i2np.tcp.allowLocal e i2np.tcp.tagFile)

## 2) 0.4.1 estado

Além dos itens no roteiro para a 0.4.1, quero incluir mais algumas coisas — tanto correções de bugs quanto atualizações de monitoramento da rede. Estou investigando, no momento, alguns problemas de churn de memória excessivo, e quero explorar algumas hipóteses sobre os problemas ocasionais de confiabilidade na rede, mas estaremos prontos para lançar a versão em breve, talvez na quinta-feira. Infelizmente, ela não será compatível com versões anteriores, então vai ser um pouco turbulento, mas, com o novo processo de atualização e a implementação de transporte mais tolerante, não deve ser tão ruim quanto as atualizações anteriores incompatíveis com versões anteriores.

## 3) ???

Sim, tivemos atualizações curtas nas últimas duas semanas, mas é porque estamos na linha de frente focados na implementação, e não em várias arquiteturas de alto nível. Eu poderia falar sobre os dados de profiling (análise de desempenho) ou sobre o cache de tags de conexão de 10.000 para o novo transporte, mas isso não é tão interessante. De qualquer forma, vocês podem ter mais coisas para discutir, então passem na reunião hoje à noite e soltem o verbo.

=jr
