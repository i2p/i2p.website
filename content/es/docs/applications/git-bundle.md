---
title: "Paquetes Git para I2P"
description: "Obtención y distribución de repositorios grandes con git bundle y BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Cuando las condiciones de red hacen que `git clone` no sea confiable, puedes distribuir repositorios como **bundles de git** a través de BitTorrent o cualquier otro transporte de archivos. Un bundle es un único archivo que contiene todo el historial del repositorio. Una vez descargado, obtienes los datos desde él localmente y luego vuelves a cambiar al remoto upstream.

## 1. Antes de Comenzar

Generar un bundle requiere un clon **completo** de Git. Los clones superficiales creados con `--depth 1` producirán silenciosamente bundles rotos que parecen funcionar pero fallan cuando otros intentan usarlos. Siempre obtenga el código de una fuente confiable (GitHub en [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), la instancia Gitea de I2P en [i2pgit.org](https://i2pgit.org), o `git.idk.i2p` sobre I2P) y ejecute `git fetch --unshallow` si es necesario para convertir cualquier clon superficial en un clon completo antes de crear bundles.

Si solo estás consumiendo un paquete existente, simplemente descárgalo. No se requiere ninguna preparación especial.

## 2. Descargando un Bundle

### Obtaining the Bundle File

Descarga el archivo bundle a través de BitTorrent usando I2PSnark (el cliente torrent integrado en I2P) u otros clientes compatibles con I2P como BiglyBT con el plugin de I2P.

**Importante**: I2PSnark solo funciona con torrents creados específicamente para la red I2P. Los torrents estándar de clearnet no son compatibles porque I2P utiliza Destinations (direcciones de 387+ bytes) en lugar de direcciones IP y puertos.

La ubicación del archivo bundle depende de tu tipo de instalación de I2P:

- **Instalaciones de usuario/manuales** (instaladas con el instalador Java): `~/.i2p/i2psnark/`
- **Instalaciones de sistema/daemon** (instaladas mediante apt-get o gestor de paquetes): `/var/lib/i2p/i2p-config/i2psnark/`

Los usuarios de BiglyBT encontrarán los archivos descargados en su directorio de descargas configurado.

### Cloning from the Bundle

**Método estándar** (funciona en la mayoría de los casos):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Si encuentras errores `fatal: multiple updates for ref` (un problema conocido en Git 2.21.0 y versiones posteriores cuando la configuración global de Git contiene refspecs de fetch conflictivos), usa el enfoque de inicialización manual:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Alternativamente, puedes usar la bandera `--update-head-ok`:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Obtención del Archivo Bundle

Después de clonar desde el bundle, apunta tu clon al remoto activo para que las futuras descargas se realicen a través de I2P o clearnet:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
O para acceso a clearnet:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
Para acceso SSH a I2P, necesitas un túnel cliente SSH configurado en la consola de tu router I2P (típicamente puerto 7670) apuntando a `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. Si usas un puerto no estándar:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Clonación desde el Bundle

Asegúrate de que tu repositorio esté completamente actualizado con un **clon completo** (no superficial):

```bash
git fetch --all
```
Si tienes un clon superficial, conviértelo primero:

```bash
git fetch --unshallow
```
### Cambio al Remoto en Vivo

**Usando el objetivo de compilación de Ant** (recomendado para el árbol de fuentes de I2P):

```bash
ant git-bundle
```
Esto crea tanto `i2p.i2p.bundle` (el archivo bundle) como `i2p.i2p.bundle.torrent` (metadatos de BitTorrent).

**Usando git bundle directamente**:

```bash
git bundle create i2p.i2p.bundle --all
```
Para paquetes más selectivos:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Siempre verifica el paquete antes de distribuirlo:

```bash
git bundle verify i2p.i2p.bundle
```
Esto confirma que el bundle es válido y muestra cualquier commit prerequisito requerido.

### Requisitos previos

Copia el paquete y sus metadatos del torrent en tu directorio de I2PSnark:

**Para instalaciones de usuario**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Para instalaciones del sistema**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark detecta y carga automáticamente archivos .torrent en cuestión de segundos. Accede a la interfaz web en [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) para comenzar a compartir.

## 4. Creating Incremental Bundles

Para actualizaciones periódicas, crea bundles incrementales que contengan únicamente los nuevos commits desde el último bundle:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Los usuarios pueden obtener desde el paquete incremental si ya tienen el repositorio base:

```bash
git fetch /path/to/update.bundle
```
Siempre verifica que los paquetes incrementales muestren los commits de requisitos previos esperados:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Una vez que tengas un repositorio funcional a partir del paquete, trátalo como cualquier otro clon de Git:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
O para flujos de trabajo más simples:

```bash
git fetch origin
git pull origin master
```
## 3. Crear un Bundle

- **Distribución resiliente**: Los repositorios grandes pueden compartirse a través de BitTorrent, que maneja reintentos, verificación de piezas y reanudación automáticamente.
- **Arranque peer-to-peer**: Los nuevos colaboradores pueden arrancar su clon desde peers cercanos en la red I2P, y luego obtener cambios incrementales directamente desde los hosts de Git.
- **Reducción de carga del servidor**: Los mirrors pueden publicar bundles periódicos para aliviar la presión sobre los hosts de Git en vivo, especialmente útil para repositorios grandes o condiciones de red lentas.
- **Transporte sin conexión**: Los bundles funcionan con cualquier transporte de archivos (unidades USB, transferencias directas, sneakernet), no solo BitTorrent.

Los bundles no reemplazan los remotos en vivo. Simplemente proporcionan un método de bootstrapping más resiliente para clones iniciales o actualizaciones importantes.

## 7. Troubleshooting

### Generando el Bundle

**Problema**: La creación del bundle tiene éxito pero otros no pueden clonar desde el bundle.

**Causa**: Tu clon de origen es superficial (creado con `--depth`).

**Solución**: Convertir a clon completo antes de crear bundles:

```bash
git fetch --unshallow
```
### Verificando tu Bundle

**Problema**: `fatal: multiple updates for ref` al clonar desde bundle.

**Causa**: Git 2.21.0+ entra en conflicto con las refspecs de fetch globales en `~/.gitconfig`.

**Soluciones**: 1. Usar inicialización manual: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. Usar la bandera `--update-head-ok`: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Eliminar la configuración conflictiva: `git config --global --unset remote.origin.fetch`

### Distribución a través de I2PSnark

**Problema**: `git bundle verify` informa prerrequisitos faltantes.

**Causa**: Bundle incremental o clonación de origen incompleta.

**Solución**: Obtenga los commits prerequisito o use primero el bundle base, luego aplique las actualizaciones incrementales.
