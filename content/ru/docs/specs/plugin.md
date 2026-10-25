---
title: "Спецификация плагина"
description: "Правила упаковки .xpi2p / .su3 для плагинов I2P"
slug: "plugin"
aliases:
  - "/ru/plugin_spec"
  - "/ru/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Обзор

Этот документ описывает формат файла .xpi2p (подобный формату Firefox .xpi), но с простым файлом описания plugin.config вместо XML-файла install.rdf. Этот формат файла используется как для первоначальной установки плагинов, так и для обновления плагинов.

Кроме того, этот документ предоставляет краткий обзор того, как router устанавливает плагины, а также политики и рекомендации для разработчиков плагинов.

Базовый формат файла .xpi2p такой же, как у файла i2pupdate.sud (формат, используемый для обновлений router), но установщик позволит пользователю установить дополнение, даже если ключ подписавшего еще неизвестен.

Начиная с версии 0.9.15, поддерживается формат файлов SU3, который является предпочтительным. Этот формат обеспечивает более сильные ключи подписи.

> **Примечание:** Мы больше не рекомендуем распространять плагины в формате xpi2p. Используйте формат su3.

Стандартная структура каталогов позволит пользователям устанавливать следующие типы дополнений:

- Веб-приложения консоли
- Новый eepsite с cgi-bin, веб-приложениями
- Темы консоли
- Переводы консоли
- Java программы
- Java программы в отдельной JVM
- Любой shell скрипт или программа

Плагин устанавливает все свои файлы в `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` в Windows). Установщик предотвратит установку в любое другое место, хотя плагин может получить доступ к библиотекам в других местах во время работы.

Это следует рассматривать только как способ упростить установку, удаление и обновление, а также уменьшить основные конфликты между плагинами.

Однако когда плагин запущен, модель безопасности практически отсутствует. Плагин работает в той же JVM и с теми же разрешениями, что и router, и имеет полный доступ к файловой системе, router'у, выполнению внешних программ и т.д.

## Подробности

foo.xpi2p — это файл подписанного обновления (sud), содержащий следующее:

Стандартный заголовок .sud, добавленный к zip-файлу, содержащий следующее:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Zip-файл, содержащий следующее:

### файл plugin.config

Этот файл обязателен. Это стандартный конфигурационный файл I2P, содержащий следующие свойства:

#### Обязательные свойства

Следующие четыре свойства являются обязательными. Первые три должны быть идентичны тем, что указаны в установленном плагине для плагина обновления.

-   **name** - Будет установлен в директорию с этим именем. Для нативных плагинов вы можете захотеть использовать отдельные имена в разных пакетах - например, foo-windows и foo-linux.
-   **key** - Публичный ключ DSA как 172 символа B64, заканчивающиеся на '='. Опустите для формата SU3.
-   **signer** - рекомендуется yourname@mail.i2p
-   **version** - Должна быть в формате, который может разобрать VersionComparator, например 1.2.3-4. Максимум 16 байт (должна совпадать с версией sud). Допустимые разделители номеров: '.', '-' и '_'. Это значение должно быть больше того, что указано в установленном плагине для обновления плагина.

#### Свойства отображения

Значения следующих свойств отображаются на странице /configplugins в консоли router'а, если они присутствуют:

-   **date** - Java time - long int
-   **author** - рекомендуется `yourname@mail.i2p`
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - Проверка обновлений будет проверять байты 41-56 по этому URL, чтобы определить, доступна ли новая версия. Начиная с версии 1.7.0 (0.9.53), можно использовать переменные `$OS` и `$ARCH` в URL. Не рекомендуется. Не используйте, если вы ранее не распространяли плагины в формате xpi2p.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - Местоположение файла обновления в формате su3, начиная с версии 0.9.15. Начиная с версии 1.7.0 (0.9.53), можно использовать переменные `$OS` и `$ARCH` в URL.
-   **description** - на английском языке
-   **description_xx** - для языка xx
-   **license** - Лицензия плагина
-   **disableStop=true** - По умолчанию false. Если true, кнопка остановки не будет показана. Используйте это, если нет веб-приложений и клиентов с stopargs.

#### Свойства ссылок панели сводки консоли

Следующие свойства используются для добавления ссылки в строку сводки консоли:

-   **consoleLinkName** - будет добавлено в панель сводки
-   **consoleLinkName_xx** - для языка xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - поддерживается начиная с версии 0.7.12-6
-   **consoleLinkTooltip_xx** - язык xx начиная с версии 0.7.12-6

#### Свойства значка консоли

Следующие дополнительные свойства могут использоваться для добавления пользовательской иконки в консоль:

