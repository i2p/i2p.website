---
title: "Quy trình Đề xuất I2P"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Tổng quan

Tài liệu này mô tả cách thay đổi các đặc tả I2P, cách hoạt động của các đề xuất I2P và mối quan hệ giữa các đề xuất I2P và các đặc tả.

Tài liệu này được điều chỉnh từ quy trình đề xuất Tor, và phần lớn nội dung bên dưới ban đầu được viết bởi Nick Mathewson.

Đây là một tài liệu thông tin.

## Động cơ

Trước đây, quy trình của chúng tôi để cập nhật các đặc tả I2P khá không chính thức: chúng tôi sẽ đưa ra một đề xuất trên diễn đàn phát triển và thảo luận các thay đổi, sau đó chúng tôi sẽ đạt sự đồng thuận và vá sửa đặc tả với các thay đổi dự thảo (không nhất thiết theo thứ tự đó), và cuối cùng chúng tôi sẽ triển khai các thay đổi.

Điều này đã gặp một số vấn đề.

Đầu tiên, ngay cả khi hiệu quả nhất, quy trình cũ sẽ thường xuyên khiến đặc tả không đồng bộ với mã. Các trường hợp tồi tệ nhất là nơi triển khai bị hoãn lại: đặc tả và mã có thể không đồng bộ trong nhiều phiên bản cùng một lúc.

Thứ hai, rất khó để tham gia vào thảo luận, vì không phải lúc nào cũng rõ phần nào của chuỗi thảo luận là một phần của đề xuất, hoặc những thay đổi nào đối với đặc tả đã được thực hiện. Các diễn đàn phát triển cũng chỉ truy cập được trong I2P, có nghĩa là các đề xuất chỉ có thể xem được bởi những người sử dụng I2P.

Thứ ba, rất dễ để quên một số đề xuất vì chúng sẽ bị chôn sâu vài trang trong danh sách chuỗi diễn đàn.

## Cách thay đổi các đặc tả bây giờ

Trước tiên, ai đó viết một tài liệu đề xuất. Nó nên mô tả thay đổi cần thực hiện một cách chi tiết, và đưa ra một số ý tưởng về cách triển khai nó. Khi nó được phát triển đủ, nó trở thành một đề xuất.

Giống như một RFC, mỗi đề xuất đều nhận được một số. Không giống như RFCs, các đề xuất có thể thay đổi theo thời gian và giữ nguyên số, cho đến khi chúng được chấp nhận hoặc từ chối. Lịch sử cho mỗi đề xuất sẽ được lưu trữ trong kho lưu trữ trang web I2P.

Khi một đề xuất đã có trong kho lưu trữ, chúng tôi nên thảo luận nó trên chuỗi tương ứng và cải thiện nó cho đến khi chúng tôi đạt được sự đồng thuận rằng đó là một ý tưởng tốt và nó đủ chi tiết để triển khai. Khi điều này xảy ra, chúng tôi triển khai đề xuất và đưa nó vào đặc tả. Do đó, đặc tả vẫn là tài liệu chính thức cho giao thức I2P: không có đề xuất nào từng là tài liệu chính thức cho một tính năng đã được triển khai.

(Quy trình này khá giống với Quy trình Nâng cao Python, với ngoại lệ chính là các đề xuất I2P được tích hợp lại vào các đặc tả sau khi triển khai, trong khi các PEP *trở thành* đặc tả mới.)

### Thay đổi nhỏ

Vẫn ổn khi thực hiện các thay đổi nhỏ trực tiếp vào đặc tả nếu mã có thể được viết ngay lập tức, hoặc những thay đổi thẩm mỹ nếu không cần thay đổi mã. Tài liệu này phản ánh *dự định* của các nhà phát triển hiện tại, không phải là một cam kết vĩnh viễn luôn sử dụng quy trình này trong tương lai: chúng tôi có quyền thực sự phấn khích và lao vào triển khai một cái gì đó trong một buổi hacking cả đêm với caffeine hoặc M&M.

## Cách thêm các đề xuất mới

Để gửi một đề xuất, đăng nó trên diễn đàn phát triển hoặc nhập một vé có kèm đề xuất.

