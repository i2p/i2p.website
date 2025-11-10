---
title: "I2P kaynak kodunu almak için git bundle (git paket dosyası) kullanımı"
date: 2020-03-18
author: "idk"
description: "I2P kaynak kodunu BitTorrent üzerinden indirin"
categories: ["development"]
---

I2P üzerinden büyük yazılım depolarını klonlamak zor olabilir ve git kullanmak bazen bunu daha da zorlaştırabilir. Neyse ki, bazen bunu kolaylaştırabilir de. Git, bir git deposunu, git'in daha sonra yerel diskinizdeki bir konumdan klonlayabileceği, fetch edebileceği veya içe aktarabileceği bir dosyaya dönüştürmek için kullanılabilen `git bundle` adlı bir komuta sahiptir. Bu yeteneği BitTorrent indirmeleriyle birleştirerek, `git clone` ile ilgili kalan sorunlarımızı çözebiliriz.

## Başlamadan Önce

Bir git bundle oluşturmayı planlıyorsanız, mtn deposunu değil, **git** deposunun tam bir kopyasına halihazırda sahip **olmalısınız**. Bunu github veya git.idk.i2p üzerinden edinebilirsiniz, ancak sığ klon (--depth=1 ile yapılmış bir klon) *çalışmayacaktır*. Hata vermeden (sessizce) başarısız olur ve bundle gibi görünen bir şey oluşturur, ancak onu klonlamayı denediğinizde başarısız olur. Eğer sadece önceden oluşturulmuş bir git bundle’ı temin ediyorsanız, o zaman bu bölüm sizin için geçerli değildir.

## BitTorrent üzerinden I2P kaynak kodunu indirme

Birinin, sizin için önceden oluşturdukları mevcut bir `git bundle`a karşılık gelen bir torrent dosyası veya magnet bağlantısı sağlaması gerekecek. Bittorrent üzerinden bir bundle edindiğinizde, ondan kullanılabilir bir depo oluşturmak için git kullanmanız gerekecek.

## `git clone` kullanımı

Bir git bundle (Git demeti) üzerinden klonlamak kolaydır, sadece:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
Aşağıdaki hatayı alırsanız, bunun yerine git init ve git fetch komutlarını manuel olarak kullanmayı deneyin:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## `git init` ve `git fetch` kullanımı

İlk olarak, Git deposuna dönüştürmek üzere i2p.i2p adlı bir dizin oluşturun:

```
mkdir i2p.i2p && cd i2p.i2p
```
Ardından, değişiklikleri bu depoya geri alabilmek için boş bir git deposu başlatın:

```
git init
```
Son olarak, depoyu paketten alın:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## bundle uzak deposunu upstream uzak deposuyla değiştirin

Artık bir paketiniz olduğuna göre, uzak depoyu upstream (ana kaynak) depoya ayarlayarak değişiklikleri takip edebilirsiniz:

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Paket Oluşturma

İlk olarak, i2p.i2p deposunun `--unshallow` uygulanmış bir klonunu başarıyla elde edene kadar Kullanıcılar için Git rehberini izleyin. Zaten bir klonunuz varsa, bir torrent paketi (bundle) oluşturmadan önce `git fetch --unshallow` komutunu çalıştırdığınızdan emin olun.

Bunu elde ettikten sonra, basitçe karşılık gelen ant hedefini çalıştırın:

```
ant bundle
```
ve ortaya çıkan paketi I2PSnark indirmeler dizinine kopyalayın. Örneğin:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
Bir-iki dakika içinde I2PSnark torrent'i algılayacaktır. Torrent'i seed etmeye başlamak için "Start" düğmesine tıklayın.