-   **console-icon** - поддерживается с версии 0.9.20. Только для веб-приложений. Путь к изображению 32x32, например /icon.png. С версии 1.7.0 (API 0.9.53), если указан consoleLinkURL, путь относителен к этому URL. Иначе он относителен к имени веб-приложения. Применяется ко всем веб-приложениям в плагине.
-   **icon-code** - поддерживается с версии 0.9.25. Предоставляет иконку консоли для плагинов без веб-ресурсов. B64 строка, полученная вызовом `net.i2p.data.Base64 encode FILE` на файле изображения png 32x32.

#### Свойства установщика

Следующие свойства используются установщиком плагинов:

-   **type** - app/theme/locale/webapp/... (не реализовано, вероятно не необходимо)
-   **min-i2p-version** - Минимальная версия I2P, требуемая этим плагином
-   **max-i2p-version** - Максимальная версия I2P, на которой будет работать этот плагин
-   **min-java-version** - Минимальная версия Java, требуемая этим плагином
-   **min-jetty-version** - поддерживается с версии 0.8.13, используйте 6 для веб-приложений Jetty 6
-   **max-jetty-version** - поддерживается с версии 0.8.13, используйте 5.99999 для веб-приложений Jetty 5
-   **required-platform-OS** - не реализовано - возможно будет только отображаться, но не проверяться
-   **other-requirements** - не реализовано, например python x.y - не проверяется установщиком, просто отображается пользователю
-   **dont-start-at-install=true** - По умолчанию false. Не будет запускать плагин при его установке или обновлении.
-   **router-restart-required=true** - По умолчанию false. Это не перезапускает router или плагин при обновлении, а только информирует пользователя о необходимости перезапуска.
-   **update-only=true** - По умолчанию false. Если true, завершится с ошибкой если установка не существует.
-   **install-only=true** - По умолчанию false. Если true, завершится с ошибкой если установка существует.
-   **min-installed-version** - для обновления поверх, если установка существует
-   **max-installed-version** - для обновления поверх, если установка существует
-   **depends=plugin1,plugin2,plugin3** - не реализовано
-   **depends-version=0.3.4,,5.6.7** - не реализовано

#### Свойства перевода

-   **langs=xx,yy,Klingon,...** - (не реализовано) (yy - это флаг страны)

### Директории и файлы приложения

Каждая из следующих директорий или файлов является необязательной, но что-то должно присутствовать, иначе ничего работать не будет:

