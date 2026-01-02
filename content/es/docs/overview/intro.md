---
title: "Introducción a I2P"
description: "Una introducción menos técnica a la red anónima I2P"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## ¿Qué es I2P?

El Invisible Internet Project (I2P) es una capa de red anónima que permite la comunicación peer-to-peer resistente a la censura. Las conexiones anónimas se logran cifrando el tráfico del usuario y enviándolo a través de una red distribuida operada por voluntarios alrededor del mundo.

## Características Clave

### Anonymity

I2P oculta tanto al emisor como al receptor de los mensajes. A diferencia de las conexiones de internet tradicionales donde tu dirección IP es visible para sitios web y servicios, I2P utiliza múltiples capas de cifrado y enrutamiento para mantener tu identidad privada.

### Decentralization

No existe una autoridad central en I2P. La red es mantenida por voluntarios que donan ancho de banda y recursos computacionales. Esto la hace resistente a la censura y a puntos únicos de fallo.

### Anonimato

Todo el tráfico dentro de I2P está cifrado de extremo a extremo. Los mensajes se cifran múltiples veces a medida que pasan por la red, de manera similar a cómo funciona Tor pero con diferencias importantes en la implementación.

## How It Works

### Descentralización

I2P utiliza "tunnels" para enrutar el tráfico. Cuando envías o recibes datos:

1. Tu router crea un túnel de salida (para enviar)
2. Tu router crea un túnel de entrada (para recibir)
3. Los mensajes se cifran y envían a través de múltiples routers
4. Cada router solo conoce el salto anterior y el siguiente, no la ruta completa

### Cifrado de Extremo a Extremo

I2P mejora el enrutamiento cebolla tradicional con "garlic routing":

- Se pueden agrupar múltiples mensajes juntos (como dientes en un bulbo de ajo)
- Esto proporciona mejor rendimiento y anonimato adicional
- Dificulta el análisis de tráfico

### Network Database

I2P mantiene una base de datos de red distribuida que contiene:

- Información del router
- Direcciones de destino (similares a sitios web .i2p)
- Datos de enrutamiento cifrados

## Common Use Cases

### Túneles

Aloja o visita sitios web que terminan en `.i2p` - estos solo son accesibles dentro de la red I2P y proporcionan fuertes garantías de anonimato tanto para los hosts como para los visitantes.

### Enrutamiento Garlic

Comparte archivos de forma anónima usando BitTorrent sobre I2P. Muchas aplicaciones de torrents tienen soporte para I2P integrado.

### Base de Datos de Red

Envía y recibe correo electrónico anónimo usando I2P-Bote u otras aplicaciones de correo electrónico diseñadas para I2P.

### Messaging

Usa IRC, mensajería instantánea u otras herramientas de comunicación de forma privada sobre la red I2P.

## Getting Started

¿Listo para probar I2P? Consulta nuestra [página de descargas](/downloads) para instalar I2P en tu sistema.

Para más detalles técnicos, consulta la [Introducción Técnica](/docs/overview/tech-intro) o explora la [documentación](/docs) completa.

## Cómo Funciona

- [Introducción Técnica](/docs/overview/tech-intro) - Conceptos técnicos más profundos
- [Modelo de Amenazas](/docs/overview/threat-model) - Comprender el modelo de seguridad de I2P
- [Comparación con Tor](/docs/overview/comparison) - En qué se diferencia I2P de Tor
- [Criptografía](/docs/specs/cryptography) - Detalles sobre los algoritmos criptográficos de I2P
