---
title: "Hola Git, adiós Monotone"
date: 2020-12-10
author: "idk"
description: "Hola git, adiós mtn"
categories: ["Status"]
---

## Hola Git, Adiós Monotone

### The I2P Git Migration is nearly concluded

Durante más de una década, I2P ha dependido del venerable servicio Monotone para satisfacer sus necesidades de control de versiones, pero en los últimos años, la mayor parte del mundo ha pasado al ahora universal sistema de control de versiones Git. En ese mismo período, la red I2P se ha vuelto más rápida y fiable, y se han desarrollado soluciones alternativas accesibles para el problema de la non-resumability (imposibilidad de reanudar transferencias) de Git.

Hoy es una ocasión significativa para I2P, ya que hemos desactivado la antigua rama mtn i2p.i2p y hemos trasladado oficialmente el desarrollo de las bibliotecas centrales de Java I2P de Monotone a Git.

Aunque en el pasado se ha cuestionado nuestro uso de mtn, y no siempre ha sido una elección popular, me gustaría aprovechar este momento, como quizá el último proyecto en usar Monotone, para agradecer a los desarrolladores de Monotone, presentes y pasados, dondequiera que estén, por el software que crearon.

## GPG Signing

Los Checkins (confirmaciones) a los repositorios del Proyecto I2P requieren que configures la firma con GPG para tus commits de git, incluyendo las Merge Requests (solicitudes de fusión) y las Pull Requests (solicitudes de extracción). Configura tu cliente de git para la firma con GPG antes de hacer un fork (bifurcación) de i2p.i2p y realizar cualquier check-in.

## Firma con GPG

El repositorio oficial es el que está alojado en https://i2pgit.org/i2p-hackers/i2p.i2p y en https://git.idk.i2p/i2p-hackers/i2p.i2p, pero hay un "espejo" disponible en Github en https://github.com/i2p/i2p.i2p.

Ahora que usamos Git, podemos sincronizar repositorios desde nuestra propia instancia autoalojada de Gitlab, con Github, y viceversa. Esto significa que es posible crear y enviar una Merge Request en Gitlab y, cuando se fusione, el resultado se sincronizará con Github, y una Pull Request en Github, cuando se fusione, aparecerá en Gitlab.

Esto significa que es posible enviarnos código a través de nuestra instancia de Gitlab o a través de Github, según lo que prefieras; sin embargo, son más los desarrolladores de I2P que monitorean regularmente Gitlab que los que monitorean Github. Los MR (Merge Requests, solicitudes de fusión) en Gitlab tienen más probabilidades de ser fusionados antes que los PR (Pull Requests, solicitudes de incorporación de cambios) en Github.

## Repositorios oficiales y sincronización con GitLab/GitHub

¡Felicitaciones y gracias a todos los que ayudaron con la migración a Git, especialmente a zzz, eche|on, nextloop y a los operadores de los espejos de nuestro sitio! Aunque algunos de nosotros echaremos de menos Monotone, se ha convertido en una barrera para los participantes nuevos y actuales en el desarrollo de I2P, y estamos entusiasmados de unirnos a la comunidad de desarrolladores que usan Git para gestionar sus proyectos distribuidos.
