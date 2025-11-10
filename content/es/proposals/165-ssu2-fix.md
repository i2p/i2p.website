---
title: "Propuesta de I2P #165: Corrección de SSU2"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Abierto"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Propuesta de weko, orignal, the Anonymous y zzz.


### Descripción general

Este documento sugiere cambios a SSU2 tras un ataque a I2P que explotó vulnerabilidades en SSU2. El objetivo principal es mejorar la seguridad y prevenir ataques de Denegación de Servicio Distribuido (DDoS) e intentos de desanonimización.

### Modelo de amenaza

Un atacante crea nuevos RIs falsos (el router no existe): es un RI regular, pero coloca la dirección, puerto, y claves s e i del router real de Bob, luego inunda la red. Cuando intentamos conectarnos a este (que creemos que es un router real), nosotros, como Alice, podemos conectar a esta dirección, pero no podemos estar seguros de lo que se hizo con el RI real de Bob. Esto es posible y se utilizó para un ataque de Denegación de Servicio Distribuido (crear una gran cantidad de tales RIs e inundar la red), también esto puede facilitar ataques de desanonimización al incriminar buenos routers y no incriminar los routers del atacante, si prohibimos IPs con muchos RIs (en lugar de distribuir mejor la construcción del túnel a estos RIs como a un solo router).


### Posibles soluciones

#### 1. Solución con soporte para routers antiguos (antes del cambio)

.. _overview-1:

Descripción general
^^^^^^^^

Una solución alternativa para soportar conexiones SSU2 con routers antiguos.

Comportamiento
^^^^^^^^^

El perfil del router de Bob debería tener un indicador 'verificado', que es falso por defecto para todos los routers nuevos (aún sin perfil). Cuando el indicador 'verificado' es falso, nunca hacemos conexiones con SSU2 como Alice a Bob - no podemos estar seguros en RI. Si Bob se conectó a nosotros (Alice) con NTCP2 o SSU2 o nosotros (Alice) nos conectamos a Bob con NTCP2 una vez (podemos verificar el RouterIdent de Bob en estos casos) - el indicador se establece en verdadero.

Problemas
^^^^^^^^

Entonces, hay un problema con la inundación de RI falsos solo SSU2: no podemos verificarlo por nosotros mismos y nos vemos obligados a esperar cuando el router real haga conexiones con nosotros.

#### 2. Verificar RouterIdent durante la creación de la conexión

.. _overview-2:

Descripción general
^^^^^^^^

Agregar un bloque de "RouterIdent" para SessionRequest y SessionCreated.

Posible formato del bloque RouterIdent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 byte de indicadores, 32 bytes de RouterIdent. Flag_0: 0 si es el RouterIdent del receptor; 1 si es el RouterIdent del remitente

Comportamiento
^^^^^^^^^

Alice (debería(1), puede(2)) envía en la carga el bloque RouterIdent Flag_0 = 0 y el RouterIdent de Bob. Bob (debería(3), puede(4)) verifica si es su RouterIdent, y si no: termina la sesión con la razón "RouterIdent incorrecto", si es su RouterIdent: envía el bloque RI con 1 en Flag_0 y el RouterIdent de Bob.

Con (1) Bob no soporta routers antiguos. Con (2) Bob soporta routers antiguos, pero puede ser víctima de DDoS por parte de routers que intentan hacer conexión con RIs falsos. Con (3) Alice no soporta routers antiguos. Con (4) Alice soporta routers antiguos y está usando un esquema híbrido: Solución 1 para routers antiguos y Solución 2 para routers nuevos. Si el RI dice nueva versión, pero mientras estamos en la conexión no recibimos el bloque RouterIdent - terminar y eliminar el RI.

.. _problems-1:

Problemas
^^^^^^^^

Un atacante puede enmascarar sus routers falsos como antiguos, y con (4) estamos esperando 'verificado' como en la solución 1 de todas formas.

Notas
^^^^^

En lugar de 32 bytes de RouterIdent, probablemente podemos usar 4 bytes de siphash-del-hash, algún HKDF o algo más, lo cual debe ser suficiente.

#### 3. Bob establece i = RouterIdent

.. _overview-3:

Descripción general
^^^^^^^^

Bob usa su RouterIdent como clave i.

.. _behavior-1:

Comportamiento
^^^^^^^^^

Bob (debería(1), puede(2)) usa su propio RouterIdent como clave i para SSU2.

Alice con (1) se conecta solo si i = RouterIdent de Bob. Alice con (2) usa el esquema híbrido (solución 3 y 1): si i = RouterIdent de Bob, podemos establecer la conexión, de lo contrario deberíamos verificarlo primero (ver solución 1).

Con (1) Alice no soporta routers antiguos. Con (2) Alice soporta routers antiguos.

.. _problems-2:

Problemas
^^^^^^^^

Un atacante puede enmascarar sus routers falsos como antiguos, y con (2) estamos esperando 'verificado' como en la solución 1 de todas formas.

.. _notes-1:

Notas
^^^^^

Para ahorrar en el tamaño del RI, es mejor agregar manipulación si la clave i no está especificada. Si lo está, entonces i = RouterIdent. En ese caso, Bob no soporta routers antiguos.

#### 4. Agregar un MixHash más al KDF de SessionRequest

.. _overview-4:

Descripción general
^^^^^^^^

Agregar MixHash(hash de ident de Bob) al estado de NOISE del mensaje "SessionRequest", por ejemplo, h = SHA256 (h || hash de ident de Bob). Debe ser el último MixHash usado como ad para ENCRYPT o DECRYPT. Debe introducirse una bandera de encabezado adicional de SSU2 "Verificar ident de Bob" = 0x02.

.. _behavior-4:

Comportamiento
^^^^^^^^

- Alice agrega MixHash con el hash de ident de Bob de RouterInfo de Bob y lo usa como ad para ENCRYPT y establece la bandera "Verificar ident de Bob"
- Bob verifica la bandera "Verificar ident de Bob" y agrega MixHash con su propio hash de ident y lo usa como ad para DECRYPT. Si AEAD/Chacha20/Poly1305 falla, Bob cierra la sesión.

Compatibilidad con routers más antiguos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice debe verificar la versión del router de Bob y si satisface la versión mínima que soporta esta propuesta, agregar este MixHash y establecer la bandera "Verificar ident de Bob". Si el router es más antiguo, Alice no agrega MixHash y no establece la bandera "Verificar ident de Bob".
- Bob verifica la bandera "Verificar ident de Bob" y agrega este MixHash si está establecida. Los routers más antiguos no establecen esta bandera y este MixHash no debe agregarse.

.. _problems-4:

Problemas
^^^^^^^^

- Un atacante puede reivindicar routers falsos con versiones más antiguas. En algún punto los routers más antiguos deben usarse con precaución y después de que sean verificados por otros medios.


### Compatibilidad hacia atrás

Descrita en las soluciones.


### Estado actual

i2pd: Solución 1.
