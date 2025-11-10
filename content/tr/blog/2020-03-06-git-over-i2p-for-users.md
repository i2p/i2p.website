---
title: "Kullanıcılar için I2P üzerinden Git"
date: 2020-03-06
author: "idk"
description: "I2P üzerinden Git"
categories: ["development"]
---

I2P Tunnel üzerinden git erişimini ayarlama kılavuzu. Bu tunnel, I2P üzerinde tek bir git hizmetine erişim noktanız olarak görev yapacaktır. Bu, I2P’yi monotone’den Git’e geçirmeye yönelik genel çabanın bir parçasıdır.

## Her şeyden önce: Hizmetin kamuya sunduğu yetenekleri bilin

Git hizmetinin nasıl yapılandırıldığına bağlı olarak, tüm hizmetleri aynı adreste sunabilir veya sunmayabilir. git.idk.i2p örneğinde, genel bir HTTP URL’si ve Git SSH istemciniz için yapılandıracağınız bir SSH URL’si vardır. Her ikisi de push (gönderme) veya pull (çekme) için kullanılabilir, ancak SSH önerilir.

## İlk olarak: Bir Git hizmetinde bir hesap oluşturun

Depolarınızı uzaktaki bir Git hizmetinde oluşturmak için o hizmette bir kullanıcı hesabı açın. Elbette depoları yerel olarak oluşturup bunları uzaktaki bir Git hizmetine push etmek de mümkündür, ancak çoğu bir hesap gerektirir ve sunucuda depo için bir alan oluşturmanızı ister.

## İkinci olarak: Test etmek için bir proje oluşturun

Kurulum sürecinin çalıştığından emin olmak için, sunucu üzerinden test etmek için bir depo oluşturmak yararlıdır. i2p-hackers/i2p.i2p deposuna gidin ve bu depoyu hesabınıza fork (çatallama) yapın.

## Üçüncü: git istemci tunnel'inizi yapılandırın

Bir sunucuya okuma-yazma erişimi elde etmek için, SSH istemciniz için bir tunnel ayarlamanız gerekir. İhtiyacınız yalnızca salt-okunur HTTP/S klonlama ise, o halde tüm bunları atlayabilir ve git'i önceden yapılandırılmış I2P HTTP Proxy'yi kullanacak şekilde ayarlamak için yalnızca http_proxy ortam değişkenini kullanabilirsiniz. Örneğin:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
SSH erişimi için, http://127.0.0.1:7657/i2ptunnelmgr adresinden "New Tunnel Wizard"ı başlatın ve Git hizmetinin SSH base32 adresine yönlendiren bir client tunnel (istemci ağ tüneli) oluşturun.

## Dördüncü: Klonlamayı deneyin

Artık tunneliniz tamamen ayarlanmış durumda, SSH üzerinden klonlamayı deneyebilirsiniz:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Uzak ucun beklenmedik şekilde bağlantıyı kapattığı bir hatayla karşılaşabilirsiniz. Ne yazık ki git hâlâ resumable cloning (kaldığı yerden devam edebilen klonlama) özelliğini desteklemiyor. Destekleyene kadar, bunu ele almanın birkaç oldukça kolay yolu var. İlki ve en kolayı, shallow depth (sığ derinlik) ile klonlamayı denemektir:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Sığ bir klon oluşturduktan sonra, depo dizinine geçip şunu çalıştırarak kalanını kaldığı yerden devam edilebilir şekilde alabilirsiniz:

```
git fetch --unshallow
```
Bu noktada hâlâ tüm dallara sahip değilsiniz. Şunu çalıştırarak onları alabilirsiniz:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Geliştiriciler için Önerilen İş Akışı

Sürüm kontrolü, doğru kullanıldığında en iyi sonuç verir! Fork-first (çatallamayı önceleyen) ve feature-branch (özellik dalı) iş akışını şiddetle öneriyoruz:

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