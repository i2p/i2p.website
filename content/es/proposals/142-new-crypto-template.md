---
title: "Nuevo Propuesta de Plantilla de Cifrado"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
toc: true
---

## Resumen

Este documento describe cuestiones importantes a considerar al proponer
un reemplazo o adición a nuestro cifrado asimétrico ElGamal.

Este es un documento informativo.


## Motivación

ElGamal es antiguo y lento, y existen mejores alternativas.
Sin embargo, hay varios problemas que deben ser abordados antes de poder añadir o cambiar a cualquier nuevo algoritmo.
Este documento destaca estos problemas no resueltos.


## Investigación de Antecedentes

Cualquiera que proponga nueva criptografía debe primero estar familiarizado con los siguientes documentos:

- [Propuesta 111 NTCP2](/es/proposals/111-ntcp-2/)
- [Propuesta 123 LS2](/es/proposals/123-new-netdb-entries/)
- [Propuesta 136 tipos de firma experimentales](/es/proposals/136-experimental-sigtypes/)
- [Propuesta 137 tipos de firma opcionales](/es/proposals/137-optional-sigtypes/)
- Hilos de discusión aquí para cada una de las propuestas anteriores, enlazados dentro
- [prioridades de propuestas 2018](http://zzz.i2p/topics/2494)
- [propuesta ECIES](http://zzz.i2p/topics/2418)
- [nuevo resumen de criptografía asimétrica](http://zzz.i2p/topics/1768)
- [Resumen de criptografía de bajo nivel](/es/docs/specs/common-structures/)


## Usos de Criptografía Asimétrica

Como repaso, usamos ElGamal para:

1) Mensajes de construcción de túnel (la clave está en RouterIdentity)

2) Cifrado entre enrutadores de netdb y otros mensajes I2NP (la clave está en RouterIdentity)

3) Cifrado de extremo a extremo del cliente ElGamal+AES/SessionTag (la clave está en LeaseSet, la clave de Destino no se usa)

4) DH efímero para NTCP y SSU


## Diseño

Cualquier propuesta para reemplazar ElGamal con otra cosa debe proporcionar los siguientes detalles.


## Especificación

Cualquier propuesta para nueva criptografía asimétrica debe especificar completamente las siguientes cosas.


### 1. General

Responda las siguientes preguntas en su propuesta. Tenga en cuenta que esto puede necesitar ser una propuesta separada de los detalles en 2) a continuación, ya que puede entrar en conflicto con las propuestas existentes 111, 123, 136, 137, u otras.

- ¿Para cuál de los casos anteriores 1-4 propone usar la nueva criptografía?
- Si es para 1) o 2) (enrutador), ¿Dónde va la clave pública, en RouterIdentity o en las propiedades de RouterInfo? ¿Intenta usar el tipo de criptografía en el certificado de clave? Especifique completamente. Justifique su decisión en cualquier caso.
- Si es para 3) (cliente), ¿intenta almacenar la clave pública en el destino y usar el tipo de criptografía en el certificado de clave (como en la propuesta ECIES), o almacenarla en LS2 (como en la propuesta 123), o algo más? Especifique completamente y justifique su decisión.
- Para todos los usos, ¿cómo se anunciará el soporte? Si es para 3), ¿va en el LS2, o en algún otro lugar? Si es para 1) y 2), ¿es similar a las propuestas 136 y/o 137? Especifique completamente y justifique sus decisiones. Probablemente necesitará una propuesta separada para esto.
- Especifique completamente cómo y por qué esto es compatible con versiones anteriores, y especifique completamente un plan de migración.
- Qué propuestas no implementadas son prerrequisitos para su propuesta?


### 2. Tipo de criptografía específico

Responda las siguientes preguntas en su propuesta:

- Información general de criptografía, curvas/parámetros específicos, justifique completamente su elección. Proporcione enlaces a especificaciones y otra información.
- Resultados de pruebas de velocidad comparados con ElG y otras alternativas cuando sea aplicable. Incluya cifrado, descifrado, y generación de claves.
- Disponibilidad de bibliotecas en C++ y Java (tanto OpenJDK, BouncyCastle, como de terceros)
  Para 3ros o no-Java, proporcione enlaces y licencias
- Número(s) de tipo de criptografía propuesto(s) (rango experimental o no)


## Notas