Khi một ý tưởng đã được đề xuất, một bản dự thảo định dạng đúng (xem bên dưới) tồn tại, và sự đồng thuận sơ bộ trong cộng đồng phát triển hoạt động tồn tại cho rằng ý tưởng này đáng được xem xét, các biên tập viên đề xuất sẽ chính thức thêm đề xuất.

Các biên tập viên đề xuất hiện tại là zzz và str4d.

## Những gì nên có trong một đề xuất

Mỗi đề xuất nên có một tiêu đề chứa các trường sau:

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- Trường `author` nên chứa tên của các tác giả của đề xuất này.
- Trường `thread` nên là liên kết đến chuỗi diễn đàn phát triển nơi đề xuất này ban đầu được đăng, hoặc đến một chuỗi mới được tạo để thảo luận về đề xuất này.
- Trường `lastupdated` ban đầu nên bằng với trường `created`, và cần được cập nhật mỗi khi đề xuất được thay đổi.

Các trường này nên được thiết lập khi cần:

```
:supercedes:
:supercededby:
:editor:
```

- Trường `supercedes` là danh sách các đề xuất mà đề xuất này thay thế. Những đề xuất đó sẽ bị từ chối và phải có trường `supercededby` của chúng được thiết lập bằng số của đề xuất này.
- Trường `editor` nên được thiết lập nếu những thay đổi đáng kể được thực hiện đối với đề xuất này mà không làm thay đổi nội dung của nó một cách đáng kể. Nếu nội dung đang bị thay đổi một cách đáng kể, một tác giả bổ sung nên được thêm vào, hoặc một đề xuất mới được tạo thay thế đề xuất này.

Các trường này là tùy chọn nhưng được khuyến nghị:

```
:target:
:implementedin:
```

- Trường `target` nên mô tả phiên bản nào mà đề xuất này hy vọng sẽ được triển khai (nếu nó là `Open` hoặc `Accepted`).
- Trường `implementedin` nên mô tả phiên bản nào mà đề xuất này đã được triển khai (nếu nó là `Finished` hoặc `Closed`).

Nội dung của đề xuất nên bắt đầu với phần Tổng quan giải thích về cái gì mà đề xuất này làm, nó làm gì, và tình trạng của nó là gì.

Sau phần Tổng quan, đề xuất trở nên linh hoạt hơn. Tùy thuộc vào độ dài và độ phức tạp của nó, đề xuất có thể được chia thành các phần như thích hợp, hoặc theo một định dạng ngắn gọn. Mỗi đề xuất nên chứa ít nhất các thông tin sau trước khi được Chấp nhận, mặc dù thông tin không cần phải nằm trong các phần với những tên gọi này.

**Động cơ**
: Vấn đề mà đề xuất đang cố gắng giải quyết là gì? Tại sao vấn đề này quan trọng? Nếu có nhiều cách tiếp cận khả dĩ, tại sao chọn cách này?

**Thiết kế**
: Một cái nhìn ở mức cao về những tính năng mới hoặc đã được sửa đổi là gì, cách mà những tính năng mới hoặc đã được sửa đổi hoạt động, cách chúng tương tác với nhau, và cách chúng tương tác với phần còn lại của I2P. Đây là phần chính của đề xuất. Một số đề xuất sẽ bắt đầu chỉ với một Động cơ và một Thiết kế, và chờ đợi một đặc tả cho đến khi Thiết kế có vẻ đúng.

**Hệ quả bảo mật**
: Những ảnh hưởng mà các thay đổi được đề xuất có thể có đối với tính ẩn danh, mức độ hiểu biết về những ảnh hưởng này như thế nào, v.v.

**Đặc tả**
: Một mô tả chi tiết về những gì cần được thêm vào các đặc tả của I2P để triển khai đề xuất. Điều này nên chi tiết gần như đặc tả cuối cùng: các lập trình viên độc lập nên có khả toán để viết các triển khai tương thích của đề xuất dựa trên đặc tả của nó.

