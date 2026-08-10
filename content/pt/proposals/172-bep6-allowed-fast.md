---
title: "Extensão Rápida (BEP 6) Rápido Permitido com Identidade de Par por Hash de Destino"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Rascunho"
toc: true
---

## Visão geral

O BEP 6 (Extensão Rápida) inclui cinco recursos: **Have All / Have None**, **Reject Requests**, **Suggestions** e **Allowed Fast**. O protocolo de comunicação — bit de negociação, IDs de mensagens e semântica de choke — é independente do transporte e funciona inalterado sobre o streaming I2P. A única parte do BEP 6 que não pode ser mapeada diretamente para o I2P é a **geração do conjunto Allowed Fast**, pois ela é definida em termos do endereço IPv4 do peer. Os peers I2P não possuem IPs; eles são identificados por hashes de destino de 32 bytes.

Esta proposta padroniza a geração de conjuntos "Allowed Fast" nativos do I2P, de modo que todos os clientes de torrent I2P gerem conjuntos *idênticos* de allowed fast para o mesmo par e torrent, tornando o recurso útil (e verificável) entre diferentes implementações.

## Motivação

Novos pares precisam dos primeiros blocos antes que o sistema de troca justa do BitTorrent possa acelerar. Na I2P, essa aceleração é mais lenta do que na rede clara: a configuração da conexão e a entrega de blocos atravessam vários saltos em túneis de alta latência, tornando o intervalo entre a conexão e o primeiro desbloqueio recíproco mais longo. O "Allowed Fast" ataca diretamente esse intervalo — um par inicial tem permissão para receber um pequeno número de blocos mesmo quando está bloqueado, recebe dados imediatamente e pode começar a retribuir mais cedo.

O BEP 6 de referência calcula o conjunto rápido permitido a partir do endereço IPv4 do par para garantir que o *remetente* possa escolher partes únicas para o *receptor* (um usuário com muitos IPs não pode coletar muitos conjuntos). No I2P, o hash de destino do par desempenha o mesmo papel de vinculação e está disponível em ambas as extremidades de cada conexão, o que torna o conjunto determinístico *e localmente verificável* — algo que o esquema baseado em IP não pode oferecer.

## Modificações para BEP 6

A negociação da extensão rápida e todos os quatro tipos de mensagens são adotados inalterados:

- Negociação: terceiro bit menos significativo do último byte reservado, `reserved[7] |= 0x04`, em ambas as extremidades
- Tem Tudo `<len=0x0001><op=0x0E>`, Não Tem Nenhum `<len=0x0001><op=0x0F>`
- Sugerir Pedaço `<len=0x0005><op=0x0D><index>`
- Rejeitar Solicitação `<len=0x000D><op=0x10><index><begin><length>`
- Rápido Permitido `<len=0x0005><op=0x11><index>`
- Cada solicitação resulta em exatamente uma resposta (pedaço ou rejeição); estrangulamento não rejeita mais implicitamente solicitações pendentes

O único desvio está na geração do conjunto Allowed Fast, substituindo os bytes do IP pelos bytes do hash do destino do par.

### Desvio: bytes de hash em vez de IP mascarado

Consulte o BEP 6, passo (1):

```
x = 0xFFFFFF00 & ip
```
Isso utiliza três bytes do endereço IPv4 do par e **zera o 4º byte**. Esta é uma heurística de sub-rede: usuários que conseguem obter múltiplos IPs na mesma sub-rede /24 não devem obter múltiplos conjuntos rápidos permitidos.

A nossa versão do I2P substitui isso pelos primeiros quatro bytes do hash de destino de 32 bytes do peer:

```
x = first 4 bytes of peer destination hash
```
A distinção em relação à implementação de referência:

> "São 3 bytes do IP seguidos por um zero. Você tem 4 bytes do hash. É diferente do BEP 6 porque não há IP e não está zerando o 4º byte."

Ambas as extremidades de uma conexão I2P já conhecem o hash de destino do par (é o endereço ao qual a conexão foi feita/dele), portanto, isso não exige troca adicional, descoberta de NAT ou detecção de IP externo — nenhum dos quais existe no I2P.

### Algoritmo de geração rápida permitido

Seja `hash` o hash de destino de 32 bytes do par receptor, `infohash` o infohash do torrent de 20 bytes, `sz` o número de partes no torrent, `k` o número final de partes no conjunto de envio rápido permitido (10, conforme BEP 6) e `a` o conjunto de saída:

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

- 4 bytes do hash de destino substituem os 3 bytes IP mascarados. Todos os quatro bytes carregam entropia do hash; nenhum é zerado.
- Como no BEP 6, a cadeia SHA1 produz uma sequência pseudorrandômica longa, particionada em índices de pedaços; `k = 10` corresponde ao padrão de referência.
- A mensagem Allowed Fast é apenas orientativa: o receptor NÃO DEVE interpretá-la como indicação de que o remetente possui o pedaço — somente que o remetente fornecerá esse pedaço enquanto estiver sufocado.

## Benefícios

