---
title: "Ayudantes de Dirección Autenticados"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Abierto"
thread: "http://zzz.i2p/topics/2241"
toc: true
---

## Visión General

Esta propuesta añade un mecanismo de autenticación a las URLs de ayuda de dirección.


## Motivación

Las URLs de ayuda de dirección son inherentemente inseguras. Cualquiera puede poner un parámetro de ayuda de dirección 
en un enlace, incluso para una imagen, y puede poner cualquier destino en el 
parámetro de URL "i2paddresshelper". Dependiendo de la implementación del proxy HTTP del usuario, esta asignación de nombre de host/destino, si no está actualmente en la libreta de direcciones, puede ser aceptada, ya sea con o sin una página intermedia para que el usuario la acepte.


## Diseño

Los servidores de salto confiables y los servicios de registro en libreta de direcciones proporcionarían nuevos 
enlaces de ayuda de dirección que añaden parámetros de autenticación. Los dos nuevos parámetros 
serían una firma en base 64 y una cadena firmada por.

Estos servicios generarían y proporcionarían un certificado de clave pública. Este 
certificado estaría disponible para descarga e inclusión en software proxy HTTP. Los usuarios y desarrolladores de software decidirían si confían en dichos 
servicios incluyendo el certificado.

Al encontrar un enlace de ayuda de dirección, el proxy HTTP verificaría los 
parámetros adicionales de autenticación e intentaría verificar la firma. En caso de 
verificación exitosa, el proxy procederá como antes, ya sea aceptando 
la nueva entrada o mostrando una página intermedia al usuario. En caso de fallo de 
verificación, el proxy podría rechazar la ayuda de dirección o mostrar información 
adicional al usuario.

Si no hay parámetros de autenticación presentes, el proxy HTTP puede aceptar, 
rechazar o presentar información al usuario.

Los servicios de salto serían confiables como de costumbre, pero con el paso adicional de autenticación. Los enlaces de ayuda de dirección en otros sitios necesitarían ser modificados.


## Implicaciones de Seguridad

Esta propuesta añade seguridad añadiendo autenticación de servicios de registro / salto 
confiables. 


## Especificación

Por Determinar.

¿Los dos nuevos parámetros podrían ser i2paddresshelpersig e i2paddresshelpersigner?

Tipos de firma aceptados por determinar. Probablemente no RSA ya que las firmas en base 64 serían 
muy largas.

Algoritmo de firma: Por Determinar. Quizás solo nombre=destinoB64 (igual que la propuesta 112 para 
autenticación de registro)

Posible tercer nuevo parámetro: La cadena de autenticación de registro (la parte 
después de "#!") para ser usada para verificación adicional por el proxy HTTP. Cualquier 
"#" en la cadena tendría que ser escapado como "&#35;" o "&num;", o 
ser reemplazado por algún otro caracter (por determinar) seguro para URLs.


## Migración

Los proxies HTTP antiguos que no soportan los nuevos parámetros de autenticación los 
ignorarían y los pasarían al servidor web, lo cual debería ser inofensivo.

Los nuevos proxies HTTP que opcionalmente soportan parámetros de autenticación funcionarían 
bien con los viejos enlaces de ayuda de dirección que no los contienen.

Los nuevos proxies HTTP que requieren parámetros de autenticación no permitirían 
enlaces de ayuda de dirección antiguos que no los contienen.

Las políticas de implementación de un proxy pueden evolucionar en el transcurso de un período de 
migración.

## Problemas

Un propietario de sitio no podría generar una ayuda de dirección para su propio sitio, ya que necesita 
la firma de un servidor de salto confiable. Tendría que registrarlo en el 
servidor confiable y obtener la URL de ayuda autenticada de ese servidor. ¿Hay 
alguna forma para que un sitio genere una URL de ayuda de dirección auto-autenticada?

Alternativamente, el proxy podría verificar el Referer para una solicitud de ayuda de 
dirección. Si el Referer estuviera presente, contuviera un b32, y el b32 coincidiera con el 
destino del ayudante, podría ser permitido como una auto-referencia. De lo contrario, podría asumirse como una solicitud de tercero y ser rechazada.
