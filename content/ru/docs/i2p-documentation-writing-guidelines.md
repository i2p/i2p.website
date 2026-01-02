---
title: "Рекомендации по написанию документации I2P"
description: "Обеспечивайте согласованность, точность и доступность во всей технической документации I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Цель:** Обеспечивать единообразие, точность и доступность во всей технической документации I2P

---

## Основные принципы

### 1. Проверьте всё

**Никогда не делайте предположений и не угадывайте.** Все технические утверждения должны быть проверены на соответствие: - Текущему исходному коду I2P (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Официальной документации API (https://i2p.github.io/i2p.i2p/  - Спецификации конфигурации [/docs/specs/](/docs/) - Недавние примечания к релизам [/releases/](/categories/release/)

**Пример корректной проверки:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. Ясность важнее краткости

Пишите для разработчиков, которые могут впервые сталкиваться с I2P. Объясняйте понятия полностью, не предполагая наличия предварительных знаний.

**Пример:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Доступность прежде всего

Документация должна быть доступна разработчикам в клирнете (обычный интернет), даже несмотря на то, что I2P — оверлейная сеть. Всегда предоставляйте альтернативы, доступные из клирнета, для внутренних ресурсов I2P.

---

## Техническая точность

### Документация по API и интерфейсу

**Всегда указывайте:** 1. Полные имена пакетов при первом упоминании: `net.i2p.app.ClientApp` 2. Полные сигнатуры методов с типами возвращаемых значений 3. Имена параметров и их типы 4. Обязательные и необязательные параметры

**Пример:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Параметры конфигурации

При документировании файлов конфигурации: 1. Показывайте точные имена свойств 2. Указывайте кодировку файла (UTF-8 для конфигов I2P) 3. Приводите полные примеры 4. Документируйте значения по умолчанию 5. Указывайте версию, в которой свойства были введены/изменены

**Пример:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Константы и перечисления

При документировании констант используйте точные имена из кода:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Различайте близкие по смыслу понятия

I2P имеет несколько пересекающихся подсистем. Всегда уточняйте, какую именно подсистему вы документируете:

**Пример:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## URL-адреса документации и ссылки

### Правила доступности URL-адресов

1. **Основные источники** должны использовать URL-адреса, доступные из clearnet (открытого интернета)
2. **Внутренние для I2P URL-адреса** (.i2p domains) должны включать примечания о доступности
3. **Всегда предоставляйте альтернативы** при ссылках на внутренние для I2P ресурсы

**Шаблон для внутренних URL-адресов I2P:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### Рекомендуемые справочные URL-адреса I2P

**Официальные спецификации:** - [Конфигурация](/docs/specs/configuration/) - [Плагин](/docs/specs/plugin/) - [Индекс документации](/docs/)

**Документация по API (выберите самую актуальную):** - Самая актуальная: https://i2p.github.io/i2p.i2p/ (API 0.9.66 по состоянию на I2P 2.10.0) - Зеркало в Clearnet (открытом интернете): https://eyedeekay.github.io/javadoc-i2p/

**Исходный код:** - GitLab (официальный): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - Зеркало на GitHub: https://github.com/i2p/i2p.i2p

### Стандарты формата ссылок

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Отслеживание версий

### Метаданные документа

Каждый технический документ должен включать метаданные версии в frontmatter (служебный блок метаданных в начале файла):

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
**Определения полей:** - `lastUpdated`: Год и месяц последней проверки/обновления документа - `accurateFor`: Версия I2P, на соответствие которой документ был проверен - `reviewStatus`: Одно из "draft", "needs-review", "verified", "outdated"

### Ссылки на версии в содержимом

При упоминании версий: 1. Выделяйте текущую версию жирным: "**версия 2.10.0** (сентябрь 2025)" 2. В исторических упоминаниях указывайте и номер версии, и дату 3. При необходимости указывайте версию API отдельно от версии I2P

**Пример:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Документирование изменений со временем

Для возможностей, которые развивались:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Уведомления об устаревании

Если вы документируете устаревшие возможности:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Стандарты терминологии

### Официальные термины I2P

Используйте эти точные термины последовательно:

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
### Терминология управляемого клиента

При документировании управляемых клиентов:

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
### Терминология конфигурации

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
### Имена пакетов и классов

Всегда при первом упоминании используйте полностью квалифицированные имена, в дальнейшем — краткие имена:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Примеры кода и форматирование

### Примеры кода на Java

Используйте правильную подсветку синтаксиса и полные примеры:

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
**Требования к примеру кода:** 1. Добавьте комментарии, объясняющие ключевые строки 2. Покажите обработку ошибок там, где это уместно 3. Используйте реалистичные имена переменных 4. Соответствуйте соглашениям кодирования I2P (отступ в 4 пробела) 5. Покажите импорты, если из контекста это не очевидно

### Примеры конфигурации

Приведите полные и корректные примеры конфигурации:

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
### Примеры командной строки

Используйте `$` для команд пользователя, `#` для суперпользователя:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Встроенный код

Используйте обратные кавычки для: - Имена методов: `startup()` - Имена классов: `ClientApp` - Имена свойств: `clientApp.0.main` - Имена файлов: `clients.config` - Константы: `SVC_HTTP_PROXY` - Имена пакетов: `net.i2p.app`

---

## Тон и голос

### Профессионально, но доступно

Пишите для технической аудитории без снисходительного тона:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Действительный залог

Используйте активный залог для ясности:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Повелительное наклонение в инструкциях

Используйте повелительное наклонение в процедурных материалах:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Избегайте лишнего жаргона

Объясняйте термины при первом упоминании:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Рекомендации по пунктуации

1. **Не используйте длинные тире** - вместо этого используйте обычные дефисы, запятые или точки с запятой
2. Используйте **оксфордскую запятую** в списках: "console, i2ptunnel, and Jetty"
3. **Точки внутри блоков кода** только при грамматической необходимости
4. **Сложные перечисления** используют точки с запятой, когда элементы содержат запятые

---

## Структура документа

### Стандартный порядок разделов

Для документации по API:

1. **Обзор** - что делает функция, для чего она нужна
2. **Реализация** - как реализовать/использовать её
3. **Настройка** - как её настроить
4. **Справочник по API** - подробные описания методов и свойств
5. **Примеры** - полные рабочие примеры
6. **Лучшие практики** - советы и рекомендации
7. **История версий** - когда появилась, изменения со временем
8. **Ссылки** - ссылки на связанную документацию

### Иерархия заголовков

Используйте семантические уровни заголовков:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Информационные блоки

Используйте блоки цитирования для специальных уведомлений:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Списки и организация

**Ненумерованные списки** для непоследовательных элементов:

```markdown
- First item
- Second item
- Third item
```
**Нумерованные списки** для последовательных шагов:

```markdown
1. First step
2. Second step
3. Third step
```
**Списки определений** для пояснения терминов:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Распространённые ошибки, которых следует избегать

### 1. Схожие системы, которые часто путают

**Не путайте:** - реестр ClientAppManager (менеджер клиентских приложений) и PortMapper - типы tunnel в i2ptunnel и константы сервиса port mapper - ClientApp и RouterApp (разные контексты) - Управляемые и неуправляемые клиенты

**Всегда уточняйте, о какой системе** вы говорите:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Ссылки на устаревшие версии

**Не делайте:** - Называть старые версии «текущими» - Давать ссылки на устаревшую документацию API - Использовать устаревшие сигнатуры методов в примерах

**Следует:** - Проверьте примечания к выпуску перед публикацией - Убедитесь, что документация по API соответствует текущей версии - Обновите примеры, чтобы использовать текущие наилучшие практики

### 3. Недоступные URL-адреса

**Не следует:** - Ссылаться только на домены .i2p без альтернатив в клирнете - Использовать битые или устаревшие URL-адреса документации - Ссылаться на локальные пути file://

**Следует:** - Предоставляйте альтернативы в clearnet (открытый интернет) для всех внутренних I2P-ссылок - Проверяйте доступность URL-адресов перед публикацией - Используйте постоянные URL-адреса (geti2p.net, а не временный хостинг)

### 4. Неполные примеры кода

**Не делайте:** - Показывать фрагменты без контекста - Опускать обработку ошибок - Использовать неопределённые переменные - Пропускать операторы импорта, когда это не очевидно

**Следует:** - Приводите полные, компилируемые примеры - Включайте необходимую обработку ошибок - Объясняйте, что делает каждая важная строка кода - Тестируйте примеры перед публикацией

### 5. Неоднозначные утверждения

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Соглашения по Markdown

### Именование файлов

Используйте kebab-case (слова, разделённые дефисами) для имён файлов: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Формат фронтматтера

Всегда включайте YAML фронтматтер:

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
### Форматирование ссылок

**Внутренние ссылки** (внутри документации):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Внешние ссылки** (на другие ресурсы):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Ссылки на репозитории исходного кода**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Форматирование таблиц

Используйте таблицы GitHub Flavored Markdown (вариант Markdown от GitHub):

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Языковые теги для блоков кода

Всегда указывайте язык для подсветки синтаксиса:

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

## Проверочный список

Перед публикацией документации проверьте:

- [ ] Все технические утверждения проверены по исходному коду или официальной документации
- [ ] Номера версий и даты актуальны
- [ ] Все URL-адреса доступны из clearnet (обычный интернет), либо предоставлены альтернативы
- [ ] Примеры кода полные и протестированы
- [ ] Терминология соответствует соглашениям I2P
- [ ] Без длинных тире (используйте обычные дефисы или другую пунктуацию)
- [ ] Раздел Frontmatter (метаданные в начале документа) заполнен полностью и корректно
- [ ] Иерархия заголовков семантическая (h1 → h2 → h3)
- [ ] Списки и таблицы корректно отформатированы
- [ ] Раздел со ссылками содержит все цитируемые источники
- [ ] Документ следует рекомендациям по структуре
- [ ] Тон профессиональный, но доступный
- [ ] Близкие по смыслу понятия четко разграничены
- [ ] Нет битых ссылок или некорректных перекрестных ссылок
- [ ] Примеры конфигурации валидны и актуальны

---

**Обратная связь:** Если вы обнаружите проблемы или у вас есть предложения по этим рекомендациям, пожалуйста, сообщите о них через официальные каналы разработки I2P.
