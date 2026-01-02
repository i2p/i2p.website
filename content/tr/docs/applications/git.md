---
title: "I2P üzerinden Git"
description: "Git istemcilerini i2pgit.org gibi I2P üzerinde barındırılan servislere bağlama"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

I2P içinde depoları klonlamak ve göndermek, zaten bildiğiniz Git komutlarını kullanır—istemciniz sadece TCP/IP yerine I2P tunnel'ları üzerinden bağlanır. Bu kılavuz, hesap oluşturma, tunnel yapılandırması ve yavaş bağlantılarla başa çıkma konularında size yol gösterir.

> **Hızlı başlangıç:** Salt okunur erişim HTTP proxy üzerinden çalışır: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. SSH okuma/yazma erişimi için aşağıdaki adımları izleyin.

## 1. Bir Hesap Oluşturun

Bir I2P Git servisi seçin ve kayıt olun:

- I2P içinde: `http://git.idk.i2p`
- Clearnet yansısı: `https://i2pgit.org`

Kayıt manuel onay gerektirebilir; talimatlar için açılış sayfasını kontrol edin. Onaylandıktan sonra, test edebileceğiniz bir şey elde etmek için bir depoyu fork'layın veya oluşturun.

## 2. Bir I2PTunnel İstemcisi Yapılandırma (SSH)

1. Router konsolu → **I2PTunnel**'ı açın ve yeni bir **Client** tunnel ekleyin.
2. Hizmetin destination'ını girin (Base32 veya Base64). `git.idk.i2p` için hem HTTP hem de SSH destination'larını proje ana sayfasında bulabilirsiniz.
3. Yerel bir port seçin (örneğin `localhost:7442`).
4. Tunnel'ı sık kullanmayı planlıyorsanız otomatik başlatmayı etkinleştirin.

UI, yeni tüneli onaylayacak ve durumunu gösterecektir. Tünel çalıştığında, SSH istemcileri seçilen portta `127.0.0.1` adresine bağlanabilir.

## 3. SSH ile Klonlama

Tunnel portunu `GIT_SSH_COMMAND` veya bir SSH yapılandırma bölümü ile kullanın:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
İlk deneme başarısız olursa (tüneller yavaş olabilir), sığ klonlamayı deneyin:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Git'i tüm dalları getirmek için yapılandırın:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Performans İpuçları

- Dayanıklılığı artırmak için tunnel editöründe bir veya iki yedek tunnel ekleyin.
- Test veya düşük riskli repolar için tunnel uzunluğunu 1 hop'a düşürebilirsiniz, ancak anonimlik ödünleşiminin farkında olun.
- `GIT_SSH_COMMAND` komutunu ortamınızda tutun veya `~/.ssh/config` dosyasına bir giriş ekleyin:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Ardından `git clone git@git.i2p:namespace/project.git` kullanarak klonlayın.

## 4. İş Akışı Önerileri

GitLab/GitHub'da yaygın olan fork-and-branch iş akışını benimseyin:

1. Bir upstream uzak depo ayarlayın: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. `master` dalınızı senkronize tutun: `git pull upstream master`
3. Değişiklikler için özellik dalları oluşturun: `git checkout -b feature/new-thing`
4. Dalları kendi fork'unuza gönderin: `git push origin feature/new-thing`
5. Bir birleştirme isteği gönderin, ardından fork'unuzun master dalını upstream'den hızlı ileri sarın.

## 5. Gizlilik Hatırlatıcıları

- Git, commit zaman damgalarını yerel saat diliminizde saklar. UTC zaman damgalarını zorlamak için:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Gizlilik önemli olduğunda `git commit` yerine `git utccommit` kullanın.

- Anonimlik bir endişe kaynağıysa, commit mesajlarına veya depo meta verilerine clearnet URL'leri veya IP adresleri gömmekten kaçının.

## 6. Sorun Giderme

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
Gelişmiş senaryolar için (harici repoları yansıtma, paket oluşturma), ilgili kılavuzlara bakın: [Git bundle iş akışları](/docs/applications/git-bundle/) ve [GitLab'ı I2P üzerinden barındırma](/docs/guides/gitlab/).
