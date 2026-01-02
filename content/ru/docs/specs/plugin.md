---
title: "Формат пакета плагина"
description: "Правила упаковки .xpi2p / .su3 для плагинов I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Обзор

Плагины I2P — это подписанные архивы, которые расширяют функциональность router. Они поставляются в виде файлов `.xpi2p` или `.su3`, устанавливаются в `~/.i2p/plugins/<name>/` (или `%APPDIR%\I2P\plugins\<name>\` в Windows) и выполняются с полными правами доступа router без sandboxing (изоляции в песочнице).

### Поддерживаемые типы плагинов

- Веб‑приложения консоли
- Новые eepsites с cgi-bin, веб‑приложениями
- Темы консоли
- Переводы консоли
- Программы на Java (внутри процесса или в отдельной JVM)
- Скрипты оболочки и нативные бинарные файлы

### Модель безопасности

**КРИТИЧНО:** Плагины выполняются в той же JVM с теми же правами, что и I2P router. Они имеют неограниченный доступ к: - Файловой системе (чтение и запись) - API router и его внутреннему состоянию - Сетевым подключениям - Выполнению внешних программ

Плагины следует рассматривать как полностью доверенный код. Пользователи должны проверять источники и подписи плагинов перед установкой.

---

## Форматы файлов

### Формат SU3 (настоятельно рекомендуется)

**Статус:** Активный, предпочтительный формат начиная с I2P 0.9.15 (сентябрь 2014)

Формат `.su3` предоставляет: - **Ключи подписи RSA-4096** (по сравнению с DSA-1024 в xpi2p) - Подпись хранится в заголовке файла - Магическое число: `I2Psu3` - Лучшая совместимость с будущими версиями

**Структура:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### Формат XPI2P (устаревший, не рекомендуется к использованию)

**Статус:** Поддерживается для обратной совместимости, не рекомендуется для новых плагинов

Формат `.xpi2p` использует устаревшие криптографические подписи: - **Подписи DSA-1024** (устарели согласно NIST-800-57) - 40-байтовая подпись DSA, добавляемая перед ZIP - Требуется поле `key` в plugin.config

**Структура:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Путь миграции:** При миграции с xpi2p на su3 указывайте оба `updateURL` и `updateURL.su3` во время перехода. Современные routers (0.9.15+) автоматически отдают приоритет SU3.

---

## Структура архива и plugin.config

### Необходимые файлы

**plugin.config** - Стандартный файл конфигурации I2P с парами ключ-значение

### Обязательные параметры

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Примеры форматов версий:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Допустимые разделители: `.` (точка), `-` (дефис), `_` (нижнее подчеркивание)

### Необязательные свойства метаданных

#### Отображение информации

- `date` - Дата релиза (метка времени в формате Java long)
- `author` - Имя разработчика (`user@mail.i2p` рекомендуется)
- `description` - Описание на английском
- `description_xx` - Локализованное описание (xx = код языка)
- `websiteURL` - Домашняя страница плагина (`http://foo.i2p/`)
- `license` - Идентификатор лицензии (например, "Apache-2.0", "GPL-3.0")

#### Настройка обновлений

- `updateURL` - адрес обновления XPI2P (устаревший)
- `updateURL.su3` - адрес обновления SU3 (предпочтительный)
- `min-i2p-version` - минимально необходимая версия I2P
- `max-i2p-version` - максимальная совместимая версия I2P
- `min-java-version` - минимальная версия Java (например, `1.7`, `17`)
- `min-jetty-version` - минимальная версия Jetty (используйте `6` для Jetty 6+)
- `max-jetty-version` - максимальная версия Jetty (используйте `5.99999` для Jetty 5)

#### Поведение установки

- `dont-start-at-install` - По умолчанию `false`. Если `true`, требуется ручной запуск
- `router-restart-required` - По умолчанию `false`. Сообщает пользователю, что после обновления требуется перезапуск
- `update-only` - По умолчанию `false`. Завершается с ошибкой, если плагин ещё не установлен
- `install-only` - По умолчанию `false`. Завершается с ошибкой, если плагин уже установлен
- `min-installed-version` - Минимальная версия, необходимая для обновления
- `max-installed-version` - Максимальная версия, которую можно обновить
- `disableStop` - По умолчанию `false`. Если `true`, скрывает кнопку остановки

#### Интеграция с консолью

- `consoleLinkName` - Текст для ссылки в сводной панели консоли
- `consoleLinkName_xx` - Локализованный текст ссылки (xx = код языка)
- `consoleLinkURL` - Адрес назначения ссылки (например, `/appname/index.jsp`)
- `consoleLinkTooltip` - Текст всплывающей подсказки (поддерживается с 0.7.12-6)
- `consoleLinkTooltip_xx` - Локализованная всплывающая подсказка
- `console-icon` - Путь к значку 32x32 (поддерживается с 0.9.20)
- `icon-code` - Base64-кодированный PNG 32x32 для плагинов без веб-ресурсов (с 0.9.25)

#### Требования к платформе (только для отображения)

- `required-platform-OS` - Требование к операционной системе (не проверяется)
- `other-requirements` - Дополнительные требования (например, "Python 3.8+")

#### Управление зависимостями (не реализовано)

- `depends` - Зависимости плагина, перечисленные через запятую
- `depends-version` - Требования к версиям для зависимостей
- `langs` - Содержимое языкового пакета
- `type` - Тип плагина (app/theme/locale/webapp)

### Обновление подстановки переменных в URL

**Статус функции:** Доступно начиная с I2P 1.7.0 (0.9.53)

И `updateURL`, и `updateURL.su3` поддерживают переменные, зависящие от платформы:

**Переменные:** - `$OS` - Операционная система: `windows`, `linux`, `mac` - `$ARCH` - Архитектура: `386`, `amd64`, `arm64`

**Пример:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Результат на Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Это позволяет использовать единый файл plugin.config для платформозависимых сборок.

---

## Структура каталогов

### Стандартная компоновка

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Назначение каталогов

**console/locale/** - файлы JAR с пакетами ресурсов для базовых переводов I2P - переводы, специфичные для плагинов, должны быть в `console/webapps/*.war` или `lib/*.jar`

**console/themes/** - Каждый подкаталог содержит полноценную тему консоли - Автоматически добавляется в путь поиска тем

**console/webapps/** - файлы `.war` для интеграции с консолью - Запускаются автоматически, если не отключены в `webapps.config` - Имя WAR не обязательно должно совпадать с именем плагина

**eepsite/** - Полноценный eepsite с собственным экземпляром Jetty - Требует конфигурации `jetty.xml` с подстановкой переменных - См. примеры zzzot и плагина pebble

**lib/** - JAR-библиотеки плагина - Укажите в classpath через `clients.config` или `webapps.config`

---

## Настройка веб-приложений

### Формат webapps.config

Стандартный файл конфигурации I2P, управляющий поведением веб‑приложения.

**Синтаксис:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Важные примечания:** - До router 0.7.12-9, используйте `plugin.warname.startOnLoad` для совместимости - До API 0.9.53, classpath (путь к классам) работал только если warname совпадал с именем плагина - Начиная с 0.9.53+, classpath работает для любого имени веб‑приложения

### Лучшие практики для веб-приложений

1. **Реализация ServletContextListener**
   - Реализуйте `javax.servlet.ServletContextListener` для очистки
   - Или переопределите `destroy()` в сервлете
   - Обеспечивает корректное завершение работы при обновлениях и остановке router

2. **Управление библиотеками**
   - Размещайте общие JAR-файлы в `lib/`, а не внутри WAR (архива веб-приложения Java)
   - Подключайте через classpath в `webapps.config`
   - Позволяет отдельно устанавливать и обновлять плагины

3. **Избегайте конфликтующих библиотек**
   - Никогда не включайте в пакет JAR‑файлы Jetty, Tomcat или сервлетов
   - Никогда не включайте JAR‑файлы из стандартной установки I2P
   - Проверьте раздел classpath на наличие стандартных библиотек

4. **Требования к компиляции**
   - Не включайте исходные файлы `.java` или `.jsp`
   - Предварительно скомпилируйте все JSP, чтобы избежать задержек при запуске
   - Нельзя предполагать наличие компилятора Java/JSP

5. **Совместимость с Servlet API**
   - I2P поддерживает Servlet 3.0 (начиная с 0.9.30)
   - **Сканирование аннотаций НЕ поддерживается** (@WebContent)
   - Необходимо предоставить традиционный дескриптор развертывания `web.xml`

6. **Версия Jetty**
   - Текущая: Jetty 9 (I2P 0.9.30+)
   - Используйте `net.i2p.jetty.JettyStart` для абстракции
   - Защищает от изменений в API Jetty

---

## Настройка клиента

### Формат clients.config

Определяет клиентов (служб), запускаемых вместе с плагином.

**Базовый клиент:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Клиент с возможностью остановки/удаления:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Справочник по свойствам

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Подстановка переменных

Следующие переменные подставляются в `args`, `stopargs`, `uninstallargs` и `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Управляемые и неуправляемые клиенты

**Управляемые клиенты (рекомендуется с версии 0.9.4):** - Создаются ClientAppManager - Обеспечивают отслеживание ссылок и состояния - Упрощают управление жизненным циклом - Улучшают управление памятью

**Неуправляемые клиенты:** - Запускаются router; отслеживание состояния не ведётся - Должны корректно обрабатывать многократные вызовы запуска/остановки - Для координации используют статическое состояние или PID-файлы - Вызываются при завершении работы router (начиная с 0.7.12-3)

### ShellService (начиная с 0.9.53 / 1.7.0)

Универсальное решение для запуска внешних программ с автоматическим отслеживанием состояния.

**Особенности:** - Управляет жизненным циклом процесса - Взаимодействует с ClientAppManager - Автоматическое управление PID - Кроссплатформенная поддержка

**Использование:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Для платформозависимых скриптов:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Альтернатива (устаревшее):** Напишите обёртку на Java, проверяющую тип ОС, и вызовите `ShellCommand` с соответствующим файлом `.bat` или `.sh`.

---

## Процесс установки

### Пользовательский процесс установки

1. Пользователь вставляет URL плагина на страницу конфигурации плагинов консоли router (`/configplugins`)
2. router загружает файл плагина
3. Проверка подписи (не проходит, если ключ неизвестен и включен строгий режим)
4. Проверка целостности ZIP
5. Извлечение и разбор `plugin.config`
6. Проверка совместимости версий (`min-i2p-version`, `min-java-version` и т. д.)
7. Обнаружение конфликта названий веб-приложений
8. Остановка существующего плагина при обновлении
9. Проверка каталога (должен находиться в `plugins/`)
10. Извлечение всех файлов в каталог плагина
11. Обновление `plugins.config`
12. Запуск плагина (если не задано `dont-start-at-install=true`)

### Безопасность и доверие

**Управление ключами:** - Модель доверия «first-key-seen» (доверие при первом использовании) для новых подписантов - Только ключи jrandom и zzz включены в поставку - Начиная с 0.9.14.1, неизвестные ключи по умолчанию отклоняются - Можно переопределить с помощью расширенного параметра для разработки

**Ограничения установки:** - Архивы должны распаковываться только в каталог плагина - Установщик отказывается принимать пути вне `plugins/` - После установки плагины могут получать доступ к файлам в других местах - Нет песочницы или изоляции привилегий

---

## Механизм обновления

### Процесс проверки обновлений

1. Router читает `updateURL.su3` (предпочтительно) или `updateURL` из plugin.config
2. HTTP HEAD или частичный запрос GET, чтобы получить байты 41-56
3. Извлечь строку версии из удаленного файла
4. Сравнить с установленной версией с помощью VersionComparator
5. Если новее, запросить у пользователя подтверждение или выполнить автоматическую загрузку (в зависимости от настроек)
6. Остановить плагин
7. Установить обновление
8. Запустить плагин (если пользовательская настройка не была изменена)

### Сравнение версий

Версии интерпретируются как компоненты, разделённые точками/дефисами/подчёркиваниями: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Максимальная длина:** 16 байт (должна совпадать с заголовком SUD/SU3)

### Лучшие практики обновления

1. Всегда увеличивайте версию для релизов
2. Протестируйте путь обновления из предыдущей версии
3. Рассмотрите использование `router-restart-required` для крупных изменений
4. Во время миграции указывайте и `updateURL`, и `updateURL.su3`
5. Используйте суффикс номера сборки для тестирования (`1.2.3-456`)

---

## Classpath и стандартные библиотеки

### Всегда доступно в Classpath

Следующие JAR-файлы из `$I2P/lib` всегда включены в classpath (путь к классам) для I2P 0.9.30+:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Особые примечания

**commons-logging.jar:** - Пустой начиная с 0.9.30 - До 0.9.30: Apache Tomcat JULI - До 0.9.24: Commons Logging + JULI - До 0.9: Только Commons Logging

**jasper-compiler.jar:** - Пустой начиная с Jetty 6 (0.9)

**systray4j.jar:** - Удалён в 0.9.26

### Отсутствует в classpath (необходимо указать)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Спецификация пути классов

**В clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**В файле webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Важно:** Начиная с версии 0.7.13-3, значения classpath (путь к классам) привязаны к потокам, а не глобальны для JVM. Указывайте полный classpath для каждого клиента.

---

## Требования к версии Java

### Текущие требования (октябрь 2025 года)

**I2P 2.10.0 и более ранние версии:** - Минимум: Java 7 (требуется с 0.9.24, январь 2016) - Рекомендуется: Java 8 или выше

**I2P 2.11.0 и новее (СКОРО):** - **Минимум: Java 17+** (объявлено в примечаниях к выпуску 2.9.0) - Предупреждение за два релиза дано (2.9.0 → 2.10.0 → 2.11.0)

### Стратегия совместимости плагинов

**Для максимальной совместимости (вплоть до I2P 2.10.x включительно):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Для возможностей Java 8+:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Для возможностей Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Подготовка к версии 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Лучшие практики компиляции

**При компиляции с более новой JDK под более старую целевую версию:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Это предотвращает использование API, недоступных в целевой версии Java.

---

## Сжатие Pack200 - УСТАРЕЛО

### Критическое обновление: не используйте Pack200

**Статус:** УСТАРЕЛО И УДАЛЕНО

В исходной спецификации настоятельно рекомендовалось сжатие Pack200 для уменьшения размера на 60–65%. **Это больше не применимо.**

**Хронология:** - **JEP 336:** Pack200 объявлён устаревшим в Java 11 (сентябрь 2018) - **JEP 367:** Pack200 удалён в Java 14 (март 2020)

**Официальная спецификация обновлений I2P гласит:** > "Файлы JAR и WAR в ZIP-архиве больше не сжимаются с помощью pack200, как описано выше для файлов 'su2', поскольку современные среды выполнения Java больше не поддерживают его."

**Что делать:**

1. **Немедленно удалите pack200 (формат сжатия JAR) из процессов сборки**
2. **Используйте стандартное сжатие ZIP**
3. **Рассмотрите альтернативы:**
   - ProGuard/R8 для уменьшения размера кода
   - UPX для нативных исполняемых файлов
   - Современные алгоритмы сжатия (zstd, brotli) при наличии собственного распаковщика

**Для существующих плагинов:** - Старые routers (0.7.11-5 до Java 10 включительно) по-прежнему могут распаковывать pack200 - Новые routers (Java 11+) не могут распаковывать pack200 - Переиздайте плагины без сжатия pack200

---

## Ключи подписи и безопасность

### Генерация ключей (формат SU3)

Используйте скрипт `makeplugin.sh` из репозитория i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Ключевые параметры:** - Алгоритм: RSA_SHA512_4096 - Формат: сертификат X.509 - Хранилище: формат Java keystore

### Подписание плагинов

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Лучшие практики управления ключами

1. **Сгенерируйте один раз — защищайте навсегда**
   - Routers отклоняют одинаковые имена ключей при разных ключах
   - Routers отклоняют одинаковые ключи с разными именами ключей
   - Обновления отклоняются при несоответствии ключа и имени

2. **Безопасное хранение**
   - Создавайте безопасные резервные копии хранилища ключей
   - Используйте надёжную парольную фразу
   - Никогда не добавляйте в систему контроля версий

3. **Ротация ключей**
   - Не поддерживается текущей архитектурой
   - Планируйте долгосрочное использование ключей
   - Рассмотрите схемы мультиподписи для командной разработки

### Устаревшее подписание DSA (XPI2P)

**Статус:** Работоспособно, но устарело

Подписи DSA-1024, используемые форматом xpi2p (формат пакета xpi2p): - подпись длиной 40 байт - открытый ключ длиной 172 символа base64 - NIST-800-57 рекомендует минимум (L=2048, N=224) - I2P использует более слабые (L=1024, N=160)

**Рекомендация:** Вместо этого используйте SU3 (формат подписанных обновлений I2P) с RSA-4096.

---

## Рекомендации по разработке плагинов

### Основные лучшие практики

1. **Документация**
   - Предоставьте понятный README с инструкциями по установке
   - Документируйте параметры конфигурации и значения по умолчанию
   - Добавляйте журнал изменений к каждому релизу
   - Укажите требуемые версии I2P/Java

2. **Оптимизация размера**
   - Включайте только необходимые файлы
   - Никогда не включайте в пакет router JARs
   - Разделяйте пакеты установки и обновления (библиотеки в lib/)
   - ~~Используйте сжатие Pack200~~ **УСТАРЕЛО - используйте стандартный ZIP**

3. **Конфигурация**
   - Никогда не изменяйте `plugin.config` во время выполнения
   - Используйте отдельный файл конфигурации для настроек времени выполнения
   - Задокументируйте требуемые настройки router (порты SAM, tunnels и т. д.)
   - Уважайте существующую конфигурацию пользователя

4. **Использование ресурсов**
   - Избегайте агрессивного использования пропускной способности по умолчанию
   - Внедрите разумные ограничения на использование процессора
   - Очищайте ресурсы при завершении работы
   - Используйте демон-потоки там, где это уместно

5. **Тестирование**
   - Протестировать установку/обновление/удаление на всех платформах
   - Протестировать обновления с предыдущей версии
   - Проверить остановку/перезапуск веб‑приложения во время обновлений
   - Протестировать с минимально поддерживаемой версией I2P

6. **Файловая система**
   - Никогда не записывайте в `$I2P` (может быть доступен только для чтения)
   - Записывайте данные времени выполнения в `$PLUGIN` или `$CONFIG`
   - Используйте `I2PAppContext` для определения расположения каталогов
   - Не предполагайте расположение `$CWD`

7. **Совместимость**
   - Не дублируйте стандартные классы I2P
   - Расширяйте классы при необходимости, не заменяйте
   - Проверьте `min-i2p-version`, `min-jetty-version` в plugin.config
   - Тестируйте со старыми версиями I2P, если вы их поддерживаете

8. **Обработка завершения работы**
   - Настройте корректные `stopargs` в clients.config
   - Зарегистрируйте хуки завершения (shutdown hooks): `I2PAppContext.addShutdownTask()`
   - Корректно обрабатывайте многократные вызовы запуска/остановки
   - Установите всем потокам режим демона

9. **Безопасность**
   - Проверяйте весь внешний ввод
   - Никогда не вызывайте `System.exit()`
   - Уважайте конфиденциальность пользователей
   - Соблюдайте безопасные практики программирования

10. **Лицензирование**
    - Чётко укажите лицензию плагина
    - Соблюдайте лицензии включённых библиотек
    - Включите обязательные упоминания авторства
    - Предоставьте доступ к исходному коду, если это требуется

### Расширенные соображения

**Обработка часовых поясов:** - Router устанавливает часовой пояс JVM на UTC - Фактический часовой пояс пользователя: `I2PAppContext` свойство `i2p.systemTimeZone`

**Обнаружение каталога:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Нумерация версий:** - Используйте семантическое версионирование (major.minor.patch) - Добавьте номер сборки для тестирования (1.2.3-456) - Обеспечьте монотонное возрастание версий при обновлениях

**Доступ к классам Router:** - Как правило, избегайте зависимостей от `router.jar` - Вместо этого используйте публичные API в `i2p.jar` - В будущих версиях I2P доступ к классам Router может быть ограничён

**Предотвращение сбоев JVM (историческое):** - Исправлено в 0.7.13-3 - Корректно используйте загрузчики классов - Избегайте обновления JAR-файлов в запущенном плагине - При необходимости проектируйте с поддержкой перезапуска при обновлении

---

## Плагины eepsite

### Обзор

Плагины могут предоставлять полноценные eepsites с собственными экземплярами Jetty и I2PTunnel.

### Архитектура

**Не пытайтесь:** - Устанавливать в существующий eepsite - Объединять с eepsite по умолчанию для router - Предполагать доступность только одного eepsite

**Вместо этого:** - Запустите новый экземпляр I2PTunnel (через CLI, интерфейс командной строки) - Запустите новый экземпляр Jetty - Настройте оба в `clients.config`

### Пример структуры

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Подстановка переменных в jetty.xml

Используйте переменную `$PLUGIN` для путей:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router выполняет подстановку при запуске плагина.

### Примеры

Эталонные реализации: - **zzzot плагин** - Торрент-трекер - **pebble плагин** - Платформа для блогов

Оба доступны на странице плагинов zzz (внутри I2P).

---

## Интеграция с консолью

### Ссылки сводной панели

Добавить кликабельную ссылку в панель сводки консоли router:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Локализованные версии:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Значки консоли

**Файл образа (начиная с 0.9.20):**

```properties
console-icon=/myicon.png
```
Путь относительно `consoleLinkURL`, если указан (начиная с 0.9.53), иначе — относительно имени веб-приложения.

**Встроенный значок (начиная с версии 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Сгенерировать с помощью:

```bash
base64 -w 0 icon-32x32.png
```
Или Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Требования: - 32x32 пикселей - формат PNG - в кодировке Base64 (без переносов строк)

---

## Интернационализация

### Пакеты переводов

**Для базовых переводов I2P:** - Поместите JAR-файлы в `console/locale/` - Содержат ресурсные пакеты для существующих приложений I2P - Именование: `messages_xx.properties` (xx = код языка)

**Для переводов, специфичных для плагина:** - Поместите в `console/webapps/*.war` - Или поместите в `lib/*.jar` - Используйте стандартный подход Java ResourceBundle

### Локализованные строки в plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Поддерживаемые поля: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Перевод темы консоли

Темы в `console/themes/` автоматически добавляются в путь поиска тем.

---

## Плагины, специфичные для платформы

### Подход с отдельными пакетами

Используйте разные имена плагинов для каждой платформы:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Подход с подстановкой переменных

Единый plugin.config с переменными платформы:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
В clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Определение ОС во время выполнения

Подход в Java к условному выполнению:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Устранение неполадок

### Распространенные проблемы

**Плагин не запускается:** 1. Проверьте совместимость с версией I2P (`min-i2p-version`) 2. Проверьте версию Java (`min-java-version`) 3. Проверьте журналы router на ошибки 4. Убедитесь, что все необходимые JAR-файлы есть в classpath (путь классов)

**Веб‑приложение недоступно:** 1. Убедитесь, что `webapps.config` не отключает его 2. Проверьте совместимость версии Jetty (`min-jetty-version`) 3. Убедитесь, что `web.xml` присутствует (сканирование аннотаций не поддерживается) 4. Проверьте, нет ли конфликтующих имён веб‑приложений

**Сбой обновления:** 1. Убедитесь, что номер версии увеличен 2. Проверьте, что подпись соответствует ключу подписи 3. Убедитесь, что имя плагина соответствует установленной версии 4. Проверьте настройки `update-only`/`install-only`

**Внешняя программа не останавливается:** 1. Используйте ShellService для автоматического управления жизненным циклом 2. Реализуйте корректную обработку `stopargs` 3. Проверьте очистку PID-файла 4. Убедитесь, что процесс завершён

### Отладочное логирование

Включите отладочное логирование в router:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Проверьте журналы:

```
~/.i2p/logs/log-router-0.txt
```
---

## Справочная информация

### Официальные спецификации

- [Спецификация плагинов](/docs/specs/plugin/)
- [Формат конфигурации](/docs/specs/configuration/)
- [Спецификация обновлений](/docs/specs/updates/)
- [Криптография](/docs/specs/cryptography/)

### История версий I2P

**Текущий релиз:** - **I2P 2.10.0** (8 сентября 2025 г.)

**Основные релизы с 0.9.53:** - 2.10.0 (сен 2025) - объявление о Java 17+ - 2.9.0 (июн 2025) - предупреждение о Java 17+ - 2.8.0 (окт 2024) - тестирование постквантовой криптографии - 2.6.0 (май 2024) - блокировка I2P поверх Tor - 2.4.0 (дек 2023) - улучшения безопасности NetDB - 2.2.0 (мар 2023) - контроль перегрузок - 2.1.0 (янв 2023) - улучшения сети - 2.0.0 (ноя 2022) - транспортный протокол SSU2 - 1.7.0/0.9.53 (фев 2022) - ShellService (служба оболочки), подстановка переменных - 0.9.15 (сен 2014) - представлен формат SU3

**Нумерация версий:** - серия 0.9.x: до версии 0.9.53 включительно - серия 2.x: начиная с 2.0.0 (введение SSU2)

### Ресурсы для разработчиков

**Исходный код:** - Основной репозиторий: https://i2pgit.org/I2P_Developers/i2p.i2p - Зеркало на GitHub: https://github.com/i2p/i2p.i2p

**Примеры плагинов:** - zzzot (трекер BitTorrent) - pebble (блог-платформа) - i2p-bote (бессерверная электронная почта) - orchid (клиент Tor) - seedless (обмен пирами)

**Инструменты сборки:** - makeplugin.sh - Генерация ключей и подписание - Находятся в репозитории i2p.scripts - Автоматизируют создание и проверку su3

### Поддержка сообщества

**Форумы:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (только внутри I2P)

**IRC/чат:** - #i2p-dev на OFTC - I2P IRC внутри сети

---

## Приложение A: Полный пример файла plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Приложение B: Полный пример clients.config

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Приложение C: Полный пример файла webapps.config

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Приложение D: Контрольный список миграции (с 0.9.53 до 2.10.0)

### Необходимые изменения

- [ ] **Удалить сжатие Pack200 из процесса сборки**
  - Удалить задачи pack200 из скриптов Ant/Maven/Gradle
  - Переиздать существующие плагины без pack200

- [ ] **Проверить требования к версиям Java**
  - Рассмотреть введение требования Java 11+ для новых возможностей
  - Запланировать введение требования Java 17+ в I2P 2.11.0
  - Обновить `min-java-version` в plugin.config

- [ ] **Обновить документацию**
  - Удалить упоминания Pack200
  - Обновить требования к версии Java
  - Обновить упоминания версий I2P (0.9.x → 2.x)

### Рекомендуемые изменения

- [ ] **Усилить криптографические подписи**
  - Перейти с XPI2P на SU3, если ещё не сделано
  - Использовать ключи RSA-4096 для новых плагинов

- [ ] **Используйте новые возможности (если используете 0.9.53+)**
  - Используйте переменные `$OS` / `$ARCH` для платформозависимых обновлений
  - Используйте ShellService (служба оболочки) для внешних программ
  - Используйте улучшенный classpath веб-приложения (работает с любым именем WAR-архива)

- [ ] **Проверить совместимость**
  - Протестировать на I2P 2.10.0
  - Проверить с Java 8, 11, 17
  - Проверить на Windows, Linux, macOS

### Необязательные улучшения

- [ ] Реализовать корректный ServletContextListener (слушатель контекста сервлета)
- [ ] Добавить локализованные описания
- [ ] Добавить значок консоли
- [ ] Улучшить обработку завершения работы
- [ ] Добавить расширенное логирование
- [ ] Написать автоматические тесты
