---
title: "Ajudantes de Endereço Autenticados"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Open"
thread: "http://zzz.i2p/topics/2241"
toc: true
---

## Visão Geral

Esta proposta adiciona um mecanismo de autenticação aos URLs dos ajudantes de endereço.


## Motivação

Os URLs dos ajudantes de endereço são inerentemente inseguros. Qualquer pessoa pode colocar um parâmetro de ajudante de endereço em um link, até mesmo para uma imagem, e pode colocar qualquer destino no parâmetro de URL "i2paddresshelper". Dependendo da implementação do proxy HTTP do usuário, esse mapeamento de nome de host/destino, se não estiver atualmente no livro de endereços, pode ser aceito, com ou sem um intermediário para que o usuário aceite.


## Design

Servidores de salto confiáveis e serviços de registro de livro de endereços forneceriam novos links de ajudante de endereço que adicionam parâmetros de autenticação. Os dois novos parâmetros seriam uma assinatura em base 64 e uma string assinada-por.

Esses serviços gerariam e forneceriam um certificado de chave pública. Este certificado estaria disponível para download e inclusão no software proxy HTTP. Usuários e desenvolvedores de software decidiriam se confiam nesses serviços, incluindo o certificado.

Ao encontrar um link de ajudante de endereço, o proxy HTTP verificaria a presença dos parâmetros de autenticação adicionais e tentaria verificar a assinatura. Com a verificação bem-sucedida, o proxy procederia como antes, aceitando a nova entrada ou mostrando um intermediário ao usuário. Em caso de falha na verificação, o proxy poderia rejeitar o ajudante de endereço ou mostrar informações adicionais ao usuário.

Se não houver parâmetros de autenticação presentes, o proxy HTTP pode aceitar, recusar ou apresentar informações ao usuário.

Os serviços de salto seriam confiáveis como de costume, mas com o passo adicional de autenticação. Links de ajudante de endereço em outros sites precisariam ser modificados.


## Implicações de Segurança

Esta proposta adiciona segurança por meio da adição de autenticação de serviços de registro/salto confiáveis.


## Especificação

A ser definido.

Os dois novos parâmetros poderiam ser i2paddresshelpersig e i2paddresshelpersigner?

Tipos de assinaturas aceitos A ser definido. Provavelmente não RSA, pois as assinaturas em base 64 seriam muito longas.

Algoritmo de assinatura: A ser definido. Talvez apenas hostname=b64dest (mesmo que a proposta 112 para autenticação de registro)

Possível terceiro novo parâmetro: A string de autenticação de registro (a parte após o "#!") a ser usada para verificação adicional pelo proxy HTTP. Qualquer "#" na string teria que ser escapado como "&#35;" ou "&num;", ou substituído por algum outro caractere seguro para URL especificado (A ser definido).


## Migração

Proxies HTTP antigos que não suportam os novos parâmetros de autenticação os ignorariam e os passariam para o servidor web, o que deve ser inofensivo.

Proxies HTTP novos que suportam opcionalmente parâmetros de autenticação funcionariam bem com antigos links de ajudante de endereço que não os contenham.

Proxies HTTP novos que exigem parâmetros de autenticação não permitiriam antigos links de ajudante de endereço que não os contenham.

As políticas de implementação de um proxy podem evoluir ao longo de um período de migração.

## Questões

Um proprietário de site não poderia gerar um ajudante de endereço para seu próprio site, pois necessita da assinatura de um servidor de salto confiável. Ele teria de registrá-lo no servidor confiável e obter o URL do ajudante autenticado desse servidor. Há uma maneira de um site gerar um URL de ajudante de endereço auto-autenticado?

Alternativamente, o proxy poderia verificar o Referer para uma solicitação de ajudante de endereço. Se o Referer estivesse presente, contivesse um b32, e o b32 correspondesse ao destino do ajudante, então poderia ser permitido como uma auto-referência. Caso contrário, poderia ser assumido como uma solicitação de terceiro e rejeitado.
