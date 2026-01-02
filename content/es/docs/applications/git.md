---
title: "Git sobre I2P"
description: "Conectar clientes Git a servicios alojados en I2P como i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Clonar y subir repositorios dentro de I2P utiliza los mismos comandos de Git que ya conoces—tu cliente simplemente se conecta a través de túneles I2P en lugar de TCP/IP. Esta guía explica cómo configurar una cuenta, configurar túneles y manejar conexiones lentas.

> **Inicio rápido:** El acceso de solo lectura funciona a través del proxy HTTP: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Sigue los pasos a continuación para acceso de lectura/escritura por SSH.

## 1. Crear una Cuenta

Elige un servicio Git de I2P y regístrate:

- Dentro de I2P: `http://git.idk.i2p`
- Espejo en Clearnet: `https://i2pgit.org`

El registro puede requerir aprobación manual; consulta la página de inicio para obtener instrucciones. Una vez aprobado, bifurca o crea un repositorio para tener algo con qué probar.

## 2. Configurar un cliente I2PTunnel (SSH)

1. Abre la consola del router → **I2PTunnel** y añade un nuevo túnel **Client**.
2. Introduce el destino del servicio (Base32 o Base64). Para `git.idk.i2p` encontrarás tanto destinos HTTP como SSH en la página principal del proyecto.
3. Elige un puerto local (por ejemplo `localhost:7442`).
4. Activa el inicio automático si planeas usar el túnel frecuentemente.

La interfaz confirmará el nuevo túnel y mostrará su estado. Cuando esté en ejecución, los clientes SSH pueden conectarse a `127.0.0.1` en el puerto elegido.

## 3. Clonar mediante SSH

Usa el puerto del túnel con `GIT_SSH_COMMAND` o una configuración SSH:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Si el primer intento falla (los túneles pueden ser lentos), intenta un clonado superficial:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Configura Git para obtener todas las ramas:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Consejos de Rendimiento

- Agrega uno o dos túneles de respaldo en el editor de túneles para mejorar la resiliencia.
- Para pruebas o repositorios de bajo riesgo, puedes reducir la longitud del túnel a 1 hop, pero ten en cuenta el compromiso con el anonimato.
- Mantén `GIT_SSH_COMMAND` en tu entorno o añade una entrada a `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Luego clona usando `git clone git@git.i2p:namespace/project.git`.

## 4. Sugerencias de Flujo de Trabajo

Adopta un flujo de trabajo de fork-and-branch común en GitLab/GitHub:

1. Configura un remoto upstream: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Mantén tu `master` sincronizado: `git pull upstream master`
3. Crea ramas de características para los cambios: `git checkout -b feature/new-thing`
4. Sube las ramas a tu fork: `git push origin feature/new-thing`
5. Envía una solicitud de fusión, luego actualiza el master de tu fork desde upstream mediante fast-forward.

## 5. Recordatorios de Privacidad

- Git almacena las marcas de tiempo de los commits en tu zona horaria local. Para forzar marcas de tiempo UTC:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Usa `git utccommit` en lugar de `git commit` cuando la privacidad es importante.

- Evite incluir URLs de clearnet o direcciones IP en mensajes de commit o metadatos del repositorio si el anonimato es una preocupación.

## 6. Solución de problemas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
Para escenarios avanzados (replicar repositorios externos, distribuir bundles), consulta las guías complementarias: [Flujos de trabajo con bundle de Git](/docs/applications/git-bundle/) y [Alojar GitLab sobre I2P](/docs/guides/gitlab/).
