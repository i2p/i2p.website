---
title: "Git через I2P для пользователей"
date: 2020-03-06
author: "idk"
description: "Git через I2P"
categories: ["development"]
---

Руководство по настройке доступа к git через I2P Tunnel. Этот tunnel будет служить вашей точкой доступа к одному git‑сервису в I2P. Это часть общей работы по переходу I2P с monotone на Git.

## Прежде всего: разберитесь в возможностях сервиса, доступных широкой публике

В зависимости от того, как настроен сервис Git, он может предоставлять все сервисы по одному и тому же адресу или нет. В случае git.idk.i2p есть публичный HTTP URL и SSH URL, который необходимо указать в вашем SSH‑клиенте Git. Любой из них можно использовать для операций push и pull, но рекомендуется SSH.

## Сначала: Создайте учетную запись на Git‑сервисе

Чтобы создать свои репозитории на удалённом git-сервисе, зарегистрируйте учётную запись пользователя на этом сервисе. Разумеется, можно также создавать репозитории локально и отправлять их на удалённый git-сервис, но большинство потребуют наличия учётной записи и чтобы вы создали репозиторий на сервере.

## Во-вторых: Создайте проект для тестирования

Чтобы убедиться, что процесс настройки работает, полезно создать на сервере тестовый репозиторий. Перейдите к репозиторию i2p-hackers/i2p.i2p и создайте его форк в своем аккаунте.

## Третье: Настройте tunnel вашего git-клиента

Чтобы иметь доступ на чтение и запись к серверу, вам нужно настроить tunnel (туннель) для вашего SSH-клиента. Если вам нужно только клонирование по HTTP/S в режиме только для чтения, то вы можете всё это пропустить и просто использовать переменную окружения http_proxy, чтобы настроить git на использование преднастроенного I2P HTTP Proxy. Например:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Для доступа по SSH запустите "New Tunnel Wizard" по адресу http://127.0.0.1:7657/i2ptunnelmgr и настройте клиентский tunnel, указывающий на SSH base32-адрес Git-сервиса.

## В-четвертых: Попробуйте клонировать

Теперь ваш tunnel полностью настроен, вы можете попробовать клонировать по SSH:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Вы можете столкнуться с ошибкой, когда удалённая сторона неожиданно закрывает соединение. К сожалению, git до сих пор не поддерживает возобновляемое клонирование. Пока этого нет, есть несколько довольно простых способов справиться с этим. Первый и самый простой — попробовать выполнить клонирование с небольшой глубиной истории (shallow clone):

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
После того как вы выполнили поверхностное клонирование, вы можете получить остальное с возможностью возобновления, перейдя в каталог репозитория и выполнив:

```
git fetch --unshallow
```
На данном этапе у вас всё ещё нет всех веток. Вы можете получить их, выполнив:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Рекомендуемый рабочий процесс для разработчиков

Система контроля версий работает лучше всего при правильном использовании! Мы настоятельно рекомендуем рабочий процесс fork-first (сначала форк) и feature-branch (разработка в отдельных ветках для каждой функции):

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```