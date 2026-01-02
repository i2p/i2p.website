---
title: "Použití IDE s I2P"
description: "Nastavení Eclipse a NetBeans pro vývoj I2P s Gradle a přiloženými projektovými soubory"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: dokumentace
reviewStatus: "needs-review"
---

<p> Hlavní vývojová větev I2P (<code>i2p.i2p</code>) byla nastavena tak, aby umožnila vývojářům snadno nastavit dvě běžně používané IDE pro vývoj v Javě: Eclipse a NetBeans. </p>

<h2>Eclipse</h2>

<p> Hlavní vývojové větve I2P (<code>i2p.i2p</code> a větve z ní odvozené) obsahují <code>build.gradle</code>, aby mohla být větev snadno nastavena v Eclipse. </p>

<ol> <li> Ujistěte se, že máte aktuální verzi Eclipse. Jakákoliv novější než 2017 by měla stačit. </li> <li> Stáhněte větev I2P do nějakého adresáře (např. <code>$HOME/dev/i2p.i2p</code>). </li> <li> Vyberte "File → Import..." a poté pod "Gradle" vyberte "Existing Gradle Project". </li> <li> Pro "Project root directory:" zvolte adresář, do kterého byla stažena větev I2P. </li> <li> V dialogu "Import Options" vyberte "Gradle Wrapper" a stiskněte Continue. </li> <li> V dialogu "Import Preview" můžete zkontrolovat strukturu projektu. Pod "i2p.i2p" by se mělo objevit více projektů. Stiskněte "Finish". </li> <li> Hotovo! Váš workspace by nyní měl obsahovat všechny projekty v rámci větve I2P a jejich build závislosti by měly být správně nastaveny. </li> </ol>

<h2>NetBeans</h2>

<p> Hlavní vývojové větve I2P (<code>i2p.i2p</code> a větve z ní vycházející) obsahují projektové soubory NetBeans. </p>

<!-- Obsah ponechejte minimální a blízký originálu; aktualizujeme později. -->
