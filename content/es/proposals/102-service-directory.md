---
title: "Directorio de Servicios"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Rechazado"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Visión General

Esta propuesta es para un protocolo que las aplicaciones podrían utilizar para registrar y buscar servicios en un directorio.


## Motivación

La forma más sencilla de soportar onioncat es con un directorio de servicios.

Esto es similar a una propuesta que Sponge hizo hace algún tiempo en IRC. No creo que la haya escrito, pero su idea era ponerla en el netDb. No estoy a favor de eso, pero la discusión sobre el mejor método para acceder al directorio (consultas en netDb, DNS-over-i2p, HTTP, hosts.txt, etc.) la dejaré para otro día.

Probablemente podría improvisar esto bastante rápido utilizando HTTP y la colección de scripts en perl que uso para el formulario de agregar clave.


## Especificación

Así es como una aplicación interactuaría con el directorio:

REGISTRAR
  - DestKey
  - Lista de pares Protocolo/Servicio:

    - Protocolo (opcional, por defecto: HTTP)
    - Servicio (opcional, por defecto: sitio web)
    - ID (opcional, por defecto: ninguno)

  - Nombre de host (opcional)
  - Expiración (por defecto: ¿1 día? 0 para eliminar)
  - Sig (usando privkey para dest)

  Devuelve: éxito o fallo

  Se permiten actualizaciones

BUSCAR
  - Hash o clave (opcional). UNO de:

    - Hash parcial de 80 bits
    - Hash completo de 256 bits
    - destkey completo

  - Par de protocolo/servicio (opcional)

  Devuelve: éxito, fallo o (para 80 bits) colisión.
  Si tiene éxito, devuelve la descripción firmada mencionada arriba.
