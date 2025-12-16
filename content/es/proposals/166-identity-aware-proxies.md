---
title: "Propuesta I2P #166: Tipos de Túneles Conscientes de Identidad/Host"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Open"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Propuesta para un Tipo de Túnel Proxy HTTP Consciente de Host

Esta es una propuesta para resolver el "Problema de Identidad Compartida" en
el uso convencional de HTTP sobre I2P introduciendo un nuevo tipo de túnel
proxy HTTP. Este tipo de túnel tiene un comportamiento suplementario que está
diseñado para prevenir o limitar la utilidad del rastreo llevado a cabo por
operadores potencialmente hostiles de servicios ocultos, contra agentes de usuario
orientados (navegadores) y la propia Aplicación Cliente de I2P.

#### ¿Qué es el problema de "Identidad Compartida"?

El problema de "Identidad Compartida" ocurre cuando un agente de usuario en una
red superpuesta con direccionamiento criptográfico comparte una identidad
criptográfica con otro agente de usuario. Esto ocurre, por ejemplo, cuando
Firefox y GNU Wget están ambos configurados para usar el mismo Proxy HTTP.

En este escenario, es posible que el servidor recolecte y almacene la
dirección criptográfica (Destino) utilizada para responder a la actividad. Puede
tratar esto como una "Huella" que siempre es 100% única, porque tiene origen
criptográfico. Esto significa que la vinculabilidad observada por el problema
de Identidad Compartida es perfecta.

Pero, ¿es un problema?
^^^^^^^^^^^^^^^^^^^^^^

El problema de identidad compartida es un problema cuando los agentes de usuario
que hablan el mismo protocolo desean desvinculabilidad. [Se mencionó por primera vez en el
contexto de HTTP en este hilo de Reddit 
](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/),
con los comentarios eliminados accesibles gracias a
[pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi).
*En ese momento* fui uno de los encuestados más activos, y *en ese
momento* creía que el problema era pequeño. En los últimos 8 años, la situación
y mi opinión sobre ella han cambiado, ahora creo que la amenaza planteada por
la correlación de destinos maliciosos crece considerablemente a medida que más
sitios están en posición de "perfiles" de usuarios específicos.

Este ataque tiene una barrera de entrada muy baja. Solo requiere que un
operador de servicio oculto opere múltiples servicios. Para ataques en
visitas contemporáneas (visitar múltiples sitios al mismo tiempo), este es
el único requisito. Para el enlace no contemporáneo, uno de esos
servicios debe ser un servicio que aloje "cuentas" que pertenezcan a un
usuario único que esté siendo rastreado.

Actualmente, cualquier operador de servicio que aloje cuentas de usuario
podrá correlacionarlas con actividad en cualquier sitio que controlen
aprovechando el problema de Identidad Compartida. Mastodon, Gitlab, o incluso
foros simples podrían ser atacantes disfrazados siempre y cuando operen más
de un servicio y tengan interés en crear un perfil para un usuario. Esta
vigilancia podría llevarse a cabo por acosar, ganar dinero o razones
relacionadas con la inteligencia. Ahora mismo hay docenas de grandes
operadores, que podrían llevar a cabo este ataque y obtener datos
significativos de él. En su mayoría confiamos en que no lo harán por ahora,
pero podrían fácilmente emerger actores a quienes no les importan nuestras
opiniones.

Esto está directamente relacionado con una forma bastante básica de
creación de perfiles en la web clara donde las organizaciones pueden
correlacionar las interacciones en su sitio con interacciones en redes que
controlan. En I2P, debido a que el destino criptográfico es único, esta técnica
a veces puede ser incluso más confiable, aunque sin el poder adicional de la
geolocalización.

La Identidad Compartida no es útil contra un usuario que usa I2P
únicamente para ofuscar la geolocalización. Tampoco se puede usar para romper el
enrutamiento de I2P. Es solo un problema de gestión de identidad contextual.

-  Es imposible usar el problema de Identidad Compartida para geolocalizar un
   usuario de I2P.
-  Es imposible usar el problema de Identidad Compartida para enlazar sesiones de I2P
   si no son contemporáneas.

Sin embargo, es posible usarlo para degradar el anonimato de un usuario de I2P
en circunstancias que probablemente son muy comunes. Una razón por la que son
comunes es porque fomentamos el uso de Firefox, un navegador web que
admite la operación con "Pestañas".

