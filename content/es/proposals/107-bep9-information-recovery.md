---
title: "Recuperación de Información BEP9"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Muerto"
thread: "http://zzz.i2p/topics/860"
---

## Descripción general

Esta propuesta trata sobre la adición de una recuperación completa de información a la implementación de I2P de BEP9.

## Motivación

BEP9 no envía el archivo torrent completo, perdiendo así varios elementos importantes del diccionario, y cambia el total SHA1 de los archivos torrent. Esto es malo para los enlaces maggot, y malo porque se pierde información importante. Las listas de trackers, comentarios, y cualquier dato adicional desaparecen. Un método para recuperar esta información es importante, y debe añadir lo menos posible al archivo torrent. Además, no debe ser circularmente dependiente. La información de recuperación no debe afectar de ninguna manera a los clientes actuales. Los torrents que son sin tracker (la URL del tracker es literalmente 'sin tracker') no contienen el campo adicional, ya que son específicos para usar el protocolo maggot de descubrimiento y descarga, que no pierde nunca la información en primer lugar.

## Solución

Todo lo que se necesita hacer es comprimir la información que se perdería, y almacenarla en el diccionario de info.

### Implementación
1. Generar el diccionario de info normal.
2. Generar el diccionario principal, y dejar fuera la entrada de info.
3. Codificar en Bencode, y comprimir el diccionario principal con gzip.
4. Añadir el diccionario principal comprimido al diccionario de info.
5. Añadir info al diccionario principal.
6. Escribir el archivo torrent.

### Recuperación
1. Descomprimir la entrada de recuperación en el diccionario de info.
2. Decodificar en Bencode la entrada de recuperación.
3. Añadir info al diccionario recuperado.
4. Para los clientes conscientes de maggot, ahora puedes verificar que el SHA1 es correcto.
5. Escribir el archivo torrent recuperado.

## Discusión

Usando el método descrito anteriormente, el aumento del tamaño del torrent es muy pequeño, de 200 a 500 bytes es típico. Robert estará enviando con la nueva creación de la entrada de diccionario de info, y no se podrá desactivar. Aquí está la estructura:

```
diccionario principal {
    Cadenas de trackres, comentarios, etc...
    info : {
        dicc. principal bencodeado y comprimido menos el diccionario de info y toda la otra
        información habitual
    }
}
```
