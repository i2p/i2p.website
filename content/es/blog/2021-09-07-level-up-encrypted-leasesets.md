---
title: "Lleva tus habilidades de I2P al siguiente nivel con LeaseSets cifrados"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "Se ha dicho que I2P pone énfasis en los servicios ocultos; examinamos una interpretación de ello"
categories: ["general"]
API_Translate: verdadero
---

## Mejora tus habilidades en I2P con LeaseSets cifrados

It has been said in the past that I2P emphasizes support for Hidden Services, which is true in many ways. However, what this means to users, developers, and hidden service administrators isn't always the same. Encrypted LeaseSets and their use-cases provide a unique, practical window into how I2P makes hidden services more versatile, easier to administer, and how I2P extends on the Hidden Service concept to provide security benefits for potentially interesting use-cases.

## ¿Qué es un LeaseSet?

Cuando creas un servicio oculto, publicas algo llamado "LeaseSet" en la I2P NetDB. El "LeaseSet" es, en términos sencillos, lo que otros usuarios de I2P necesitan para descubrir "dónde" se encuentra tu servicio oculto en la red I2P. Contiene "Leases" que identifican tunnels que pueden utilizarse para alcanzar tu servicio oculto, y la clave pública de tu destino, con la que los clientes cifrarán los mensajes. Este tipo de servicio oculto es accesible para cualquiera que tenga la dirección, lo cual probablemente sea el caso de uso más común por ahora.

A veces, sin embargo, puede que no quieras permitir que tus servicios ocultos sean accesibles para cualquiera. Algunas personas usan los servicios ocultos como una forma de acceder a un servidor SSH en un PC doméstico, o para interconectar una red de dispositivos IoT. En estos casos no es necesario, y puede ser contraproducente, hacer que tu servicio oculto sea accesible para todos en la red I2P. Aquí es donde entran en juego los "LeaseSets cifrados".

## LeaseSets cifrados: servicios MUY ocultos

Los LeaseSets cifrados son LeaseSets que se publican en la NetDB de forma cifrada, donde ninguno de los Leases ni las claves públicas son visibles a menos que el cliente tenga las claves necesarias para descifrar el LeaseSet en su interior. Solo los clientes con los que compartas claves(Para PSK Encrypted LeaseSets), o que compartan sus claves contigo(Para DH Encrypted LeaseSets), podrán ver el destino y nadie más.

I2P admite varias estrategias para LeaseSets cifrados. Es importante comprender las características clave de cada estrategia al decidir cuál utilizar. Si un LeaseSet cifrado utiliza una estrategia de "clave precompartida (PSK)", entonces el servidor generará una clave (o claves) que el operador del servidor compartirá con cada cliente. Por supuesto, este intercambio debe realizarse fuera de banda, posiblemente mediante un intercambio en IRC, por ejemplo. Esta versión de LeaseSets cifrados es algo así como conectarse a una red Wi‑Fi con una contraseña. Excepto que, en este caso, te estás conectando a un Servicio Oculto.

Si un Encrypted LeaseSet utiliza una estrategia Diffie-Hellman (DH), entonces las claves se generan en el cliente. Cuando un cliente Diffie-Hellman se conecta a un destino con un Encrypted LeaseSet, primero debe compartir sus claves con el operador del servidor. El operador del servidor entonces decide si autoriza al cliente DH. Esta versión de Encrypted LeaseSets es algo parecido a SSH con un archivo `authorized_keys`. Excepto que, en este caso, donde inicias sesión es en un Servicio Oculto.

Al cifrar su LeaseSet, no solo hace que sea imposible que usuarios no autorizados se conecten a su destino, sino que también hace imposible que visitantes no autorizados siquiera descubran el destino real del servicio oculto de I2P. Es probable que algunos lectores ya hayan considerado un caso de uso para su propio LeaseSet cifrado.

## Uso de LeaseSets cifrados para acceder de forma segura a la consola del router

Como regla general, cuanto más información compleja tenga un servicio sobre tu dispositivo, más peligroso es exponer ese servicio a Internet o, de hecho, a una red de servicios ocultos como I2P. Si quieres exponer un servicio así, debes protegerlo con algo como una contraseña o, en el caso de I2P, una opción mucho más exhaustiva y segura podría ser un LeaseSet (conjunto de arrendamiento) cifrado.

**Antes de continuar, lea y comprenda que, si realiza el siguiente procedimiento sin un Encrypted LeaseSet, estará comprometiendo la seguridad de su router de I2P. No configure el acceso a la consola de su router a través de I2P sin un Encrypted LeaseSet. Además, no comparta las PSK de su Encrypted LeaseSet con ningún dispositivo que usted no controle.**

Uno de esos servicios que es útil compartir a través de I2P, pero SOLO con un LeaseSet cifrado, es la propia consola del router de I2P. Exponer la consola del router de I2P de una máquina en I2P con un LeaseSet cifrado permite que otra máquina con un navegador administre la instancia de I2P remota. Esto me resulta útil para supervisar de forma remota mis servicios habituales de I2P. También podría utilizarse para supervisar un servidor que se usa para sembrar un torrent a largo plazo, como una manera de acceder a I2PSnark.

Aunque lleve tiempo explicarlo, configurar un LeaseSet cifrado es sencillo mediante la interfaz de usuario del Administrador de Servicios Ocultos.

## En el "Servidor"

Comience abriendo el Administrador de Servicios Ocultos en http://127.0.0.1:7657/i2ptunnelmgr y desplácese hasta el final de la sección que dice "I2P Hidden Services." Cree un nuevo servicio oculto con el host "127.0.0.1" y el puerto "7657", con estas "Tunnel Cryptography Options", y guarde el servicio oculto.

Luego, seleccione su nuevo tunnel desde la página principal del Administrador de Servicios Ocultos. Las opciones de criptografía del tunnel ahora deberían incluir su primera Pre-Shared Key (clave precompartida). Anote esto para el siguiente paso, junto con la dirección Base32 cifrada de su tunnel.

## En el "Client"

Ahora cambia al equipo cliente que se conectará al servicio oculto y visita la Configuración de Keyring en http://127.0.0.1:7657/configkeyring para agregar las claves anteriores. Comienza pegando el Base32 del Servidor en el campo etiquetado: "Full destination, name, Base32, or hash." Luego, pega la Clave precompartida del Servidor en el campo "Encryption Key". Haz clic en guardar, y ya estás listo para visitar de forma segura el Servicio Oculto usando un Encrypted LeaseSet.

## Ahora ya está listo para administrar I2P de forma remota

Como puede verse, I2P ofrece capacidades únicas a los Administradores de Servicios Ocultos que les permiten gestionar de forma segura sus conexiones de I2P desde cualquier lugar del mundo. Otros Encrypted LeaseSets que mantengo en el mismo dispositivo por el mismo motivo apuntan al servidor SSH, a la instancia de Portainer que uso para gestionar mis contenedores de servicios y a mi instancia personal de NextCloud. Con I2P, el autoalojamiento verdaderamente privado y siempre accesible es un objetivo alcanzable; de hecho, creo que es una de las cosas para las que estamos singularmente capacitados, gracias a Encrypted LeaseSets. Con ellos, I2P podría convertirse en la clave para asegurar la domótica autoalojada o simplemente convertirse en la columna vertebral de una nueva web de igual a igual (peer-to-peer) más privada.
