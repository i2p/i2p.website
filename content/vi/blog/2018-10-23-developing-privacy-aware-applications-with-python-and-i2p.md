---
title: "Phát triển các ứng dụng chú trọng quyền riêng tư với Python và I2P"
date: 2018-10-23
author: "villain"
description: "Các khái niệm cơ bản về phát triển ứng dụng I2P bằng Python"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P) cung cấp một khuôn khổ để phát triển các ứng dụng chú trọng quyền riêng tư. Đó là một mạng ảo hoạt động trên nền Internet thông thường, nơi các nút có thể trao đổi dữ liệu mà không tiết lộ địa chỉ IP "thực" của mình. Các kết nối bên trong mạng I2P được thiết lập giữa các địa chỉ ảo gọi là *I2P destinations* (điểm đích I2P). Có thể có bao nhiêu destination tùy nhu cầu, thậm chí sử dụng một destination mới cho mỗi kết nối; chúng không tiết lộ bất kỳ thông tin nào về địa chỉ IP thực cho phía bên kia.

Bài viết này mô tả các khái niệm cơ bản mà bạn cần biết khi phát triển ứng dụng I2P. Các ví dụ mã được viết bằng Python, sử dụng framework (khung) bất đồng bộ tích hợp sẵn asyncio.

## Kích hoạt SAM API và cài đặt i2plib

I2P cung cấp nhiều API khác nhau cho các ứng dụng khách. Các ứng dụng client-server thông thường có thể dùng I2PTunnel, các proxy HTTP và Socks, các ứng dụng Java thường dùng I2CP. Khi phát triển bằng các ngôn ngữ khác, như Python, lựa chọn tốt nhất là [SAM](/docs/api/samv3/). SAM bị tắt theo mặc định trong bản triển khai client Java gốc, vì vậy chúng ta cần bật nó. Vào Router Console, trang "I2P internals" -> "Clients". Đánh dấu chọn "Run at Startup" và nhấn "Start", sau đó nhấn "Save Client Configuration".

![Bật SAM API](https://geti2p.net/images/enable-sam.jpeg)

[Triển khai C++ i2pd](https://i2pd.website) bật SAM theo mặc định.

Tôi đã phát triển một thư viện Python tiện dụng cho SAM API có tên là [i2plib](https://github.com/l-n-s/i2plib). Bạn có thể cài đặt nó bằng pip hoặc tải xuống mã nguồn từ GitHub một cách thủ công.

```bash
pip install i2plib
```
Thư viện này hoạt động với [framework bất đồng bộ asyncio](https://docs.python.org/3/library/asyncio.html) tích hợp sẵn của Python, vì vậy xin lưu ý rằng các ví dụ mã được lấy từ các hàm async (coroutines) đang chạy bên trong event loop (vòng lặp sự kiện). Các ví dụ bổ sung về cách sử dụng i2plib có thể được tìm thấy trong [kho mã nguồn](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## Tạo I2P Destination (đích I2P) và phiên

I2P destination (điểm đích I2P) thực chất là một tập hợp các khóa mã hóa và khóa chữ ký số. Các khóa công khai trong tập này được công bố lên mạng I2P và được dùng để thiết lập kết nối thay cho địa chỉ IP.

Đây là cách bạn tạo [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
Địa chỉ base32 là một mã băm được các nút khác dùng để tìm ra Destination đầy đủ của bạn trong mạng. Nếu bạn định dùng Destination này làm địa chỉ cố định trong chương trình của mình, hãy lưu dữ liệu nhị phân từ *dest.private_key.data* vào một tệp cục bộ.

Bây giờ bạn có thể tạo một phiên SAM, theo nghĩa đen là đưa Destination trực tuyến trong I2P:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Lưu ý quan trọng: Destination (đích I2P) sẽ vẫn trực tuyến khi socket *session_writer* được giữ mở. Nếu bạn muốn tắt nó, bạn có thể gọi *session_writer.close()*.

## Thiết lập kết nối ra ngoài

Bây giờ khi Destination (điểm đích) đã trực tuyến, bạn có thể dùng nó để kết nối tới các nút khác. Ví dụ, đây là cách bạn kết nối tới "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", gửi yêu cầu HTTP GET và đọc phản hồi (đó là máy chủ web "i2p-projekt.i2p"):

```python
remote_host = "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"
reader, writer = await i2plib.stream_connect(session_nickname, remote_host)

writer.write("GET /en/ HTTP/1.0\nHost: {}\r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
    data = await reader.read(buflen)
    if len(data) > 0:
        resp += data
    else:
        break

writer.close()
print(resp.decode())
```
## Chấp nhận kết nối đến

Trong khi việc tạo kết nối ra ngoài là đơn giản, khi bạn chấp nhận kết nối có một chi tiết quan trọng. Sau khi một client mới được kết nối, SAM API gửi một chuỗi ASCII chứa Destination của client được mã hóa base64 tới socket. Vì Destination và dữ liệu có thể đến trong một chunk (khối), bạn nên lưu ý điều này.

Một máy chủ PING-PONG đơn giản trông như sau. Nó chấp nhận kết nối đến, lưu Destination (địa chỉ đích trong I2P) của máy khách vào biến *remote_destination* và gửi lại chuỗi "PONG":

```python
async def handle_client(incoming, reader, writer):
    """Client connection handler"""
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not data:
        data = await reader.read(BUFFER_SIZE)
    if data == b"PING":
        writer.write(b"PONG")
    writer.close()

# An endless loop which accepts connetions and runs a client handler
while True:
    reader, writer = await i2plib.stream_accept(session_nickname)
    incoming = await reader.read(BUFFER_SIZE)
    asyncio.ensure_future(handle_client(incoming, reader, writer))
```
## Thông tin thêm

Bài viết này mô tả cách sử dụng một giao thức Streaming tương tự TCP. SAM API cũng cung cấp một giao thức tương tự UDP để gửi và nhận các datagram. Tính năng này sẽ được bổ sung vào i2plib sau này.

Đây chỉ là một số thông tin cơ bản, nhưng đủ để bạn bắt đầu dự án riêng của mình với I2P. Invisible Internet là một công cụ tuyệt vời để phát triển mọi loại ứng dụng chú trọng quyền riêng tư. Mạng không áp đặt ràng buộc thiết kế nào; các ứng dụng đó có thể theo mô hình máy khách - máy chủ cũng như ngang hàng (P2P).

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
