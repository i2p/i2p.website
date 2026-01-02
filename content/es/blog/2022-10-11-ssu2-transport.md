---
title: "Transporte SSU2"
date: 2022-10-11
author: "zzz"
description: "Transporte SSU2"
categories: ["development"]
API_Translate: verdadero
---

## Descripción general

I2P ha utilizado un protocolo de transporte UDP resistente a la censura, "SSU", desde 2005. Hemos tenido pocos, si es que alguno, informes de que SSU haya sido bloqueado en 17 años. Sin embargo, según los estándares actuales de seguridad, resistencia al bloqueo y rendimiento, podemos hacerlo mejor. Mucho mejor.

Por eso, junto con el [proyecto i2pd](https://i2pd.xyz/), hemos creado e implementado "SSU2", un protocolo UDP moderno diseñado conforme a los más altos estándares de seguridad y resistencia al bloqueo. Este protocolo reemplazará a SSU.

Hemos combinado el cifrado estándar del sector con las mejores características de los protocolos UDP WireGuard y QUIC, junto con las características de resistencia a la censura de nuestro protocolo TCP "NTCP2". SSU2 puede ser uno de los protocolos de transporte más seguros jamás diseñados.

Los equipos de Java I2P e i2pd están finalizando el transporte SSU2 y lo habilitaremos para todos los routers en la próxima versión. Esto completa nuestro plan de una década para actualizar toda la criptografía desde la implementación original de Java I2P que se remonta a 2003. SSU2 reemplazará SSU, nuestro único uso restante de la criptografía de ElGamal.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

Después de la transición a SSU2, habremos migrado todos nuestros protocolos autenticados y cifrados a procedimientos de negociación estándar del [Noise Protocol](https://noiseprotocol.org/):

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Todos los protocolos Noise de I2P utilizan los siguientes algoritmos criptográficos estándar:

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

## Diseño

I2P utiliza múltiples capas de cifrado para proteger el tráfico frente a atacantes. La capa más baja es la capa del protocolo de transporte, utilizada para enlaces punto a punto entre dos routers. Actualmente contamos con dos protocolos de transporte: NTCP2, un protocolo TCP moderno introducido en 2018, y SSU, un protocolo UDP desarrollado en 2005.

SSU2, como los protocolos de transporte de I2P anteriores, no es un canal de propósito general para datos. Su tarea principal es entregar de forma segura los mensajes I2NP de bajo nivel de I2P de un router al siguiente. Cada una de estas conexiones punto a punto constituye un salto en un tunnel de I2P. Los protocolos de I2P de capas superiores se ejecutan sobre estas conexiones punto a punto para entregar garlic messages (mensajes «garlic») de extremo a extremo entre los destinos de I2P.

Diseñar un transporte UDP presenta desafíos únicos y complejos que no están presentes en los protocolos TCP. Un protocolo UDP debe gestionar problemas de seguridad causados por la suplantación de direcciones y debe implementar su propio control de congestión. Además, todos los mensajes deben fragmentarse para ajustarse al tamaño máximo de paquete (MTU) de la ruta de red y reensamblarse en el receptor.

Primero, nos apoyamos en gran medida en nuestra experiencia previa con nuestros protocolos NTCP2, SSU y de streaming. Luego, revisamos cuidadosamente y tomamos prestado en gran medida de dos protocolos UDP desarrollados recientemente:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

La clasificación y el bloqueo de protocolos por parte de atacantes adversarios on-path (en el camino), como los cortafuegos de estados nacionales, no forman parte explícita del modelo de amenazas de esos protocolos. Sin embargo, sí es una parte importante del modelo de amenazas de I2P, ya que nuestra misión es proporcionar un sistema de comunicaciones anónimo y resistente a la censura a usuarios en riesgo en todo el mundo. Por lo tanto, gran parte de nuestro trabajo de diseño consistió en combinar las lecciones aprendidas de NTCP2 y SSU con las funciones y la seguridad que proporcionan QUIC y WireGuard.

## Rendimiento

La red I2P es una mezcla compleja de routers diversos. Existen dos implementaciones principales que se ejecutan en todo el mundo en hardware que va desde computadoras de alto rendimiento en centros de datos hasta dispositivos Raspberry Pi y teléfonos Android. Los routers utilizan ambos transportes TCP y UDP. Si bien las mejoras de SSU2 son significativas, no esperamos que sean evidentes para el usuario, ni localmente ni en las velocidades de transferencia de extremo a extremo.

Estos son algunos aspectos destacados de las mejoras estimadas para SSU2 frente a SSU:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Transition Plan

I2P se esfuerza por mantener la compatibilidad con versiones anteriores, tanto para garantizar la estabilidad de la red como para permitir que routers más antiguos sigan siendo útiles y seguros. Sin embargo, existen límites, porque la compatibilidad incrementa la complejidad del código y los requisitos de mantenimiento.

Los proyectos Java I2P e i2pd habilitarán SSU2 de forma predeterminada en sus próximas versiones (2.0.0 y 2.44.0) a finales de noviembre de 2022. Sin embargo, tienen planes distintos para desactivar SSU. I2pd desactivará SSU de inmediato, porque SSU2 es una mejora sustancial respecto a su implementación de SSU. Java I2P planea desactivar SSU a mediados de 2023, para apoyar una transición gradual y dar tiempo a los routers más antiguos a actualizarse.

## Resumen


Los fundadores de I2P tuvieron que tomar varias decisiones sobre algoritmos y protocolos criptográficos. Algunas de esas decisiones fueron mejores que otras, pero, veinte años después, la mayoría de ellas ya acusa el paso del tiempo. Por supuesto, sabíamos que esto se avecinaba, y hemos pasado la última década planificando e implementando actualizaciones criptográficas.

SSU2 fue el último y más complejo protocolo por desarrollar en nuestro largo camino de actualización. UDP tiene un conjunto de supuestos y un modelo de amenazas muy exigentes. Primero diseñamos y desplegamos otras tres variantes de protocolos Noise (un marco de protocolos criptográficos), y adquirimos experiencia y una comprensión más profunda de los problemas de seguridad y del diseño de protocolos.

Se espera que SSU2 esté habilitado en las versiones de i2pd y Java I2P programadas para finales de noviembre de 2022. Si la actualización sale bien, nadie notará nada diferente. Las mejoras en el rendimiento, aunque significativas, probablemente no serán medibles para la mayoría de las personas.

Como de costumbre, recomendamos actualizar a la nueva versión en cuanto esté disponible. La mejor manera de mantener la seguridad y ayudar a la red es ejecutar la versión más reciente.
