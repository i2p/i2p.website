---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Rejected"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Tổng quan

Đề xuất này phác thảo API2 cho I2PControl.

Đề xuất này đã bị từ chối và sẽ không được triển khai, vì nó phá vỡ khả năng tương thích ngược.
Xem liên kết thảo luận để biết chi tiết.

### Thông báo đến nhà phát triển!

Tất cả các tham số RPC giờ đây sẽ viết thường. Điều này *sẽ* phá vỡ khả năng
tương thích ngược với các triển khai API1. Lý do cho điều này là để cung cấp
cho người dùng từ >=API2 với API đơn giản nhất và nhất quán nhất có thể.


## Đặc tả API 2

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### Tham số

**`"id"`**

Số id hoặc yêu cầu. Dùng để xác định phản hồi nào đã được sinh ra bởi yêu cầu nào.

**`"method_name"`**

Tên của RPC đang được gọi.

**`"auth_token"`**

Mã thông báo xác thực phiên. Cần được cung cấp với mọi RPC ngoại trừ cuộc gọi 'authenticate'.

**`"method_parameter_value"`**

Tham số phương thức. Dùng để cung cấp các phiên bản khác nhau của một phương thức. Như 'get', 'set' và các phiên bản tương tự.

**`"result_value"`**

Giá trị mà RPC trả về. Loại và nội dung của nó phụ thuộc vào phương thức và phương thức nào.


### Tiền tố

