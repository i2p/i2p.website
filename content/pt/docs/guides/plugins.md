---
title: "Instalando Plugins Personalizados"
description: "Instalando, atualizando e desenvolvendo plugins de roteador"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

O framework de plugins do I2P permite que você estenda o router sem tocar na instalação principal. Os plugins disponíveis cobrem e-mail, blogs, IRC, armazenamento, wikis, ferramentas de monitoramento e muito mais.

> **Nota de segurança:** Os plugins são executados com as mesmas permissões do router. Trate downloads de terceiros da mesma forma que trataria qualquer atualização de software assinada—verifique a fonte antes de instalar.

## 1. Instalar um Plugin

1. Copie o URL de download do plugin da página do projeto.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Abra a [página de Configuração de Plugins](http://127.0.0.1:7657/configplugins) do console do router.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. Cole o URL no campo de instalação e clique em **Install Plugin**.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

O router obtém o arquivo assinado, verifica a assinatura e ativa o plugin imediatamente. A maioria dos plugins adiciona links no console ou serviços em segundo plano sem exigir uma reinicialização do router.

## 2. Por Que os Plugins São Importantes

- Distribuição com um clique para utilizadores finais—sem edições manuais em `wrapper.config` ou `clients.config`
- Mantém o pacote central `i2pupdate.su3` pequeno enquanto fornece funcionalidades grandes ou de nicho sob demanda
- JVMs opcionais por plugin fornecem isolamento de processos quando necessário
- Verificações automáticas de compatibilidade com a versão do router, runtime Java e Jetty
- Mecanismo de atualização espelha o router: pacotes assinados e downloads incrementais
- Integrações na consola, pacotes de idiomas, temas de UI e aplicações não-Java (via scripts) são todos suportados
- Permite diretórios de "loja de aplicações" curados como `plugins.i2p`

## 3. Gerenciar Plugins Instalados

Use os controles no [Plugin do Roteador I2P](http://127.0.0.1:7657/configclients.jsp#plugin) para:

- Verificar atualizações de um único plugin
- Verificar todos os plugins de uma vez (acionado automaticamente após atualizações do router)
- Instalar quaisquer atualizações disponíveis com um clique  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- Ativar/desativar início automático para plugins que registram serviços
- Desinstalar plugins de forma limpa

## 4. Construa Seu Próprio Plugin

1. Revise a [especificação de plugin](/docs/specs/plugin/) para requisitos de empacotamento, assinatura e metadados.
2. Use [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) para empacotar um binário ou webapp existente em um arquivo instalável.
3. Publique URLs tanto de instalação quanto de atualização para que o router possa distinguir instalações iniciais de atualizações incrementais.
4. Forneça checksums e chaves de assinatura de forma destacada na página do seu projeto para ajudar os usuários a verificar a autenticidade.

Procurando exemplos? Navegue pelo código-fonte dos plugins da comunidade em `plugins.i2p` (por exemplo, o exemplo `snowman`).

## 5. Limitações Conhecidas

- Atualizar um plugin que fornece arquivos JAR simples pode exigir uma reinicialização do router porque o carregador de classes Java mantém classes em cache.
- O console pode exibir um botão **Parar** mesmo que o plugin não tenha nenhum processo ativo.
- Plugins lançados em uma JVM separada criam um diretório `logs/` no diretório de trabalho atual.
- Na primeira vez que uma chave de assinante aparece, ela é automaticamente confiável; não há autoridade central de assinatura.
- O Windows às vezes deixa diretórios vazios para trás após desinstalar um plugin.
- Instalar um plugin exclusivo para Java 6 em uma JVM Java 5 reporta "plugin está corrompido" devido à compressão Pack200.
- Plugins de tema e tradução permanecem amplamente não testados.
- Flags de início automático nem sempre persistem para plugins não gerenciados.

## 6. Requisitos e Melhores Práticas

- O suporte a plugins está disponível no I2P **0.7.12 e versões mais recentes**.
- Mantenha seu router e plugins atualizados para receber correções de segurança.
- Distribua notas de lançamento concisas para que os usuários entendam o que muda entre versões.
- Quando possível, hospede arquivos de plugin via HTTPS dentro do I2P para minimizar a exposição de metadados na clearnet.

## 7. Leitura Adicional

- [Especificação de plugin](/docs/specs/plugin/)
- [Framework de aplicação cliente](/docs/applications/managed-clients/)
- [Repositório de scripts I2P](https://github.com/i2p/i2p.scripts/) para utilitários de empacotamento
