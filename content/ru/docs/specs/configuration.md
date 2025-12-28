---
title: "Настройка router"
description: "Параметры конфигурации и форматы для I2P router'ов и клиентов"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Обзор

В этом документе представлена исчерпывающая техническая спецификация файлов конфигурации I2P, используемых router и различными приложениями. Она охватывает спецификации форматов файлов, определения свойств и детали реализации, проверенные по исходному коду I2P и официальной документации.

### Область применения

- Файлы и форматы конфигурации Router
- Конфигурации клиентских приложений
- Конфигурации tunnel для I2PTunnel
- Спецификации форматов файлов и реализация
- Версионные особенности и устаревшие возможности

### Примечания по реализации

Файлы конфигурации читаются и записываются с использованием методов `DataHelper.loadProps()` и `storeProps()` в библиотеке ядра I2P. Формат файла существенно отличается от сериализованного формата, используемого в протоколах I2P (см. [Спецификация общих структур — Сопоставление типов](/docs/specs/common-structures/#type-mapping)).

---

## Общий формат конфигурационного файла

Файлы конфигурации I2P следуют модифицированному формату Java Properties с определёнными исключениями и ограничениями.

### Спецификация формата

Основано на [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) со следующими существенными отличиями:

#### Кодирование

- **ОБЯЗАТЕЛЬНО** использовать кодировку UTF-8 (НЕ ISO-8859-1, как в стандартных Java Properties)
- Реализация: использует утилиту `DataHelper.getUTF8()` для всех операций с файлами

#### Экранирующие последовательности

- Последовательности экранирования **НЕ** распознаются (включая обратную косую черту `\`)
- Продолжение строки **НЕ** поддерживается
- Символы обратной косой черты трактуются как литералы

#### Символы комментариев

- `#` начинает комментарий в любом месте строки
- `;` начинает комментарий **только** если находится в первом столбце
- `!` **НЕ** начинает комментарий (в отличие от Java Properties)

#### Разделители пар ключ–значение

- `=` — **ЕДИНСТВЕННЫЙ** допустимый разделитель пары «ключ–значение»
- `:` **НЕ** распознаётся как разделитель
- Пробельные символы **НЕ** распознаются как разделители

#### Обработка пробельных символов

- Начальные и конечные пробельные символы в ключах **НЕ** обрезаются
- Начальные и конечные пробельные символы в значениях **обрезаются**

#### Обработка строк

- Строки без `=` игнорируются (считаются комментариями или пустыми строками)
- Пустые значения (`key=`) поддерживаются начиная с версии 0.9.10
- Ключи с пустыми значениями сохраняются и извлекаются как обычно

#### Ограничения на символы

**Ключи НЕ могут содержать**: - `#` (знак решётки) - `=` (знак равенства) - `\n` (символ новой строки) - Не могут начинаться с `;` (точка с запятой)

**Значения НЕ могут содержать**: - `#` (знак решётки) - `\n` (символ перевода строки) - Не могут начинаться или заканчиваться на `\r` (возврат каретки) - Не могут начинаться или заканчиваться пробельными символами (удаляются автоматически)

### Сортировка файлов

Конфигурационные файлы не обязательно сортировать по ключам. Однако большинство приложений I2P при записи конфигурационных файлов сортируют ключи в алфавитном порядке, чтобы упростить: - Ручное редактирование - Операции diff в системах контроля версий - Читаемость для людей

### Подробности реализации

#### Чтение конфигурационных файлов

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Поведение**: - Читает файлы в кодировке UTF-8 - Обеспечивает соблюдение всех правил формата, описанных выше - Проверяет соблюдение ограничений на символы - Возвращает пустой объект Properties, если файл не существует - Выбрасывает `IOException` при ошибках чтения

#### Создание файлов конфигурации

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Поведение**: - Записывает файлы в кодировке UTF-8 - Сортирует ключи в алфавитном порядке (если не используется OrderedProperties) - Устанавливает для файла права доступа 600 (только чтение/запись для пользователя) начиная с версии 0.8.1 - Выбрасывает `IllegalArgumentException` при недопустимых символах в ключах или значениях - Выбрасывает `IOException` при ошибках записи

#### Проверка формата

Реализация выполняет строгую проверку:
- Ключи и значения проверяются на запрещённые символы
- Недопустимые записи вызывают исключения при операциях записи
- При чтении некорректные строки (строки без `=`) молча игнорируются

### Примеры форматов

#### Корректный файл конфигурации

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Примеры некорректных настроек

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Библиотека ядра и конфигурация Router

### Конфигурация клиентов (clients.config)

**Расположение**: `$I2P_CONFIG_DIR/clients.config` (устаревший) или `$I2P_CONFIG_DIR/clients.config.d/` (современный)   **Интерфейс конфигурации**: консоль Router на `/configclients`   **Изменение формата**: Версия 0.9.42 (август 2019 г.)

#### Структура каталогов (версия 0.9.42+)

Начиная с релиза 0.9.42, файл clients.config по умолчанию автоматически разделяется на отдельные файлы конфигурации:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Поведение при миграции**: - При первом запуске после обновления до 0.9.42+ монолитный файл автоматически разделяется на несколько файлов - Параметры в разделённых файлах имеют префикс `clientApp.0.` - Устаревший формат по-прежнему поддерживается для обратной совместимости - Разделённый формат позволяет модульное пакетирование и управление плагинами

#### Формат свойства

Строки имеют вид `clientApp.x.prop=val`, где `x` — номер приложения.

**Требования к нумерации приложений**: - ДОЛЖНА начинаться с 0 - ДОЛЖНА быть последовательной (без пропусков) - Порядок определяет последовательность запуска

#### Обязательные свойства

##### основной

- **Тип**: String (полностью квалифицированное имя класса)
- **Обязательный**: Да
- **Описание**: В этом классе будет вызван конструктор или метод `main()` в зависимости от типа клиента (управляемый или неуправляемый)
- **Пример**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Необязательные параметры

##### имя

- **Тип**: Строка
- **Обязательный**: Нет
- **Описание**: Отображаемое имя в консоли router
- **Пример**: `clientApp.0.name=Router Console`

##### args

- **Тип**: Строка (разделители: пробел или символ табуляции)
- **Обязательно**: Нет
- **Описание**: Аргументы, передаваемые конструктору главного класса или методу main()
- **Кавычки**: Аргументы, содержащие пробелы или табуляцию, можно заключать в кавычки `'` или `"`
- **Пример**: `clientApp.0.args=-d $CONFIG/eepsite`

##### задержка

- **Тип**: Целое число (секунды)
- **Обязательный**: Нет
- **Значение по умолчанию**: 120
- **Описание**: Количество секунд ожидания перед запуском клиента
- **Переопределение**: Переопределяется `onBoot=true` (устанавливает задержку в 0)
- **Специальные значения**:
  - `< 0`: Дождаться, пока router достигнет состояния RUNNING, затем запустить немедленно в новом потоке
  - `= 0`: Запустить немедленно в том же потоке (исключения передаются в консоль)
  - `> 0`: Запустить после задержки в новом потоке (исключения логируются, не передаются)

##### onBoot

- **Тип**: Логическое значение
- **Обязательный**: Нет
- **Значение по умолчанию**: false
- **Описание**: Принудительно устанавливает задержку 0, переопределяет явную настройку задержки
- **Сценарий использования**: Немедленный запуск критически важных служб при загрузке router

##### startOnLoad

- **Тип**: Логический
- **Обязательный**: Нет
- **Значение по умолчанию**: true
- **Описание**: Следует ли вообще запускать клиент
- **Сценарий использования**: Отключать клиентов без удаления конфигурации

#### Свойства, специфичные для плагина

Эти свойства используются только плагинами (а не основными клиентами):

##### stopargs

- **Тип**: Строка (разделённая пробелами или табуляцией)
- **Описание**: Аргументы, передаваемые для остановки клиента
- **Подстановка переменных**: Да (см. ниже)

##### uninstallargs

- **Тип**: Строка (разделённая пробелами или табуляцией)
- **Описание**: Аргументы, передаваемые при удалении клиента
- **Подстановка переменных**: Да (см. ниже)

##### путь к классам

- **Тип**: Строка (пути, разделённые запятыми)
- **Описание**: Дополнительные элементы classpath (путь к классам) для клиента
- **Подстановка переменных**: Да (см. ниже)

#### Подстановка переменных (только для плагинов)

Следующие переменные подставляются в `args`, `stopargs`, `uninstallargs` и `classpath` для плагинов:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Примечание**: Подстановка переменных выполняется только для плагинов, а не для основных клиентов.

#### Типы клиентов

##### Управляемые клиенты

- Конструктор вызывается с параметрами `RouterContext` и `ClientAppManager`
- Клиент должен реализовывать интерфейс `ClientApp`
- Жизненный цикл контролируется router
- Может быть запущен, остановлен и перезапущен динамически

##### Неуправляемые клиенты

- вызывается метод `main(String[] args)`
- запускается в отдельном потоке
- жизненный цикл не управляется router
- устаревший тип клиента

#### Пример конфигурации

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Конфигурация логгера (logger.config)

**Расположение**: `$I2P_CONFIG_DIR/logger.config`   **Интерфейс конфигурации**: консоль Router по адресу `/configlogging`

#### Справочник свойств

##### Настройка буфера консоли

###### logger.consoleBufferSize

- **Тип**: Целое число
- **По умолчанию**: 20
- **Описание**: Максимальное количество сообщений журнала для буферизации в консоли
- **Диапазон**: 1-1000, рекомендуется

##### Форматирование даты и времени

###### logger.dateFormat

- **Тип**: Строка (шаблон SimpleDateFormat)
- **Значение по умолчанию**: Определяется системной локалью
- **Пример**: `HH:mm:ss.SSS`
- **Документация**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Уровни журналирования

###### logger.defaultLevel

- **Тип**: перечисление
- **По умолчанию**: ERROR
- **Значения**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Описание**: Уровень логирования по умолчанию для всех классов

###### logger.minimumOnScreenLevel

- **Тип**: Перечисление (Enum)
- **По умолчанию**: CRIT
- **Значения**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Описание**: Минимальный уровень для сообщений, отображаемых на экране

###### logger.record.{class}

- **Тип**: перечисление (Enum)
- **Значения**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Описание**: Переопределение уровня логирования для конкретного класса
- **Пример**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Параметры отображения

###### logger.displayOnScreen

- **Тип**: логический
- **По умолчанию**: true
- **Описание**: Показывать ли сообщения журнала в консольном выводе

###### logger.dropDuplicates

- **Тип**: булево
- **По умолчанию**: true
- **Описание**: Отбрасывать повторяющиеся подряд сообщения журнала

###### logger.dropOnOverflow

- **Тип**: логический тип (Boolean)
- **По умолчанию**: false
- **Описание**: Отбрасывать сообщения, когда буфер заполнен (вместо блокировки)

##### Поведение при сбросе буфера

###### logger.flushInterval

- **Тип**: целое число (секунды)
- **По умолчанию**: 29
- **С версии**: 0.9.18
- **Описание**: Как часто сбрасывать буфер журнала на диск

##### Настройка формата

###### logger.format

- **Тип**: String (последовательность символов)
- **Описание**: Шаблон формата сообщения журнала
- **Символы формата**:
  - `d` = дата/время
  - `c` = имя класса
  - `t` = имя потока
  - `p` = приоритет (уровень логирования)
  - `m` = сообщение
- **Пример**: `dctpm` выдаёт `[timestamp] [class] [thread] [level] message`

##### Сжатие (версия 0.9.56+)

###### logger.gzip

- **Тип**: булево
- **По умолчанию**: false
- **С версии**: 0.9.56
- **Описание**: Включает сжатие gzip для файлов журналов после ротации

###### logger.minGzipSize

- **Тип**: Целое число (байты)
- **По умолчанию**: 65536
- **Начиная с**: версии 0.9.56
- **Описание**: Минимальный размер файла для включения сжатия (по умолчанию 64 КБ)

##### Управление файлами

###### logger.logBufferSize

- **Тип**: Целое число (байты)
- **По умолчанию**: 1024
- **Описание**: Максимальное число сообщений, накапливаемых в буфере перед сбросом

###### logger.logFileName

- **Тип**: Строка (путь к файлу)
- **Значение по умолчанию**: `logs/log-@.txt`
- **Описание**: Шаблон именования файла журнала (`@` заменяется номером ротации)

###### logger.logFilenameOverride

- **Тип**: Строка (путь к файлу)
- **Описание**: Переопределение имени файла журнала (отключает шаблон ротации)

###### logger.logFileSize

- **Тип**: Строка (размер с единицей измерения)
- **По умолчанию**: 10M
- **Единицы**: K (килобайты), M (мегабайты), G (гигабайты)
- **Пример**: `50M`, `1G`

###### logger.logRotationLimit

- **Тип**: целое число
- **По умолчанию**: 2
- **Описание**: Максимальный номер файла ротации (от log-0.txt до log-N.txt)

#### Пример конфигурации

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Настройка плагина

#### Конфигурация отдельного плагина (plugins/*/plugin.config)

**Расположение**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Формат**: Стандартный формат файла конфигурации I2P   **Документация**: [Спецификация плагина](/docs/specs/plugin/)

##### Обязательные свойства

###### имя

- **Тип**: строка
- **Обязательно**: Да
- **Описание**: Отображаемое имя плагина
- **Пример**: `name=I2P Plugin Example`

###### ключ

- **Тип**: Строка (открытый ключ)
- **Обязателен**: Да (опустите для плагинов, подписанных SU3)
- **Описание**: Открытый ключ для проверки подписи плагина
- **Формат**: Ключ подписи, закодированный в Base64

###### подписант

- **Тип**: Строка
- **Обязательно**: Да
- **Описание**: Идентификатор подписанта плагина
- **Пример**: `signer=user@example.i2p`

###### версия

- **Тип**: Строка (формат VersionComparator)
- **Обязательный**: Да
- **Описание**: Версия плагина для проверки обновлений
- **Формат**: Семантическое версионирование или пользовательский сравнимый формат
- **Пример**: `version=1.2.3`

##### Свойства отображения

###### дата

- **Тип**: Long (метка времени Unix в миллисекундах)
- **Описание**: Дата выпуска плагина

###### автор

- **Тип**: строка
- **Описание**: Имя автора плагина

###### websiteURL

- **Тип**: Строка (URL)
- **Описание**: URL веб-сайта плагина

###### updateURL

- **Тип**: Строка (URL)
- **Описание**: URL для проверки обновлений плагина

###### updateURL.su3

- **Тип**: Строка (URL)
- **Начиная с**: Версия 0.9.15
- **Описание**: URL обновления в формате SU3 (предпочтительно)

###### описание

- **Тип**: String
- **Описание**: Описание плагина на английском языке

###### description_{language}

- **Тип**: Строка
- **Описание**: Локализованное описание плагина
- **Пример**: `description_de=Немецкое описание`

###### лицензия

- **Тип**: строка
- **Описание**: Идентификатор лицензии плагина
- **Пример**: `license=Apache 2.0`

##### Параметры установки

###### не запускать после установки

- **Тип**: логический
- **По умолчанию**: false
- **Описание**: Предотвращает автоматический запуск после установки

###### Требуется перезапуск router

- **Тип**: Булево
- **По умолчанию**: false
- **Описание**: Требует перезапуска router после установки

###### только установка

- **Тип**: булево
- **По умолчанию**: false
- **Описание**: Однократная установка (без обновлений)

###### только для обновления

- **Тип**: логический
- **По умолчанию**: false
- **Описание**: Обновлять только существующую установку (без чистой установки)

##### Пример настройки плагина

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Глобальная конфигурация плагинов (plugins.config)

**Расположение**: `$I2P_CONFIG_DIR/plugins.config`   **Назначение**: Глобальное включение/отключение установленных плагинов

##### Формат свойства

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Имя плагина из plugin.config
- `startOnLoad`: Запускать ли плагин при запуске router

##### Пример

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Конфигурация веб-приложений (webapps.config)

**Расположение**: `$I2P_CONFIG_DIR/webapps.config`   **Назначение**: Включение/отключение и настройка веб-приложений

#### Формат свойства

##### webapps.{name}.startOnLoad

- **Тип**: Логический
- **Описание**: Запускать ли веб-приложение при запуске router
- **Формат**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Тип**: Строка (пути, разделённые пробелом или запятой)
- **Описание**: Дополнительные элементы classpath (путь к классам) для веб-приложения
- **Формат**: `webapps.{name}.classpath=[paths]`

#### Подстановка переменных

Пути поддерживают следующие подстановки переменных:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Разрешение пути классов

- **Основные веб-приложения**: Пути относительно `$I2P/lib`
- **Веб-приложения плагинов**: Пути относительно `$CONFIG/plugins/{appname}/lib`

#### Пример конфигурации

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Конфигурация Router (router.config)

**Расположение**: `$I2P_CONFIG_DIR/router.config`   **Интерфейс конфигурации**: Консоль Router на `/configadvanced`   **Назначение**: Основные настройки router и сетевые параметры

#### Категории конфигурации

##### Настройка сети

Настройки пропускной способности:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Конфигурация транспорта:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Поведение Router

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Настройка консоли

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Настройка времени

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Примечание**: Конфигурация router обширна. См. консоль router на странице `/configadvanced` для полного справочника по свойствам.

---

## Файлы конфигурации приложений

### Настройка адресной книги (addressbook/config.txt)

**Расположение**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Приложение**: SusiDNS   **Назначение**: Разрешение имён хостов и управление адресной книгой

#### Расположение файлов

##### router_addressbook

- **По умолчанию**: `../hosts.txt`
- **Описание**: Основная адресная книга (общесистемные имена хостов)
- **Формат**: Стандартный формат файла hosts

##### privatehosts.txt

- **Расположение**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Описание**: Частные сопоставления имён хостов
- **Приоритет**: Наивысший (переопределяет все остальные источники)

##### userhosts.txt

- **Расположение**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Описание**: Добавленные пользователем сопоставления имён хостов
- **Управление**: через интерфейс SusiDNS

##### hosts.txt

- **Расположение**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Описание**: Загруженная общедоступная адресная книга
- **Источник**: Ленты подписок

#### Служба имен

##### BlockfileNamingService (служба имён на основе блок-файла; по умолчанию с 0.8.8)

Формат хранения: - **Файл**: `hostsdb.blockfile` - **Расположение**: `$I2P_CONFIG_DIR/addressbook/` - **Производительность**: ~в 10 раз более быстрое разрешение имен, чем в hosts.txt - **Формат**: двоичный формат базы данных

Устаревшая служба имён: - **Формат**: Текстовый файл hosts.txt - **Статус**: Устаревший, но всё ещё поддерживается - **Сценарий использования**: Ручное редактирование, контроль версий

#### Правила имён хостов

Имена хостов I2P должны соответствовать:

1. **Требование к домену верхнего уровня (TLD)**: Должно оканчиваться на `.i2p`
2. **Максимальная длина**: всего 67 символов
3. **Набор символов**: `[a-z]`, `[0-9]`, `.` (точка), `-` (дефис)
4. **Регистр**: только строчные буквы
5. **Ограничения на начало**: не может начинаться с `.` или `-`
6. **Запрещённые последовательности**: не может содержать `..`, `.-` или `-.` (начиная с 0.6.1.33)
7. **Зарезервировано**: Base32-имена хостов `*.b32.i2p` (52 символа base32.b32.i2p)

##### Корректные примеры

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Некорректные примеры

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Управление подписками

##### subscriptions.txt

- **Расположение**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Формат**: По одному URL на строку
- **По умолчанию**: `http://i2p-projekt.i2p/hosts.txt`

##### Формат ленты подписки (с версии 0.9.26)

Расширенный формат ленты с метаданными:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Свойства метаданных: - `added`: Дата добавления имени хоста (формат YYYYMMDD) - `src`: Идентификатор источника - `sig`: Необязательная подпись

**Обратная совместимость**: Простой формат hostname=destination по-прежнему поддерживается.

#### Пример конфигурации

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### Конфигурация I2PSnark (i2psnark.config.d/i2psnark.config)

**Расположение**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Приложение**: BitTorrent‑клиент I2PSnark   **Интерфейс конфигурации**: Веб‑интерфейс по адресу http://127.0.0.1:7657/i2psnark

#### Структура каталогов

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Основная конфигурация (i2psnark.config)

Минимальная конфигурация по умолчанию:

```properties
i2psnark.dir=i2psnark
```
Дополнительные параметры, управляемые через веб-интерфейс:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Индивидуальная настройка торрента

**Расположение**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Формат**: Настройки для каждого торрента   **Управление**: Автоматическое (через веб-интерфейс)

Свойства включают: - Параметры отдачи/скачивания, специфичные для торрента - Приоритеты файлов - Информация о трекере - Лимиты пиров

**Примечание**: Настройка торрентов в основном осуществляется через веб-интерфейс. Ручное редактирование не рекомендуется.

#### Организация данных торрента

Хранение данных отделено от конфигурации:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### Конфигурация I2PTunnel (i2ptunnel.config)

**Расположение**: `$I2P_CONFIG_DIR/i2ptunnel.config` (устаревший) или `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (современный)   **Интерфейс конфигурации**: консоль Router по адресу `/i2ptunnel`   **Изменение формата**: версия 0.9.42 (август 2019)

#### Структура каталогов (версия 0.9.42+)

Начиная с релиза 0.9.42, файл i2ptunnel.config по умолчанию автоматически разделяется:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Критическое различие форматов**: - **Монолитный формат**: Свойства с префиксом `tunnel.N.` - **Раздельный формат**: Свойства **БЕЗ** префикса (например, `description=`, а не `tunnel.0.description=`)

#### Поведение при миграции

При первом запуске после обновления до 0.9.42: 1. Существующий i2ptunnel.config читается 2. Отдельные конфигурации tunnel создаются в i2ptunnel.config.d/ 3. В разделённых файлах у свойств удаляются префиксы 4. Создаётся резервная копия исходного файла 5. Устаревший формат по-прежнему поддерживается для обратной совместимости

#### Разделы конфигурации

Конфигурация I2PTunnel подробно описана в разделе [Справочник по конфигурации I2PTunnel](#i2ptunnel-configuration-reference) ниже. Описания свойств применимы для обоих форматов: монолитного (`tunnel.N.property`) и раздельного (`property`).

---

## Справочник по конфигурации I2PTunnel

В этом разделе приведена исчерпывающая техническая справочная информация по свойствам конфигурации I2PTunnel. Свойства показаны в раздельном формате (без префикса `tunnel.N.`). Для монолитного формата добавьте ко всем свойствам префикс `tunnel.N.`, где N — номер tunnel.

**Важно**: Свойства, описанные как `tunnel.N.option.i2cp.*`, реализованы в I2PTunnel (приложение для прокидывания TCP через I2P) и **НЕ** поддерживаются через другие интерфейсы, такие как протокол I2CP (I2P Client Protocol — клиентский протокол I2P) или SAM API.

### Основные свойства

#### tunnel.N.description (описание)

- **Тип**: Строка
- **Контекст**: Все tunnels
- **Описание**: Человекочитаемое описание tunnel для отображения в пользовательском интерфейсе
- **Пример**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (имя)

- **Тип**: Строка
- **Контекст**: Все tunnels
- **Обязателен**: Да
- **Описание**: Уникальный идентификатор tunnel и отображаемое имя
- **Пример**: `name=I2P HTTP Proxy`

#### tunnel.N.type (тип)

- **Тип**: Перечисление
- **Контекст**: Все tunnels
- **Обязательно**: Да
- **Значения**:
  - `client` - Универсальный клиентский tunnel
  - `httpclient` - Клиент HTTP-прокси
  - `ircclient` - Клиентский IRC tunnel
  - `socksirctunnel` - SOCKS IRC-прокси
  - `sockstunnel` - SOCKS-прокси (версии 4, 4a, 5)
  - `connectclient` - Клиент CONNECT-прокси
  - `streamrclient` - Клиент Streamr
  - `server` - Универсальный серверный tunnel
  - `httpserver` - HTTP-серверный tunnel
  - `ircserver` - IRC-серверный tunnel
  - `httpbidirserver` - Двунаправленный HTTP-сервер
  - `streamrserver` - Сервер Streamr

#### tunnel.N.interface (интерфейс)

- **Тип**: Строка (IP-адрес или имя хоста)
- **Контекст**: Только для Client tunnels
- **По умолчанию**: 127.0.0.1
- **Описание**: Локальный интерфейс, к которому привязывать входящие подключения
- **Примечание по безопасности**: Привязка к 0.0.0.0 разрешает удалённые подключения
- **Пример**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Тип**: целое число
- **Контекст**: только для клиентских tunnels
- **Диапазон**: 1-65535
- **Описание**: Локальный порт для прослушивания клиентских подключений
- **Пример**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Тип**: Строка (IP-адрес или имя хоста)
- **Контекст**: только для Server tunnels
- **Описание**: Локальный сервер, на который перенаправлять соединения
- **Пример**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Тип**: Целое число
- **Контекст**: Только для серверных tunnels
- **Диапазон**: 1-65535
- **Описание**: Порт на targetHost для подключения
- **Пример**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Тип**: Строка (назначения, разделённые запятыми или пробелами)
- **Контекст**: только для Client tunnels
- **Формат**: `destination[:port][,destination[:port]]`
- **Описание**: I2P-адрес(а) назначения для подключения
- **Примеры**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Тип**: Строка (IP-адрес или имя хоста)
- **По умолчанию**: 127.0.0.1
- **Описание**: Адрес интерфейса I2CP I2P router
- **Примечание**: Игнорируется при запуске в контексте router
- **Пример**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Тип**: Целое число
- **По умолчанию**: 7654
- **Диапазон**: 1-65535
- **Описание**: Порт I2CP для I2P router
- **Примечание**: Игнорируется при запуске в контексте router
- **Пример**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Тип**: Логический
- **Значение по умолчанию**: true
- **Описание**: Следует ли запускать tunnel при загрузке I2PTunnel
- **Пример**: `startOnLoad=true`

### Настройка прокси

#### tunnel.N.proxyList (proxyList)

- **Тип**: Строка (имена хостов, разделённые запятыми или пробелами)
- **Контекст**: Только для HTTP- и SOCKS-прокси
- **Описание**: Список хостов outproxy (внешний прокси в I2P)
- **Пример**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Конфигурация сервера

#### tunnel.N.privKeyFile (privKeyFile)

- **Тип**: Строка (путь к файлу)
- **Контекст**: Серверы и постоянные клиентские tunnels
- **Описание**: Файл, содержащий закрытые ключи постоянного destination (адреса назначения)
- **Путь**: Абсолютный или относительный к каталогу конфигурации I2P
- **Пример**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Тип**: Строка (имя хоста)
- **Контекст**: только для HTTP-серверов
- **По умолчанию**: имя хоста назначения в формате Base32
- **Описание**: Значение заголовка Host, передаваемое локальному серверу
- **Пример**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Тип**: Строка (имя хоста)
- **Контекст**: Только для HTTP-серверов
- **Описание**: Переопределение виртуального хоста для конкретного входящего порта
- **Сценарий использования**: Размещение нескольких сайтов на разных портах
- **Пример**: `spoofedHost.8080=site1.example.i2p`

### Параметры для конкретного клиента

#### tunnel.N.sharedClient (sharedClient)

- **Тип**: Логическое значение
- **Контекст**: Только для клиентских tunnels
- **По умолчанию**: false
- **Описание**: Могут ли несколько клиентов совместно использовать этот tunnel
- **Пример**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Тип**: логический
- **Контекст**: Только для Client tunnels
- **Значение по умолчанию**: false
- **Описание**: Сохранять и повторно использовать ключи назначения между перезапусками
- **Конфликт**: Взаимоисключимо с `i2cp.newDestOnResume=true`
- **Пример**: `option.persistentClientKey=true`

### Параметры I2CP (реализация I2PTunnel)

**Важно**: Эти свойства имеют префикс `option.i2cp.`, но **реализованы в I2PTunnel**, а не на уровне протокола I2CP. Они недоступны через API I2CP или SAM.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Тип**: Boolean
- **Контекст**: Только клиентские tunnel
- **Значение по умолчанию**: false
- **Описание**: Отложить создание tunnel до первого подключения
- **Сценарий использования**: Экономия ресурсов для редко используемых tunnel
- **Пример**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Тип**: Булево
- **Контекст**: Только для клиентских tunnels
- **По умолчанию**: false
- **Требуется**: `i2cp.closeOnIdle=true`
- **Конфликт**: Взаимоисключимо с `persistentClientKey=true`
- **Описание**: Создавать новый destination (криптографический адрес назначения) после истечения тайм-аута простоя
- **Пример**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Тип**: Строка (ключ, закодированный в base64)
- **Контекст**: Только для server tunnels
- **Описание**: Постоянный закрытый ключ шифрования leaseSet
- **Сценарий использования**: Обеспечить сохранение одного и того же зашифрованного leaseSet при перезапусках
- **Пример**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Тип**: Строка (sigtype:base64)
- **Контекст**: Только для серверных tunnel'ов
- **Формат**: `sigtype:base64key`
- **Описание**: Постоянный закрытый ключ подписи leaseSet (набор аренд входящих tunnel'ов)
- **Пример**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Параметры, специфичные для сервера

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Тип**: Логический (Boolean)
- **Контекст**: Только для серверных tunnel'ов
- **По умолчанию**: false
- **Описание**: Использовать уникальный локальный IP для каждого удалённого I2P-назначения (destination)
- **Сценарий использования**: Отслеживать IP клиентов в журналах сервера
- **Примечание по безопасности**: Может снизить анонимность
- **Пример**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Тип**: Строка (hostname:port)
- **Контекст**: Только для server tunnels
- **Описание**: Переопределяет targetHost/targetPort для входящего порта NNNN
- **Сценарий использования**: Маршрутизация по портам к разным локальным сервисам
- **Пример**: `option.targetForPort.8080=localhost:8080`

### Конфигурация пула потоков

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Тип**: Булево
- **Контекст**: только для server tunnels
- **По умолчанию**: true
- **Описание**: использовать пул потоков для обработки подключений
- **Примечание**: всегда false для стандартных серверов (игнорируется)
- **Пример**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Тип**: Целое число
- **Контекст**: Только для серверных tunnels
- **По умолчанию**: 65
- **Описание**: Максимальный размер пула потоков
- **Примечание**: Не применяется для стандартных серверов
- **Пример**: `option.i2ptunnel.blockingHandlerCount=100`

### Параметры HTTP-клиента

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Тип**: булево
- **Контекст**: только для HTTP-клиентов
- **По умолчанию**: false
- **Описание**: Разрешить SSL-подключения к адресам .i2p
- **Пример**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Тип**: Булево
- **Контекст**: только для HTTP-клиентов
- **По умолчанию**: false
- **Описание**: Отключить ссылки address helper (ссылки‑помощники адреса) в ответах прокси
- **Пример**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Тип**: Строка (URL-адреса, разделённые запятыми или пробелами)
- **Контекст**: Только для HTTP-клиентов
- **Описание**: URL-адреса Jump server (служба Jump) для разрешения имён хостов
- **Пример**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Тип**: Логический (Boolean)
- **Контекст**: только для HTTP-клиентов
- **Значение по умолчанию**: false
- **Описание**: Передавать заголовки Accept-* (кроме Accept и Accept-Encoding)
- **Пример**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Тип**: Логический
- **Контекст**: только для HTTP-клиентов
- **По умолчанию**: false
- **Описание**: Передавать заголовки Referer через прокси
- **Примечание о конфиденциальности**: Может привести к утечке информации
- **Пример**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Тип**: логический
- **Контекст**: только для HTTP‑клиентов
- **По умолчанию**: false
- **Описание**: Передавать заголовки User-Agent через прокси
- **Примечание по конфиденциальности**: Может раскрывать информацию о браузере
- **Пример**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Тип**: Логический
- **Контекст**: только для HTTP‑клиентов
- **Значение по умолчанию**: false
- **Описание**: Передавать заголовки Via через прокси
- **Пример**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Type**: String (назначения, разделённые запятыми или пробелами)
- **Context**: только HTTP-клиенты
- **Description**: Внутрисетевые SSL outproxies (прокси-шлюзы из I2P в Интернет) для HTTPS
- **Example**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Тип**: логический
- **Контекст**: только для HTTP‑клиентов
- **Значение по умолчанию**: true
- **Описание**: Использовать зарегистрированные локальные плагины outproxy (выходного прокси)
- **Пример**: `option.i2ptunnel.useLocalOutproxy=true`

### Аутентификация клиента HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Тип**: Enum (перечисление)
- **Контекст**: только для HTTP‑клиентов
- **По умолчанию**: false
- **Значения**: `true`, `false`, `basic`, `digest`
- **Описание**: Требовать локальную аутентификацию для доступа к прокси
- **Примечание**: `true` эквивалентно `basic`
- **Пример**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Тип**: Строка (32-символьная шестнадцатеричная строка в нижнем регистре)
- **Контекст**: только клиенты HTTP
- **Требуется**: `proxyAuth=basic` или `proxyAuth=digest`
- **Описание**: MD5-хеш пароля для пользователя USER
- **Устарело**: вместо этого используйте SHA-256 (0.9.56+)
- **Пример**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Тип**: Строка (64-символьное шестнадцатеричное значение в нижнем регистре)
- **Контекст**: только для HTTP-клиентов
- **Требуется**: `proxyAuth=digest`
- **С версии**: 0.9.56
- **Стандарт**: RFC 7616
- **Описание**: хеш SHA-256 пароля для пользователя USER
- **Пример**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Аутентификация Outproxy (внешнего прокси)

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Тип**: логический
- **Контекст**: только для HTTP‑клиентов
- **Значение по умолчанию**: false
- **Описание**: Отправлять данные аутентификации на outproxy (прокси-сервер выхода в обычный интернет)
- **Пример**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Тип**: Строка
- **Контекст**: только для HTTP‑клиентов
- **Требует**: `outproxyAuth=true`
- **Описание**: Имя пользователя для аутентификации на outproxy (внешний прокси I2P)
- **Пример**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Тип**: Строка
- **Контекст**: Только для HTTP-клиентов
- **Требует**: `outproxyAuth=true`
- **Описание**: Пароль для аутентификации на outproxy
- **Безопасность**: Хранится в незашифрованном виде
- **Пример**: `option.outproxyPassword=secret`

### Параметры клиента SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Тип**: Строка (адреса назначения, разделённые запятыми или пробелами)
- **Контекст**: Только для клиентов SOCKS
- **Описание**: Внутрисетевые outproxies (прокси для выхода из сети I2P в Интернет) для неуказанных портов
- **Пример**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Тип**: Строка (destinations (адреса назначения в I2P), разделённые запятыми или пробелами)
- **Контекст**: только для клиентов SOCKS
- **Описание**: outproxies (аутпрокси) внутри сети I2P специально для порта NNNN
- **Пример**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Тип**: Перечисление
- **Контекст**: Только клиенты SOCKS
- **По умолчанию**: socks
- **Начиная с**: версии 0.9.57
- **Значения**: `socks`, `connect` (HTTPS)
- **Описание**: Тип настроенного outproxy (прокси-выход в обычный интернет)
- **Пример**: `option.outproxyType=connect`

### Параметры HTTP-сервера

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Тип**: Целое число
- **Контекст**: Только для HTTP-серверов
- **По умолчанию**: 0 (без ограничений)
- **Описание**: Максимальное число POST-запросов от одного назначения за postCheckTime
- **Пример**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Тип**: Целое число
- **Контекст**: Только для HTTP-серверов
- **По умолчанию**: 0 (неограниченно)
- **Описание**: Максимальное число POST-запросов со всех источников за период postCheckTime
- **Пример**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Тип**: Целое число (секунды)
- **Контекст**: только для HTTP-серверов
- **По умолчанию**: 300
- **Описание**: Временное окно для проверки лимитов POST
- **Пример**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Тип**: Целое число (секунды)
- **Контекст**: только для HTTP-серверов
- **По умолчанию**: 1800
- **Описание**: Срок блокировки после превышения maxPosts для одного назначения
- **Пример**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Тип**: Целое число (секунды)
- **Контекст**: Только для HTTP-серверов
- **По умолчанию**: 600
- **Описание**: Длительность блокировки после превышения maxTotalPosts
- **Пример**: `option.postTotalBanTime=1200`

### Параметры безопасности HTTP-сервера

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Тип**: Логический
- **Контекст**: только HTTP-серверы
- **По умолчанию**: false
- **Описание**: Отклонять подключения, предположительно идущие через inproxy (входящий прокси для доступа к I2P из обычного интернета)
- **Пример**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Тип**: булево значение
- **Контекст**: только для HTTP-серверов
- **По умолчанию**: false
- **С версии**: 0.9.25
- **Описание**: Отклонять соединения с заголовком Referer
- **Пример**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Тип**: Логическое значение
- **Контекст**: Только для HTTP-серверов
- **Значение по умолчанию**: false
- **С версии**: 0.9.25
- **Требуется**: свойство `userAgentRejectList`
- **Описание**: Отклоняет соединения с совпадающим значением User-Agent
- **Пример**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Тип**: Строка (список шаблонов сопоставления, разделённых запятыми)
- **Контекст**: только HTTP-серверы
- **Начиная с**: версии 0.9.25
- **Регистр**: регистрозависимое сопоставление
- **Особое**: "none" (начиная с 0.9.33) соответствует пустому User-Agent
- **Описание**: Список шаблонов User-Agent для отклонения
- **Пример**: `option.userAgentRejectList=Mozilla,Opera,none`

### Параметры сервера IRC

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Тип**: Строка (шаблон имени хоста)
- **Контекст**: Только для серверов IRC
- **По умолчанию**: `%f.b32.i2p`
- **Токены**:
  - `%f` = Полный base32-хеш назначения
  - `%c` = Замаскированный хеш назначения (см. cloakKey)
- **Описание**: Формат имени хоста, отправляемый на сервер IRC
- **Пример**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Тип**: Строка (парольная фраза)
- **Контекст**: Только для серверов IRC
- **По умолчанию**: Случайное для каждой сессии
- **Ограничения**: Без кавычек и пробелов
- **Описание**: Парольная фраза для единообразного маскирования имени хоста
- **Сценарий использования**: Постоянное отслеживание пользователя при перезапусках/на разных серверах
- **Пример**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Тип**: перечисление
- **Контекст**: только для серверов IRC
- **По умолчанию**: user
- **Значения**: `user`, `webirc`
- **Описание**: метод аутентификации для сервера IRC
- **Пример**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Тип**: Строка (пароль)
- **Контекст**: только IRC-серверы
- **Требует**: `method=webirc`
- **Ограничения**: без кавычек и пробелов
- **Описание**: Пароль для аутентификации по протоколу WEBIRC
- **Пример**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Тип**: строка (IP-адрес)
- **Контекст**: только для IRC‑серверов
- **Требует**: `method=webirc`
- **Описание**: Подменённый IP‑адрес для протокола WEBIRC
- **Пример**: `option.ircserver.webircSpoofIP=10.0.0.1`

### Настройка SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **Тип**: логический
- **По умолчанию**: false
- **Контекст**: Все tunnels
- **Поведение**:
  - **Серверы**: Использовать SSL для соединений с локальным сервером
  - **Клиенты**: Требовать SSL от локальных клиентов
- **Пример**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Тип**: Строка (путь к файлу)
- **Контекст**: Только Client tunnels
- **По умолчанию**: `i2ptunnel-(random).ks`
- **Путь**: Относительный к `$(I2P_CONFIG_DIR)/keystore/`, если путь не абсолютный
- **Автоматическое создание**: Создается, если не существует
- **Описание**: Файл хранилища ключей (keystore), содержащий закрытый ключ SSL
- **Пример**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Тип**: Строка (пароль)
- **Контекст**: Только клиентские tunnels
- **По умолчанию**: changeit
- **Автоматически генерируется**: Случайный пароль, если создано новое хранилище ключей
- **Описание**: Пароль для SSL хранилища ключей
- **Пример**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Тип**: Строка (псевдоним)
- **Контекст**: только для клиентских tunnels
- **Автоматически создаётся**: если сгенерирован новый ключ
- **Описание**: Псевдоним для закрытого ключа в хранилище ключей
- **Пример**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Тип**: Строка (пароль)
- **Контекст**: Только для client tunnels
- **Автоматически генерируется**: Случайный пароль при создании нового ключа
- **Описание**: Пароль для закрытого ключа в хранилище ключей
- **Пример**: `option.keyPassword=keypass123`

### Общие параметры I2CP и Streaming (библиотека потоковой передачи данных)

Все свойства `tunnel.N.option.*` (не описанные явно выше) передаются в интерфейс I2CP и библиотеку потоковой передачи без префикса `tunnel.N.option.`.

**Важно**: Это отдельные параметры, отличные от параметров, специфичных для I2PTunnel. Смотрите: - [Спецификация I2CP](/docs/specs/i2cp/) - [Спецификация потоковой библиотеки](/docs/specs/streaming/)

Примеры параметров стриминга:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Полный пример Tunnel

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## История версий и хронология функций

### Версия 0.9.10 (2013)

**Новая возможность**: Поддержка пустых значений в файлах конфигурации - Ключи с пустыми значениями (`key=`) теперь поддерживаются - Ранее игнорировались или вызывали ошибки разбора

### Версия 0.9.18 (2015)

**Функция**: Настройка интервала сброса буфера логгера - Свойство: `logger.flushInterval` (по умолчанию 29 секунд) - Снижает нагрузку на дисковый ввод-вывод при сохранении приемлемой задержки записи логов

### Версия 0.9.23 (Ноябрь 2015)

**Важное изменение**: минимальное требование — Java 7 - поддержка Java 6 прекращена - требуется для дальнейших обновлений безопасности

### Версия 0.9.25 (2015)

**Функции**: Параметры безопасности HTTP-сервера - `tunnel.N.option.rejectReferer` - Отклонять соединения с заголовком Referer - `tunnel.N.option.rejectUserAgents` - Отклонять определённые заголовки User-Agent - `tunnel.N.option.userAgentRejectList` - Шаблоны User-Agent для отклонения - **Сценарий использования**: Снизить активность краулеров и нежелательных клиентов

### Версия 0.9.33 (январь 2018)

**Функция**: Улучшенная фильтрация заголовка User-Agent - `userAgentRejectList` строка "none" соответствует пустому User-Agent - Дополнительные исправления ошибок для i2psnark, i2ptunnel, streaming, SusiMail

### Версия 0.9.41 (2019)

**Объявление об устаревании**: протокол BOB удалён из Android - пользователям Android необходимо перейти на SAM или I2CP

### Версия 0.9.42 (август 2019 г.)

**Существенное изменение**: Разделение конфигурационных файлов - `clients.config` разделён на структуру каталога `clients.config.d/` - `i2ptunnel.config` разделён на структуру каталога `i2ptunnel.config.d/` - Автоматическая миграция при первом запуске после обновления - Обеспечивает модульное пакетирование и управление плагинами - Устаревший монолитный формат по-прежнему поддерживается

**Дополнительные возможности**: - Улучшения производительности SSU - Предотвращение межсетевых соединений (Предложение 147) - Начальная поддержка типов шифрования

### Версия 0.9.56 (2021)

**Возможности**: улучшения безопасности и журналирования - `logger.gzip` - Gzip-сжатие для ротируемых логов (по умолчанию: false) - `logger.minGzipSize` - Минимальный размер для сжатия (по умолчанию: 65536 байт) - `tunnel.N.option.proxy.auth.USER.sha256` - Дайджест-аутентификация SHA-256 (RFC 7616) - **Безопасность**: SHA-256 заменяет MD5 для дайджест-аутентификации

### Версия 0.9.57 (январь 2023)

**Функция**: Настройка типа SOCKS outproxy (прокси-сервера для выхода во внешний Интернет) - `tunnel.N.option.outproxyType` - Выбор типа outproxy (socks|connect) - По умолчанию: socks - Поддержка HTTPS CONNECT для HTTPS outproxy

### Версия 2.6.0 (июль 2024)

**Несовместимое изменение**: I2P-over-Tor заблокирован - Подключения с IP-адресов выходных узлов Tor теперь отклоняются - **Причина**: ухудшает производительность I2P, расходует ресурсы выходных узлов Tor - **Последствия**: пользователи, обращающиеся к I2P через выходные узлы Tor, будут заблокированы - Невыходные ретрансляторы и клиенты Tor не затронуты

### Версия 2.10.0 (сентябрь 2025 - настоящее время)

**Основные возможности**: - **Постквантовая криптография** доступна (опционально через Hidden Service Manager) - **Поддержка UDP-трекеров** для I2PSnark для снижения нагрузки на трекеры - **Стабильность Скрытого режима** улучшена для уменьшения истощения RouterInfo (метаданных router) - Улучшения сети для перегруженных router - Улучшено прохождение через UPnP/NAT - Улучшения NetDB с агрессивным удалением leaseset - Снижение наблюдаемости событий router

**Конфигурация**: Новых параметров конфигурации не добавлено

**Критическое предстоящее изменение**: Следующий релиз (вероятно, 2.11.0 или 3.0.0) потребует Java 17 или новее

---

## Устаревшие функции и изменения, нарушающие обратную совместимость

### Критические устаревания

#### Доступ к I2P поверх Tor (Версия 2.6.0+)

- **Статус**: ЗАБЛОКИРОВАНО с июля 2024 года
- **Влияние**: Соединения с IP-адресов выходных узлов Tor отклоняются
- **Причина**: Ухудшает производительность сети I2P, не давая преимуществ в анонимности
- **Затрагивает**: Только выходные узлы Tor; ретрансляторы и обычные клиенты Tor не затрагиваются
- **Альтернатива**: Используйте I2P или Tor отдельно, не совместно

#### Digest-аутентификация MD5

- **Статус**: Устарело (используйте SHA-256)
- **Свойство**: `tunnel.N.option.proxy.auth.USER.md5`
- **Причина**: MD5 криптографически небезопасен
- **Замена**: `tunnel.N.option.proxy.auth.USER.sha256` (начиная с 0.9.56)
- **Статус поддержки**: MD5 всё ещё поддерживается, но не рекомендуется

### Изменения в архитектуре конфигурации

#### Монолитные файлы конфигурации (Версия 0.9.42+)

- **Затронуто**: `clients.config`, `i2ptunnel.config`
- **Статус**: Устарело в пользу раздельной структуры каталогов
- **Миграция**: Автоматическая при первом запуске после обновления до 0.9.42
- **Совместимость**: Устаревший формат по-прежнему работает (обратная совместимость)
- **Рекомендация**: Используйте раздельный формат для новых конфигураций

### Требования к версии Java

#### Поддержка Java 6

- **Завершено**: версия 0.9.23 (ноябрь 2015)
- **Минимум**: Java 7 требуется начиная с 0.9.23

#### Требование Java 17 (в ближайшее время)

- **Статус**: КРИТИЧЕСКОЕ ПРЕДСТОЯЩЕЕ ИЗМЕНЕНИЕ
- **Цель**: Следующий мажорный релиз после 2.10.0 (вероятно, 2.11.0 или 3.0.0)
- **Текущая минимальная версия**: Java 8
- **Необходимо**: Подготовиться к переходу на Java 17
- **Сроки**: Будут объявлены вместе с примечаниями к релизу

### Удалённые функции

#### Протокол BOB (Android)

- **Удалено**: Версия 0.9.41
- **Платформа**: только для Android
- **Альтернатива**: протоколы SAM (протокол взаимодействия с I2P) или I2CP
- **Настольные системы**: BOB (интерфейс управления I2P) по-прежнему доступен на настольных платформах

### Рекомендуемые миграции

1. **Аутентификация**: Перейти с MD5 на аутентификацию по дайджесту SHA-256
2. **Формат конфигурации**: Перейти на раздельную структуру каталогов для клиентов и tunnels
3. **Среда выполнения Java**: Запланировать обновление до Java 17 перед следующим крупным релизом
4. **Интеграция с Tor**: Не маршрутизировать I2P через выходные узлы Tor

---

## Ссылки

### Официальная документация

- [I2P Configuration Specification](/docs/specs/configuration/) - Официальная спецификация формата конфигурационного файла
- [I2P Plugin Specification](/docs/specs/plugin/) - Конфигурация и упаковка плагинов
- [I2P Common Structures - Type Mapping](/docs/specs/common-structures/#type-mapping) - Формат сериализации данных протокола
- [Java Properties Format](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Базовая спецификация формата

### Исходный код

- [Репозиторий I2P Java Router](https://github.com/i2p/i2p.i2p) - Зеркало на GitHub
- [Gitea разработчиков I2P](https://i2pgit.org/I2P_Developers/i2p.i2p) - Официальный репозиторий исходного кода I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Реализация ввода/вывода файлов конфигурации

### Ресурсы сообщества

- [Форум I2P](https://i2pforum.net/) - Активные обсуждения в сообществе и поддержка
- [Сайт I2P](/) - Официальный сайт проекта

### Документация по API

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - документация по API для методов файла конфигурации

### Статус спецификации

- **Последнее обновление спецификации**: январь 2023 (версия 0.9.57)
- **Текущая версия I2P**: 2.10.0 (сентябрь 2025)
- **Техническая корректность**: спецификация остаётся корректной вплоть до 2.10.0 (без несовместимых изменений)
- **Сопровождение**: живой документ, обновляется при изменении формата конфигурации
