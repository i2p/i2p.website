---
title: "SAMv3"
description: "Protocolo de Mensajería Anónima Simple para aplicaciones I2P no Java"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM es un protocolo cliente sencillo para interactuar con I2P. SAM es el protocolo recomendado para que aplicaciones no-Java se conecten a la red I2P, y es compatible con múltiples implementaciones de routers. Las aplicaciones Java deberían usar directamente las API de transmisión o I2CP.

La versión 3 de SAM se introdujo en la versión de I2P 0.7.3 (mayo de 2009) y es una interfaz estable y compatible. La versión 3.1 también es estable y soporta la opción de tipo de firma, la cual se recomienda encarecidamente. Las versiones 3.x más recientes soportan funciones avanzadas. Tenga en cuenta que i2pd actualmente no soporta la mayoría de las funciones de las versiones 3.2 y 3.3.

Alternativas: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (obsoleto)](/docs/api/bob). Versiones obsoletas: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Bibliotecas SAM conocidas

Advertencia: Algunos de estos pueden ser muy antiguos o ya no tener soporte. Ninguno ha sido probado, revisado o mantenido por el proyecto I2P, salvo que se indique lo contrario más abajo. Realice su propia investigación.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Inicio rápido

Para implementar una aplicación básica punto a punto solo con TCP, el cliente debe soportar los siguientes comandos:

