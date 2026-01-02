---
title: "Acerca de I2P"
description: "Aprende sobre The Invisible Internet Project - una red de superposición totalmente encriptada, de igual a igual, diseñada para la comunicación anónima."
tagline: "The Invisible Internet Project"
type: "about"
layout: "about"
established: "2002"
---

El Invisible Internet Project comenzó en 2002. La visión para el proyecto era que la Red I2P "proporcionara anonimato, privacidad y seguridad completos al más alto nivel posible. Un Internet descentralizado y de igual a igual significa no más preocupaciones sobre que tu proveedor de servicios de Internet controle tu tráfico. Esto permitirá a las personas realizar actividades sin interrupciones y cambiar nuestra percepción sobre la seguridad e incluso el Internet, utilizando criptografía de clave pública, esteganografía IP y autenticación de mensajes. El Internet que debería haber sido, pronto lo será."

Desde entonces, I2P ha evolucionado para especificar e implementar un conjunto completo de protocolos de red capaces de proporcionar un alto nivel de privacidad, seguridad y autenticación a una variedad de aplicaciones.

## La Red I2P

La red I2P es una red de superposición totalmente encriptada de igual a igual. Un observador no puede ver el contenido, origen o destino de un mensaje. Nadie puede ver de dónde proviene el tráfico, hacia dónde se dirige o cuál es su contenido. Además, los transportes I2P ofrecen resistencia al reconocimiento y bloqueo por censores. Debido a que la red depende de pares para enrutamiento del tráfico, el bloqueo basado en ubicación es un desafío que crece con la red. Cada enrutador en la red participa en hacer anónima la red. Excepto en casos donde sería inseguro, todos participan en el envío y recepción de tráfico de red.

## Cómo Conectar a la Red I2P

El software central (Java) incluye un enrutador que introduce y mantiene una conexión con la red. También proporciona aplicaciones y opciones de configuración para personalizar tu experiencia y flujo de trabajo. Aprende más en nuestra [documentación](/docs/).

## ¿Qué Puedo Hacer en la Red I2P?

La red proporciona una capa de aplicación para servicios, aplicaciones y gestión de red. La red también tiene su propio DNS único que permite autoalojamiento y espejo de contenido de Internet (Clearnet). La red I2P funciona de la misma manera que el Internet. El software Java incluye un cliente BitTorrent, y correo electrónico así como una plantilla de sitio web estático. Otras aplicaciones pueden añadirse fácilmente a tu consola de enrutador.

## Una Visión General de la Red

I2P utiliza criptografía para lograr una variedad de propiedades para los túneles que construye y las comunicaciones que transporta. Los túneles I2P usan transportes, [NTCP2](/docs/specs/ntcp2/) y [SSU2](/docs/specs/ssu2/), para ocultar el tráfico que se transporta sobre ellos. Las conexiones están encriptadas de enrutador a enrutador, y de cliente a cliente (de extremo a extremo). Se proporciona secreto hacia adelante para todas las conexiones. Debido a que I2P está dirigido criptográficamente, las direcciones de red I2P son autoautenticables y solo pertenecen al usuario que las generó.

La red está compuesta de pares ("enrutadores") y túneles virtuales unidireccionales de entrada y salida. Los enrutadores se comunican entre sí utilizando protocolos construidos sobre mecanismos de transporte existentes (TCP, UDP), enviando mensajes. Las aplicaciones cliente tienen su propio identificador criptográfico ("Destino") que les permite enviar y recibir mensajes. Estos clientes pueden conectarse a cualquier enrutador y autorizar la asignación temporal ("cesión") de algunos túneles que se usarán para enviar y recibir mensajes a través de la red. I2P tiene su propia base de datos interna de la red (usando una modificación de Kademlia DHT) para distribuir la información de contacto y enrutamiento de manera segura.

## Acerca de la Descentralización y la Red I2P

La red I2P es casi completamente descentralizada, con excepción de lo que se llaman Servidores Reseed. Esto es para tratar con el problema de arranque de DHT (Tabla Hash Distribuida). Básicamente, no hay una manera buena y confiable de evitar ejecutar al menos un nodo de arranque permanente que los no participantes en la red puedan encontrar para comenzar. Una vez conectado a la red, un enrutador solo descubre pares construyendo túneles "exploratorios", pero para hacer la conexión inicial, se requiere un host reseed para crear conexiones y conectar un nuevo enrutador a la red. Los servidores reseed pueden observar cuando un nuevo enrutador ha descargado un reseed de ellos, pero nada más sobre el tráfico en la red I2P.

## Comparaciones

Existen muchas otras aplicaciones y proyectos que trabajan en comunicación anónima e I2P se ha inspirado en gran parte de sus esfuerzos. Esta no es una lista exhaustiva de recursos sobre anonimato - tanto la [Bibliografía sobre Anonimato de freehaven](http://freehaven.net/anonbib/topic.html) como los [proyectos relacionados de GNUnet](https://www.gnunet.org/links/) cumplen bien ese propósito. Dicho esto, algunos sistemas destacan para una comparación más detallada. Aprende más sobre cómo I2P se compara con otras redes de anonimato en nuestra [documentación de comparación detallada](/docs/overview/comparison/). 
