---
title: "Помогите друзьям присоединиться к I2P, поделившись Reseed Bundles (наборы для начального подключения)."
date: 2020-06-07
author: "idk"
description: "Создавайте, обменивайтесь и используйте reseed bundles (пакеты для пересева)"
categories: ["reseed"]
---

Большинство новых I2P routers подключается к сети, выполняя начальную инициализацию с помощью службы reseed (первичной загрузки в сеть). Однако службы reseed централизованы и их сравнительно легко блокировать, учитывая, что в остальной части сети I2P делается упор на децентрализованные и неблокируемые подключения. Если новый I2P router не может выполнить начальную инициализацию, можно использовать уже работающий I2P router, чтобы создать рабочий "Reseed bundle" и выполнить начальную инициализацию без необходимости в службе reseed.

Пользователь с рабочим подключением к I2P может помочь заблокированному router присоединиться к сети, создав reseed-файл и передав его по секретному или незаблокированному каналу. На самом деле, во многих случаях уже подключенный I2P router вовсе не будет затронут блокировкой reseed, так что **наличие работающих I2P routers рядом означает, что существующие I2P routers могут помогать новым I2P routers, предоставляя им скрытый способ первичной инициализации (bootstrapping)**.

## Создание пакета Reseed

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Выполнение Reseed из файла

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