-  Es *siempre* posible producir una huella del problema de Identidad
   Compartida en *cualquier* navegador web que soporte solicitar recursos de
   terceros.
-  Desactivar Javascript no logra **nada** contra el problema de Identidad Compartida.
-  Si se puede establecer un enlace entre sesiones no contemporáneas como
  mediante el uso de una "tradicional" huella digital del navegador, entonces
  la Identidad Compartida puede aplicarse transitivamente, permitiendo
  potencialmente una estrategia de enlace no contemporáneo.
-  Si se puede establecer un enlace entre una actividad en la red clara y una
  identidad de I2P, por ejemplo, si el objetivo está conectado a un sitio
  con presencia tanto en I2P como en la red clara en ambos lados, la
  Identidad Compartida puede aplicarse transitivamente, permitiendo
  potencialmente una des-anonimización completa.

Cómo veas la gravedad del problema de Identidad Compartida tal como aplica
al proxy HTTP de I2P depende de dónde pienses tú (o mejor dicho, un
"usuario" con expectativas potencialmente mal informadas) que la "identidad
contextual" para la aplicación reside. Hay varias posibilidades:

1. HTTP es tanto la Aplicación como la Identidad Contextual - Así es como
   funciona ahora. Todas las aplicaciones HTTP comparten una identidad.
2. El Proceso es la Aplicación y la Identidad Contextual - Así es como
   funciona cuando una aplicación utiliza una API como SAMv3 o I2CP,
   donde una aplicación crea su identidad y controla su duración.
3. HTTP es la Aplicación, pero el Host es la Identidad Contextual
   - Este es el objeto de esta propuesta, que trata a cada Host como una
   potencial "Aplicación Web" y trata la superficie de amenaza como tal.

¿Es Solucionable?
^^^^^^^^^^^^^^^^^

Probablemente no sea posible hacer un proxy que responda
inteligentemente a cada posible caso en el que su operación podría
debilitar el anonimato de una aplicación. Sin embargo, es posible
construir un proxy que responda inteligentemente a una aplicación
específica que se comporte de una manera predecible. Por ejemplo, en
navegadores web modernos, se espera que los usuarios tengan múltiples pestañas
abiertas, donde estarán interactuando con múltiples sitios web, que se
distinguirán por el nombre del host.

Esto nos permite mejorar el comportamiento del Proxy HTTP para este tipo
de agente de usuario HTTP haciendo que el comportamiento del proxy
coincida con el comportamiento del agente de usuario al dar a cada host
su propio Destino cuando se utilice con el Proxy HTTP. Este cambio hace
que sea imposible usar el problema de Identidad Compartida para derivar
una huella que pueda ser usada para correlacionar la actividad del cliente
con 2 hosts, porque los 2 hosts simplemente ya no compartirán una
identidad de retorno.

Descripción:
^^^^^^^^^^^^

Se creará un nuevo Proxy HTTP y se añadirá al Gestor de Servicios Ocultos
(I2PTunnel). El nuevo Proxy HTTP operará como un "multiplexor"
de I2PSocketManagers. El multiplexor en sí no tiene destino. Cada
I2PSocketManager individual que pasa a formar parte del múltiplex tiene su
propio destino local, y su propia reserva de túneles. Los I2PSocketManagers se
crean bajo demanda por el multiplexor, donde la "demanda" es la primera
visita al nuevo host. Es posible optimizar la creación de los I2PSocketManagers
antes de insertarlos en el multiplexor creando uno o más con antelación
y almacenándolos fuera del multiplexor. Esto puede mejorar el rendimiento.

Se configura un I2PSocketManager adicional, con su propio destino, como el
transportador de un “Outproxy” para cualquier sitio que *no* tenga un
Destino I2P, por ejemplo, cualquier sitio de Clearnet. Esto efectivamente
hace que todo uso de Outproxy sea una única Identidad Contextual, con la
advertencia de que configurar múltiples Outproxies para el túnel causará la
rotación normal de "Sticky" del outproxy, donde cada outproxy solo recibe
solicitudes para un sitio. Esto es *casi* el comportamiento equivalente a
aislar los proxies HTTP sobre I2P por destino, en el internet claro.

Consideraciones de Recursos:
''''''''''''''''''''''''''''

El nuevo proxy HTTP requiere recursos adicionales en comparación con el
proxy HTTP existente. Requerirá:

-  Potencialmente construir más túneles y I2PSocketManagers
-  Construir túneles más a menudo

Cada uno de estos requiere:

-  Recursos informáticos locales
-  Recursos de red de pares

Configuraciones:
'''''''''

