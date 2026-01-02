---
title: "Formato del filtro de acceso"
description: "Sintaxis de los archivos de filtro de control de acceso de tunnel"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Los filtros de acceso permiten a los operadores de servidores I2PTunnel permitir, denegar o limitar las conexiones entrantes según el Destino de origen y la tasa reciente de conexiones. El filtro es un archivo de texto plano de reglas. El archivo se lee de arriba hacia abajo y **la primera regla que coincida se aplica**.

> Los cambios en la definición del filtro surten efecto **al reiniciar el tunnel**. Algunas compilaciones pueden volver a leer listas basadas en archivos en tiempo de ejecución, pero planifique un reinicio para garantizar que se apliquen los cambios.

## Formato de archivo

- Una regla por línea.  
- Las líneas en blanco se ignoran.  
- `#` inicia un comentario que se extiende hasta el final de la línea.  
- Las reglas se evalúan en orden; se usa la primera coincidencia.

## Umbrales

Un **umbral** define cuántos intentos de conexión desde un único Destination (destino en I2P) se permiten en una ventana de tiempo deslizante.

- **Numérico:** `N/S` significa permitir `N` conexiones cada `S` segundos. Ejemplo: `15/5` permite hasta 15 conexiones cada 5 segundos. El intento `N+1` dentro de la ventana se rechaza.  
- **Palabras clave:** `allow` significa que no hay límite. `deny` significa rechazar siempre.

## Sintaxis de reglas

Las reglas tienen la forma:

```
<threshold> <scope> <target>
```
Dónde:

- `<threshold>` es `N/S`, `allow` o `deny`  
- `<scope>` es uno de `default`, `explicit`, `file` o `record` (ver más abajo)  
- `<target>` depende del ámbito

### Regla predeterminada

Se aplica cuando ninguna otra regla coincide. Solo se permite **una** regla predeterminada. Si se omite, se permiten Destinos desconocidos sin restricciones.

```
15/5 default
allow default
deny default
```
### Regla explícita

Apunta a un Destino específico mediante una dirección Base32 (por ejemplo `example1.b32.i2p`) o una clave completa.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Regla basada en archivos

Apunta a **todos** los Destinos enumerados en un archivo externo. Cada línea contiene un Destino; se permiten comentarios con `#` y líneas en blanco.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> Nota operativa: Algunas implementaciones vuelven a leer las listas de archivos periódicamente. Si edita una lista mientras el tunnel está en ejecución, espere un breve retraso antes de que se detecten los cambios. Reinicie para aplicar de inmediato.

### Grabador (control progresivo)

Un **registrador** supervisa los intentos de conexión y escribe en un archivo las Destinations (destinos de I2P) que superan un umbral. Luego puedes hacer referencia a ese archivo en una regla `file` para aplicar limitaciones o bloqueos en intentos futuros.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Verifique el soporte del grabador en su compilación antes de depender de él. Use listas `file` para un comportamiento garantizado.

## Orden de evaluación

Pon primero las reglas específicas y luego las generales. Un patrón común:

1. Permisos explícitos para pares de confianza  
2. Denegaciones explícitas para abusadores conocidos  
3. Listas de permitir/denegar basadas en archivos  
4. Registradores para limitación progresiva  
5. Regla predeterminada como comodín

## Ejemplo completo

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Notas de implementación

- El filtro de acceso opera en la capa de tunnel, antes del procesamiento de la aplicación, de modo que el tráfico abusivo pueda rechazarse de forma temprana.  
- Coloca el archivo de filtro en tu directorio de configuración de I2PTunnel y reinicia el tunnel para aplicar los cambios.  
- Comparte listas basadas en archivos entre varios tunnels si quieres una política coherente en todos los servicios.
