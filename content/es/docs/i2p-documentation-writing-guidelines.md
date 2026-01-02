---
title: "Pautas de redacción de la documentación de I2P"
description: "Mantén la coherencia, la precisión y la accesibilidad en toda la documentación técnica de I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Propósito:** Mantener la coherencia, la precisión y la accesibilidad en toda la documentación técnica de I2P

---

## Principios fundamentales

### 1. Verifique todo

**Nunca asumas ni adivines.** Todas las afirmaciones técnicas deben verificarse frente a: - Código fuente actual de I2P (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Documentación oficial de la API (https://i2p.github.io/i2p.i2p/  - Especificaciones de configuración [/docs/specs/](/docs/) - Notas de lanzamiento recientes [/releases/](/categories/release/)

**Ejemplo de verificación adecuada:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. La claridad por encima de la brevedad

Escribe para desarrolladores que quizá estén conociendo I2P por primera vez. Explica los conceptos por completo en lugar de asumir conocimientos previos.

**Ejemplo:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Primero la accesibilidad

La documentación debe ser accesible para los desarrolladores desde la clearnet (internet convencional) aunque I2P sea una superposición de red. Proporcione siempre alternativas accesibles desde la clearnet a los recursos internos de I2P.

---

## Precisión técnica

### Documentación de la API y de la interfaz

**Incluye siempre:** 1. Nombres de paquete completos en la primera mención: `net.i2p.app.ClientApp` 2. Firmas de métodos completas con tipos de retorno 3. Nombres y tipos de parámetros 4. Parámetros obligatorios vs opcionales

**Ejemplo:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Propiedades de configuración

Al documentar archivos de configuración: 1. Mostrar los nombres exactos de las propiedades 2. Especificar la codificación del archivo (UTF-8 para configuraciones de I2P) 3. Proporcionar ejemplos completos 4. Documentar los valores predeterminados 5. Indicar la versión en la que se introdujeron/cambiaron las propiedades

**Ejemplo:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Constantes y enumeraciones

Al documentar constantes, utiliza los nombres reales del código:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Distinguir entre conceptos similares

I2P tiene varios sistemas superpuestos. Aclara siempre qué sistema estás documentando:

**Ejemplo:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## URLs y referencias de la documentación

### Reglas de accesibilidad de URL

1. **Referencias principales** deben usar URLs accesibles desde la Internet abierta
2. **URLs internas de I2P** (dominios .i2p) deben incluir notas de accesibilidad
3. **Proporcione siempre alternativas** al enlazar recursos internos de I2P

**Plantilla para URLs internas de I2P:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### URLs de referencia recomendadas para I2P

**Especificaciones oficiales:** - [Configuración](/docs/specs/configuration/) - [Complemento](/docs/specs/plugin/) - [Índice de documentación](/docs/)

**Documentación de la API (elige la más reciente):** - Más reciente: https://i2p.github.io/i2p.i2p/ (API 0.9.66 a partir de I2P 2.10.0) - Espejo en clearnet (red abierta): https://eyedeekay.github.io/javadoc-i2p/

**Código fuente:** - GitLab (oficial): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - Espejo en GitHub: https://github.com/i2p/i2p.i2p

### Normas de formato de enlaces

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Seguimiento de versiones

### Metadatos del documento

Todo documento técnico debe incluir metadatos de versión en el frontmatter (cabecera de metadatos):

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Definiciones de campos:** - `lastUpdated`: Año-mes cuando el documento fue revisado/actualizado por última vez - `accurateFor`: Versión de I2P con la que se verificó el documento - `reviewStatus`: Uno de "draft", "needs-review", "verified", "outdated"

### Referencias de versión en el contenido

Al mencionar versiones: 1. Usa **negrita** para la versión actual: "**versión 2.10.0** (septiembre de 2025)" 2. Especifica tanto el número de versión como la fecha para referencias históricas 3. Indica la versión de la API por separado de la versión de I2P cuando sea relevante

**Ejemplo:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Documentación de los cambios a lo largo del tiempo

Para las características que evolucionaron:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Avisos de obsolescencia

Si se documentan características obsoletas:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Estándares de terminología

### Términos oficiales de I2P

Usa estos términos exactos de manera consistente:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Terminología de clientes gestionados

Al documentar clientes gestionados:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Terminología de configuración

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Nombres de paquetes y clases

Use siempre nombres completamente calificados en la primera mención, y nombres cortos en lo sucesivo:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Ejemplos de código y formato

### Ejemplos de código Java

Utiliza un resaltado de sintaxis adecuado y ejemplos completos:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Requisitos del ejemplo de código:** 1. Incluye comentarios que expliquen las líneas clave 2. Muestra el manejo de errores cuando sea pertinente 3. Utiliza nombres de variables realistas 4. Cumple con las convenciones de codificación de I2P (indentación de 4 espacios) 5. Muestra las importaciones si no son obvias por el contexto

### Ejemplos de configuración

Mostrar ejemplos completos y válidos de configuración:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Ejemplos de línea de comandos

Usa `$` para comandos de usuario, `#` para root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Código en línea

Usa comillas invertidas para: - Nombres de métodos: `startup()` - Nombres de clases: `ClientApp` - Nombres de propiedades: `clientApp.0.main` - Nombres de archivos: `clients.config` - Constantes: `SVC_HTTP_PROXY` - Nombres de paquetes: `net.i2p.app`

---

## Tono y voz

### Profesional pero accesible

Redacta para una audiencia técnica sin ser condescendiente:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Voz activa

Usa la voz activa para mayor claridad:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Imperativos para instrucciones

Usa imperativos directos en el contenido procedimental:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Evite la jerga innecesaria

Explica los términos la primera vez que se usen:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Directrices de puntuación

1. **Sin guiones largos** - use guiones normales, comas o punto y coma en su lugar
2. Use la **coma de Oxford** en listas: "console, i2ptunnel, and Jetty"
3. **Puntos dentro de bloques de código** solo cuando sea gramaticalmente necesario
4. **Listas en serie** utilizan punto y coma cuando los elementos contienen comas

---

## Estructura del documento

### Orden estándar de secciones

Para la documentación de la API:

1. **Descripción general** - qué hace la característica, por qué existe
2. **Implementación** - cómo implementarla/usarla
3. **Configuración** - cómo configurarla
4. **Referencia de API** - descripciones detalladas de métodos/propiedades
5. **Ejemplos** - ejemplos completos y funcionales
6. **Mejores prácticas** - consejos y recomendaciones
7. **Historial de versiones** - cuándo se introdujo, cambios a lo largo del tiempo
8. **Referencias** - enlaces a documentación relacionada

### Jerarquía de encabezados

Utilice niveles de encabezado semánticos:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Cajas de información

Utiliza citas en bloque para avisos especiales:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Listas y organización

**Listas no ordenadas** para elementos no secuenciales:

```markdown
- First item
- Second item
- Third item
```
**Listas ordenadas** para pasos secuenciales:

```markdown
1. First step
2. Second step
3. Third step
```
**Listas de definiciones** para explicaciones de términos:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Errores comunes que se deben evitar

### 1. Confundir sistemas similares

**No confundir:** - registro de ClientAppManager vs. PortMapper - tipos de tunnel de i2ptunnel vs. constantes del servicio de port mapper - ClientApp vs. RouterApp (contextos diferentes) - clientes gestionados vs. no gestionados

**Aclara siempre de qué sistema** estás hablando:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Referencias a versiones obsoletas

**No hagas:** - Hacer referencia a versiones anteriores como "actuales" - Enlazar a documentación de la API desactualizada - Usar firmas de métodos en desuso en los ejemplos

**Haz:** - Consulta las notas de la versión antes de publicar - Verifica que la documentación de la API coincida con la versión actual - Actualiza los ejemplos para usar las mejores prácticas actuales

### 3. URLs inaccesibles

**No hagas:** - Enlazar únicamente a dominios .i2p sin alternativas en clearnet (Internet abierta) - Usar URLs de documentación rotas u obsoletas - Enlazar a rutas locales file://

**Haz:** - Proporciona alternativas en clearnet (Internet pública) para todos los enlaces internos de I2P - Verifica que las URL sean accesibles antes de publicar - Usa URL persistentes (geti2p.net, no alojamiento temporal)

### 4. Ejemplos de código incompletos

**No hagas:** - Mostrar fragmentos sin contexto - Omitir el manejo de errores - Usar variables indefinidas - Omitir declaraciones de importación cuando no sea obvio

**Haz:** - Muestra ejemplos completos y compilables - Incluye el manejo de errores necesario - Explica qué hace cada línea significativa - Prueba los ejemplos antes de publicarlos

### 5. Declaraciones ambiguas

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Convenciones de Markdown

### Nomenclatura de archivos

Usa kebab-case (palabras separadas por guiones) para los nombres de archivo: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Formato del front matter (bloque de metadatos al inicio del documento)

Incluye siempre el front matter de YAML (cabecera de metadatos):

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Formato de enlaces

**Enlaces internos** (dentro de la documentación):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Enlaces externos** (a otros recursos):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Enlaces a repositorios de código**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Formato de tablas

Usa tablas de Markdown al estilo de GitHub:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Etiquetas de lenguaje para bloques de código

Especifica siempre el lenguaje para el resaltado de sintaxis:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## Lista de verificación de revisión

Antes de publicar la documentación, verifica:

- [ ] Todas las afirmaciones técnicas están verificadas frente al código fuente o la documentación oficial
- [ ] Los números de versión y las fechas están actualizados
- [ ] Todas las URLs son accesibles desde clearnet (Internet abierta) (o se proporcionan alternativas)
- [ ] Los ejemplos de código son completos y han sido probados
- [ ] La terminología sigue las convenciones de I2P
- [ ] Sin guiones largos (em dashes) (usa guiones normales u otros signos de puntuación)
- [ ] El frontmatter (metadatos iniciales del documento) está completo y es preciso
- [ ] La jerarquía de encabezados es semántica (h1 → h2 → h3)
- [ ] Las listas y las tablas están correctamente formateadas
- [ ] La sección de referencias incluye todas las fuentes citadas
- [ ] El documento sigue las directrices de estructura
- [ ] El tono es profesional pero accesible
- [ ] Los conceptos similares están claramente diferenciados
- [ ] No hay enlaces ni referencias rotos
- [ ] Los ejemplos de configuración son válidos y actuales

---

**Comentarios:** Si encuentra problemas o tiene sugerencias para estas directrices, envíelos a través de los canales oficiales de desarrollo de I2P.