Para minimizar el impacto del aumento en el uso de recursos, el
proxy debe configurarse para usar lo mínimo posible. Los proxies que
son parte del multiplexor (no el proxy principal) deben configurarse para:

-  I2PSocketManagers multiplexados construyen 1 túnel de entrada, 1 túnel de
   salida en sus reservas de túneles
-  I2PSocketManagers multiplexados toman 3 saltos por defecto.
-  Cierran los sockets después de 10 minutos de inactividad
-  I2PSocketManagers iniciados por el Multiplexor comparten la duración del
   Multiplexor. Los túneles multiplexados no se "Destruyen" hasta que el
   Multiplexor principal lo hace.

Diagramas:
^^^^^^^^^^

El siguiente diagrama representa la operación actual del proxy HTTP,
que corresponde a la "Posibilidad 1" bajo la sección "¿Es un problema?".
Como puedes ver, el proxy HTTP interactúa con los sitios I2P directamente
utilizando solo un destino. En este escenario, HTTP es tanto la
aplicación como la identidad contextual.

```text
**Situación Actual: HTTP es la Aplicación, HTTP es la Identidad Contextual**
                                                          __-> Outproxy <-> i2pgit.org
                                                         /
   Navegador <-> Proxy HTTP (un solo Destino) <-> I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

El siguiente diagrama representa la operación de un proxy HTTP consciente de
host, que corresponde a la "Posibilidad 3" bajo la sección "¿Es un problema?".
En este escenario, HTTP es la aplicación, pero el Host define la identidad
contextual, donde cada sitio I2P interactúa con un proxy HTTP diferente con un
destino único por host. Esto evita que los operadores de múltiples sitios
puedan distinguir cuándo la misma persona está visitando múltiples sitios que
ellos operan.

```text
**Después del Cambio: HTTP es la Aplicación, Host es la Identidad Contextual**
                                                        __-> I2PSocketManager(Destino A - Solo Outproxies) <--> i2pgit.org
                                                       /
   Navegador <-> Multiplexor de Proxy HTTP (Sin Destino) <---> I2PSocketManager(Destino B) <--> idk.i2p
                                                       \__-> I2PSocketManager(Destino C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager(Destino C) <--> git.idk.i2p
```

Estado:
^^^^^^^

Una implementación funcional en Java del proxy consciente de host que conforme a
una versión anterior de esta propuesta está disponible en la bifurcación de idk
bajo la rama: i2p.i2p.2.6.0-browser-proxy-post-keepalive Enlace en citas. Está
bajo intensa revisión, con el fin de desglosar los cambios en secciones más
pequeñas.

Se han escrito implementaciones con capacidades variables en Go usando la
biblioteca SAMv3, pueden ser útiles para integrar en otras aplicaciones Go o
para go-i2p pero no son adecuadas para Java I2P. Además, carecen de buen
soporte para trabajar interactivamente con leaseSets cifrados.

Adenda: ``i2psocks``
                      

Es posible un enfoque simple orientado a la aplicación para aislar otros
tipos de clientes sin implementar un nuevo tipo de túnel o cambiar el código
existente de I2P combinando herramientas existentes de I2PTunnel que ya están
ampliamente disponibles y probadas en la comunidad de privacidad. Sin embargo,
este enfoque hace una suposición difícil que no es cierta para HTTP y tampoco
es cierta para muchos otros tipos de clientes potenciales de I2P.

Aproximadamente, el siguiente script producirá un proxy SOCKS5 consciente de la
aplicación y socksificará el comando subyacente:

```sh
#! /bin/sh
comando_a_proxi="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $comando_a_proxi
```

Adenda: ``implementación de ejemplo del ataque``
                                                  

[Un ejemplo de implementación del ataque de Identidad Compartida en Agentes de
Usuario HTTP](https://github.com/eyedeekay/colluding_sites_attack/)
ha existido por varios años. Un ejemplo adicional está disponible en el
subdirectorio ``simple-colluder`` del [repositorio de idk para prop166
](https://git.idk.i2p/idk/i2p.host-aware-proxy) Estos ejemplos están
diseñados deliberadamente para demostrar que el ataque funciona y requerirían
modificación (aunque menor) para convertirse en un ataque real.

