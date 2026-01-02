---
title: "Хосты Reseed (серверы начальной загрузки)"
description: "Эксплуатация служб ресида и альтернативные методы начальной инициализации"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## О хостах reseed (серверы начальной загрузки сети)

Новым router нужно несколько пиров, чтобы присоединиться к сети I2P. Ресид-серверы предоставляют этот начальный набор через зашифрованные загрузки по HTTPS. Каждый ресид-пакет подписан сервером, что предотвращает подмену со стороны неаутентифицированных сторон. Уже работающие router могут время от времени выполнять ресид, если их набор пиров устаревает.

### Процесс начальной инициализации сети

Когда I2P router запускается впервые или находился офлайн длительное время, ему требуются данные RouterInfo (сведения о router) для подключения к сети. Поскольку у router нет существующих пиров, он не может получить эту информацию внутри самой сети I2P. Механизм reseed (получение стартовых данных из внешних источников) решает эту проблему начальной загрузки, предоставляя файлы RouterInfo с доверенных внешних HTTPS‑серверов.

Процесс reseed (получение начального набора данных сети) доставляет 75–100 файлов RouterInfo в одном криптографически подписанном пакете. Это гарантирует, что новые routers смогут быстро установить соединения, не подвергая их атакам типа «человек посередине», которые могли бы изолировать их в отдельные недоверенные сегменты сети.

### Текущее состояние сети

По состоянию на октябрь 2025 года сеть I2P работает с версией router 2.10.0 (версия API 0.9.67). Протокол reseed (механизм начальной загрузки сети), представленный в версии 0.9.14, остаётся стабильным и неизменным в своей основной функциональности. Сеть поддерживает несколько независимых reseed servers, распределённых по всему миру, чтобы обеспечить доступность и устойчивость к цензуре.