**console/**

-   **locale/** - Только jar-файлы, содержащие новые наборы ресурсов (переводы) для приложений в базовой установке I2P. Наборы для этого плагина должны находиться внутри console/webapp/foo.war или lib/foo.jar
-   **themes/** - Новые темы для консоли router. Размещайте каждую тему в отдельной подпапке.
-   **webapps/** - (См. важные заметки ниже о webapps) .war файлы - Они будут запущены во время установки, если не отключены в webapps.config. Имя war не обязательно должно совпадать с именем плагина. Не дублируйте имена war из базовой установки I2P.
-   **webapps.config** - Тот же формат, что и webapps.config router'а. Также используется для указания дополнительных jar-файлов в $PLUGIN/lib/ или $I2P/lib для classpath веб-приложения, с помощью `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Примечание:** До релиза 1.7.0 (API 0.9.53) строка classpath загружалась только если warname совпадало с именем плагина. Начиная с API 0.9.53, настройка classpath будет работать для любого warname.

> **Примечание:** До версии router 0.7.12-9, router искал `plugin.warname.startOnLoad` вместо `webapps.warname.startOnLoad`. Для совместимости со старыми версиями router, плагин, желающий отключить war, должен включать обе строки.

**eepsite/**

(См. важные примечания ниже о eepsites)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - Установщик должен будет выполнить подстановку переменных здесь для установки пути. Расположение и имя этого файла не имеют особого значения, пока оно установлено в clients.config - может быть удобнее разместить его на один уровень выше отсюда.

**lib/**

Поместите любые jar-файлы здесь и укажите их в строке classpath в console/webapps.config и/или clients.config

### файл clients.config

Этот файл является необязательным и указывает клиенты, которые будут запущены при старте плагина. Он использует тот же формат, что и файл clients.config роутера. См. спецификацию конфигурационного файла clients.config для получения дополнительной информации о формате и важных деталях о том, как клиенты запускаются и останавливаются.

-   **clientApp.0.stopargs=foo bar stop baz** - Если присутствует, класс будет вызван с этими аргументами для остановки клиента. Все задачи остановки вызываются с нулевой задержкой. Примечание: router не может определить, запущены ли ваши неуправляемые клиенты или нет.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Если присутствует, класс будет вызван с этими аргументами непосредственно перед удалением $PLUGIN. Все задачи удаления вызываются с нулевой задержкой.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - Исполнитель плагина выполнит подстановку переменных в строках args и stopargs следующим образом:
    -   `$I2P` - базовая директория установки I2P
    -   `$CONFIG` - директория конфигурации I2P (обычно ~/.i2p)
    -   `$PLUGIN` - директория установки этого плагина (обычно ~/.i2p/plugins/appname)
    -   `$OS` - операционная система хоста в форме `windows`, `linux`, `mac`
    -   `$ARCH` - архитектура хоста в форме `386`, `amd64`, `arm64`

(См. важные примечания ниже о запуске shell-скриптов или внешних программ)

## Задачи установщика плагинов

Здесь перечислено, что происходит при установке плагина в I2P.

1.  Файл .xpi2p загружается.
2.  Подпись .sud проверяется относительно сохраненных ключей. Начиная с версии 0.9.14.1, если соответствующий ключ не найден, установка завершается неудачно, если только не установлено расширенное свойство router для разрешения всех ключей.
3.  Проверить целостность zip-файла.
4.  Извлечь файл plugin.config.
5.  Проверить версию I2P, чтобы убедиться, что плагин будет работать.
6.  Проверить, что webapps не дублируют существующие приложения $I2P.
7.  Остановить существующий плагин (если присутствует).
8.  Проверить, что каталог установки еще не существует, если update=false, или запросить перезапись.
9.  Проверить, что каталог установки существует, если update=true, или запросить создание.
10. Распаковать плагин в appDir/plugins/name/
11. Добавить плагин в plugins.config

## Задачи для начинающих разработчиков плагинов

Здесь перечислено, что происходит при запуске плагинов. Сначала проверяется plugins.config, чтобы узнать, какие плагины нужно запустить. Для каждого плагина:

1.  Проверить clients.config, и загрузить и запустить каждый элемент (добавить настроенные jar-файлы в classpath).
2.  Проверить console/webapp и console/webapp.config. Загрузить и запустить требуемые элементы (добавить настроенные jar-файлы в classpath).
3.  Добавить console/locale/foo.jar в classpath переводов, если присутствует.
4.  Добавить console/theme в путь поиска тем, если присутствует.
5.  Добавить ссылку на панель сводки.

## Заметки о веб-приложении консоли

Консольные веб-приложения с фоновыми задачами должны реализовывать ServletContextListener (см. примеры seedless или i2pbote), или переопределять destroy() в сервлете, чтобы их можно было остановить. Начиная с версии router 0.7.12-3, консольные веб-приложения всегда будут останавливаться перед перезапуском, поэтому вам не нужно беспокоиться о множественных экземплярах, при условии, что вы это делаете. Также начиная с версии router 0.7.12-3, консольные веб-приложения будут останавливаться при выключении router.

Не включайте библиотечные jar-файлы в веб-приложение; поместите их в lib/ и укажите classpath в webapps.config. Тогда вы сможете создать отдельные плагины для установки и обновления, где плагин обновления не будет содержать библиотечные jar-файлы.

Никогда не включайте Jetty, Tomcat или servlet jar-файлы в ваш плагин, так как они могут конфликтовать с версией в установке I2P. Будьте осторожны, чтобы не включать конфликтующие библиотеки.

Не включайте файлы .java или .jsp; иначе Jetty перекомпилирует их при установке, что увеличит время запуска. Хотя большинство установок I2P имеют рабочий компилятор Java и JSP в classpath, это не гарантировано и может работать не во всех случаях.

На данный момент веб-приложение, которому необходимо добавить файлы classpath в $PLUGIN, должно иметь то же имя, что и плагин. Например, веб-приложение в плагине foo должно называться foo.war.

Хотя I2P поддерживает Servlet 3.0 начиная с версии 0.9.30, он НЕ поддерживает сканирование аннотаций для @WebContent (нет файла web.xml). Потребовались бы несколько дополнительных jar-файлов для выполнения, и мы не предоставляем их в стандартной установке. Свяжитесь с разработчиками I2P, если вам нужна поддержка @WebContent.

## Заметки о eepsite

Не ясно, как установить плагин на существующий eepsite. У router'а нет подключения к eepsite, он может работать или не работать, и их может быть несколько. Лучше запустить свой собственный экземпляр Jetty и экземпляр I2PTunnel для совершенно нового eepsite.

Он может создать новый I2PTunnel (примерно так же, как это делает CLI i2ptunnel), но он, конечно, не появится в графическом интерфейсе i2ptunnel, поскольку это другой экземпляр. Но это нормально. Тогда вы можете запускать и останавливать i2ptunnel и jetty вместе.

Так что не рассчитывайте на то, что router автоматически объединит это с каким-то существующим eepsite. Скорее всего, этого не произойдет. Запустите новый I2PTunnel и Jetty из clients.config. Лучшими примерами этого являются плагины zzzot и pebble.

Как внедрить подстановку путей в jetty.xml? См. примеры в плагинах zzzot и pebble.

## Примечания к запуску/остановке клиента

Начиная с версии 0.9.4, router поддерживает "управляемые" клиенты плагинов. Управляемые клиенты плагинов создаются и запускаются `ClientAppManager`. ClientAppManager поддерживает ссылку на клиента и получает обновления о состоянии клиента. Управляемые клиенты плагинов предпочтительны, поскольку гораздо проще реализовать отслеживание состояния и запуск/остановку клиента. Также гораздо проще избежать статических ссылок в коде клиента, которые могут привести к чрезмерному использованию памяти после остановки клиента. Смотрите спецификацию конфигурационного файла clients.config для получения дополнительной информации о написании управляемого клиента.

Для "неуправляемых" клиентов плагинов router не имеет способа отслеживать состояние клиентов, запущенных через clients.config. Автор плагина должен корректно обрабатывать множественные вызовы запуска или остановки, если это вообще возможно, ведя статичную таблицу состояний или используя PID-файлы и т.д. Избегайте логирования или исключений при множественных запусках или остановках. Это также касается вызова остановки без предварительного запуска. Начиная с версии router 0.7.12-3, плагины будут остановлены при выключении router, что означает, что все клиенты с stopargs в clients.config будут вызваны, независимо от того, были ли они запущены ранее.

## Примечания к Shell-скриптам и внешним программам

Для запуска shell-скриптов или других внешних программ напишите небольшой Java-класс, который проверяет тип ОС, а затем запускает ShellCommand для .bat или .sh файла, который вы предоставляете. Обобщенное решение для этого было добавлено в I2P 1.7.0/0.9.53 — "ShellService", который выполняет отслеживание состояния для одной команды и взаимодействует с ClientAppManager.

Внешние программы не будут остановлены при остановке router, и вторая копия запустится при старте router. Обычно это можно устранить, используя ShellService для отслеживания состояния. Если это не подходит для вашего случая использования, вы можете написать класс-обёртку или shell-скрипт, который выполняет обычное сохранение PID в PID-файле и проверяет его при запуске.

## Другие рекомендации по плагинам

-   См. monotone ветку i2p.scripts или любой из примеров плагинов на странице zzz для shell-скрипта makeplugin.sh. Он автоматизирует большинство задач для генерации ключей, создания su3 файла плагина и верификации. Вы должны включить этот скрипт в процесс сборки вашего плагина.
-   Pack200 для jar и war файлов настоятельно рекомендуется для плагинов, обычно это сжимает плагины на 60-65%. См. любой из примеров плагинов на странице zzz для примера. Распаковка Pack200 поддерживается на роутерах 0.7.11-5 или выше, что по сути охватывает все роутеры, которые вообще поддерживают плагины.
-   Плагины не должны пытаться писать куда-либо в $I2P, поскольку это может быть только для чтения, и в любом случае это не является хорошей практикой.
-   Плагины могут писать в $CONFIG, но рекомендуется хранить файлы только в $PLUGIN. Все файлы в $PLUGIN будут удалены при деинсталляции.
-   $CWD может находиться где угодно; не предполагайте, что он находится в определенном месте, не пытайтесь читать или писать файлы относительно $CWD. Для ShellService это всегда то же самое, что и $PLUGIN.
-   Java программы должны узнавать, где они находятся, с помощью геттеров директорий в I2PAppContext.
-   Директория плагина - это `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, или поместите аргумент $PLUGIN в строку args в clients.config.
-   Все конфигурационные файлы должны быть в UTF-8.
-   Для запуска в отдельной JVM используйте ShellCommand с `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Как альтернатива stopargs в clients.config, Java клиент может зарегистрировать shutdown hook с помощью `I2PAppContext.addShutdownTask()`. Но это не остановит плагин при обновлении, поэтому рекомендуется stopargs. Также установите все созданные потоки в daemon режим.
-   Не включайте классы, дублирующие те, что есть в стандартной установке. При необходимости расширяйте классы.
-   Остерегайтесь различных определений classpath в wrapper.config между старыми и новыми установками.
-   Клиенты будут отклонять дублирующиеся ключи с разными именами ключей, и дублирующиеся имена ключей с разными ключами, и разные ключи или имена ключей в пакетах обновлений. Защищайте свои ключи. Генерируйте их только один раз.
-   Не изменяйте файл plugin.config во время выполнения, поскольку он будет перезаписан при обновлении. Используйте другой конфигурационный файл в директории для хранения конфигурации времени выполнения.
-   В общем случае плагины не должны требовать доступа к $I2P/lib/router.jar. Не обращайтесь к классам роутера, если только вы не делаете что-то особенное.
-   Поскольку каждая версия должна быть выше предыдущей, вы можете улучшить свой скрипт сборки, добавив номер сборки в конец версии.
-   Плагины никогда не должны вызывать `System.exit()`.
-   Пожалуйста, соблюдайте лицензии, выполняя требования лицензий для любого программного обеспечения, которое вы включаете.
-   Роутер устанавливает часовой пояс JVM в UTC. Если плагину нужно знать фактический часовой пояс пользователя, он хранится роутером в свойстве I2PAppContext `i2p.systemTimeZone`.

## Пути к классам

Следующие jar-файлы в $I2P/lib можно считать находящимися в стандартном classpath для всех установок I2P, независимо от того, насколько старой или новой является первоначальная установка.

Все последние публичные API в i2p jar-файлах имеют номер версии выпуска, указанный в Javadocs. Если вашему плагину требуются определенные функции, доступные только в последних версиях, обязательно установите свойства min-i2p-version, min-jetty-version или оба в файле plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Следующие jar-файлы в $I2P/lib можно считать присутствующими во всех установках I2P, независимо от того, насколько старой или новой была исходная установка, но они не обязательно находятся в classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Всё, что не указано выше, может отсутствовать в classpath у всех пользователей, даже если у вас это есть в classpath в ВАШЕЙ версии i2p. Если вам нужен какой-либо jar-файл, не указанный выше, добавьте $I2P/lib/foo.jar в classpath, указанный в clients.config или webapps.config в вашем плагине.

Ранее запись classpath, указанная в clients.config, добавлялась в classpath для всей JVM. Однако начиная с версии 0.7.13-3 это было исправлено с использованием загрузчиков классов, и теперь, как изначально задумывалось, указанный classpath в clients.config предназначен только для конкретного потока. Поэтому указывайте полный необходимый classpath для каждого клиента.

## Примечания по версии Java

I2P требует Java 7 начиная с релиза 0.9.24 (январь 2016). I2P требует Java 6 начиная с релиза 0.9.12 (апрель 2014). Все пользователи I2P на последнем релизе должны использовать JVM версии 1.7 (7.0).

Если ваш плагин **не требует 1.7**:

-   Убедитесь, что все файлы java и jsp компилируются с source="1.6" target="1.6".
-   Убедитесь, что все включенные библиотечные jar-файлы также предназначены для версии 1.6 или ниже.

Если ваш плагин **требует версию 1.7**:

-   Отметьте это на вашей странице загрузки.
-   Добавьте min-java-version=1.7 в ваш plugin.config

В любом случае, вы **должны** установить bootclasspath при компиляции с Java 8, чтобы предотвратить сбои во время выполнения.

## JVM падает при обновлении

Примечание - сейчас всё это должно быть исправлено.

JVM имеет тенденцию к сбою при обновлении jar-файлов в плагине, если этот плагин работал с момента запуска I2P (даже если плагин был позже остановлен). Возможно, это было исправлено с реализацией загрузчика классов в версии 0.7.13-3, но может быть и нет.

Самый безопасный способ — проектировать плагин с jar внутри war (для веб-приложения), либо требовать перезапуск после обновления, либо не обновлять jar-файлы в вашем плагине.

Из-за особенностей работы загрузчиков классов внутри веб-приложения, _возможно_ безопасно использовать внешние jar-файлы, если вы укажете classpath в webapps.config. Требуется дополнительное тестирование для проверки этого. Не указывайте classpath с 'фальшивым' клиентом в clients.config, если он нужен только для веб-приложения - используйте вместо этого webapps.config.

Наименее безопасными и, по-видимому, источником большинства сбоев являются клиенты с plugin jar-файлами, указанными в classpath в clients.config.

Ничего из этого не должно быть проблемой при первоначальной установке - вам никогда не потребуется перезапуск при первоначальной установке плагина.

## Справочники

-   [Спецификация файла конфигурации](/docs/specs/configuration)
-   [Криптография DSA](/docs/specs/cryptography#DSA)
-   [Спецификация обновлений](/docs/specs/updates)
