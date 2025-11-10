---
title: "소개자 만료"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Closed"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## 개요

이 제안서는 소개의 성공률을 높이기 위한 것입니다. [TRAC-TICKET]_을 참조하십시오.

## 동기

소개자는 일정 시간이 지나면 만료되지만, 그 정보는 [RouterInfo]_에 공개되지 않습니다. 현재 라우터는 소개자가 더 이상 유효하지 않은 시점을 추정하기 위해 발견법(휴리스틱)을 사용해야 합니다.

## 디자인

소개자를 포함한 SSU [RouterAddress]_에서 퍼블리셔는 선택적으로 각 소개자의 만료 시간을 포함할 수 있습니다.

## 사양

.. raw:: html

  {% highlight lang='dataspec' %}
iexp{X}={nnnnnnnnnn}

  X :: 소개자 번호 (0-2)

  nnnnnnnnnn :: 에포크 이후 초 단위 시간.
{% endhighlight %}

Notes
`````
* 각 만료는 [RouterInfo]_의 발행 날짜보다 커야 하며, RouterInfo 발행 날짜로부터 6시간 이내여야 합니다.

* 발행 라우터와 소개자는 만료 시점까지 소개자를 유효하게 유지하기 위해 노력해야 하지만, 이를 보장할 방법은 없습니다.

* 라우터는 만료 후 공개된 소개자를 사용해서는 안 됩니다.

* 소개자 만료는 [RouterAddress]_ 매핑에 있습니다.
  현재 사용되지 않는 [RouterAddress]_의 8바이트 만료 필드가 아닙니다.

예시: ``iexp0=1486309470``

## 마이그레이션

문제가 없습니다. 구현은 선택 사항입니다.
이전 라우터는 알 수 없는 매개변수를 무시하므로, 하위 호환성이 보장됩니다.

## 참고문헌

.. [RouterAddress]
    {{ ctags_url('RouterAddress') }}

.. [RouterInfo]
    {{ ctags_url('RouterInfo') }}

.. [TRAC-TICKET]
    http://{{ i2pconv('trac.i2p2.i2p') }}/ticket/1352