Quy tắc đặt tên RPC tương tự như cách thực hiện trong CSS, với tiền tố của nhà cung cấp
cho các triển khai API khác nhau (i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
i2p.XXX.YYY.ZZZ
i2pd.XXX.YYY.ZZZ
kovri.XXX.YYY.ZZZ
```

Ý tưởng chung với tiền tố đặc trưng cho nhà cung cấp là cho phép một số linh hoạt
và để các triển khai phát triển mà không phải chờ đợi các triển khai khác
bắt kịp. Nếu một RPC được triển khai bởi tất cả các triển khai, nhiều tiền tố của nó có thể bị xóa bỏ và nó có thể được bao gồm như một RPC lõi trong phiên bản API tiếp theo.


### Hướng dẫn đọc phương thức

 * **rpc.method**

   * *parameter* [kiểu tham số]:  [null], [number], [string], [boolean],
     [array] hoặc [object]. [object] là một bản đồ {key:value}.
  * Trả về:

```text
"return_value" [string] // Đây là giá trị được trả về bởi cuộc gọi RPC
```


### Phương thức

* **authenticate** - Với điều kiện mật khẩu đúng được cung cấp, phương thức này cung cấp cho bạn một mã thông báo để truy cập thêm và danh sách các cấp độ API hỗ trợ.

  * *password* [string]:  Mật khẩu cho triển khai i2pcontrol này

    Trả về:
```text
    [object]
    {
      "token" : [string], // Mã thông báo sẽ được sử dụng cung cấp với tất cả các phương thức RPC khác
      "api" : [[int],[int], ...]  // Danh sách các cấp độ API hỗ trợ.
    }
```


* **control.** - Kiểm soát i2p

  * **control.reseed** - Bắt đầu tải xuống lại

    * [nil]: Không cần tham số

    Trả về:
```text
      [nil]
```

  * **control.restart** - Khởi động lại phiên bản i2p

    * [nil]: Không cần tham số

    Trả về:
```text
      [nil]
```

  * **control.restart.graceful** - Khởi động lại phiên bản i2p một cách nhã nhặn

    * [nil]: Không cần tham số

    Trả về:
```text
      [nil]
```

  * **control.shutdown** - Tắt phiên bản i2p

    * [nil]: Không cần tham số

    Trả về:
```text
      [nil]
```

  * **control.shutdown.graceful** - Tắt phiên bản i2p một cách nhã nhặn

    * [nil]: Không cần tham số

    Trả về:
```text
      [nil]
```

  * **control.update.find** - **KHỐI** Tìm kiếm bản cập nhật có chữ ký

    * [nil]: Không cần tham số

    Trả về:
```text
      true [boolean] // Đúng nếu có bản cập nhật có chữ ký
```

  * **control.update.start** - Bắt đầu quá trình cập nhật

    * [nil]: Không cần tham số

    Trả về:
```text
      [nil]
```


* **i2pcontrol.** - Cấu hình i2pcontrol

  * **i2pcontrol.address** - Nhận/Đặt địa chỉ IP mà i2pcontrol lắng nghe.

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Đây sẽ là một địa chỉ IP như "0.0.0.0" hoặc "192.168.0.1"

    Trả về:
```text
      [nil]
```

  * **i2pcontrol.password** - Đổi mật khẩu i2pcontrol.

    * *set* [string]: Đặt mật khẩu mới cho chuỗi này

    Trả về:
```text
      [nil]
```

  * **i2pcontrol.port** - Nhận/Đặt cổng mà i2pcontrol lắng nghe.

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      7650 [number]
```

    * *set* [number]: Thay đổi cổng mà i2pcontrol lắng nghe đến cổng này

    Trả về:
```text
      [nil]
```


* **settings.** - Nhận/Đặt cấu hình phiên bản i2p

  * **settings.advanced** - Cài đặt nâng cao

    * *get*  [string]: Nhận giá trị của cài đặt này

    Trả về:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    Trả về:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: Đặt giá trị của cài đặt này
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    Trả về:
```text
      [nil]
```

  * **settings.bandwidth.in** - Cài đặt băng thông đầu vào
  * **settings.bandwidth.out** - Cài đặt băng thông đầu ra

    * *get* [nil]: Tham số này không cần phải đặt.

    Trả về:
```text
      0 [number]
```

    * *set* [number]: Đặt giới hạn băng thông

    Trả về:
```text
     [nil]
```

  * **settings.ntcp.autoip** - Nhận cài đặt tự động phát hiện IP cho NTCP

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - Nhận tên máy chủ NTCP

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Đặt tên máy chủ mới

    Trả về:
```text
      [nil]
```

  * **settings.ntcp.port** - Cổng NTCP

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      0 [number]
```

    * *set* [number]: Đặt cổng NTCP mới.

    Trả về:
```text
      [nil]
```

    * *set* [boolean]: Đặt tự động phát hiện IP cho NTCP

    Trả về:
```text
      [nil]
```

  * **settings.ssu.autoip** - Cấu hình cài đặt tự động phát hiện IP cho SSU

    * *get* [nil]: Tham số này không cần phải đặt.

    Trả về:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - Cấu hình tên máy chủ SSU

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Đặt tên máy chủ SSU mới

    Trả về:
```text
      [nil]
```

  * **settings.ssu.port** - Cổng SSU

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      0 [number]
```

    * *set* [number]: Đặt cổng SSU mới.

    Trả về:
```text
      [nil]
```

    * *set* [boolean]: Đặt tự động phát hiện IP cho SSU

    Trả về:
```text
      [nil]
```

  * **settings.share** - Nhận tỷ lệ chia sẻ băng thông

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      0 [number] // Tỷ lệ chia sẻ băng thông (0-100)
```

    * *set* [number]: Đặt tỷ lệ chia sẻ băng thông (0-100)

    Trả về:
```text
      [nil]
```

  * **settings.upnp** - Bật hoặc tắt UPNP

    * *get* [nil]: Tham số này không cần phải đặt.

    Trả về:
```text
      true [boolean]
```

    * *set* [boolean]: Đặt tự động phát hiện IP cho SSU

    Trả về:
```text
      [nil]
```



* **stats.** - Nhận thống kê từ phiên bản i2p

  * **stats.advanced** - Phương thức này cung cấp quyền truy cập vào tất cả các thống kê được giữ trong phiên bản.

    * *get* [string]:  Tên của thống kê nâng cao cần cung cấp
    * *Tùy chọn:* *period* [number]:  Thời kỳ cho thống kê yêu cầu

  * **stats.knownpeers** - Trả về số lượng peers đã biết
  * **stats.uptime** - Trả về thời gian bằng ms kể từ khi router khởi động
  * **stats.bandwidth.in** - Trả về băng thông đầu vào (lý tưởng cho giây cuối cùng)
  * **stats.bandwidth.in.total** - Trả về số byte nhận được kể từ lần khởi động lại cuối cùng
  * **stats.bandwidth.out** - Trả về băng thông đầu ra (lý tưởng cho giây cuối cùng)'
  * **stats.bandwidth.out.total** - Trả về số byte đã gửi kể từ lần khởi động lại cuối cùng'
  * **stats.tunnels.participating** - Trả về số lượng đường hầm tham gia hiện tại
  * **stats.netdb.peers.active** - Trả về số lượng peers mà chúng tôi đã liên lạc gần đây
  * **stats.netdb.peers.fast** - Trả về số lượng peers 'nhanh'
  * **stats.netdb.peers.highcapacity** - Trả về số lượng peers 'cao năng suất'
  * **stats.netdb.peers.known** - Trả về số lượng peers đã biết

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      0.0 [number]
```


* **status.** - Nhận trạng thái phiên bản i2p

  * **status.router** - Nhận trạng thái của router

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      "status" [string]
```

  * **status.net** - Nhận trạng thái mạng của router

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – ĐANG THỬ NGHIỆM
       *    2 – BỊ CHẶN TƯỜNG LỬA
       *    3 – ẨN
       *    4 – CẢNH BÁO_TƯỜNG_LỎA_VÀ_NHANH
       *    5 – CẢNH BÁO_TƯỜNG_LỎA_VÀ_NỀN
       *    6 – CẢNH BÁO_TƯỜNG_LỎA_VỚI_TCP_INBOUND
       *    7 – CẢNH BÁO_TƯỜNG_LỎA_VỚI_UDP_Vô_HIỆU_HÓA
       *    8 – LỖI_I2CP
       *    9 – LỖI_ĐỘ_LỆCH_ĐỒNG_HỒ
       *   10 – LỖI_ĐỊA_CHỈ_TCP_RIENG
       *   11 – LỖI_NAT_ĐỐI_XỨNG
       *   12 – LỖI_CỔNG_UDP_TRONG_SỬ_DỤNG
       *   13 – LỖI_KHÔNG_CÓ_PEERS_CHỦ_ĐỘNG_KIỂM_TRA_KẾT_NỐI_VÀ_TƯỜNG_LỎA
       *   14 – LỖI_UDP_Vô_HIỆU_HÓA_VÀ_TCP_CHƯA_ĐẶT
       */
```

  * **status.isfloodfill** - Instance i2p hiện tại có phải là floodfill không

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      true [boolean]
```

  * **status.isreseeding** - Instance i2p hiện tại có đang tải xuống lại không

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      true [boolean]
```

  * **status.ip** - IP công khai phát hiện của instance i2p này

    * *get* [null]: Tham số này không cần phải đặt.

    Trả về:
```text
      "0.0.0.0" [string]
```
