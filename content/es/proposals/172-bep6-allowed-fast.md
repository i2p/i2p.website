---
title: "Extensión rápida (BEP 6) Rápido permitido con identidad de par hash de destino"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Borrador"
toc: true
---

## Descripción general

BEP 6 (extensión Fast) incluye cinco características: **Have All / Have None**, **Reject Requests**, **Suggestions** y **Allowed Fast**. El protocolo de comunicación —bit de negociación, IDs de mensajes y semántica de choke— es independiente del transporte y funciona tal cual sobre el streaming de I2P. La única parte de BEP 6 que no puede mapearse directamente a I2P es la **generación del conjunto Allowed Fast**, porque está definida en términos de la dirección IPv4 del par. Los pares en I2P no tienen direcciones IP; se identifican mediante hashes de destino de 32 bytes.

Esta propuesta estandariza la generación de un conjunto de Allowed Fast nativo de I2P, de modo que todos los clientes torrent de I2P generen conjuntos de allowed fast *idénticos* para el mismo par y torrent, haciendo que esta función sea útil (y verificable) entre diferentes implementaciones.

## Motivación

Los nuevos pares necesitan los primeros fragmentos antes de que el sistema BitTorrent de "ojo por ojo" pueda acelerarse. En I2P, esta aceleración es más lenta que en la red convencional: la configuración de la conexión y la entrega de fragmentos atraviesan varios saltos a través de túneles de alta latencia, por lo que el periodo entre la conexión y el primer desbloqueo recíproco es más largo. Allowed Fast ataca directamente este periodo: se permite a un par recién conectado obtener un pequeño número de fragmentos incluso mientras está bloqueado, recibe datos inmediatamente y puede comenzar a reciprocitar antes.

El BEP 6 de referencia calcula el conjunto rápido permitido a partir de la dirección IPv4 del par para garantizar que el *emisor* pueda seleccionar piezas únicas para el *receptor* (un usuario con muchas IPs no puede obtener muchos conjuntos). En I2P, el hash de destino del par cumple la misma función de vinculación y está disponible en ambos extremos de cada conexión, lo que hace que el conjunto sea determinista y *verificable localmente* — algo que el esquema basado en IP no puede ofrecer.

## Modificaciones a BEP 6

La negociación de la extensión rápida y los cuatro tipos de mensajes se adoptan sin cambios:

- Negociación: tercer bit menos significativo del último byte reservado, `reserved[7] |= 0x04`, ambos extremos
- Tener Todo `<len=0x0001><op=0x0E>`, No Tener Nada `<len=0x0001><op=0x0F>`
- Sugerir Trozo `<len=0x0005><op=0x0D><index>`
- Rechazar Solicitud `<len=0x000D><op=0x10><index><begin><length>`
- Rápido Permitido `<len=0x0005><op=0x11><index>`
- Cada solicitud da como resultado exactamente una respuesta (trozo o rechazo); el bloqueo ya no rechaza implícitamente las solicitudes pendientes

La única desviación está en la generación del conjunto Permitido Rápido, reemplazando los bytes de la IP con bytes del hash de destino del par.

### Desviación: bytes de hash en lugar de IP enmascarada

Referencia BEP 6, paso (1):

```
x = 0xFFFFFF00 & ip
```
Eso toma tres bytes de la dirección IPv4 del par y **pone a cero el 4º byte**. Esta es una heurística de subred: los usuarios que puedan obtener múltiples IPs en la misma red /24 no deberían obtener múltiples conjuntos rápidos permitidos.

Nuestra versión de I2P reemplaza esto con los primeros cuatro bytes del hash de destino de 32 bytes del par:

```
x = first 4 bytes of peer destination hash
```
La diferencia con respecto a la implementación de referencia:

> "Son 3 bytes de la IP seguidos por un cero. Tú eres 4 bytes del hash. Es diferente del BEP 6 porque no hay IP y no está poniendo a cero el cuarto byte."

Ambos extremos de una conexión I2P ya conocen el hash de destino del par (es la dirección a/la cual se estableció la conexión), por lo que no requiere intercambio adicional, descubrimiento NAT ni detección de IP externa; nada de lo cual existe en I2P.

### Algoritmo permitido de generación rápida

Sea `hash` el hash de destino de 32 bytes del par receptor, `infohash` el infohash del torrent de 20 bytes, `sz` el número de piezas en el torrent, `k` el número final de piezas en el conjunto de transferencia rápida permitida (10, como en BEP 6), y `a` el conjunto de salida:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
Notas:

- 4 bytes del hash de destino reemplazan los 3 bytes IP enmascarados. Los cuatro bytes contienen entropía del hash; ninguno se pone a cero.
- Como en BEP 6, la cadena SHA1 produce una secuencia pseudoraleatoria larga, dividida en índices de fragmentos; `k = 10` coincide con el valor predeterminado de referencia.
- El mensaje Allowed Fast es orientativo: el receptor NO DEBE interpretarlo como que el remitente posee el fragmento, sino únicamente que el remitente proporcionará ese fragmento mientras esté estrangulado.

## Beneficios

