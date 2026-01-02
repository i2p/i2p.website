---
title: "Enrutamiento de Túneles"
description: "Descripción general de la terminología, construcción y ciclo de vida de los túneles I2P"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

I2P construye túneles temporales y unidireccionales — secuencias ordenadas de routers que reenvían tráfico cifrado. Los túneles se clasifican como **inbound** (los mensajes fluyen hacia el creador) o **outbound** (los mensajes fluyen desde el creador).

Un intercambio típico enruta el mensaje de Alice a través de uno de sus túneles de salida, instruye al punto final de salida para que lo reenvíe a la puerta de enlace de uno de los túneles de entrada de Bob, y luego Bob lo recibe en su punto final de entrada.

![Alice conectándose a través de su túnel de salida a Bob mediante su túnel de entrada](/images/tunnelSending.png)

- **A**: Gateway de Salida (Alice)
- **B**: Participante de Salida
- **C**: Punto Final de Salida
- **D**: Gateway de Entrada
- **E**: Participante de Entrada
- **F**: Punto Final de Entrada (Bob)

Los tunnels tienen una duración fija de 10 minutos y transportan mensajes de tamaño fijo de 1024 bytes (1028 bytes incluyendo el encabezado del tunnel) para prevenir el análisis de tráfico basado en patrones de tamaño o temporización de mensajes.

## Vocabulario de Túneles

- **Tunnel gateway:** Primer router en un túnel. Para túneles de entrada, la identidad de este router aparece en el [LeaseSet](/docs/specs/common-structures/) publicado. Para túneles de salida, el gateway es el router de origen (A y D arriba).
- **Tunnel endpoint:** Último router en un túnel (C y F arriba).
- **Tunnel participant:** Router intermedio en un túnel (B y E arriba). Los participantes no pueden determinar su posición o la dirección del túnel.
- **Túnel de n-saltos:** Número de saltos entre routers.
  - **0-saltos:** Gateway y endpoint son el mismo router – anonimato mínimo.
  - **1-salto:** Gateway se conecta directamente al endpoint – baja latencia, bajo anonimato.
  - **2-saltos:** Predeterminado para túneles exploratorios; seguridad/rendimiento balanceado.
  - **3-saltos:** Recomendado para aplicaciones que requieren anonimato fuerte.
- **Tunnel ID:** Entero de 4 bytes único por router y por salto, elegido aleatoriamente por el creador. Cada salto recibe y reenvía con IDs diferentes.

## Información de Construcción de Túneles

Los routers que cumplen los roles de gateway (puerta de enlace), participant (participante) y endpoint (punto final) reciben diferentes registros dentro del Mensaje de Construcción de Túnel. El I2P moderno soporta dos métodos:

- **ElGamal** (heredado, registros de 528 bytes)
- **ECIES-X25519** (actual, registros de 218 bytes mediante Short Tunnel Build Message – STBM)

### Information Distributed to Participants

**El gateway recibe:** - Clave de capa de tunnel (clave AES-256 o ChaCha20 dependiendo del tipo de tunnel) - Clave IV de tunnel (para cifrar vectores de inicialización) - Clave de respuesta e IV de respuesta (para el cifrado de respuesta de construcción) - ID de tunnel (solo gateways de entrada) - Hash de identidad del siguiente salto e ID de tunnel (si no es terminal)

**Los participantes intermedios reciben:** - Clave de capa de tunnel e IV para su salto - ID del tunnel e información del siguiente salto - Clave de respuesta e IV para el cifrado de la respuesta de construcción

**Los endpoints reciben:** - Claves de la capa de túnel e IV - Router de respuesta e ID del túnel (solo endpoints salientes) - Clave de respuesta e IV (solo endpoints salientes)

Para más detalles consulte la [Especificación de Creación de Túneles](/docs/specs/implementation/) y la [Especificación de Creación de Túneles ECIES](/docs/specs/implementation/).

## Tunnel Pooling

Los routers agrupan túneles en **conjuntos de túneles** (tunnel pools) para redundancia y distribución de carga. Cada conjunto mantiene múltiples túneles paralelos, permitiendo la conmutación por error cuando uno falla. Los conjuntos utilizados internamente son **túneles exploratorios** (exploratory tunnels), mientras que los conjuntos específicos de aplicaciones son **túneles de cliente** (client tunnels).