**Tương thích**
: Phiên bản I2P theo đề xuất sẽ tương thích với phiên bản không theo đề xuất không? Nếu có, cách nào để đạt được sự tương thích? Nói chung, chúng tôi cố gắng không làm mất sự tương thích nếu có thể; chúng tôi chưa thực hiện một thay đổi "ngày cờ" nào kể từ tháng 3 năm 2008, và chúng tôi không muốn thực hiện một thay đổi khác.

**Triển khai**
: Nếu đề xuất sẽ khó thực hiện trong kiến trúc hiện tại của I2P, tài liệu có thể chứa một số thảo luận về cách thực hiện. Các bản vá thực tế nên được đưa vào các nhánh công khai monotone, hoặc được tải lên Trac.

**Ghi chú về hiệu suất và khả năng mở rộng**
: Nếu tính năng sẽ có ảnh hưởng đến hiệu suất (trong RAM, CPU, băng thông) hoặc khả năng mở rộng, nên có một số phân tích về tác động này để chúng tôi có thể tránh các suy giảm hiệu suất tốn kém, và để chúng tôi có thể tránh lãng phí thời gian vào những cải tiến không đáng kể.

**Tham chiếu**
: Nếu đề xuất đề cập đến các tài liệu bên ngoài, chúng nên được liệt kê.

## Trạng thái của đề xuất

**Open**
: Một đề xuất đang được thảo luận.

**Accepted**
: Đề xuất đã hoàn thiện, và chúng tôi định triển khai nó. Sau thời điểm này, những thay đổi quan trọng đối với đề xuất nên được tránh, và được coi là dấu hiệu cho thấy quy trình đã thất bại ở đâu đó.

**Finished**
: Đề xuất đã được chấp nhận và triển khai. Sau thời điểm này, đề xuất không nên thay đổi.

**Closed**
: Đề xuất đã được chấp nhận, triển khai và tích hợp vào các tài liệu đặc tả chính. Đề xuất không nên thay đổi sau thời điểm này.

**Rejected**
: Chúng tôi sẽ không triển khai tính năng như mô tả trong đây, mặc dù chúng tôi có thể thực hiện một phiên bản khác. Xem các nhận xét trong tài liệu để biết chi tiết. Đề xuất không nên thay đổi sau thời điểm này; để đưa ra một phiên bản khác của ý tưởng, hãy viết một đề xuất mới.

**Draft**
: Đây chưa phải là một đề xuất hoàn chỉnh; còn thiếu những phần rõ ràng. Xin đừng thêm bất kỳ đề xuất mới nào với trạng thái này; đưa chúng vào thư mục "ideas".

**Needs-Revision**
: Ý tưởng cho đề xuất là tốt, nhưng đề xuất hiện tại có những vấn đề nghiêm trọng khiến nó không thể được chấp nhận. Xem nhận xét trong tài liệu để biết chi tiết.

**Dead**
: Đề xuất đã không được cập nhật trong một thời gian dài, và không có vẻ ai đó sẽ hoàn thành nó sớm. Nó có thể trở lại trạng thái "Open" nếu có một người đề xướng mới.

**Needs-Research**
: Có những vấn đề nghiên cứu cần được giải quyết trước khi rõ ràng liệu đề xuất có phải là một ý tưởng tốt không.

**Meta**
: Đây không phải là một đề xuất, mà là một tài liệu về các đề xuất.

**Reserve**
: Đề xuất này không phải là thứ mà chúng tôi đang có kế hoạch triển khai, nhưng chúng tôi có thể muốn phục hồi nó một ngày nào đó nếu chúng tôi quyết định thực hiện một cái gì đó như những gì nó đề xuất.

**Informational**
: Đề xuất này là từ cuối cùng về những gì nó đang làm. Nó sẽ không trở thành một đặc tả trừ khi ai đó sao chép và dán nó vào một đặc tả mới cho một hệ thống con mới.

Các biên tập viên duy trì trạng thái đúng của các đề xuất, dựa trên sự đồng thuận sơ bộ và sự quyết định của họ.

## Đánh số đề xuất

Số 000-099 được dành riêng cho các đề xuất đặc biệt và meta. Từ 100 trở lên được sử dụng cho các đề xuất thực tế. Số không được tái sử dụng.

## Tham chiếu

- [Quy trình Đề xuất Tor](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
