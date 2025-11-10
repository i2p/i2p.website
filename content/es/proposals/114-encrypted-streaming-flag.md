---
title: "'Flag de Streaming Encriptado'"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Necesita-Investigación"
thread: "http://zzz.i2p/topics/1795"
---

## Resumen

Esta propuesta trata sobre la adición de un flag al streaming que especifique el tipo de
encriptación de extremo a extremo que se está utilizando.


## Motivación

Las aplicaciones con alta carga pueden enfrentar una escasez de etiquetas ElGamal/AES+SessionTags.


## Diseño

Agregar un nuevo flag en algún lugar dentro del protocolo de streaming. Si un paquete viene con
este flag significa que la carga útil está encriptada con AES mediante una clave proveniente de la clave privada y la clave pública del par. Eso permitiría eliminar la encriptación de ajo (ElGamal/AES) y el problema de escasez de etiquetas.

Puede establecerse por paquete o por flujo a través de SYN.
