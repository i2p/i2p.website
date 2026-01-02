---
title: "Discusión sobre NTCP (protocolo de transporte de I2P basado en TCP)"
description: "Notas históricas que comparan los transportes NTCP y SSU y propuestas de ajuste"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## Discusión NTCP vs. SSU (marzo de 2007)

### Preguntas sobre NTCP

_Adaptado de una conversación en IRC entre zzz y cervantes._

- **¿Por qué NTCP tiene prioridad sobre SSU cuando NTCP parece añadir sobrecarga y latencia?**  
  NTCP generalmente ofrece mejor fiabilidad que la implementación original de SSU.
- **¿El streaming sobre NTCP incurre en el clásico colapso de TCP sobre TCP (TCP-over-TCP)?**  
  Es posible, pero SSU se concibió como la opción ligera basada en UDP y resultó demasiado poco fiable en la práctica.

### “NTCP considerado perjudicial” (zzz, 25 de marzo de 2007)

Resumen: la mayor latencia y sobrecarga de NTCP pueden causar congestión; sin embargo, el enrutamiento prefiere NTCP porque sus valores de puja están fijados en el código como más bajos que los de SSU. El análisis planteó varios puntos:

- Actualmente, NTCP ofrece un coste inferior al de SSU, por lo que los routers prefieren NTCP salvo que ya exista una sesión SSU.
- SSU implementa acuses de recibo con temporizadores estrictamente acotados y estadísticas; NTCP se apoya en Java NIO TCP con temporizadores al estilo de las RFC que pueden ser mucho más largos.
- La mayor parte del tráfico (HTTP, IRC, BitTorrent) usa la biblioteca de streaming de I2P, que efectivamente apila TCP sobre NTCP. Cuando ambas capas retransmiten, es posible un colapso. Las referencias clásicas incluyen [TCP over TCP is a bad idea](http://sites.inka.de/~W1011/devel/tcp-tcp.html).
- Los tiempos de espera de la biblioteca de streaming aumentaron de 10 s a 45 s en la versión 0.8; el tiempo de espera máximo de SSU es de 3 s, mientras que se presume que los tiempos de espera de NTCP se acercan a 60 s (recomendación de la RFC). Los parámetros de NTCP son difíciles de inspeccionar externamente.
- Las observaciones de campo en 2007 mostraron que el rendimiento de subida de i2psnark oscilaba, lo que sugiere un colapso periódico por congestión.
- Las pruebas de eficiencia (forzando la preferencia por SSU) redujeron las proporciones de sobrecarga de tunnel de aproximadamente 3.5:1 a 3:1 y mejoraron las métricas de streaming (tamaño de ventana, RTT, proporción envío/ack).

#### Propuestas del hilo de 2007

1. **Invertir las prioridades de transporte** para que los routers prefieran SSU (restaurando `i2np.udp.alwaysPreferred`).
2. **Etiquetar el tráfico de streaming** de modo que SSU puje más bajo solo para los mensajes etiquetados, sin comprometer el anonimato.
3. **Restringir los límites de retransmisión de SSU** para reducir el riesgo de colapso.
4. **Estudiar underlays (capas subyacentes) semiconfiables** para determinar si las retransmisiones por debajo de la biblioteca de streaming aportan un beneficio neto.
5. **Revisar las colas de prioridad y los tiempos de espera**—por ejemplo, aumentar los tiempos de espera de streaming más allá de 45 s para alinearlos con NTCP.

### Respuesta de jrandom (27 de marzo de 2007)

Contraargumentos clave:

- NTCP existe porque los primeros despliegues de SSU sufrieron colapso por congestión. Incluso tasas modestas de retransmisión por salto pueden dispararse a través de tunnels de múltiples saltos.
- Sin acuses de recibo a nivel de tunnel, solo una fracción de los mensajes recibe estado de entrega extremo a extremo; los fallos pueden ser silenciosos.
- El control de congestión de TCP cuenta con décadas de optimizaciones; NTCP aprovecha eso mediante pilas TCP maduras.
- Las ganancias de eficiencia observadas al preferir SSU podrían reflejar el comportamiento de encolado del router más que ventajas intrínsecas del protocolo.
- Plazos de espera de streaming más largos ya estaban mejorando la estabilidad; se alentó recopilar más observaciones y datos antes de realizar cambios importantes.

El debate ayudó a perfeccionar el ajuste posterior del transporte, pero no refleja la arquitectura moderna de NTCP2/SSU2.
