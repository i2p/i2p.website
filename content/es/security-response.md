---
title: "Proceso de Respuesta a Vulnerabilidades"
description: "Proceso de reporte y respuesta a vulnerabilidades de seguridad de I2P"
layout: "security-response"
aliases:
  - /en/research/vrp
---

<div id="contact"></div>

## Reportar una Vulnerabilidad

¿Descubriste un problema de seguridad? Repórtalo a **security@i2p.net** (se recomienda PGP)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">Descargar clave PGP</a> | Huella digital de la clave GPG: `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Directrices de Investigación

**Por favor NO:**
- Explotar la red I2P en vivo
- Realizar ingeniería social o atacar la infraestructura de I2P
- Interrumpir los servicios para otros usuarios

**Por favor SÍ:**
- Utilizar redes de prueba aisladas cuando sea posible
- Seguir prácticas de divulgación coordinada
- Contactarnos antes de realizar pruebas en la red en vivo

<div id="process"></div>

## Proceso de Respuesta

### 1. Reporte Recibido
- Respuesta dentro de **3 días laborables**
- Asignación de un Gerente de Respuesta
- Clasificación de severidad (ALTA/MEDIA/BAJA)

### 2. Investigación y Desarrollo
- Desarrollo de parches privados vía canales cifrados
- Pruebas en red aislada
- **Severidad ALTA:** Notificación pública dentro de 3 días (sin detalles de explotación)

### 3. Lanzamiento y Divulgación
- Implementación de actualización de seguridad
- Cronograma máximo de **90 días** para divulgación completa
- Crédito opcional al investigador en anuncios

### Niveles de Severidad

**ALTA** - Impacto en toda la red, se requiere atención inmediata
**MEDIA** - Routers individuales, explotación dirigida
**BAJA** - Impacto limitado, escenarios teóricos

<div id="communication"></div>

## Comunicación Segura

Utiliza cifrado PGP/GPG para todos los informes de seguridad:

```
Huella digital: 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

Incluye en tu informe:
- Descripción técnica detallada
- Pasos para reproducir
- Código de prueba de concepto (si es aplicable)

<div id="timeline"></div>

## Cronograma

| Fase | Periodo |
|------|---------|
| Respuesta Inicial | 0-3 días |
| Investigación | 1-2 semanas |
| Desarrollo y Pruebas | 2-6 semanas |
| Lanzamiento | 6-12 semanas |
| Divulgación Completa | Max. 90 días |

<div id="faq"></div>

## Preguntas Frecuentes

**¿Tendré problemas por reportar?**
No. La divulgación responsable es apreciada y protegida.

**¿Puedo probar en la red en vivo?**
No. Utiliza solo redes de prueba aisladas.

**¿Puedo mantenerme anónimo?**
Sí, aunque podría complicar la comunicación.

**¿Ofrecen recompensas por errores?**
Actualmente no. I2P es impulsado por voluntarios con recursos limitados.

<div id="examples"></div>

## Qué Reportar

**En Alcance:**
- Vulnerabilidades del router I2P
- Fallos en protocolo o criptografía
- Ataques a nivel de red
- Técnicas de desanonimización
- Problemas de denegación de servicio

**Fuera de Alcance:**
- Aplicaciones de terceros (contactar a los desarrolladores)
- Ingeniería social o ataques físicos
- Vulnerabilidades conocidas/divulgadas
- Problemas puramente teóricos

---

**¡Gracias por ayudar a mantener la seguridad de I2P!**
