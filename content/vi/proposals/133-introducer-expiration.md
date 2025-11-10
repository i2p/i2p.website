---
title: "Giới thiệu Hết hạn"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Closed"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Tổng quan

Đề xuất này nhằm cải thiện tỷ lệ thành công cho việc giới thiệu. Xem
[TRAC-TICKET]_.


## Động lực

Người giới thiệu hết hạn sau một thời gian nhất định, nhưng thông tin đó không được công bố trong
[RouterInfo]_. Các router hiện tại phải sử dụng các phương pháp suy đoán để ước tính khi nào một người giới thiệu không còn hợp lệ.


## Thiết kế

Trong một [RouterAddress]_ SSU chứa người giới thiệu, nhà phát hành có thể tùy chọn
bao gồm thời gian hết hạn cho mỗi người giới thiệu.


## Đặc tả

.. raw:: html

  {% highlight lang='dataspec' %}
iexp{X}={nnnnnnnnnn}

  X :: Số của người giới thiệu (0-2)

  nnnnnnnnnn :: Thời gian tính bằng giây (không phải ms) kể từ kỷ nguyên.
{% endhighlight %}

Ghi chú
`````
* Mỗi thời gian hết hạn phải lớn hơn ngày công bố của [RouterInfo]_,
  và nhỏ hơn 6 giờ sau ngày công bố của RouterInfo.

* Các router phát hành và người giới thiệu nên cố gắng giữ cho người giới thiệu còn hợp lệ
  cho đến khi hết hạn, tuy nhiên không có cách nào để đảm bảo điều này.

* Các router không nên sử dụng một người giới thiệu sau khi hết hạn.

* Thời gian hết hạn của người giới thiệu nằm trong ánh xạ [RouterAddress]_.
  Chúng không phải là trường hết hạn (hiện không được sử dụng) 8-byte trong [RouterAddress]_.

Ví dụ: ``iexp0=1486309470``


## Di cư

Không có vấn đề. Việc triển khai là tùy chọn.
Tương thích ngược được đảm bảo, vì các router cũ sẽ bỏ qua các tham số không xác định.



## Tài liệu tham khảo

.. [RouterAddress]
    {{ ctags_url('RouterAddress') }}

.. [RouterInfo]
    {{ ctags_url('RouterInfo') }}

.. [TRAC-TICKET]
    http://{{ i2pconv('trac.i2p2.i2p') }}/ticket/1352