| Área              | Beneficio                                                                                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Latencia de inicio | Los nuevos pares descargan los primeros fragmentos incluso cuando están bloqueados, acortando la fase inicial de intercambio lenta que se produce en túneles I2P de múltiples saltos                                                                     |
| Determinismo       | El conjunto es una función pura del hash de destino + infohash, por lo que cualquier implementación calcula el mismo conjunto — a diferencia del BEP 6 basado en IP, donde la percepción del emisor sobre la IP del receptor puede diferir (NAT) |
| Verificabilidad    | El par receptor conoce su propio hash de destino y puede volver a calcular y validar localmente el conjunto, detectando emisores con mal comportamiento                                       |
| Sin mecanismo IP   | No se requiere travesía de NAT, descubrimiento de IP externa ni heurísticas de subred — todos ellos imposibles o carentes de sentido en I2P                                                   |
| Vinculación de identidad | Un conjunto rápido permitido por destino. Un usuario con muchos destinos obtiene un conjunto por cada uno — la misma propiedad anti-manipulación que proporcionaba la máscara IP en clearnet |
| Privacidad         | Nunca se transmite ni se infiere ninguna dirección IP en el cálculo                                                                                                                           |
| Ancho de banda     | "Tengo todo" / "No tengo nada" reemplaza el bitfield completo en torrents grandes; "Rechazar" elimina re-peticiones redundantes                                                               |
## Consideraciones de implementación

- **Identidad del par**: el hash de destino del par se obtiene de la conexión de transmisión (el destino de la sesión), y es el mismo valor que utilizan ambos extremos. Para conexiones salientes, use el destino al que se conectó; para conexiones entrantes, use el destino desde el cual llegó la conexión.
- **Negociación**: envíe `reserved[7] |= 0x04` en el saludo inicial (handshake); solo envíe mensajes de extensión rápida (Fast Extension) si el saludo del par también tiene activado ese bit; si un par envía mensajes de extensión rápida sin negociación, cierre la conexión.
- **Tengo todo / No tengo nada**: envíe exactamente uno de los siguientes mensajes —campo de bits (bitfield), Tengo todo (Have All) o No tengo nada (Have None)— inmediatamente después del saludo. Use Tengo todo para semillas, y No tengo nada hasta obtener la primera pieza.
- **Lado que envía Tengo rápido (Allowed Fast)**: solo anuncie piezas que realmente posea; el receptor podría solicitarlas incluso si está estrangulado (choked). Limite el conjunto *servido* (por ejemplo, rechace solicitudes de tipo allowed-fast de un par que ya posea más de `k` piezas, según la recomendación de BEP 6).
- **Lado que recibe Tengo rápido (Allowed Fast)**: almacene el conjunto recibido; permita solicitudes de esas piezas incluso cuando esté estrangulado; opcionalmente, verifique el conjunto recalculándolo a partir de su propio hash de destino y del infohash, e ignore las piezas que no estén en el conjunto calculado.
- **Rechazo**: cada solicitud DEBE recibir exactamente una respuesta; cuando esté estrangulado, rechace todo lo que no esté en el conjunto de Tengo rápido, en lugar de silenciar pasivamente al par.
- **Tamaño del conjunto**: use `k = 10` para mantener compatibilidad; los pares pueden elegir un valor menor de `k` bajo carga, pero ambos extremos deben anunciar únicamente lo que realmente servirán.
- **Límite de pieza**: `index = y % sz` debe usar el número total de piezas del torrent `sz`; ignore los índices mayores o iguales a `sz` (medida defensiva), ya que una cadena hash no se limita por rango de piezas.
- **Compatibilidad hacia atrás**: los clientes que no negocian el bit rápido simplemente nunca verán estos mensajes; no se requieren otros cambios de protocolo.

## Implementaciones de referencia

El algoritmo es pequeño y autónomo: unas pocas docenas de líneas en cualquier lenguaje. Los tres ejemplos siguientes calculan el mismo conjunto para entradas idénticas (`hash[0:4] ++ infohash`, cadena SHA1, `y % sz`, con `k = 10`).

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## Compatibilidad

- **Compatible con el protocolo**: el bit de negociación y los formatos de mensaje son idénticos byte a byte al BEP 6 de clearnet; solo difiere la entrada para la generación del conjunto.
- **No interoperable entre redes**: un cliente I2P y un cliente de clearnet no pueden conectarse entre sí de todos modos; la diferencia afecta únicamente a los bytes de identidad del par, nunca al formato del protocolo.
- **Dentro de I2P**: cualquier cliente que implemente esta propuesta calcula conjuntos rápidos permitidos idénticos y puede servirlos y verificarlos indistintamente. Los clientes que ignoran Allowed Fast simplemente lo tratan como una sugerencia sin efecto y solo pierden el beneficio de inicio.

## Preguntas abiertas

1. ¿Debe mantenerse el tamaño del conjunto `k` fijo en 10, o debe adaptarse según la carga (por ejemplo, reducirse bajo alta carga de solicitudes) como permite BEP 6?
2. ¿Deben los receptores verificar el conjunto frente al hash de su propio destino y descartar los índices que no coincidan (protección contra emisores defectuosos o maliciosos)? Se recomienda: sí.
3. Elegir el *prefijo* de 4 bytes (bytes 0-3) como se muestra, o los últimos 4 bytes; cualquier ventana fija de 4 bytes ofrece las mismas propiedades; usar el prefijo mantiene el orden de bytes natural en el código de referencia (`hash[0:4]`).

## Estado de la técnica

- Referencia: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- Implementación de referencia en I2PSnark: `PeerState.sendAllowedFast()` /  
  `generateAllowedFastSet()` en  
  `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@since 0.9.71+)
- Funciona conjuntamente con BEP 40 (prioridad canónica de peers) y BEP 21 (seeds parciales), ambos compatibles con I2PSnark
