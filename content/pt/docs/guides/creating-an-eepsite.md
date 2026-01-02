---
title: "Criando um Eepsite no I2P"
description: "Aprenda a criar e hospedar seu próprio site na rede I2P usando o servidor web Jetty integrado"
lastUpdated: "2025-11"
toc: true
---

## O que é um Eepsite (site acessível apenas pela rede I2P)?

Um **eepsite** é um site que existe exclusivamente na rede I2P. Ao contrário dos sites tradicionais acessíveis pela clearnet (internet pública), os eepsites só podem ser alcançados por meio do I2P, oferecendo anonimato e privacidade tanto para o operador do site quanto para os visitantes. Os eepsites usam o pseudo-domínio de topo `.i2p` e são acessados por meio de endereços especiais `.b32.i2p` ou nomes legíveis por humanos registrados no livro de endereços do I2P.

Todas as implantações do I2P em Java vêm com o [Jetty](https://jetty.org/index.html), um servidor web leve baseado em Java, pré-instalado e pré-configurado. Isso torna simples começar a hospedar seu próprio eepsite em poucos minutos — sem necessidade de instalar software adicional.

Este guia guiará você passo a passo pelo processo de criar e configurar seu primeiro eepsite usando as ferramentas integradas do I2P.

---

## Passo 1: Acesse o Gerenciador de Serviços Ocultos

O Gerenciador de Serviços Ocultos (também chamado de I2P Tunnel Manager) é onde você configura todos os tunnels de servidor e de cliente do I2P, incluindo servidores HTTP (eepsites).

1. Abra o seu [I2P Router Console](http://127.0.0.1:7657)
2. Navegue até o [Gerenciador de Serviços Ocultos](http://127.0.0.1:7657/i2ptunnelmgr)

Você deve ver a interface do Gerenciador de Serviços Ocultos mostrando: - **Mensagens de status** - Estado atual do tunnel e do cliente - **Controle Global de Tunnel** - Botões para gerenciar todos os tunnels de uma vez - **Serviços Ocultos do I2P** - Lista de tunnels de servidor configurados

![Gerenciador de Serviços Ocultos](/images/guides/eepsite/hidden-services-manager.png)

Por padrão, você verá uma entrada existente de **servidor web I2P** configurada, mas não iniciada. Este é o servidor web Jetty pré-configurado, pronto para você usar.

---

## Etapa 2: Configure as configurações do servidor do seu Eepsite

Clique no item **I2P webserver** na lista de Serviços Ocultos para abrir a página de configuração do servidor. É aqui que você personalizará as configurações do seu eepsite (site hospedado na rede I2P).

![Configurações do Servidor do Eepsite](/images/guides/eepsite/webserver-settings.png)

### Opções de Configuração Explicadas

**Nome** - Este é um identificador interno para o seu tunnel - Útil se você estiver executando vários eepsites para manter o controle de qual é qual - Padrão: "I2P webserver"

**Descrição** - Uma breve descrição do seu eepsite para sua própria referência - Visível apenas para você no Gerenciador de Serviços Ocultos - Exemplo: "Meu eepsite" ou "Blog pessoal"

**Início automático do Tunnel** - **Importante**: Marque esta caixa para iniciar automaticamente sua eepsite quando seu router I2P iniciar - Garante que seu site permaneça disponível sem intervenção manual após reinicializações do router - Recomendado: **Ativado**

**Destino (Host e Porta)** - **Host**: O endereço local onde seu servidor web está em execução (padrão: `127.0.0.1`) - **Porta**: A porta em que seu servidor web escuta (padrão: `7658` para o Jetty) - Se você estiver usando o servidor web Jetty pré-instalado, deixe estes com os valores padrão - Só altere se estiver executando um servidor web personalizado em uma porta diferente

**Nome de host do site** - Este é o nome de domínio `.i2p` legível por humanos do seu eepsite - Padrão: `mysite.i2p` (exemplo) - Você pode registrar um domínio personalizado como `stormycloud.i2p` ou `myblog.i2p` - Deixe em branco se você quiser usar apenas o endereço `.b32.i2p` gerado automaticamente (para outproxies (proxies de saída)) - Veja [Registrando seu domínio I2P](#registering-your-i2p-domain) abaixo para saber como reivindicar um nome de host personalizado

**Destino local** - Este é o identificador criptográfico exclusivo do seu eepsite (endereço de destino) - Gerado automaticamente quando o tunnel é criado pela primeira vez - Pense nisso como o "endereço IP" permanente do seu site no I2P - A longa sequência alfanumérica é o endereço `.b32.i2p` do seu site em formato codificado

**Arquivo de chave privada** - Local onde as chaves privadas do seu eepsite são armazenadas - Padrão: `eepsite/eepPriv.dat` - **Mantenha este arquivo seguro** - qualquer pessoa com acesso a este arquivo pode assumir a identidade do seu eepsite - Nunca compartilhe nem exclua este arquivo

### Nota importante

A caixa de aviso amarela lembra você de que, para ativar a geração de códigos QR ou os recursos de registro e autenticação, você deve configurar um Nome de Host do Site com o sufixo `.i2p` (por exemplo, `mynewsite.i2p`).

---

## Etapa 3: Opções Avançadas de Rede (Opcional)

Se você rolar para baixo na página de configuração, encontrará opções avançadas de rede. **Essas configurações são opcionais** - as configurações padrão funcionam bem para a maioria dos usuários. No entanto, você pode ajustá-las com base nos seus requisitos de segurança e necessidades de desempenho.

### Opções de Comprimento do Tunnel

![Opções de Comprimento e Quantidade de Tunnel (túnel do I2P)](/images/guides/eepsite/tunnel-options.png)

**Comprimento do tunnel** - **Padrão**: tunnel de 3 saltos (alto anonimato) - Controla quantos saltos de router uma solicitação atravessa antes de chegar ao seu eepsite - **Mais saltos = Anonimato maior, mas desempenho mais lento** - **Menos saltos = Desempenho mais rápido, mas anonimato reduzido** - As opções vão de 0 a 3 saltos, com configurações de variância - **Recomendação**: Mantenha em 3 saltos, a menos que você tenha requisitos específicos de desempenho

**Variação de tunnel** - **Padrão**: 0 de variação de saltos (sem aleatoriedade, desempenho consistente) - Adiciona aleatoriedade ao comprimento do tunnel para maior segurança - Exemplo: "0-1 de variação de saltos" significa que os tunnels serão aleatoriamente de 3 ou 4 saltos - Aumenta a imprevisibilidade, mas pode causar tempos de carregamento inconsistentes

### Opções de Quantidade de Túneis

**Quantidade (tunnels de entrada/saída)** - **Padrão**: 2 tunnels de entrada, 2 tunnels de saída (largura de banda e confiabilidade padrão) - Controla quantos tunnels paralelos são dedicados ao seu eepsite - **Mais tunnels = Melhor disponibilidade e capacidade de lidar com carga, porém maior uso de recursos** - **Menos tunnels = Menor uso de recursos, porém menor redundância** - Recomendado para a maioria dos usuários: 2/2 (padrão) - Sites de alto tráfego podem se beneficiar de 3/3 ou mais

**Número de tunnels de backup** - **Padrão**: 0 backup tunnels (sem redundância, sem uso adicional de recursos) - tunnels em espera que são ativados se os tunnels primários falharem - Aumenta a confiabilidade, mas consome mais largura de banda e CPU - A maioria dos eepsites pessoais não precisa de backup tunnels

### Limites de POST

![Configuração dos limites de POST](/images/guides/eepsite/post-limits.png)

Se o seu eepsite incluir formulários (formulários de contato, seções de comentários, envio de arquivos, etc.), você pode configurar limites para requisições POST para evitar abuso:

**Limites por Cliente** - **Por Período**: Número máximo de solicitações de um único cliente (padrão: 6 a cada 5 minutos) - **Duração do Bloqueio**: Por quanto tempo bloquear clientes abusivos (padrão: 20 minutos)

**Limites Totais** - **Total**: Número máximo de requisições POST de todos os clientes somadas (padrão: 20 a cada 5 minutos) - **Duração do bloqueio**: Por quanto tempo rejeitar todas as requisições POST se o limite for excedido (padrão: 10 minutos)

**Período de Limite de POST** - Intervalo de tempo para medir a taxa de requisições (padrão: 5 minutos)

Esses limites ajudam a proteger contra spam, ataques de negação de serviço e abuso de envio automatizado de formulários.

### Quando Ajustar as Configurações Avançadas

- **Site comunitário de alto tráfego**: Aumente a quantidade de tunnels (3-4 de entrada/de saída)
- **Aplicação com desempenho crítico**: Reduza o comprimento do tunnel para 2 saltos (compromisso de privacidade)
- **Anonimato máximo exigido**: Mantenha 3 saltos, adicione 0-1 de variância
- **Formulários com uso legítimo elevado**: Aumente os limites de POST conforme necessário
- **Blog/portfólio pessoal**: Use todos os valores padrão

---

## Etapa 4: Adicionando conteúdo ao seu Eepsite

Agora que seu eepsite está configurado, você precisa adicionar os arquivos do seu site (HTML, CSS, imagens, etc.) ao diretório raiz de documentos do servidor web. A localização varia dependendo do seu sistema operacional, do tipo de instalação e da implementação do I2P.

### Encontrando o diretório raiz do site

A **raiz do documento** (frequentemente chamada de `docroot`) é o diretório onde você coloca todos os arquivos do seu site. Seu arquivo `index.html` deve ir diretamente nesse diretório.

#### Java I2P (Distribuição Padrão)

**Linux** - **Instalação padrão**: `~/.i2p/eepsite/docroot/` - **Instalação por pacote (executando como serviço)**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **Instalação padrão**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - Caminho típico: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Instalação como Serviço do Windows**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - Caminho típico: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **Instalação padrão**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+ (Distribuição I2P Aprimorada)

O I2P+ usa a mesma estrutura de diretórios que o Java I2P. Siga os caminhos acima de acordo com o seu sistema operacional.

#### i2pd (Implementação em C++)

**Linux/Unix** - **Padrão**: `/var/lib/i2pd/eepsite/` ou `~/.i2pd/eepsite/` - Verifique o arquivo de configuração `i2pd.conf` para a definição real de `root` no tunnel do seu servidor HTTP

**Windows** - Verifique `i2pd.conf` no diretório de instalação do i2pd

**macOS** - Normalmente: `~/Library/Application Support/i2pd/eepsite/`

### Adicionando os arquivos do seu site

1. **Navegue até o diretório raiz do seu site** usando o seu gerenciador de arquivos ou o terminal
2. **Crie ou copie os arquivos do seu site** para a pasta `docroot`
   - No mínimo, crie um arquivo `index.html` (esta é a sua página inicial)
   - Adicione CSS, JavaScript, imagens e outros recursos conforme necessário
3. **Organize os subdiretórios** como você faria para qualquer site:
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### Início rápido: Exemplo simples de HTML

Se você está apenas começando, crie um arquivo básico `index.html` na sua pasta `docroot`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### Permissões (Linux/Unix/macOS)

Se você estiver executando o I2P como um serviço ou com um usuário diferente, certifique-se de que o processo do I2P tenha acesso de leitura aos seus arquivos:

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### Dicas

- **Conteúdo padrão**: Quando você instala o I2P pela primeira vez, já há conteúdo de exemplo na pasta `docroot` - sinta-se à vontade para substituí-lo
- **Sites estáticos funcionam melhor**: Embora o Jetty suporte servlets e JSP, sites simples em HTML/CSS/JavaScript são mais fáceis de manter
- **Servidores web externos**: Usuários avançados podem executar servidores web personalizados (Apache, Nginx, Node.js, etc.) em portas diferentes e apontar o I2P tunnel para eles

---

## Etapa 5: Iniciando seu Eepsite

Agora que o seu eepsite está configurado e tem conteúdo, é hora de iniciá-lo e torná-lo acessível na rede I2P.

### Iniciar o Tunnel

1. **Volte ao [Gerenciador de Serviços Ocultos](http://127.0.0.1:7657/i2ptunnelmgr)**
2. Encontre a sua entrada do **servidor web I2P** na lista
3. Clique no botão **Iniciar** na coluna Controle

![Eepsite em execução](/images/guides/eepsite/eepsite-running.png)

### Aguardar o estabelecimento do tunnel

Depois de clicar em Iniciar, seu eepsite tunnel começará a ser construído. Esse processo normalmente leva **30-60 segundos**. Observe o indicador de status:

- **Luz vermelha** = Tunnel iniciando/em construção
- **Luz amarela** = Tunnel parcialmente estabelecido
- **Luz verde** = Tunnel totalmente operacional e pronto

Assim que você vir a **luz verde**, seu eepsite estará no ar na rede I2P!

### Acesse seu Eepsite

Clique no botão **Preview** ao lado do seu eepsite em execução. Isso abrirá uma nova aba do navegador com o endereço do seu eepsite.

Seu eepsite possui dois tipos de endereços:

1. **Endereço Base32 (.b32.i2p)**: Um endereço criptográfico longo que se parece com:
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - Este é o endereço permanente, derivado criptograficamente, do seu eepsite
   - Não pode ser alterado e está vinculado à sua chave privada
   - Funciona sempre, mesmo sem registro de domínio

2. **Domínio legível por humanos (.i2p)**: Se você definir um Nome de host do site (por exemplo, `testwebsite.i2p`)
   - Só funciona após o registro de domínio (veja a próxima seção)
   - Mais fácil de lembrar e compartilhar
   - Aponta para o seu endereço .b32.i2p

O botão **Copy Hostname** permite copiar rapidamente o seu endereço `.b32.i2p` completo para compartilhamento.

---

## ⚠️ Crítico: Faça backup da sua chave privada

Antes de prosseguir, você **deve fazer backup** do arquivo de chave privada do seu eepsite. Isto é crucial por vários motivos:

### Por que fazer backup da sua chave?

**Sua chave privada (`eepPriv.dat`) é a identidade do seu eepsite.** Ela determina o seu endereço `.b32.i2p` e comprova a propriedade do seu eepsite.

- **Chave = endereço .b32**: Sua chave privada gera matematicamente seu endereço .b32.i2p exclusivo
- **Não pode ser recuperada**: Se você perder sua chave, perderá permanentemente o endereço da sua eepsite
- **Não pode ser alterado**: Se você registrou um domínio apontando para um endereço .b32, **não há como atualizá-lo** - o registro é permanente
- **Necessária para migração**: Migrar para um novo computador ou reinstalar o I2P requer essa chave para manter o mesmo endereço
- **Suporte a multihoming (hospedagem a partir de múltiplas localizações)**: Executar sua eepsite a partir de múltiplos locais requer a mesma chave em cada servidor

### Onde está a chave privada?

Por padrão, sua chave privada é armazenada em: - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (ou `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat` para instalações como serviço) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` ou `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

Você também pode verificar/alterar esse caminho na configuração do seu tunnel em "Private Key File".

### Como fazer backup

1. **Pare o seu tunnel** (túnel do I2P; opcional, mas mais seguro)
2. **Copie `eepPriv.dat`** para um local seguro:
   - Unidade USB externa
   - Unidade de backup criptografada
   - Arquivo protegido por senha
   - Armazenamento em nuvem seguro (criptografado)
3. **Mantenha vários backups** em diferentes locais físicos
4. **Nunca compartilhe este arquivo** - qualquer pessoa com ele pode se passar pelo seu eepsite (site hospedado no I2P)

### Restaurar a partir do backup

Para restaurar seu eepsite em um novo sistema ou após uma reinstalação:

1. Instale o I2P e crie/configure as configurações do seu tunnel
2. **Pare o tunnel** antes de copiar a chave
3. Copie o seu `eepPriv.dat` de backup para o local correto
4. Inicie o tunnel - ele usará seu endereço .b32 original

---

## Se você não for registrar um domínio

**Parabéns!** Se você não planeja registrar um nome de domínio `.i2p` personalizado, seu eepsite agora está completo e operacional.

Você pode: - Compartilhar seu endereço `.b32.i2p` com outras pessoas - Acessar seu site pela rede I2P usando qualquer navegador compatível com I2P - Atualizar os arquivos do seu site na pasta `docroot` a qualquer momento - Monitorar o status do seu tunnel no Gerenciador de Serviços Ocultos

**Se você quiser um domínio legível por humanos** (como `mysite.i2p` em vez de um endereço .b32 longo), continue para a próxima seção.

---

## Registrando seu domínio I2P

Um domínio `.i2p` legível por humanos (como `testwebsite.i2p`) é muito mais fácil de lembrar e compartilhar do que um endereço `.b32.i2p` longo. O registro de domínio é gratuito e vincula o nome escolhido ao endereço criptográfico do seu eepsite.

### Pré-requisitos

- Seu eepsite deve estar em execução com a luz verde acesa
- Você deve ter definido um **Nome de host do site** na configuração do seu tunnel (Etapa 2)
- Exemplo: `testwebsite.i2p` ou `myblog.i2p`

### Etapa 1: Gerar string de autenticação

1. **Volte para a configuração do seu tunnel** no Hidden Services Manager
2. Clique na sua entrada do **servidor web I2P** para abrir as configurações
3. Role a página para baixo para encontrar o botão **Registration Authentication**

![Autenticação de Registro](/images/guides/eepsite/registration-authentication.png)

4. Clique em **Autenticação de Registro**
5. **Copie toda a cadeia de autenticação** mostrada para "Autenticação para adicionar o host [yourdomainhere]"

A sequência de autenticação terá o seguinte formato:

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
Esta cadeia de caracteres contém: - O seu nome de domínio (`testwebsite.i2p`) - O seu endereço de destino (o identificador criptográfico longo) - Um carimbo de data/hora - Uma assinatura criptográfica que comprova que você possui a chave privada

**Guarde esta cadeia de autenticação** - você vai precisar dela para ambos os serviços de registro.

### Etapa 2: Registre-se em stats.i2p

1. **Acesse** [stats.i2p Adicionar chave](http://stats.i2p/i2p/addkey.html) (dentro do I2P)

![Registro de domínio do stats.i2p](/images/guides/eepsite/stats-i2p-add.png)

2. **Cole a string de autenticação** no campo "Authentication String"
3. **Adicione seu nome** (opcional) - o padrão é "Anonymous"
4. **Adicione uma descrição** (recomendado) - descreva brevemente do que se trata o seu eepsite
   - Exemplo: "Novo I2P Eepsite", "Blog pessoal", "Serviço de compartilhamento de arquivos"
5. **Marque "HTTP Service?"** se for um site (mantenha marcado para a maioria dos eepsites)
   - Desmarque para IRC, NNTP, proxies, XMPP, git, etc.
6. Clique em **Submit**

Se for bem-sucedido, você verá uma confirmação de que seu domínio foi adicionado ao livro de endereços do stats.i2p.

### Passo 3: Registre-se no reg.i2p

Para garantir a máxima disponibilidade, você também deve se registrar no serviço reg.i2p:

1. **Acesse** [reg.i2p Add Domain](http://reg.i2p/add) (dentro do I2P)

![Registro de Domínio do reg.i2p](/images/guides/eepsite/reg-i2p-add.png)

2. **Cole a mesma string de autenticação** no campo "Auth string"
3. **Adicione uma descrição** (opcional, mas recomendável)
   - Isso ajuda outros usuários do I2P a entender o que o seu site oferece
4. Clique em **Submit**

Você deve receber uma confirmação de que seu domínio foi registrado.

### Etapa 4: Aguarde a propagação

Após enviar para ambos os serviços, o registro do seu domínio se propagará pelo sistema de livro de endereços da rede I2P.

**Cronograma de propagação**: - **Registro inicial**: imediato nos serviços de registro - **Propagação em toda a rede**: de várias horas a mais de 24 horas - **Disponibilidade total**: pode levar até 48 horas para que todos os routers sejam atualizados

**Isso é normal!** O sistema de livro de endereços do I2P é atualizado periodicamente, não instantaneamente. Seu eepsite está funcionando - outros usuários só precisam receber o livro de endereços atualizado.

### Verifique seu domínio

Após algumas horas, você pode testar seu domínio:

1. **Abra uma nova aba do navegador** no seu navegador I2P
2. Tente acessar seu domínio diretamente: `http://yourdomainname.i2p`
3. Se carregar, seu domínio está registrado e em propagação!

Se ainda não funcionar: - Espere mais (os livros de endereços são atualizados no seu próprio cronograma) - O livro de endereços do seu router pode precisar de tempo para sincronizar - Tente reiniciar o seu router I2P para forçar uma atualização do livro de endereços

### Notas importantes

- **O registro é permanente**: Uma vez registrado e propagado, seu domínio aponta para o seu endereço `.b32.i2p` permanentemente
- **Não é possível alterar o destino**: Você não pode atualizar para qual endereço `.b32.i2p` o seu domínio aponta - por isso fazer backup do `eepPriv.dat` é fundamental
- **Propriedade do domínio**: Apenas o detentor da chave privada pode registrar ou atualizar o domínio
- **Serviço gratuito**: O registro de domínios no I2P é gratuito, mantido pela comunidade e descentralizado
- **Múltiplos registradores**: Registrar tanto no stats.i2p quanto no reg.i2p aumenta a confiabilidade e a velocidade de propagação

---

## Parabéns!

Seu I2P eepsite agora está totalmente operacional com um domínio registrado!

**Próximos passos**: - Adicione mais conteúdo à sua pasta `docroot` - Compartilhe seu domínio com a comunidade I2P - Mantenha seu backup `eepPriv.dat` em segurança - Monitore o status do seu tunnel (túnel do I2P) regularmente - Considere participar dos fóruns do I2P ou do IRC para divulgar seu site

Bem-vindo à rede I2P! 🎉