- `HELLO VERSION MIN=3.1 MAX=3.1` - Necesario para todos los demás comandos
- `DEST GENERATE SIGNATURE_TYPE=7` - Para generar nuestra clave privada y destino
- `NAMING LOOKUP NAME=...` - Para convertir direcciones .i2p en destinos
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - Necesario para STREAM CONNECT y STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` - Para realizar conexiones salientes
- `STREAM ACCEPT ID=...` - Para aceptar conexiones entrantes

## Orientación general para desarrolladores

### Diseño de la aplicación

Las sesiones SAM (o dentro de I2P, grupos de túneles o conjuntos de túneles) están diseñadas para tener una larga duración. La mayoría de las aplicaciones solo necesitarán una sesión, creada al iniciarse y cerrada al salir. I2P es diferente de Tor, donde los circuitos pueden crearse y descartarse rápidamente. Piense cuidadosamente y consulte con los desarrolladores de I2P antes de diseñar su aplicación para usar más de una o dos sesiones simultáneas, o para crear y descartar sesiones rápidamente. La mayoría de los modelos de amenazas no requerirán una sesión única para cada conexión.

Además, asegúrese de que la configuración de su aplicación (y las indicaciones a los usuarios sobre la configuración del router, o los valores predeterminados del router si incluye uno) haga que sus usuarios aporten más recursos a la red de los que consumen. I2P es una red entre pares (peer-to-peer), y la red no puede sobrevivir si una aplicación popular lleva a la red a una congestión permanente.

### Compatibilidad y pruebas

Las implementaciones del router Java I2P e i2pd son independientes y tienen pequeñas diferencias en el comportamiento, soporte de funciones y valores predeterminados. Pruebe su aplicación con la última versión de ambos routers.

i2pd SAM está habilitado de forma predeterminada; Java I2P SAM no lo está. Proporcione instrucciones a sus usuarios sobre cómo habilitar SAM en Java I2P (a través de /configclients en la consola del router), y/o proporcione un mensaje de error claro al usuario si la conexión inicial falla, por ejemplo: "asegúrese de que I2P esté en ejecución y de que la interfaz SAM esté habilitada".

Los routers Java I2P e i2pd tienen valores predeterminados diferentes para la cantidad de túneles. El valor predeterminado en Java es 2 y el de i2pd es 5. Para la mayoría de los casos con ancho de banda bajo a medio y con cantidades bajas a medias de conexiones, 2 o 3 son suficientes. Especifique la cantidad de túneles en el mensaje SESSION CREATE para obtener un rendimiento consistente con los routers Java I2P e i2pd. Vea a continuación.

Para obtener más orientación para desarrolladores sobre cómo garantizar que su aplicación utilice únicamente los recursos que necesita, consulte [nuestra guía para integrar I2P con su aplicación](/docs/applications/embedding).

### Tipos de firma y cifrado

I2P admite múltiples tipos de firma y cifrado. Por compatibilidad con versiones anteriores, SAM utiliza por defecto tipos antiguos e ineficientes, por lo que todos los clientes deberían especificar tipos más recientes.

El tipo de firma se especifica en los comandos DEST GENERATE y SESSION CREATE (para transitorios). Todos los clientes deben establecer `SIGNATURE_TYPE=7` (Ed25519).

El tipo de cifrado se especifica en el comando SESSION CREATE. Se permiten múltiples tipos de cifrado. Los clientes deben establecer `i2cp.leaseSetEncType=4` (solo para ECIES-X25519) o `i2cp.leaseSetEncType=6,4` (para MLKEM-768 y ECIES-X25519, para routers que soporten la API 0.9.67 o superior).

## Cambios en la versión 3

### Cambios en la versión 3.0

La versión 3.0 se introdujo en la versión de I2P 0.7.3. SAM v2 proporcionaba una forma de gestionar varios sockets en el mismo destino de I2P *en paralelo*, es decir, el cliente no tenía que esperar a que los datos se enviaran correctamente a través de un socket antes de enviar datos por otro socket. Pero todos los datos transitaban a través del mismo socket cliente-SAM, lo cual era bastante complicado de gestionar para el cliente.

SAM v3 gestiona los sockets de una manera diferente: cada *socket I2P* coincide con un socket único cliente-SAM, lo cual es mucho más sencillo de manejar. Esto es similar a [BOB](/docs/api/bob).

SAM v3 también ofrece un puerto UDP para enviar datagramas a través de I2P, y puede reenviar al cliente los datagramas I2P entrantes desde su servidor de datagramas.

### Cambios en la versión 3.1

La versión 3.1 se introdujo en el lanzamiento de Java I2P 0.9.14 (julio de 2014). SAM 3.1 es la implementación mínima recomendada debido a su soporte para tipos de firma mejores que SAM 3.0. i2pd también admite la mayoría de las características de la versión 3.1.

- DEST GENERATE y SESSION CREATE ahora admiten un parámetro SIGNATURE_TYPE.
- Los parámetros MIN y MAX en HELLO VERSION ahora son opcionales.
- Los parámetros MIN y MAX en HELLO VERSION ahora admiten versiones de un solo dígito como "3".
- RAW SEND ahora es compatible con el socket puente.

### Cambios en la versión 3.2

La versión 3.2 se introdujo en el lanzamiento de Java I2P 0.9.24 (enero de 2016). Tenga en cuenta que i2pd actualmente no admite la mayoría de las funciones de la versión 3.2.

#### Soporte de puerto y protocolo I2CP

- Opciones FROM_PORT y TO_PORT en SESSION CREATE
- Opción PROTOCOL en SESSION CREATE con STYLE=RAW
- Opciones FROM_PORT y TO_PORT en STREAM CONNECT, DATAGRAM SEND y RAW SEND
- Opción PROTOCOL en RAW SEND
- DATAGRAM RECEIVED, RAW RECEIVED, y flujos o datagramas recibidos o reenviados, incluyen FROM_PORT y TO_PORT
- La opción de sesión RAW HEADER=true hará que a los datagramas RAW reenviados se les anteponga una línea con PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- La primera línea de los datagramas enviados a través del puerto 7655 ahora puede comenzar con cualquier versión 3.x
- La primera línea de los datagramas enviados a través del puerto 7655 puede contener cualquiera de las opciones FROM_PORT, TO_PORT, PROTOCOL
- RAW RECEIVED incluye PROTOCOL=nnn

#### SSL y Autenticación

- USER/PASSWORD en los parámetros de HELLO para autorización. Ver [abajo](#authorization).
- Configuración opcional de autorización con el comando AUTH. Ver [abajo](#authorization-configuration-sam-32-or-higher-optional-feature).
- Soporte opcional de SSL/TLS en el socket de control. Ver [abajo](#ssl).
- Opción STREAM FORWARD SSL=true

#### Multithreading

- Se permiten múltiples ACCEPT de STREAM pendientes simultáneos en el mismo ID de sesión.

#### Análisis de Línea de Comandos y Mantenimiento de Conexión (Keepalive)

- Comandos opcionales QUIT, STOP y EXIT para cerrar la sesión y el socket. Consulte [abajo](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- El análisis de comandos manejará correctamente UTF-8.
- El análisis de comandos maneja de forma confiable los espacios en blanco dentro de comillas.
- Una barra invertida '\\' puede escapar comillas en la línea de comandos.
- Se recomienda que el servidor mapee los comandos a mayúsculas, para facilitar las pruebas mediante telnet.
- Pueden permitirse valores de opción vacíos como PROTOCOL o PROTOCOL=, dependiendo de la implementación.
- PING/PONG para mantener la conexión activa. Ver más abajo.
- Los servidores pueden implementar tiempos de espera para el comando HELLO o comandos posteriores, dependiendo de la implementación.

### Cambios en la versión 3.3

La versión 3.3 fue introducida en el lanzamiento de Java I2P 0.9.25 (marzo de 2016). Tenga en cuenta que i2pd actualmente no admite la mayoría de las funciones de la versión 3.3.

- La misma sesión puede usarse simultáneamente para flujos, datagramas y modo crudo. Los paquetes y flujos entrantes serán enrutados según el protocolo I2P y el puerto de destino. Consulte [la sección PRIMARY más abajo](#sam-primary-sessions-v33-and-higher).
- DATAGRAM SEND y RAW SEND ahora admiten las opciones SEND_TAGS, TAG_THRESHOLD, EXPIRES y SEND_LEASESET. Vea [la sección de envío de datagramas más abajo](#sending-repliable-or-raw-datagrams).

### Cambios de 2025-04

Dos propuestas fueron aprobadas e incorporadas a la especificación aquí en abril de 2025. No hay cambio de versión para indicar el soporte. Algunas implementaciones aún no lo soportan, y en otras, el soporte es preliminar.

- Soporte para datagrama 2/3 (propuesta 163). Especificado en SESSION CREATE y SESSION ADD (subsiones). Ver más abajo.
- Recuperación de opciones de leaseset (propuesta 167). Especificado con NAMING LOOKUP OPTIONS=true. Ver más abajo.

## Protocolo de versión 3

### Especificación de la versión 3.3 de Mensajería Anónima Simple (SAM) - Resumen

La aplicación cliente se comunica con el puente SAM, que gestiona toda la funcionalidad de I2P (usando la [biblioteca de transmisión](/docs/api/streaming) para flujos virtuales, o [I2CP](/docs/protocol/i2cp) directamente para datagramas).

Por defecto, la comunicación entre el cliente y el puente SAM no está cifrada ni autenticada. El puente SAM puede admitir conexiones SSL/TLS; los detalles de configuración e implementación están fuera del alcance de esta especificación. A partir de SAM 3.2, se admiten parámetros opcionales de autenticación usuario/contraseña en el intercambio inicial, y el puente puede requerirlos.

Las comunicaciones de I2P pueden adoptar varias formas distintas:

- [Flujos virtuales](/docs/api/streaming)
- [Datagramas autenticados y con respuesta](/docs/specs/datagrams#repliable) (mensajes con un campo FROM)
- [Datagramas anónimos](/docs/specs/datagrams#raw) (mensajes anónimos en bruto)
- [Datagram2](/docs/specs/datagrams#datagram2) (un nuevo formato autenticado y con respuesta)
- [Datagram3](/docs/specs/datagrams#datagram3) (un nuevo formato con respuesta pero no autenticado)

Las comunicaciones I2P están soportadas por sesiones I2P, y cada sesión I2P está vinculada a una dirección (llamada destino). Una sesión I2P se asocia con uno de los tres tipos anteriores, y no puede llevar comunicaciones de otro tipo, a menos que se utilicen [sesiones PRINCIPALES](#sam-primary-sessions-v33-and-higher).

### Codificación y escape

Todos estos mensajes SAM se envían en una sola línea, terminada por el carácter de nueva línea (\\n). Antes de SAM 3.2, solo se admitía ASCII de 7 bits. A partir de SAM 3.2, la codificación debe ser UTF-8. Cualquier clave o valor codificado en UTF-8 debería funcionar.

El formato mostrado en esta especificación a continuación es únicamente para facilitar la lectura, y aunque las dos primeras palabras en cada mensaje deben mantenerse en su orden específico, el orden de los pares clave=valor puede cambiar (por ejemplo, "ONE TWO A=B C=D" o "ONE TWO C=D A=B" son construcciones igualmente válidas). Además, el protocolo distingue entre mayúsculas y minúsculas. En lo siguiente, los ejemplos de mensajes van precedidos por "->" para los mensajes enviados por el cliente al puente SAM, y por "<-" para los mensajes enviados por el puente SAM al cliente.

La línea básica de comando o respuesta tiene una de las siguientes formas:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
COMMAND sin SUBCOMMAND es compatible solo para algunos comandos nuevos en SAM 3.2.

Los pares clave=valor deben separarse con un solo espacio. (A partir de SAM 3.2, se permiten múltiples espacios) Los valores deben ir entre comillas dobles si contienen espacios, por ejemplo: clave="texto con espacios". (Antes de SAM 3.2, esto no funcionaba de forma confiable en algunas implementaciones)

Antes de SAM 3.2, no existía ningún mecanismo de escape. A partir de SAM 3.2, las comillas dobles pueden escaparse con una barra invertida '\\' y una barra invertida puede representarse como dos barras invertidas '\\\\'.

### Valores vacíos

A partir de SAM 3.2, pueden permitirse valores de opciones vacíos como KEY, KEY= o KEY="", dependiendo de la implementación.

### Sensibilidad a mayúsculas y minúsculas

El protocolo, según se especifica, distingue entre mayúsculas y minúsculas. Se recomienda —aunque no es obligatorio— que el servidor convierta los comandos a mayúsculas, para facilitar las pruebas mediante telnet. Esto permitiría, por ejemplo, que funcionara "hello version". Esto depende de la implementación. No convierta las claves ni los valores a mayúsculas, ya que esto corrompería las opciones [I2CP](/docs/protocol/i2cp).

### Handshake de conexión SAM

No puede haber comunicación SAM hasta que el cliente y el puente hayan acordado una versión del protocolo, lo cual se realiza enviando el cliente un HELLO y el puente respondiendo con un HELLO REPLY:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
y

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
A partir de la versión 3.1 (I2P 0.9.14), los parámetros MIN y MAX son opcionales. SAM siempre devolverá la versión más alta posible dadas las restricciones MIN y MAX, o la versión actual del servidor si no se especifican restricciones.

Si el puente SAM no puede encontrar una versión adecuada, responde con:

```
<- HELLO REPLY RESULT=NOVERSION
```
Si ocurre algún error, como un formato de solicitud incorrecto, responde con:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

El socket de control del servidor puede ofrecer opcionalmente soporte SSL/TLS, según esté configurado en el servidor y el cliente. Las implementaciones pueden ofrecer otras capas de transporte también; esto queda fuera del alcance de la definición del protocolo.

#### Autorización

Para la autorización, el cliente añade USER="xxx" PASSWORD="yyy" a los parámetros de HELLO. Se recomienda usar comillas dobles para el usuario y la contraseña, aunque no es obligatorio. Una comilla doble dentro del usuario o la contraseña debe escaparse con una barra invertida. En caso de fallo, el servidor responderá con un I2P_ERROR y un mensaje. Se recomienda habilitar SSL en cualquier servidor SAM donde se requiera autorización.

#### Tiempo de espera agotado

Los servidores pueden implementar tiempos de espera para el comando HELLO o comandos posteriores, dependiendo de la implementación. Los clientes deben enviar rápidamente el HELLO y el siguiente comando tras la conexión.

Si ocurre un tiempo de espera antes de recibir el HELLO, el puente responde con:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
y luego se desconecta.

Si ocurre un tiempo de espera después de recibir el HELLO pero antes del siguiente comando, el puente responde con:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
y luego se desconecta.

### Puertos y protocolo I2CP

A partir de SAM 3.2, el remitente del cliente SAM puede especificar los puertos y el protocolo [I2CP](/docs/protocol/i2cp) para que se transmitan a [I2CP](/docs/protocol/i2cp), y el puente SAM pasará al cliente SAM la información de puerto y protocolo [I2CP](/docs/protocol/i2cp) recibida.

Para FROM_PORT y TO_PORT, el rango válido es de 0 a 65535, y el valor predeterminado es 0.

Para PROTOCOL, que solo puede especificarse para RAW, el rango válido es de 0 a 255, y el valor predeterminado es 18.

Para los comandos SESSION, los puertos y el protocolo especificados son los valores predeterminados para esa sesión. Para flujos o datagramas individuales, los puertos y el protocolo especificados anulan los valores predeterminados de la sesión. Para flujos o datagramas recibidos, los puertos y el protocolo indicados son los recibidos a través de [I2CP](/docs/protocol/i2cp).

#### Diferencias importantes respecto al IP estándar

Los puertos I2CP son para sockets y datagramas de I2P. No están relacionados con tus sockets locales que se conectan a SAM.

- El puerto 0 es válido y tiene un significado especial.
- Los puertos 1-1023 no son especiales ni privilegiados.
- Los servidores escuchan en el puerto 0 por defecto, lo que significa "todos los puertos".
- Los clientes envían al puerto 0 por defecto, lo que significa "cualquier puerto".
- Los clientes envían desde el puerto 0 por defecto, lo que significa "no especificado".
- Un servidor puede tener un servicio escuchando en el puerto 0 y otros servicios escuchando en puertos superiores. En ese caso, el servicio del puerto 0 es el predeterminado, y será al que se conecte si el puerto entrante del socket o datagrama no coincide con otro servicio.
- La mayoría de los destinos I2P solo tienen un servicio en ejecución, por lo que puedes usar los valores predeterminados e ignorar la configuración de puertos I2CP.
- Se requiere SAM 3.2 o 3.3 para especificar puertos I2CP.
- Si no necesitas puertos I2CP, no necesitas SAM 3.2 ni 3.3; con SAM 3.1 es suficiente.
- El protocolo 0 es válido y significa "cualquier protocolo". Esto no se recomienda y probablemente no funcione.
- Los sockets I2P se rastrean mediante un ID interno de conexión. Por lo tanto, no es necesario que la 5-tupla de dest:puerto:dest:puerto:protocolo sea única. Por ejemplo, puede haber múltiples sockets con los mismos puertos entre dos destinos. Los clientes no necesitan elegir un "puerto libre" para una conexión saliente.

Si estás diseñando una aplicación SAM 3.3 con múltiples subsesiones, piensa cuidadosamente cómo usar los puertos y protocolos de forma eficiente. Consulta la especificación [I2CP](/docs/protocol/i2cp) para obtener más información.

### Sesiones SAM

Una sesión SAM se crea cuando un cliente abre un socket hacia el puente SAM, realiza un handshake y envía un mensaje SESSION CREATE, y la sesión finaliza cuando se desconecta el socket.

Cada Destino I2P registrado está asociado de forma única a un ID de sesión (o apodo). Los IDs de sesión, incluidos los IDs de subsesión para sesiones PRINCIPALES, deben ser globalmente únicos en el servidor SAM. Para prevenir posibles colisiones de IDs con otros clientes, la mejor práctica es que el cliente genere los IDs aleatoriamente.

Cada sesión está asociada de forma única con:

- el socket desde el cual el cliente crea la sesión
- su ID (o apodo)

#### Solicitud de creación de sesión

El mensaje de creación de sesión solo puede usar una de estas formas (los mensajes recibidos mediante otras formas se responden con un mensaje de error):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION especifica qué destino debe utilizarse para enviar y recibir mensajes/flujos. El $privkey es la representación en base 64 de la concatenación de la [Destination](/docs/specs/common-structures#type_Destination), seguida de la [Private Key](/docs/specs/common-structures#type_PrivateKey), seguida de la [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), opcionalmente seguida por la [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), que tiene 663 o más bytes en formato binario y 884 o más bytes en base 64, dependiendo del tipo de firma. El formato binario se especifica en Private Key File. Vea notas adicionales sobre la [Private Key](/docs/specs/common-structures#type_PrivateKey) en la sección Generación de Claves de Destino a continuación.

Si la clave privada de firma es todo ceros, sigue la sección de [Firma sin conexión](/docs/specs/common-structures#struct_OfflineSignature). Las firmas sin conexión solo son compatibles con sesiones STREAM y RAW. Las firmas sin conexión no pueden crearse con DESTINATION=TRANSIENT. El formato de la sección de firma sin conexión es:

1. Marca de tiempo de expiración (4 bytes, big endian, segundos desde la época, se reinicia en 2106)
2. Tipo de firma de la clave pública de firma transitoria (2 bytes, big endian)
3. Clave pública de firma transitoria (longitud según lo especificado por el tipo de firma transitoria)
4. Firma de los tres campos anteriores mediante la clave fuera de línea (longitud según lo especificado por el tipo de firma del destino)
5. Clave privada de firma transitoria (longitud según lo especificado por el tipo de firma transitoria)

Si el destino se especifica como TRANSITORIO, el puente SAM crea un nuevo destino. A partir de la versión 3.1 (I2P 0.9.14), si el destino es TRANSITORIO, se admite un parámetro opcional SIGNATURE_TYPE. El valor de SIGNATURE_TYPE puede ser cualquier nombre (por ejemplo, ECDSA_SHA256_P256, sin distinguir mayúsculas y minúsculas) o número (por ejemplo, 1) admitido por [Certificados de clave](/docs/specs/common-structures#type_Certificate). El valor predeterminado es DSA_SHA1, que NO es lo que desea. Para la mayoría de las aplicaciones, especifique SIGNATURE_TYPE=7.

$nickname es la elección del cliente. No se permite espacios en blanco.

Las opciones adicionales proporcionadas se pasan a la configuración de la sesión de I2P si no son interpretadas por el puente SAM (por ejemplo, outbound.length=0).

Los routers Java I2P e i2pd tienen valores predeterminados diferentes para la cantidad de túneles. El valor predeterminado en Java es 2 y el de i2pd es 5. Para la mayoría de los casos con ancho de banda bajo a medio y cantidades bajas a medias de conexiones, 2 o 3 son suficientes. Especifique las cantidades de túneles en el mensaje SESSION CREATE para obtener un rendimiento consistente con los routers Java I2P e i2pd, utilizando opciones como por ejemplo inbound.quantity=3 outbound.quantity=3. Estas y otras opciones [están documentadas en los enlaces a continuación](#tunnel-i2cp-and-streaming-options).

El puente SAM en sí ya debería estar configurado con qué router debe comunicarse a través de I2P (aunque si es necesario, puede haber una forma de proporcionar una configuración alternativa, por ejemplo i2cp.tcp.host=localhost y i2cp.tcp.port=7654).

#### Respuesta de creación de sesión

Después de recibir el mensaje de creación de sesión, el puente SAM responderá con un mensaje de estado de sesión, de la siguiente manera:

Si la creación fue exitosa:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
La $privkey es la representación base 64 de la concatenación de la [Destination](/docs/specs/common-structures#type_Destination), seguida por la [Private Key](/docs/specs/common-structures#type_PrivateKey), seguida por la [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), opcionalmente seguida por la [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), lo cual tiene 663 o más bytes en binario y 884 o más bytes en base 64, dependiendo del tipo de firma. El formato binario se especifica en Private Key File.

Si el SESSION CREATE contenía una clave privada de firma compuesta completamente por ceros y una sección de [Firma sin conexión](/docs/specs/common-structures#struct_OfflineSignature), la respuesta SESSION STATUS incluirá los mismos datos en el mismo formato. Consulte la sección SESSION CREATE anterior para obtener más detalles.

Si el apodo ya está asociado con una sesión:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Si el destino ya está en uso:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Si el destino no es una clave de destino privado válida:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Si ha ocurrido algún otro error:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Si no está bien, el MENSAJE debe contener información legible para humanos sobre por qué no se pudo crear la sesión.

Tenga en cuenta que el router construye túneles antes de responder con SESSION STATUS. Esto podría tardar varios segundos, o, durante el arranque del router o en caso de congestión severa de la red, un minuto o más. Si no tiene éxito, el router no responderá con un mensaje de error durante varios minutos. No establezca un tiempo de espera corto esperando la respuesta. No abandone la sesión mientras la construcción del túnel esté en curso ni intente reintentarla.

Las sesiones SAM viven y mueren con el socket al que están asociadas. Cuando el socket se cierra, la sesión termina, y todas las comunicaciones que usan dicha sesión también finalizan al mismo tiempo. Y a la inversa, cuando la sesión termina por cualquier motivo, el puente SAM cierra el socket.

### Transmisiones virtuales SAM

Se garantiza que los flujos virtuales se enviarán de forma confiable y en orden, con notificación de éxito o fallo tan pronto como esté disponible.

Los streams son sockets de comunicación bidireccional entre dos destinos I2P, pero su apertura debe ser solicitada por uno de ellos. A partir de ahora, los comandos CONNECT son utilizados por el cliente SAM para dicha solicitud. Los comandos FORWARD / ACCEPT son usados por el cliente SAM cuando desea escuchar solicitudes provenientes de otros destinos I2P.

### Flujos Virtuales SAM: CONECTAR

Un cliente solicita una conexión mediante:

- abrir un nuevo socket con el puente SAM
- pasar el mismo intercambio de saludo HELLO que el anterior
- enviar el comando STREAM CONNECT

#### Solicitud de conexión

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Esto establece una nueva conexión virtual desde la sesión local cuya ID es $nickname al par especificado.

El objetivo es $destination, que es la codificación base 64 de la [Destination](/docs/specs/common-structures#type_Destination), la cual consta de 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

**NOTA:** Desde aproximadamente 2014 (SAM v3.1), Java I2P también ha admitido nombres de host y direcciones b32 para el $destination, aunque esto anteriormente no estaba documentado. Los nombres de host y las direcciones b32 ahora son oficialmente compatibles con Java I2P a partir de la versión 0.9.48. El router i2pd admite nombres de host y direcciones b32 desde la versión 2.38.0 (0.9.50). Para ambos routers, el soporte de "b32" incluye el soporte extendido de direcciones "b33" para destinos enmascarados.

#### Respuesta de conexión

Si se pasa SILENT=true, el puente SAM no emitirá ningún otro mensaje en el socket. Si la conexión falla, el socket será cerrado. Si la conexión tiene éxito, todos los datos restantes que pasen por el socket actual serán reenviados desde y hacia el par de destino I2P conectado.

Si SILENT=false, que es el valor predeterminado, el puente SAM envía un último mensaje a su cliente antes de reenviar o cerrar el socket:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
El valor de RESULTADO puede ser uno de:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Si el RESULTADO es OK, todos los datos restantes que pasan por el socket actual se reenvían desde y hacia el par destino I2P conectado. Si la conexión no fue posible (tiempo de espera agotado, etc.), RESULTADO contendrá el valor de error correspondiente (acompañado por un MENSAJE opcional legible para humanos), y el puente SAM cierra el socket.

El tiempo de espera interno para la conexión del flujo del router es aproximadamente de un minuto, dependiendo de la implementación. No establezca un tiempo de espera más corto al esperar la respuesta.

### Flujos virtuales SAM: ACEPTAR

Un cliente espera una solicitud de conexión entrante mediante:

- abrir un nuevo socket con el puente SAM
- pasar el mismo saludo HELLO como se indicó anteriormente
- enviar el comando STREAM ACCEPT

#### Aceptar solicitud

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Esto hace que la sesión ${nickname} escuche una solicitud de conexión entrante desde la red I2P. No se permite ACCEPT mientras haya un FORWARD activo en la sesión.

A partir de SAM 3.2, se permiten múltiples aceptaciones STREAM pendientes simultáneas en el mismo ID de sesión (incluso con el mismo puerto). Antes de la versión 3.2, las aceptaciones simultáneas fallaban con ALREADY_ACCEPTING. Nota: Java I2P también admite aceptaciones simultáneas en SAM 3.1, a partir de la versión 0.9.24 (2016-01). i2pd también admite aceptaciones simultáneas en SAM 3.1, a partir de la versión 2.50.0 (2023-12).

#### Aceptar respuesta

Si se pasa SILENT=true, el puente SAM no emitirá ningún otro mensaje en el socket. Si la aceptación falla, el socket será cerrado. Si la aceptación tiene éxito, todos los datos restantes que pasen por el socket actual serán reenviados desde y hacia el par de destino I2P conectado. Para mayor confiabilidad, y para recibir el destino de conexiones entrantes, se recomienda SILENT=false.

Si SILENT=false, que es el valor predeterminado, el puente SAM responde con:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
El valor de RESULTADO puede ser uno de:

```
OK
I2P_ERROR
INVALID_ID
```
Si el resultado no es OK, el puente SAM cierra el socket inmediatamente. Si el resultado es OK, el puente SAM comienza a esperar una solicitud de conexión entrante desde otro par I2P. Cuando llega una solicitud, el puente SAM la acepta y:

Si se pasó SILENT=true, el puente SAM no emitirá ningún otro mensaje en el socket del cliente. Todos los datos restantes que pasen por el socket actual se reenviarán desde y hacia el par de destino I2P conectado.

Si se pasó SILENT=false, que es el valor predeterminado, el puente SAM envía al cliente una línea ASCII que contiene la clave pública de destino en base64 del par solicitante, y información adicional solo para SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Después de esta línea terminada en '\\n', todos los datos restantes que pasan a través del socket actual se reenvían desde y hacia el par de destino I2P conectado, hasta que uno de los pares cierre el socket.

#### Errores después de OK

En casos raros, el puente SAM podría encontrar un error después de enviar RESULT=OK, pero antes de que llegue una conexión y se envíe la línea $destination al cliente. Estos errores pueden incluir apagado del router, reinicio del router y cierre de sesión. En estos casos, cuando SILENT=false, el puente SAM podría, aunque no es obligatorio (depende de la implementación), enviar la línea:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
antes de cerrar inmediatamente el socket. Por supuesto, esta línea no es decodificable como un destino Base 64 válido.

### Transmisiones virtuales SAM: REENVÍO

Un cliente puede usar un servidor de sockets regular y esperar solicitudes de conexión provenientes de I2P. Para ello, el cliente debe:

- abrir un nuevo socket con el puente SAM
- enviar el mismo intercambio de saludos HELLO que arriba
- enviar el comando de reenvío

#### Solicitud de reenvío

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Esto hace que la sesión ${nickname} escuche solicitudes de conexión entrantes de la red I2P. No se permite FORWARD mientras haya un ACCEPT pendiente en la sesión.

#### Respuesta de reenvío

SILENT tiene como valor predeterminado false. Tanto si SILENT es true como false, el puente SAM siempre responde con un mensaje STREAM STATUS. Tenga en cuenta que este comportamiento es diferente al de STREAM ACCEPT y STREAM CONNECT cuando SILENT=true. El mensaje STREAM STATUS es:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
El valor de RESULTADO puede ser uno de:

```
OK
I2P_ERROR
INVALID_ID
```
$host es el nombre de host o la dirección IP del servidor de sockets al que SAM redirigirá las solicitudes de conexión. Si no se proporciona, SAM toma la IP del socket que emitió el comando de reenvío.

$port es el número de puerto del servidor de sockets al que SAM redirigirá las solicitudes de conexión. Es obligatorio.

Cuando llega una solicitud de conexión desde I2P, el puente SAM abre una conexión de socket a $host:$port. Si se acepta en menos de 3 segundos, SAM aceptará la conexión desde I2P, y luego:

Si se pasó SILENT=true, todos los datos que pasan por el socket actual obtenido son reenviados desde y hacia el par de destino I2P conectado.

Si se pasó SILENT=false, que es el valor predeterminado, el puente SAM envía a través del socket obtenido una línea ASCII que contiene la clave pública de destino en base64 del par solicitante, y información adicional solo para SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Después de esta línea terminada en '\\n', todos los datos restantes que pasan a través del socket se reenvían desde y hacia el par de destino I2P conectado, hasta que uno de los lados cierra el socket.

A partir de SAM 3.2, si se especifica SSL=true, el socket de reenvío utiliza SSL/TLS.

El router I2P dejará de escuchar solicitudes de conexión entrantes tan pronto como se cierre el socket "forwarding".

### Datagramas SAM

SAMv3 proporciona mecanismos para enviar y recibir datagramas a través de sockets de datagramas locales. Algunas implementaciones de SAMv3 también admiten la forma más antigua v1/v2 de enviar/recibir datagramas a través del socket puente SAM. Ambos métodos se documentan a continuación.

I2P admite cuatro tipos de datagramas:

- Los datagramas reenviables y autenticados tienen como prefijo el destino del remitente y contienen la firma del remitente, de modo que el receptor puede verificar que el destino del remitente no fue falsificado y puede responder al datagrama. El nuevo formato Datagram2 también es reenviable y autenticado.
- El nuevo formato Datagram3 es reenviable pero no autenticado. La información del remitente no está verificada.
- Los datagramas sin procesar (raw datagrams) no contienen el destino del remitente ni una firma.

Los puertos I2CP predeterminados están definidos tanto para datagramas con respuesta como para datagramas sin procesar. El puerto I2CP puede cambiarse para los datagramas sin procesar.

Un patrón común en el diseño de protocolos consiste en enviar datagramas con respuesta a servidores, incluyendo un identificador, y que el servidor responda con un datagrama en bruto que contenga dicho identificador, de modo que la respuesta pueda asociarse con la solicitud. Este patrón de diseño elimina la sobrecarga considerable de los datagramas con respuesta en las respuestas. Todas las elecciones de protocolos y puertos I2CP son específicas de la aplicación, y los diseñadores deben tener en cuenta estos aspectos.

Véanse también las notas importantes sobre el MTU de datagramas en la sección inferior.

#### Envío de datagramas con respuesta o en bruto

Aunque I2P no contiene inherentemente una dirección FROM, para facilitar el uso se proporciona una capa adicional como datagramas con respuesta posible (repliable datagrams): mensajes desordenados e inseguros de hasta 31744 bytes que incluyen una dirección FROM (dejando hasta 1KB para cabeceras). Esta dirección FROM se autentica internamente mediante SAM (haciendo uso de la clave de firma del destino para verificar el origen) e incluye prevención de reproducción (replay prevention).

El tamaño mínimo es de 1. Para obtener la máxima confiabilidad en la entrega, el tamaño máximo recomendado es aproximadamente de 11 KB. La confiabilidad es inversamente proporcional al tamaño del mensaje, quizás incluso de forma exponencial.

Después de establecer una sesión SAM con STYLE=DATAGRAM o STYLE=RAW, el cliente puede enviar datagramas con respuesta o datagramas sin procesar a través del puerto UDP de SAM (7655 por defecto).

La primera línea de un datagrama enviado a través de este puerto debe tener el siguiente formato. Todo esto está en una sola línea (separado por espacios), mostrado en varias líneas para mayor claridad:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 es la versión de SAM. A partir de SAM 3.2, se permite cualquier versión 3.x.
- $nickname es el identificador de la sesión DATAGRAM que se utilizará
- El destino es $destination, que es la codificación en base 64 de la [Destination](/docs/specs/common-structures#type_Destination), con una longitud de 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma. **NOTA:** Desde aproximadamente 2014 (SAM v3.1), Java I2P también ha soportado nombres de host y direcciones b32 para $destination, aunque anteriormente no estaba documentado. Las direcciones b32 y los nombres de host ahora son oficialmente compatibles con Java I2P a partir de la versión 0.9.48. Actualmente, el router i2pd no soporta nombres de host ni direcciones b32; este soporte podría añadirse en futuras versiones.
- Todas las opciones son configuraciones por datagrama que sobrescriben los valores predeterminados especificados en SESSION CREATE.
- Las opciones de la versión 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES y SEND_LEASESET se pasarán a [I2CP](/docs/protocol/i2cp) si son compatibles. Consulte [la especificación I2CP](/docs/protocol/i2cp#msg_SendMessageExpire) para más detalles. El soporte por parte del servidor SAM es opcional; estas opciones serán ignoradas si no son compatibles.
- esta línea termina con '\\n'.

La primera línea será descartada por SAM antes de enviar los datos restantes del mensaje al destino especificado.

Para un método alternativo de enviar datagramas con respuesta y datagramas sin procesar, consulta [DATAGRAM SEND y RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagramas SAM Reembolsables: Recibiendo un Datagrama

Los datagramas recibidos son escritos por SAM en el socket desde el cual se abrió la sesión de datagrama, si no se especifica un PUERTO de reenvío en el comando SESSION CREATE. Esta es la forma compatible con v1/v2 de recibir datagramas.

Cuando llega un datagrama, el puente lo entrega al cliente mediante el mensaje:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
La fuente es $destination, que es la codificación base 64 de la [Destination](/docs/specs/common-structures#type_Destination), compuesta por 516 o más caracteres base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

El puente SAM nunca expone al cliente los encabezados de autenticación ni otros campos, solo los datos que proporcionó el remitente. Esto continúa hasta que la sesión se cierra (cuando el cliente desconecta la conexión).

#### Reenvío de Datagramas en Bruto o Reutilizables

Al crear una sesión de datagrama, el cliente puede solicitar a SAM que redirija los mensajes entrantes a una ip:puerto especificada. Para ello, emite el comando CREATE con las opciones PORT y HOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
El $privkey es el base 64 de la concatenación de la [Destination](/docs/specs/common-structures#type_Destination), seguida por la [Private Key](/docs/specs/common-structures#type_PrivateKey), seguida por la [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), opcionalmente seguida por la [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), lo que resulta en 884 o más caracteres en base 64 (663 o más bytes en binario), dependiendo del tipo de firma. El formato binario se especifica en Private Key File.

Las firmas fuera de línea son compatibles con los datagramas RAW, DATAGRAM2 y DATAGRAM3, pero no con DATAGRAM. Consulte la sección SESSION CREATE anterior y la sección DATAGRAM2/3 a continuación para obtener más detalles.

$host es el nombre de host o la dirección IP del servidor de datagramas al que SAM reenviará los datagramas. Si no se proporciona, SAM toma la dirección IP del socket que emitió el comando de reenvío.

$port es el número de puerto del servidor de datagramas al que SAM reenviará los datagramas. Si $port no está establecido, los datagramas NO serán reenviados; en su lugar, serán recibidos en el socket de control, de la manera compatible con v1/v2.

Las opciones adicionales proporcionadas se pasan a la configuración de la sesión I2P si no son interpretadas por el puente SAM (por ejemplo, outbound.length=0). Estas opciones [se documentan a continuación](#tunnel-i2cp-and-streaming-options).

Los datagramas reenviados con respuesta habilitada siempre tienen como prefijo el destino en base64, excepto para Datagram3, ver más abajo. Cuando llega un datagrama con respuesta habilitada, el puente envía al host:puerto especificado un paquete UDP que contiene los siguientes datos:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Los datagramas sin procesar reenviados se transmiten tal como están al host:puerto especificado sin prefijo. El paquete UDP contiene los siguientes datos:

```
$datagram_payload
```
A partir de SAM 3.2, cuando se especifica HEADER=true en SESSION CREATE, al datagrama en bruto reenviado se le antepone una línea de encabezado de la siguiente manera:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
El $destination es la representación en base 64 de la [Destination](/docs/specs/common-structures#type_Destination), que consta de 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

#### Datagramas anónimos SAM (sin formato)

Al maximizar el ancho de banda de I2P, SAM permite a los clientes enviar y recibir datagramas anónimos, dejando la autenticación y la información de respuesta en manos del propio cliente. Estos datagramas son inseguros y no ordenados, y pueden tener hasta 32768 bytes.

El tamaño mínimo es 1. Para una confiabilidad óptima en la entrega, el tamaño máximo recomendado es aproximadamente 11 KB.

Después de establecer una sesión SAM con STYLE=RAW, el cliente puede enviar datagramas anónimos a través del puente SAM exactamente de la misma manera que [enviar datagramas con respuesta o sin formato](#sending-repliable-or-raw-datagrams).

Ambas formas de recibir datagramas también están disponibles para datagramas anónimos.

Los datagramas recibidos son escritos por SAM en el socket desde el cual se abrió la sesión de datagrama, si no se especifica un PUERTO de reenvío en el comando SESSION CREATE. Esta es la forma compatible con v1/v2 de recibir datagramas.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Cuando se deben reenviar datagramas anónimos a algún host:puerto, el puente envía al host:puerto especificado un mensaje que contiene los siguientes datos:

```
$datagram_payload
```
A partir de SAM 3.2, cuando se especifica HEADER=true en SESSION CREATE, al datagrama en bruto reenviado se le antepone una línea de encabezado de la siguiente manera:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Para un método alternativo de envío de datagramas anónimos, consulte [ENVÍO EN BRUTO](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagrama 2/3

Los datagramas 2/3 son formatos nuevos especificados a principios de 2025. Actualmente no existen implementaciones conocidas. Consulte la documentación de implementación para obtener el estado actual. Vea [la especificación](/docs/specs/datagrams) para más información.

No hay planes actuales para incrementar la versión de SAM para indicar soporte para Datagrama 2/3. Esto podría ser problemático ya que algunas implementaciones podrían desear soportar Datagrama 2/3 pero no las características de SAM v3.3. Cualquier cambio de versión queda por determinar (TBD).

Tanto Datagram2 como Datagram3 son respuestas posibles. Solo Datagram2 está autenticado.

Datagram2 es idéntico a los datagramas con respuesta desde la perspectiva de SAM. Ambos están autenticados. Solo el formato I2CP y la firma son diferentes, pero esto no es visible para los clientes SAM. Datagram2 también admite firmas fuera de línea, por lo que puede ser utilizado por destinos con firma fuera de línea.

La intención es que Datagram2 reemplace a los datagramas con respuesta (Repliable) en nuevas aplicaciones que no requieran compatibilidad hacia atrás. Datagram2 proporciona protección contra repeticiones (replay protection), la cual no está presente en los datagramas Repliable. Si se requiere compatibilidad hacia atrás, una aplicación puede admitir tanto Datagram2 como Repliable en la misma sesión, utilizando sesiones PRIMARY de SAM 3.3.

Datagram3 es repliable pero no autenticado. El campo 'from' en el formato I2CP es un hash, no un destino. El $destination enviado desde el servidor SAM al cliente será un hash base64 de 44 bytes. Para convertirlo en un destino completo para la respuesta, descodifíquelo de base64 a binario de 32 bytes, luego codifíquelo en base32 a 52 caracteres y añada ".b32.i2p" para una BÚSQUEDA DE NOMBRES. Como es habitual, los clientes deberían mantener su propia caché para evitar búsquedas de nombres repetidas.

Los diseñadores de aplicaciones deben tener extrema precaución y considerar las implicaciones de seguridad de los datagramas no autenticados.

#### Consideraciones sobre el MTU de datagramas V3

Los datagramas de I2P pueden ser más grandes que la MTU típica de Internet de 1500 bytes. Es probable que los datagramas enviados localmente y los datagramas reenviados con respuesta, que llevan como prefijo el destino en base64 de 516+ bytes, excedan esa MTU. Sin embargo, las MTU de localhost en sistemas Linux suelen ser mucho más grandes, por ejemplo 65536. Las MTU de localhost variarán según el sistema operativo. Los datagramas de I2P nunca serán mayores de 65536. El tamaño del datagrama depende del protocolo de la aplicación.

Si el cliente SAM está en la misma ubicación que el servidor SAM y el sistema admite un MTU mayor, entonces los datagramas no se fragmentarán localmente. Sin embargo, si el cliente SAM está remoto, los datagramas IPv4 se fragmentarían y los datagramas IPv6 fallarían (IPv6 no admite la fragmentación UDP).

Los desarrolladores de bibliotecas y aplicaciones cliente deben ser conscientes de estos problemas y documentar recomendaciones para evitar la fragmentación y prevenir la pérdida de paquetes, especialmente en conexiones remotas cliente-servidor SAM.

#### ENVÍO DE DATAGRAMAS, ENVÍO EN BRUTO (GESTIÓN DE DATAGRAMAS COMPATIBLE CON V1/V2)

En SAM V3, la forma preferida de enviar datagramas es a través del socket de datagramas en el puerto 7655, como se documentó anteriormente. Sin embargo, los datagramas con respuesta pueden enviarse directamente a través del socket puente SAM utilizando el comando DATAGRAM SEND, como se documenta en [SAM V1](/docs/api/sam) y [SAM V2](/docs/api/samv2).

A partir de la versión 0.9.14 (versión 3.1), los datagramas anónimos pueden enviarse directamente a través del socket del puente SAM utilizando el comando RAW SEND, como se documenta en [SAM V1](/docs/api/sam) y [SAM V2](/docs/api/samv2).

A partir de la versión 0.9.24 (versión 3.2), DATAGRAM SEND y RAW SEND pueden incluir los parámetros FROM_PORT=nnnn y/o TO_PORT=nnnn para sobrescribir los puertos predeterminados. A partir de la versión 0.9.24 (versión 3.2), RAW SEND puede incluir el parámetro PROTOCOL=nnn para sobrescribir el protocolo predeterminado.

Estos comandos *no* admiten el parámetro ID. Los datagramas se envían a la sesión de estilo DATAGRAMA o RAW creada más recientemente, según corresponda. La compatibilidad con el parámetro ID podría agregarse en una versión futura.

Los formatos DATAGRAM2 y DATAGRAM3 *no* son compatibles de forma compatible con V1/V2.

### Sesiones PRINCIPALES de SAM (V3.3 y superiores)

*La versión 3.3 se introdujo en la versión de I2P 0.9.25.*

*En una versión anterior de esta especificación, las sesiones PRIMARY eran conocidas como sesiones MASTER. Tanto en `i2pd` como en `I2P+`, aún se conocen únicamente como sesiones MASTER.*

SAM v3.3 añade soporte para ejecutar subsesiones de streaming, datagramas y subsesiones raw sobre la misma sesión principal, y para ejecutar múltiples subsesiones del mismo tipo. Todo el tráfico de las subsesiones utiliza un único destino, o conjunto de túneles. El enrutamiento del tráfico hacia I2P se basa en las opciones de puerto y protocolo de las subsesiones.

Para crear subsesiones multiplexadas, debes crear una sesión principal y luego agregar subsesiones a la sesión principal. Cada subsesión debe tener un ID único y un protocolo y puerto de escucha únicos. Las subsesiones también pueden eliminarse de la sesión principal.

Con una sesión PRINCIPAL y una combinación de subsesiones, un cliente SAM puede admitir múltiples aplicaciones, o una única aplicación sofisticada que utilice diversos protocolos, sobre un único conjunto de túneles. Por ejemplo, un cliente bittorrent podría configurar una subsesión de streaming para conexiones entre pares (peer-to-peer), junto con subsesiones de datagramas y subsesiones raw para la comunicación DHT.

#### Creación de una sesión PRINCIPAL

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
El puente SAM responderá con éxito o fracaso como en [la respuesta a una creación de sesión estándar](#session-creation-response).

No establezca las opciones PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL ni HEADER en una sesión principal. No puede enviar ningún dato en un ID de sesión PRIMARY ni en el socket de control. Todos los comandos como STREAM CONNECT, DATAGRAM SEND, etc., deben usar el ID de subsesión en un socket separado.

La sesión PRINCIPAL se conecta al router y construye túneles. Cuando la puente SAM responde, los túneles ya han sido creados y la sesión está lista para que se le agreguen subsesiones. Todas las opciones [I2CP](/docs/protocol/i2cp) relacionadas con los parámetros de túnel, como longitud, cantidad y apodo, deben proporcionarse en la creación de la sesión principal (SESSION CREATE).

Todos los comandos de utilidad son compatibles en una sesión principal.

Cuando se cierra la sesión principal, todas las subsesiones también se cierran.

NOTA: Antes de la versión 0.9.47, use STYLE=MASTER. A partir de la versión 0.9.47, se admite STYLE=PRIMARY. MASTER sigue siendo compatible por motivos de retrocompatibilidad.

#### Creación de una Subsesión

Usando el mismo socket de control en el que se creó la sesión PRINCIPAL:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
El puente SAM responderá con éxito o fracaso como en [la respuesta a una creación estándar de SESIÓN](#session-creation-response). Dado que los túneles ya fueron construidos en la creación principal de SESIÓN, el puente SAM debería responder inmediatamente.

No establezca la opción DESTINATION en un SESSION ADD. La subsesión usará el destino especificado en la sesión principal. Todas las subsesiones deben agregarse en el socket de control, es decir, en la misma conexión en la que creó la sesión principal.

Las múltiples subsesiones deben tener opciones suficientemente únicas para que los datos entrantes puedan enrutar correctamente. En particular, múltiples sesiones del mismo estilo deben tener opciones LISTEN_PORT diferentes (y/o LISTEN_PROTOCOL, solo para RAW). Un SESSION ADD con puerto y protocolo de escucha que duplique una subsesión existente resultará en un error.

El LISTEN_PORT es el puerto I2P local, es decir, el puerto de recepción (TO) para datos entrantes. Si no se especifica el LISTEN_PORT, se utilizará el valor de FROM_PORT. Si no se especifican ni LISTEN_PORT ni FROM_PORT, el enrutamiento entrante se basará únicamente en STYLE y PROTOCOL. Para LISTEN_PORT y LISTEN_PROTOCOL, 0 significa cualquier valor, es decir, un comodín. Si tanto LISTEN_PORT como LISTEN_PROTOCOL son 0, esta subsesión será la predeterminada para el tráfico entrante que no sea enrutado a otra subsesión. El tráfico entrante de streaming (protocolo 6) nunca será enrutado a una subsesión RAW, incluso si su LISTEN_PROTOCOL es 0. Una subsesión RAW no puede establecer un LISTEN_PROTOCOL de 6. Si no existe una subsesión predeterminada o una que coincida con el protocolo y puerto del tráfico entrante, esos datos serán descartados.

Utilice el ID de subsesión, no el ID de sesión principal, para enviar y recibir datos. Todos los comandos como STREAM CONNECT, DATAGRAM SEND, etc., deben usar el ID de subsesión.

Todos los comandos de utilidad son compatibles en una sesión principal o en subsesiones. El envío/recepción de datagramas/raw v1/v2 no es compatible en una sesión principal ni en subsesiones.

#### Detener una Subsesión

Usando el mismo socket de control en el que se creó la sesión PRINCIPAL:

```
->  SESSION REMOVE
          ID=$nickname
