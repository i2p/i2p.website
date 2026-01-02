---
title: "Git через I2P"
description: "Подключение Git-клиентов к сервисам, размещенным в I2P, таким как i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Клонирование и отправка репозиториев внутри I2P использует те же команды Git, которые вы уже знаете — ваш клиент просто подключается через I2P tunnel вместо TCP/IP. Это руководство описывает настройку учетной записи, конфигурирование tunnel и работу с медленными соединениями.

> **Быстрый старт:** Доступ только для чтения работает через HTTP-прокси: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Следуйте инструкциям ниже для SSH доступа с правами чтения и записи.

## 1. Создайте аккаунт

Выберите I2P Git-сервис и зарегистрируйтесь:

- Внутри I2P: `http://git.idk.i2p`
- Зеркало в открытой сети: `https://i2pgit.org`

Регистрация может требовать ручного одобрения; проверьте главную страницу для получения инструкций. После одобрения создайте форк или новый репозиторий, чтобы было с чем тестировать.

## 2. Настройка клиента I2PTunnel (SSH)

1. Откройте консоль роутера → **I2PTunnel** и добавьте новый туннель типа **Client**.
2. Введите адрес назначения сервиса (Base32 или Base64). Для `git.idk.i2p` вы найдёте адреса как для HTTP, так и для SSH на домашней странице проекта.
3. Выберите локальный порт (например, `localhost:7442`).
4. Включите автозапуск, если планируете часто использовать этот туннель.

Интерфейс подтвердит создание нового туннеля и отобразит его статус. Когда он будет запущен, SSH-клиенты смогут подключаться к `127.0.0.1` на выбранном порту.

## 3. Клонирование через SSH

Используйте порт туннеля с `GIT_SSH_COMMAND` или в секции конфигурации SSH:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Если первая попытка не удалась (туннели могут работать медленно), попробуйте поверхностное клонирование:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Настройте Git для получения всех веток:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Советы по производительности

- Добавьте один или два резервных tunnel в редакторе tunnel для повышения устойчивости.
- Для тестирования или репозиториев с низким риском вы можете уменьшить длину tunnel до 1 hop, но учитывайте компромисс с анонимностью.
- Сохраните `GIT_SSH_COMMAND` в вашем окружении или добавьте запись в `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Затем клонируйте с помощью `git clone git@git.i2p:namespace/project.git`.

## 4. Рекомендации по рабочему процессу

Используйте рабочий процесс с форками и ветками, распространённый на GitLab/GitHub:

1. Установите upstream remote: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Поддерживайте ваш `master` в синхронизации: `git pull upstream master`
3. Создавайте feature-ветки для изменений: `git checkout -b feature/new-thing`
4. Отправляйте ветки в ваш форк: `git push origin feature/new-thing`
5. Отправьте merge request, затем синхронизируйте master вашего форка с upstream методом fast-forward.

## 5. Напоминания о конфиденциальности

- Git сохраняет временные метки коммитов в вашем локальном часовом поясе. Чтобы принудительно использовать временные метки UTC:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Используйте `git utccommit` вместо `git commit`, когда важна конфиденциальность.

- Избегайте встраивания clearnet URL-адресов или IP-адресов в сообщения коммитов или метаданные репозитория, если анонимность важна.

## 6. Устранение неполадок

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
Для продвинутых сценариев (зеркалирование внешних репозиториев, распространение bundle-файлов) см. дополнительные руководства: [Работа с Git bundle](/docs/applications/git-bundle/) и [Хостинг GitLab через I2P](/docs/guides/gitlab/).
