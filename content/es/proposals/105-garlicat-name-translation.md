---
title: "Traducción de Nombre para GarliCat"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Muerto"
thread: "http://zzz.i2p/topics/453"
---

## Visión General

Esta propuesta trata sobre agregar soporte para búsquedas DNS inversas en I2P.


## Mecanismo de Traducción Actual

GarliCat (GC) realiza la traducción de nombres para establecer conexiones con otros nodos de GC. Esta traducción de nombres es simplemente una recodificación de la representación binaria de una dirección a la forma codificada en Base32. Así, la traducción funciona en ambas direcciones.

Esas direcciones se eligen para tener 80 bits de longitud. Esto se debe a que Tor usa valores de 80 bits para direccionar sus servicios ocultos. Así, OnionCat (que es GC para Tor) funciona con Tor sin intervención adicional.

Desafortunadamente (respecto a este esquema de direccionamiento), I2P utiliza valores de 256 bits para direccionar sus servicios. Como se mencionó anteriormente, GC transcodifica entre la forma binaria y la codificación en Base32. Debido a la naturaleza de GC siendo una VPN de capa 3, en su representación binaria las direcciones están definidas como direcciones IPv6 que tienen una longitud total de 128 bits. Obviamente, las direcciones de 256 bits de I2P no caben en esto.

Por lo tanto, se hace necesario un segundo paso de traducción de nombres:
Dirección IPv6 (binaria) -1a-> Dirección Base32 (80 bits) -2a-> Dirección I2P (256 bits)
-1a- ... traducción GC
-2a- ... búsqueda en hosts.txt de I2P

La solución actual es dejar que el enrutador de I2P haga el trabajo. Esto se logra insertando la dirección Base32 de 80 bits y su destino (la dirección I2P) como un par nombre/valor en el archivo hosts.txt o privatehosts.txt del enrutador de I2P.

Básicamente funciona, pero depende de un servicio de nombres que (IMHO) está en un estado de desarrollo y no es lo suficientemente maduro (especialmente respecto a la distribución de nombres).


## Una Solución Escalable

Sugiero cambiar las etapas de direccionamiento respecto a I2P (y tal vez también para Tor) de modo que GC realice búsquedas inversas en las direcciones IPv6 usando el protocolo DNS común. La zona inversa deberá contener directamente la dirección I2P de 256 bits en su forma codificada en Base32. Esto cambia el mecanismo de búsqueda a un solo paso, añadiendo así más ventajas.
Dirección IPv6 (binaria) -1b-> Dirección I2P (256 bits)
-1b- ... búsqueda DNS inversa

Las búsquedas DNS dentro de Internet son conocidas como riesgos de fuga de información respecto al anonimato. Por lo tanto, esas búsquedas deben realizarse dentro de I2P. Esto implica que varios servicios DNS deberían estar presentes dentro de I2P. Dado que las consultas DNS generalmente se realizan usando el protocolo UDP, GC mismo es necesario para el transporte de datos porque lleva paquetes UDP que I2P no maneja de manera nativa.

Existen más ventajas asociadas con DNS:
1) Es un protocolo estándar bien conocido, por lo tanto, está en continua mejora y existen muchas herramientas (clientes, servidores, bibliotecas,...).
2) Es un sistema distribuido. Soporta que el espacio de nombres se aloje en varios servidores en paralelo por defecto.
3) Soporta criptografía (DNSSEC) que permite la autenticación de registros de recursos. Esto podría vincularse directamente con las claves de un destino.


## Oportunidades Futuras

Puede ser posible que este servicio de nombres también se utilice para realizar búsquedas directas. Esto es, traducir nombres de host a direcciones I2P y/o direcciones IPv6. Pero este tipo de búsqueda necesita investigación adicional porque esas búsquedas generalmente las realiza la biblioteca resolutora local instalada, que usa servidores de nombres comunes de Internet (por ejemplo, como se especifica en /etc/resolv.conf en sistemas tipo Unix). Esto es diferente de las búsquedas inversas de GC que expliqué arriba.
Otra oportunidad podría ser que la dirección I2P (destino) se registre automáticamente al crear un túnel de entrada GC. Esto mejoraría en gran medida la usabilidad.