Cada destino mantiene pools de entrada y salida separados configurados mediante opciones I2CP (cantidad de túneles, cantidad de respaldo, longitud y parámetros de QoS). Los routers monitorean la salud de los túneles, ejecutan pruebas periódicas y reconstruyen automáticamente los túneles fallidos para mantener el tamaño del pool.

## Agrupación de túneles

**Túneles de 0 saltos**: Ofrecen únicamente negación plausible. El tráfico siempre se origina y termina en el mismo router — desaconsejado para cualquier uso anónimo.

**Túneles de 1 salto**: Proporcionan anonimato básico contra observadores pasivos, pero son vulnerables si un adversario controla ese único salto.

**Túneles de 2 saltos**: Incluyen dos routers remotos y aumentan sustancialmente el costo de ataque. Predeterminado para pools exploratorios.

**Túneles de 3 saltos**: Recomendado para aplicaciones que requieren protección robusta de anonimato. Los saltos adicionales añaden latencia sin una ganancia significativa de seguridad.

**Valores predeterminados**: Los routers utilizan túneles exploratorios de **2 saltos** y túneles de cliente específicos de aplicación de **2 o 3 saltos**, equilibrando rendimiento y anonimato.

## Longitud del Túnel

Los routers prueban periódicamente los túneles enviando un `DeliveryStatusMessage` a través de un túnel de salida hacia un túnel de entrada. Si la prueba falla, ambos túneles reciben una ponderación negativa en el perfil. Fallos consecutivos marcan un túnel como inutilizable; el router entonces reconstruye un reemplazo y publica un nuevo LeaseSet. Los resultados alimentan las métricas de capacidad de peers utilizadas por el [sistema de selección de peers](/docs/overview/tunnel-routing/).

## Prueba de Túneles

Los routers construyen túneles usando un método **telescópico** no interactivo: un único Tunnel Build Message se propaga salto a salto. Cada salto descifra su registro, añade su respuesta y reenvía el mensaje. El salto final devuelve la respuesta agregada de construcción a través de una ruta diferente, evitando la correlación. Las implementaciones modernas usan **Short Tunnel Build Messages (STBM)** para ECIES y **Variable Tunnel Build Messages (VTBM)** para rutas heredadas. Cada registro se cifra por salto usando ElGamal o ECIES-X25519.

## Creación de Túneles

El tráfico del túnel utiliza cifrado multicapa. Cada salto agrega o elimina una capa de cifrado a medida que los mensajes atraviesan el túnel.

- **Túneles ElGamal:** AES-256/CBC para cargas útiles con relleno PKCS#5.
- **Túneles ECIES:** ChaCha20 o ChaCha20-Poly1305 para cifrado autenticado.

Cada salto tiene dos claves: una **clave de capa** y una **clave IV**. Los routers descifran el IV, lo usan para procesar la carga útil, y luego vuelven a cifrar el IV antes de reenviar. Este esquema de doble IV previene el etiquetado de mensajes.

Los gateways de salida pre-descifran todas las capas para que los endpoints reciban texto plano después de que todos los participantes hayan añadido cifrado. Los túneles de entrada cifran en la dirección opuesta. Los participantes no pueden determinar la dirección o longitud del túnel.

## Cifrado de Túnel

- Tiempos de vida dinámicos de túneles y dimensionamiento adaptativo de pools para balanceo de carga de red
- Estrategias alternativas de prueba de túneles y diagnósticos de saltos individuales
- Validación opcional de proof-of-work o certificados de ancho de banda (implementado en API 0.9.65+)
- Investigación de modelado de tráfico e inserción de chaff para mezcla de endpoints
- Retiro continuo de ElGamal y migración a ECIES-X25519

## Desarrollo Continuo

- [Especificación de Implementación de Túneles](/docs/specs/implementation/)
- [Especificación de Creación de Túneles (ElGamal)](/docs/specs/implementation/)
- [Especificación de Creación de Túneles (ECIES-X25519)](/docs/specs/implementation/)
- [Especificación de Mensajes de Túnel](/docs/specs/implementation/)
- [Enrutamiento Garlic](/docs/overview/garlic-routing/)
- [Base de Datos de Red I2P](/docs/specs/common-structures/)
- [Perfilado y Selección de Pares](/docs/overview/tunnel-routing/)
- [Modelo de Amenazas de I2P](/docs/overview/threat-model/)
- [Cifrado ElGamal/AES + SessionTag](/docs/legacy/elgamal-aes/)
- [Opciones I2CP](/docs/specs/i2cp/)
