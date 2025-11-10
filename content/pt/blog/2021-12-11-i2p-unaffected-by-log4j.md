---
title: "O I2P não é afetado pela vulnerabilidade do log4j"
date: 2021-12-11
author: "idk, zzz"
description: "O I2P não utiliza log4j e, portanto, não é afetado pela CVE-2021-44228"
categories: ["security"]
---

O I2P não é afetado pela vulnerabilidade zero-day do log4j divulgada ontem, CVE-2021-44228. O I2P não usa log4j para geração de logs; no entanto, também foi necessário revisar nossas dependências quanto ao uso de log4j, especialmente o jetty. Essa revisão não revelou nenhuma vulnerabilidade.

Também foi importante verificar todos os nossos plugins. Os plugins podem trazer seus próprios sistemas de log, incluindo o log4j. Concluímos que a maioria dos plugins também não usa o log4j e que, entre os que usam, nenhum empregava uma versão vulnerável do log4j.

Não encontramos nenhuma dependência, plugin ou aplicativo vulnerável.

Incluímos um arquivo log4j.properties com o jetty para plugins que introduzem log4j. Este arquivo só tem efeito sobre plugins que usam o registro de logs do log4j internamente. Adicionamos a mitigação recomendada ao arquivo log4j.properties. Plugins que habilitam o log4j serão executados com a funcionalidade vulnerável desativada. Como não conseguimos encontrar nenhum uso de log4j 2.x em lugar algum, não temos planos de fazer um lançamento de emergência neste momento.
