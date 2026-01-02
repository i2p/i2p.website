---
title: "Git přes I2P"
description: "Připojení Git klientů k službám hostovaným na I2P, jako je i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Klonování a nahrávání repozitářů v rámci I2P používá stejné příkazy Gitu, které již znáte—váš klient se jednoduše připojuje přes I2P tunely místo TCP/IP. Tento návod vás provede vytvořením účtu, konfigurací tunelů a řešením pomalých připojení.

> **Rychlý start:** Přístup pouze pro čtení funguje přes HTTP proxy: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Pro SSH přístup pro čtení/zápis postupujte podle níže uvedených kroků.

## 1. Vytvořit účet

Vyberte si I2P Git službu a zaregistrujte se:

- Uvnitř I2P: `http://git.idk.i2p`
- Clearnet zrcadlo: `https://i2pgit.org`

Registrace může vyžadovat manuální schválení; zkontrolujte úvodní stránku pro instrukce. Po schválení vytvořte fork nebo vytvořte repozitář, abyste měli něco k testování.

## 2. Konfigurace I2PTunnel klienta (SSH)

1. Otevřete konzoli routeru → **I2PTunnel** a přidejte nový **Client** tunel.
2. Zadejte cílovou adresu služby (Base32 nebo Base64). Pro `git.idk.i2p` najdete HTTP i SSH cílové adresy na domovské stránce projektu.
3. Zvolte lokální port (například `localhost:7442`).
4. Povolte automatické spuštění, pokud plánujete tunel používat často.

UI potvrdí nový tunel a zobrazí jeho stav. Když běží, SSH klienti se mohou připojit k `127.0.0.1` na zvoleném portu.

## 3. Klonování přes SSH

Použijte port tunelu s `GIT_SSH_COMMAND` nebo konfigurační stanzou SSH:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Pokud první pokus selže (tunely mohou být pomalé), zkuste mělké klonování:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Nakonfigurujte Git pro stažení všech větví:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Tipy pro výkon

- Přidejte jeden nebo dva záložní tunnely v editoru tunnelů pro zlepšení odolnosti.
- Pro testování nebo repozitáře s nízkým rizikem můžete snížit délku tunnelu na 1 hop, ale mějte na paměti kompromis v anonymitě.
- Udržujte `GIT_SSH_COMMAND` ve svém prostředí nebo přidejte záznam do `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Poté naklonujte pomocí `git clone git@git.i2p:namespace/project.git`.

## 4. Návrhy pracovních postupů

Použijte pracovní postup fork-and-branch běžný na GitLabu/GitHubu:

1. Nastavte upstream remote: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Udržujte svůj `master` synchronizovaný: `git pull upstream master`
3. Vytvářejte feature větve pro změny: `git checkout -b feature/new-thing`
4. Pushujte větve do svého forku: `git push origin feature/new-thing`
5. Odešlete merge request a poté proveďte fast-forward master větve vašeho forku z upstream.

## 5. Připomínky o soukromí

- Git ukládá časové značky commitů v místním časovém pásmu. Pro vynucení UTC časových značek:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Použijte `git utccommit` místo `git commit`, když záleží na soukromí.

- Vyhněte se vkládání clearnet URL nebo IP adres do commit zpráv nebo metadat repozitáře, pokud je anonymita důležitá.

## 6. Řešení problémů

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
Pro pokročilé scénáře (zrcadlení externích repozitářů, seedování bundlů) viz doprovodné návody: [Pracovní postupy Git bundle](/docs/applications/git-bundle/) a [Hosting GitLabu přes I2P](/docs/guides/gitlab/).