| Área              | Benefício                                                                                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Latência de inicialização | Novos pares baixam os primeiros pedaços mesmo quando bloqueados, reduzindo a rampa de troca lenta típica de túneis I2P de múltiplos saltos                                                                       |
| Determinismo       | O conjunto é uma função pura do hash de destino + infohash, portanto qualquer implementação calcula o mesmo conjunto — diferentemente do BEP 6 baseado em IP, onde a visão do remetente sobre o IP do receptor pode diferir (NAT) |
| Verificabilidade   | O par receptor conhece seu próprio hash de destino e pode recomputar localmente e validar o conjunto, detectando remetentes com comportamento incorreto                                                               |
| Sem mecanismos IP  | Sem necessidade de traversão de NAT, descoberta de IP externo ou heurísticas de sub-rede — todos esses mecanismos são impossíveis ou sem sentido no I2P                                                             |
| Vinculação à identidade | Um único conjunto rápido permitido por destino. Um usuário com muitos destinos obtém um conjunto para cada um — a mesma propriedade anti-manipulação fornecida pela máscara de IP na rede clara                                        |
| Privacidade        | Nenhum endereço IP é transmitido ou implícito no cálculo                                                                                                                               |
| Largura de banda   | "Tem Tudo" / "Não Tem Nenhum" substitui o campo de bits completo em torrents grandes; "Reject" elimina requisições redundantes                                                                                       |
## Considerações sobre implementação

- **Identidade do par**: o hash de destino do par é obtido a partir da conexão de streaming (o destino da sessão) e é o mesmo valor usado por ambas as extremidades. Para conexões de saída, use o destino ao qual você se conectou; para conexões de entrada, use o destino de onde a conexão veio.
- **Negociação**: envie `reserved[7] |= 0x04` no handshake; envie mensagens Fast Extension apenas se o handshake do par também tiver definido esse bit; se um par enviar mensagens Fast Extension sem negociação, feche a conexão.
- **Have All / Have None**: envie exatamente um dos três — bitfield, Have All ou Have None — imediatamente após o handshake. Use Have All para seeds e Have None até a primeira peça.
- **Lado que envia Allowed Fast**: anuncie apenas peças que você realmente possui; o receptor pode solicitá-las mesmo quando estiver choked. Limite o conjunto *servido* (por exemplo, rejeite solicitações allowed-fast de um par que já possui mais de `k` peças, conforme orientação da BEP 6).
- **Lado que recebe Allowed Fast**: armazene o conjunto; permita solicitações para essas peças mesmo quando choked; opcionalmente, verifique o conjunto recalculando-o a partir do seu próprio hash de destino e do infohash, e ignore peças que não estejam no conjunto calculado.
- **Reject**: cada solicitação DEVE receber exatamente uma resposta; ao ser choked, rejeite tudo o que não estiver no conjunto allowed fast, em vez de silenciar silenciosamente o par.
- **Tamanho do conjunto**: use `k = 10` para compatibilidade; pares podem escolher um valor menor de `k` sob carga, mas ambas as extremidades devem anunciar apenas o que realmente irão servir.
- **Limite da peça**: `index = y % sz` deve usar a contagem total de peças do torrent `sz`; ignore índices >= sz (medida defensiva), já que uma cadeia de hash não é limitada por faixa de peças.
- **Compatibilidade reversa**: clientes que não negociarem o bit fast simplesmente nunca verão essas mensagens; nenhuma outra alteração de protocolo é necessária.

## Implementações de referência

O algoritmo é pequeno e autossuficiente — algumas dezenas de linhas em qualquer linguagem. Os três exemplos abaixo calculam o mesmo conjunto para entradas idênticas (`hash[0:4] ++ infohash`, cadeia SHA1, `y % sz`, com `k = 10`).

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
## Compatibilidade

- **Compatível com o protocolo**: o bit de negociação e os formatos de mensagem são byte-a-byte idênticos ao BEP 6 da rede clara; apenas a entrada para geração do conjunto difere.
- **Não interoperável entre redes**: um cliente I2P e um cliente da rede clara não podem se conectar entre si de qualquer forma; a divergência afeta apenas os bytes de identidade do par, nunca o formato do protocolo.
- **Dentro do I2P**: qualquer cliente que implemente esta proposta calcula conjuntos rápidos permitidos idênticos e pode fornecê-los e verificá-los de forma intercambiável. Clientes que ignoram o Allowed Fast simplesmente o tratam como uma recomendação sem efeito e perdem apenas o benefício de inicialização.

## Perguntas em aberto

1. O tamanho do conjunto `k` deve permanecer fixo em 10, ou deve ser adaptativo conforme a carga (por exemplo, menor sob alta carga de solicitações), conforme permitido pelo BEP 6?
2. Os destinatários devem verificar o conjunto contra seu próprio hash de destino e descartar índices incompatíveis (proteção contra remetentes com defeito ou maliciosos)? Recomenda-se sim.
3. Escolher o *prefixo* de 4 bytes (bytes 0-3) conforme mostrado, ou os últimos 4 bytes — qualquer janela fixa de 4 bytes produz as mesmas propriedades; o prefixo mantém a ordem natural dos bytes no código de referência (`hash[0:4]`).

## Técnica anterior

- Referência: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- Implementação de referência do I2PSnark: `PeerState.sendAllowedFast()` / `generateAllowedFastSet()` em `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@since 0.9.71+)
- Funciona em conjunto com BEP 40 (prioridade canônica de peers) e BEP 21 (sementes parciais), ambos suportados pelo I2PSnark