Сервис [checki2p](https://checki2p.com/reseed) отслеживает все I2P reseed-серверы (серверы начальной загрузки пиров) каждые 4 часа, предоставляя проверки статуса и метрики доступности в реальном времени для reseed-инфраструктуры.

## Спецификация формата файла SU3

Формат файла SU3 является основой протокола reseed I2P (первичной загрузки адресной базы), обеспечивая криптографически подписанную доставку контента. Понимание этого формата необходимо для реализации серверов и клиентов reseed.

### Структура файлов

Формат SU3 состоит из трех основных компонентов: заголовка (40+ байт), содержимого (переменной длины) и подписи (длина указана в заголовке).

#### Формат заголовка (минимум — байты 0–39)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Параметры SU3, специфичные для Reseed (сервер начальной раздачи узлов)

Для reseed bundles (пакетов для начальной загрузки сети) файл SU3 должен иметь следующие характеристики:

- **Имя файла**: Должно быть точно `i2pseeds.su3`
- **Тип содержимого** (байт 27): 0x03 (RESEED)
- **Тип файла** (байт 25): 0x00 (ZIP)
- **Тип подписи** (байты 8-9): 0x0006 (RSA-4096-SHA512)
- **Строка версии**: метка времени Unix в ASCII (секунды с начала эпохи, формат date +%s)
- **Идентификатор подписанта**: идентификатор в стиле адреса электронной почты, совпадающий с CN сертификата X.509

#### Параметр запроса идентификатора сети

Начиная с версии 0.9.42, routers добавляют `?netid=2` к reseed-запросам. Это предотвращает соединения между сетями, поскольку тестовые сети используют другие идентификаторы сети. Текущая рабочая сеть I2P использует идентификатор сети 2.

Пример запроса: `https://reseed.example.com/i2pseeds.su3?netid=2`

### Структура содержимого ZIP-архива

Раздел содержимого (после заголовка, перед подписью) содержит стандартный ZIP-архив со следующими требованиями:

- **Сжатие**: Стандартное сжатие ZIP (DEFLATE)
- **Количество файлов**: Обычно 75–100 файлов RouterInfo (метаданные о router)
- **Структура каталога**: Все файлы должны находиться на верхнем уровне (без подкаталогов)
- **Именование файлов**: `routerInfo-{44-character-base64-hash}.dat`
- **Алфавит Base64**: Необходимо использовать модифицированный алфавит Base64 I2P

Алфавит I2P base64 отличается от стандартного base64 использованием `-` и `~` вместо `+` и `/`, чтобы обеспечить совместимость с файловой системой и URL.

### Криптографическая подпись

Подпись покрывает весь файл от байта 0 до конца раздела содержимого. Сама подпись добавляется после содержимого.

#### Алгоритм подписи (RSA-4096-SHA512)

1. Вычислите хэш SHA-512 для данных с 0-го байта до конца содержимого
2. Подпишите хэш с помощью «raw» RSA (без дополнительного хеширования/форматирования; NONEwithRSA в терминологии Java)
3. При необходимости дополните подпись ведущими нулями до 512 байт
4. Добавьте 512-байтовую подпись в конец файла

#### Процесс проверки подписи

Клиенты должны:

1. Прочитать байты 0-11, чтобы определить тип и длину подписи
2. Прочитать весь заголовок, чтобы определить границы содержимого
3. Передавать содержимое потоком, одновременно вычисляя хэш SHA-512
4. Извлечь подпись с конца файла
5. Проверить подпись с использованием открытого ключа RSA-4096 подписанта
6. Отклонить файл, если проверка подписи не удалась

### Модель доверия сертификатов

Ключи подписанта reseed распространяются в виде самоподписанных сертификатов X.509 с ключами RSA-4096. Эти сертификаты входят в состав пакетов I2P router в каталоге `certificates/reseed/`.

Формат сертификата: - **Тип ключа**: RSA-4096 - **Подпись**: Самоподписанная - **Subject CN**: Должно совпадать с Signer ID (идентификатор подписанта) в заголовке SU3 - **Сроки действия**: Клиенты должны обеспечивать соблюдение сроков действия сертификата

## Запуск Reseed-сервера

Эксплуатация reseed-сервиса (службы начальной загрузки сети для новых routers) требует тщательного учета требований безопасности, надежности и разнообразия сети. Большее число независимых reseed-хостов повышает устойчивость и усложняет злоумышленникам или цензорам блокирование присоединения новых routers.

### Технические требования

#### Технические характеристики сервера

- **Операционная система**: Unix/Linux (Ubuntu, Debian, FreeBSD протестированы и рекомендуются)
- **Подключение**: требуется статический IPv4-адрес, IPv6 рекомендуется, но необязателен
- **Процессор**: минимум 2 ядра
- **ОЗУ**: минимум 2 ГБ
- **Трафик**: примерно 15 ГБ в месяц
- **Время работы**: требуется режим 24/7
- **I2P Router**: корректно настроенный I2P router, работающий постоянно

#### Требования к программному обеспечению

- **Java**: JDK 8 или новее (Java 17+ станет обязательной начиная с I2P 2.11.0)
- **Веб-сервер**: nginx или Apache с поддержкой обратного прокси (Lighttpd больше не поддерживается из-за ограничений заголовка X-Forwarded-For)
- **TLS/SSL**: Действительный сертификат TLS (Let's Encrypt, самоподписанный или коммерческий УЦ)
- **Защита от DDoS**: fail2ban или аналог (обязательно, не опционально)
- **Reseed Tools** (ресид — начальная загрузка данных сети): официальные reseed-tools с https://i2pgit.org/idk/reseed-tools

### Требования безопасности

#### Настройка HTTPS/TLS

- **Протокол**: только HTTPS, без резервного перехода на HTTP
- **Версия TLS**: минимум TLS 1.2
- **Наборы шифров**: должны поддерживаться сильные наборы шифров, совместимые с Java 8+
- **CN/SAN сертификата**: должны совпадать с именем хоста в обслуживаемом URL
- **Тип сертификата**: может быть самоподписанным при согласовании с командой разработки или выданным признанным УЦ

#### Управление сертификатами

Сертификаты подписи SU3 (формат пакетов обновления I2P) и сертификаты TLS предназначены для разных целей:

- **Сертификат TLS** (`certificates/ssl/`): Обеспечивает защищённый транспорт по HTTPS
- **Сертификат подписи SU3** (`certificates/reseed/`): Подписывает пакеты reseed (для начальной инициализации сети)

Оба сертификата должны быть предоставлены координатору reseed (начальной загрузки списка узлов) (zzz@mail.i2p) для включения в пакеты router.

#### Защита от DDoS-атак и скрейпинга

Reseed servers (серверы начальной загрузки I2P) сталкиваются с периодическими атаками со стороны ошибочных реализаций, ботнетов и злоумышленников, пытающихся массово выгружать данные из сетевой базы данных. Меры защиты включают:

- **fail2ban**: Требуется для ограничения частоты запросов и смягчения атак
- **Bundle Diversity**: Выдавать разные наборы RouterInfo (информация о router) разным запрашивающим
- **Bundle Consistency**: Выдавать тот же набор при повторных запросах с одного и того же IP в пределах настраиваемого временного окна
- **Ограничения на логирование IP**: Не публиковать логи или IP-адреса (требование политики конфиденциальности)

### Методы реализации

#### Способ 1: Официальные reseed-tools (Рекомендуется)

Каноническая реализация, поддерживаемая проектом I2P. Репозиторий: https://i2pgit.org/idk/reseed-tools

**Установка**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
При первом запуске утилита создаст: - `your-email@mail.i2p.crt` (сертификат для подписи SU3) - `your-email@mail.i2p.pem` (закрытый ключ для подписи SU3) - `your-email@mail.i2p.crl` (список отзыва сертификатов) - файлы сертификата и ключа TLS

**Возможности**: - Автоматическая генерация пакетов SU3 (350 вариантов, по 77 RouterInfo (метаданные router в I2P) в каждом) - Встроенный HTTPS-сервер - Перестроение кэша каждые 9 часов через cron - Поддержка заголовка X-Forwarded-For с флагом `--trustProxy` - Совместимо с конфигурациями обратного прокси

**Развертывание в продакшн-среде**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Метод 2: Реализация на Python (pyseeder)

Альтернативная реализация проекта PurpleI2P: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Метод 3: Развертывание с помощью Docker

Для контейнеризованных окружений существует несколько реализаций, готовых для работы в Docker:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Добавляет onion‑сервис Tor и поддержку IPFS

### Настройка обратного прокси-сервера

#### Конфигурация nginx

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Конфигурация Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Регистрация и координация

Чтобы включить ваш reseed server (сервер начальной загрузки) в официальный пакет I2P:

1. Завершите настройку и тестирование
2. Отправьте оба сертификата (для подписания SU3 и TLS) координатору reseed (первичной загрузки узлов)
3. Контакты: zzz@mail.i2p или zzz@i2pmail.org
4. Присоединитесь к #i2p-dev в IRC2P для координации с другими операторами

### Лучшие операционные практики

#### Мониторинг и логирование

- Включить комбинированный формат журналов Apache/nginx для статистики
- Реализовать ротацию журналов (журналы быстро разрастаются)
- Отслеживать успешность генерации bundle (пакета) и время пересборки
- Отслеживать использование пропускной способности и паттерны запросов
- Никогда не публиковать IP-адреса или подробные журналы доступа

#### График технического обслуживания

- **Каждые 9 часов**: Пересобрать кэш пакетов SU3 (автоматизировано через cron)
- **Еженедельно**: Просматривать журналы на предмет шаблонов атак
- **Ежемесячно**: Обновлять I2P router и reseed-tools (инструменты для начальной загрузки списка пиров)
- **По мере необходимости**: Продлевать TLS-сертификаты (автоматизировать с помощью Let's Encrypt)

#### Выбор порта

- По умолчанию: 8443 (рекомендуется)
- Альтернатива: любой порт в диапазоне 1024-49151
- Порт 443: требует прав root или проброса портов (рекомендуется перенаправление через iptables)

Пример проброса портов:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Альтернативные методы Reseed (первоначальная загрузка данных для netDb)

Другие варианты начальной инициализации помогают пользователям, находящимся в сетях с ограничениями:

### Reseed (первичная загрузка узлов сети) из файла

Начиная с версии 0.9.16, файловый ресидинг позволяет пользователям вручную загружать пакеты с RouterInfo (запись о router в netDb). Этот метод особенно полезен для пользователей в регионах с цензурой, где HTTPS-ресид-серверы заблокированы.

**Процесс**: 1. Доверенный контакт создает пакет SU3, используя свой router 2. Пакет передается по электронной почте, через USB-накопитель или другим внеполосным каналом связи 3. Пользователь помещает `i2pseeds.su3` в каталог конфигурации I2P 4. При перезапуске router автоматически обнаруживает и обрабатывает пакет

**Документация**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Сценарии использования**: - Пользователи за национальными брандмауэрами, блокирующими reseed servers (ресид-серверы) - Изолированные сети, которым требуется ручной bootstrap (ручная инициализация) - Среды тестирования и разработки

### Ресидинг через Cloudflare

Маршрутизация reseed-трафика (процесс начальной загрузки списка узлов I2P) через CDN Cloudflare предоставляет операторам в регионах с жесткой цензурой ряд преимуществ.

**Преимущества**: - IP-адрес origin-сервера (исходного сервера) скрыт от клиентов - Защита от DDoS через инфраструктуру Cloudflare - Географическое распределение нагрузки за счет edge caching (кеширования на периферии сети) - Улучшенная производительность для клиентов по всему миру

**Требования к реализации**: - `--trustProxy` флаг включён в reseed-tools - Прокси Cloudflare включён для записи DNS - Корректная обработка заголовка X-Forwarded-For

**Важные замечания**: - Действуют ограничения Cloudflare на порты (нужно использовать поддерживаемые порты) - Для обеспечения консистентности bundle (набор) для одного и того же клиента требуется поддержка X-Forwarded-For - Конфигурация SSL/TLS управляется Cloudflare

**Документация**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Стратегии устойчивости к цензуре

Исследование Нгуен Фонга Хоанга (USENIX FOCI 2019) выявляет дополнительные методы начальной загрузки для сетей, подвергающихся цензуре:

#### Поставщики облачного хранилища

- **Box, Dropbox, Google Drive, OneDrive**: Размещать файлы SU3 (формат файла обновлений I2P) через публичные ссылки
- **Преимущество**: Сложно заблокировать, не нарушив работу легитимных сервисов
- **Ограничение**: Требует ручного распространения URL среди пользователей

#### Распространение через IPFS

- Размещать пакеты reseed (начальная загрузка списка узлов I2P) в InterPlanetary File System (IPFS)
- Хранилище с адресацией по содержимому предотвращает подмену данных
- Устойчиво к попыткам принудительного удаления

#### Скрытые сервисы Tor

- Reseed servers (серверы начальной загрузки) доступны через адреса .onion
- Устойчиво к блокировке по IP-адресам
- Требуется клиент Tor на системе пользователя

**Исследовательская документация**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Страны, где известно о блокировке I2P

По состоянию на 2025 год подтверждено, что следующие страны блокируют ресид-серверы I2P: - Китай - Иран - Оман - Катар - Кувейт

Пользователям в этих регионах следует использовать альтернативные методы bootstrap (первичной инициализации сети) или устойчивые к цензуре стратегии reseeding (получения первоначальных пиров).

## Подробности протокола для реализаторов

### Спецификация запроса Reseed (первичная загрузка списка узлов)

#### Поведение клиента

1. **Выбор сервера**: Router хранит жестко заданный список URL reseed (первичная загрузка данных о сети)
2. **Случайный выбор**: Клиент случайным образом выбирает сервер из доступного списка
3. **Формат запроса**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Должен имитировать распространенные браузеры (например, "Wget/1.11.4")
5. **Логика повторных попыток**: Если запрос SU3 завершается неудачей, перейти к разбору индексной страницы
6. **Проверка сертификата**: Проверить сертификат TLS по системному хранилищу доверенных сертификатов
7. **Проверка подписи SU3**: Проверить подпись по известным сертификатам reseed

#### Поведение сервера

1. **Выбор набора**: Выбрать псевдослучайное подмножество RouterInfos из netDb
2. **Отслеживание клиентов**: Идентифицировать запросы по исходному IP-адресу (с учетом X-Forwarded-For)
3. **Согласованность набора**: Возвращать один и тот же набор для повторных запросов в пределах временного окна (обычно 8–12 часов)
4. **Разнообразие наборов**: Возвращать разные наборы разным клиентам для повышения разнообразия сети
5. **Content-Type**: `application/octet-stream` или `application/x-i2p-reseed`

### Формат файла RouterInfo

Каждый файл `.dat` в пакете reseed содержит структуру RouterInfo:

**Именование файлов**: `routerInfo-{base64-hash}.dat` - Хэш состоит из 44 символов, используется алфавит I2P base64 - Пример: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Содержимое файла**: - RouterIdentity (идентификатор router; хэш router, ключ шифрования, ключ подписи) - Временная метка публикации - Адреса router (IP, порт, тип транспорта) - Возможности и параметры router - Подпись, охватывающая все приведённые выше данные

### Требования к разнообразию сети

Чтобы предотвратить централизацию сети и обеспечить обнаружение Sybil-атак (атак Сивиллы):

- **Никаких полных дампов NetDb**: Никогда не выдавать все RouterInfos одному клиенту
- **Случайная выборка**: Каждый пакет содержит различное подмножество доступных пиров
- **Минимальный размер пакета**: 75 RouterInfos (увеличено с изначальных 50)
- **Максимальный размер пакета**: 100 RouterInfos
- **Актуальность**: RouterInfos должны быть свежими (в течение 24 часов после генерации)

### Особенности IPv6

**Текущий статус** (2025): - Несколько ресид-серверов не отвечают по IPv6 - Клиентам следует предпочитать или принудительно использовать IPv4 ради надежности - Поддержка IPv6 рекомендуется для новых развертываний, но не критична

**Примечание по реализации**: При настройке серверов с двойным стеком убедитесь, что оба адреса прослушивания IPv4 и IPv6 работают корректно, или отключите IPv6, если обеспечить его корректную поддержку невозможно.

## Соображения безопасности

### Модель угроз

Протокол reseed защищает от:

1. **Атаки «человек посередине»**: Подписи RSA-4096 предотвращают подмену пакетов
2. **Разделение сети**: Несколько независимых reseed-серверов исключают единую точку контроля
3. **Атаки Сивиллы**: Разнообразие пакетов ограничивает возможности атакующего изолировать пользователей
4. **Цензура**: Несколько серверов и альтернативные методы обеспечивают избыточность

Протокол reseed (первичная загрузка списка узлов) НЕ защищает от:

1. **Скомпрометированные reseed-серверы (процедура начальной загрузки сети)**: если атакующий контролирует закрытые ключи сертификатов reseed
2. **Полная блокировка сети**: если в регионе заблокированы все методы reseed
3. **Долгосрочное наблюдение**: запросы reseed раскрывают IP-адрес, пытающийся присоединиться к I2P

### Управление сертификатами

**Безопасность приватных ключей**: - Храните ключи подписи SU3 офлайн, когда они не используются - Используйте надежные пароли для шифрования ключей - Поддерживайте защищенные резервные копии ключей и сертификатов - Рассмотрите hardware security modules (HSMs; аппаратные модули безопасности) для критически важных развертываний

**Отзыв сертификатов**: - Списки отзыва сертификатов (CRLs) распространяются через новостную ленту - Скомпрометированные сертификаты могут быть отозваны координатором - Routers автоматически обновляют CRLs вместе с обновлениями ПО

### Смягчение атак

**Защита от DDoS**: - правила fail2ban при чрезмерном количестве запросов - ограничение частоты запросов на уровне веб-сервера - лимиты соединений на один IP-адрес - Cloudflare или аналогичный CDN в качестве дополнительного слоя защиты

**Предотвращение скрейпинга**: - Разные пакеты для каждого запрашивающего IP-адреса - Кэширование пакетов по времени для каждого IP-адреса - Логирование шаблонов, указывающих на попытки скрейпинга - Координация с другими операторами по обнаруженным атакам

## Тестирование и валидация

### Тестирование вашего Reseed‑сервера (сервер начальной загрузки сети I2P)

#### Метод 1: Чистая установка Router

1. Установите I2P на чистую систему
2. Добавьте свой URL для reseed (процедура начальной загрузки узлов сети) в конфигурацию
3. Удалите или отключите другие URL для reseed
4. Запустите router и следите за журналами на предмет успешного reseed
5. Проверьте подключение к сети в течение 5–10 минут

Ожидаемый вывод журнала:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Метод 2: Ручная проверка SU3

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Метод 3: мониторинг checki2p

Сервис по адресу https://checki2p.com/reseed выполняет автоматические проверки каждые 4 часа всех зарегистрированных reseed-серверов I2P (серверы начальной загрузки). Это обеспечивает:

- Мониторинг доступности
- Метрики времени отклика
- Проверка сертификата TLS
- Проверка подписи SU3
- Исторические данные о времени безотказной работы

Как только ваш reseed (сервер начальной раздачи данных о маршрутизаторах I2P) будет зарегистрирован в проекте I2P, он автоматически появится на checki2p в течение 24 часов.

### Устранение распространённых неполадок

**Проблема**: "Unable to read signing key" при первом запуске - **Решение**: Это ожидаемо. Ответьте 'y', чтобы сгенерировать новые ключи.

**Проблема**: Router не удаётся проверить подпись - **Причина**: Сертификат отсутствует в хранилище доверенных сертификатов router - **Решение**: Поместите сертификат в каталог `~/.i2p/certificates/reseed/`

**Проблема**: Один и тот же бандл выдаётся разным клиентам - **Причина**: заголовок X-Forwarded-For передаётся некорректно - **Решение**: включите `--trustProxy` и настройте заголовки обратного прокси

**Проблема**: ошибки «Connection refused» - **Причина**: порт недоступен из Интернета - **Решение**: проверьте правила брандмауэра, убедитесь в корректной настройке проброса портов

**Проблема**: Высокая загрузка процессора при пересборке бандла - **Причина**: Нормальное поведение при генерации 350+ вариантов SU3 (формат подписанных обновлений I2P) - **Решение**: Обеспечьте достаточные ресурсы процессора, рассмотрите снижение частоты пересборки

## Справочная информация

### Официальная документация

- **Руководство для участников Reseed (сервер начальной загрузки сети I2P)**: /guides/creating-and-running-an-i2p-reseed-server/
- **Требования политики Reseed**: /guides/reseed-policy/
- **Спецификация SU3**: /docs/specs/updates/
- **Репозиторий инструментов Reseed**: https://i2pgit.org/idk/reseed-tools
- **Документация по инструментам Reseed**: https://eyedeekay.github.io/reseed-tools/

### Альтернативные реализации

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder (сервер начальной загрузки узлов)**: https://github.com/torbjo/i2p-reseeder

### Ресурсы сообщества

- **Форум I2P**: https://i2pforum.net/
- **Репозиторий Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev на IRC2P
- **Мониторинг статуса**: https://checki2p.com/reseed

### История версий

- **0.9.14** (2014): Введён формат SU3 для reseed (первичная загрузка пиров)
- **0.9.16** (2014): Добавлен reseeding на основе файлов
- **0.9.42** (2019): Параметр запроса Network ID стал обязательным
- **2.0.0** (2022): Введён транспортный протокол SSU2
- **2.4.0** (2024): Изоляция NetDB и улучшения безопасности
- **2.6.0** (2024): Подключения I2P-over-Tor заблокированы
- **2.10.0** (2025): Текущий стабильный релиз (по состоянию на сентябрь 2025)

### Справочник по типам подписей

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Стандарт Reseed**: Тип 6 (RSA-SHA512-4096) требуется для пакетов reseed (первичная загрузка).

## Благодарность

Спасибо всем операторам reseed (сервер начальной загрузки узлов сети) за поддержание доступности и устойчивости сети. Особая признательность следующим участникам и проектам:

- **zzz**: Многолетний разработчик I2P и координатор reseed (серверов начальной загрузки сети I2P)
- **idk**: Текущий мейнтейнер reseed-tools и менеджер релизов
- **Nguyen Phong Hoang**: Исследования стратегий reseeding, устойчивых к цензуре
- **PurpleI2P Team**: Альтернативные реализации I2P и инструменты
- **checki2p**: Автоматический сервис мониторинга инфраструктуры reseed

Децентрализованная инфраструктура reseed (механизм первоначального получения списка узлов сети) сети I2P является результатом совместных усилий десятков операторов по всему миру, гарантируя, что новые пользователи всегда могут найти способ присоединиться к сети независимо от локальной цензуры или технических барьеров.