```
Esto elimina una subsesión de la sesión principal. No establezca ninguna otra opción en un SESSION REMOVE. Las subsesiones deben eliminarse a través del socket de control, es decir, en la misma conexión en la que creó la sesión principal. Después de que se elimina una subsesión, esta se cierra y no puede utilizarse para enviar ni recibir datos.

El puente SAM responderá con éxito o fracaso como en [la respuesta a una creación de sesión estándar](#session-creation-response).

### Comandos de utilidad SAM

Algunos comandos de utilidad requieren una sesión preexistente y otros no. Consulte los detalles a continuación.

#### Búsqueda de nombre de host

El siguiente mensaje puede ser utilizado por el cliente para consultar al puente SAM sobre la resolución de nombres:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
que es respondido por

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
El valor de RESULTADO puede ser uno de:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Si NAME=ME, entonces la respuesta contendrá el destino utilizado por la sesión actual (útil si estás usando uno TRANSITORIO). Si $result no es OK, MESSAGE puede transmitir un mensaje descriptivo, como "formato incorrecto", etc. INVALID_KEY implica que hay algo mal con $name en la solicitud, posiblemente caracteres inválidos.

El $destination es la representación en base 64 de la [Destination](/docs/specs/common-structures#type_Destination), que consta de 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

NAMING LOOKUP no requiere que primero se haya creado una sesión. Sin embargo, en algunas implementaciones, una búsqueda .b32.i2p que no esté en caché y requiera una consulta de red puede fallar, ya que no hay túneles cliente disponibles para la búsqueda.

#### Opciones de búsqueda de nombres

NAMING LOOKUP se ha extendido a partir de la API del router 0.9.66 para admitir búsquedas de servicios. La compatibilidad puede variar según la implementación. Consulte la propuesta 167 para obtener información adicional.

NAMING LOOKUP NAME=example.i2p OPTIONS=true solicita la asignación de opciones en la respuesta. NAME puede ser un destino base64 completo cuando OPTIONS=true.

Si la búsqueda del destino fue exitosa y había opciones presentes en el leaseset, entonces en la respuesta, después del destino, habrá una o más opciones en la forma de OPTION:clave=valor. Cada opción tendrá un prefijo OPTION: separado. Se incluirán todas las opciones del leaseset, no solo las opciones de registro de servicio. Por ejemplo, podrían estar presentes opciones para parámetros definidos en el futuro. Ejemplo:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Las claves que contienen '=', y las claves o valores que contienen un salto de línea, se consideran inválidos y el par clave/valor será eliminado de la respuesta. Si no se encuentran opciones en el leaseset, o si el leaseset era de la versión 1, entonces la respuesta no incluirá ninguna opción. Si OPTIONS=true estaba en la búsqueda y el leaseset no se encuentra, se devolverá un nuevo valor de resultado LEASESET_NOT_FOUND.

#### Generación de clave de destino

Las claves base64 públicas y privadas se pueden generar utilizando el siguiente mensaje:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
que es respondido por

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
A partir de la versión 3.1 (I2P 0.9.14), se admite un parámetro opcional SIGNATURE_TYPE. El valor de SIGNATURE_TYPE puede ser cualquier nombre (por ejemplo, ECDSA_SHA256_P256, sin distinguir mayúsculas) o número (por ejemplo, 1) que sea compatible con [Certificados de Clave](/docs/specs/common-structures#type_Certificate). El valor predeterminado es DSA_SHA1, que NO es lo que desea. Para la mayoría de las aplicaciones, especifique SIGNATURE_TYPE=7.

El $destination es la representación en base 64 de la [Destination](/docs/specs/common-structures#type_Destination), que consta de 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

La $privkey es la representación en base 64 de la concatenación de la [Destination](/docs/specs/common-structures#type_Destination), seguida de la [Private Key](/docs/specs/common-structures#type_PrivateKey) y luego de la [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), lo que resulta en 884 o más caracteres en base 64 (663 o más bytes en binario), dependiendo del tipo de firma. El formato binario se especifica en Private Key File.

Notas sobre la clave privada binaria de 256 bytes [Private Key](/docs/specs/common-structures#type_PrivateKey): Este campo ha estado sin usar desde la versión 0.6 (2005). Las implementaciones de SAM pueden enviar datos aleatorios o todo ceros en este campo; no se alarme si ve una cadena de AAAA en la codificación base64. La mayoría de las aplicaciones simplemente almacenarán la cadena en base64 y la devolverán tal como está en el SESSION CREATE, o la decodificarán a binario para almacenarla, y luego la volverán a codificar para el SESSION CREATE. Sin embargo, las aplicaciones podrían decodificar el base64, analizar el binario según la especificación PrivateKeyFile, descartar la porción de 256 bytes de la clave privada, y luego reemplazarla con 256 bytes de datos aleatorios o todo ceros al volver a codificarla para el SESSION CREATE. DEBEN preservarse TODOS los demás campos en la especificación PrivateKeyFile. Esto ahorraría 256 bytes de almacenamiento en el sistema de archivos, pero probablemente no valga la pena el esfuerzo para la mayoría de las aplicaciones. Consulte la propuesta 161 para obtener información adicional y antecedentes.

DEST GENERATE no requiere que primero se haya creado una sesión.

DEST GENERATE no puede utilizarse para crear un destino con firmas fuera de línea.

#### PING/PONG (SAM 3.2 o superior)

Cualquiera de los dos, el cliente o el servidor, puede enviar:

```
PING[ arbitrary text]
```
en el puerto de control, con la respuesta:

```
PONG[ arbitrary text from the ping]
```
para usar en el mantenimiento activo del socket de control. Cualquier lado puede cerrar la sesión y el socket si no se recibe respuesta en un tiempo razonable, dependiendo de la implementación.

Si ocurre un tiempo de espera aguardando un PONG del cliente, el puente puede enviar:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
y luego desconéctese.

Si se produce un tiempo de espera aguardando un PONG desde el puente, el cliente puede simplemente desconectarse.

PING/PONG no requiere que primero se haya creado una sesión.

#### QUIT/STOP/EXIT (SAM 3.2 o superior, características opcionales)

Los comandos QUIT, STOP y EXIT cerrarán la sesión y el socket. La implementación es opcional, para facilitar las pruebas mediante telnet. Si se envía alguna respuesta antes de que el socket se cierre (por ejemplo, un mensaje SESSION STATUS) depende de la implementación y queda fuera del alcance de esta especificación.

QUIT/STOP/EXIT no requieren que primero se haya creado una sesión.

#### AYUDA (característica opcional)

Los servidores pueden implementar un comando HELP. La implementación es opcional, para facilitar las pruebas mediante telnet. El formato de salida y la detección del final de la salida dependen de la implementación y quedan fuera del alcance de esta especificación.

HELP no requiere que primero se haya creado una sesión.

#### Configuración de autorización (SAM 3.2 o superior, característica opcional)

Configuración de autorización utilizando el comando AUTH. Un servidor SAM puede implementar estos comandos para facilitar el almacenamiento persistente de credenciales. La configuración de autenticación diferente a través de estos comandos es específica de la implementación y queda fuera del alcance de esta especificación.

- AUTH ENABLE habilita la autorización en conexiones posteriores
- AUTH DISABLE deshabilita la autorización en conexiones posteriores
- AUTH ADD USER="foo" PASSWORD="bar" añade un usuario/contraseña
- AUTH REMOVE USER="foo" elimina a este usuario

Se recomiendan comillas dobles para el usuario y la contraseña, pero no son obligatorias. Una comilla doble dentro del usuario o la contraseña debe escaparse con una barra invertida. En caso de error, el servidor responderá con un I2P_ERROR y un mensaje.

AUTH no requiere que primero se haya creado una sesión.

### Valores RESULT

Estos son los valores que puede contener el campo RESULT, junto con su significado:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Diferentes implementaciones pueden no ser consistentes en cuál RESULTADO se devuelve en diversos escenarios.

La mayoría de las respuestas con un RESULTADO, distinto de OK, también incluirán un MENSAJE con información adicional. El MENSAJE generalmente será útil para depurar problemas. Sin embargo, las cadenas de MENSAJE dependen de la implementación, pueden o no ser traducidas por el servidor SAM al idioma actual, pueden contener información interna específica de la implementación como excepciones, y están sujetas a cambios sin previo aviso. Aunque los clientes SAM pueden optar por mostrar las cadenas de MENSAJE a los usuarios, no deberían tomar decisiones programáticas basadas en esas cadenas, ya que eso sería frágil.

### Opciones de túnel, I2CP y transmisión

Estas opciones pueden pasarse como pares nombre=valor en la línea SAM SESSION CREATE.

Todas las sesiones pueden incluir [opciones de I2CP como longitudes y cantidades de túneles](/docs/protocol/i2cp#options). Las sesiones STREAM pueden incluir [opciones de la biblioteca de transmisión](/docs/api/streaming#options).

Consulte esas referencias para los nombres de opciones y valores predeterminados. La documentación referenciada es para la implementación del router en Java. Los valores predeterminados pueden cambiar. Los nombres y valores de las opciones distinguen entre mayúsculas y minúsculas. Otras implementaciones de routers pueden no soportar todas las opciones y pueden tener valores predeterminados diferentes; consulte la documentación del router para más detalles.

### Notas sobre Base 64

La codificación Base 64 debe utilizar el alfabeto Base 64 estándar de I2P: "A-Z, a-z, 0-9, -, ~".

### Configuración predeterminada de SAM

El puerto SAM predeterminado es 7656. SAM no está habilitado por defecto en el router Java I2P; debe iniciarse manualmente o configurarse para iniciarse automáticamente, en la página de configuración de clientes en la consola del router, o en el archivo clients.config. El puerto UDP de SAM predeterminado es 7655, escuchando en 127.0.0.1. Estos valores pueden cambiarse en el router Java agregando los argumentos sam.udp.port=nnnnn y/o sam.udp.host=w.x.y.z a la invocación, o en la línea SESSION.

La configuración en otros routers depende de la implementación. Consulta [la guía de configuración de i2pd aquí](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
