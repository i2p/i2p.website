---
title: "Đặc Tả Plugin"
description: "Quy tắc đóng gói .xpi2p / .su3 cho các plugin I2P"
slug: "plugin"
aliases:
  - "/vi/plugin_spec"
  - "/vi/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Tổng quan

Tài liệu này quy định định dạng tệp .xpi2p (giống như .xpi của Firefox), nhưng với tệp mô tả plugin.config đơn giản thay vì tệp XML install.rdf. Định dạng tệp này được sử dụng cho cả việc cài đặt plugin ban đầu và cập nhật plugin.

Ngoài ra, tài liệu này cung cấp một tổng quan ngắn gọn về cách router cài đặt plugin và các chính sách cũng như hướng dẫn dành cho các nhà phát triển plugin.

Định dạng tệp .xpi2p cơ bản giống như tệp i2pupdate.sud (định dạng được sử dụng cho các bản cập nhật router), nhưng trình cài đặt sẽ cho phép người dùng cài đặt addon ngay cả khi chưa biết khóa của người ký.

Từ phiên bản 0.9.15 trở đi, định dạng file SU3 được hỗ trợ và được ưu tiên sử dụng. Định dạng này cho phép sử dụng các khóa ký mạnh hơn.

> **Lưu ý:** Chúng tôi không khuyến nghị phân phối các plugin ở định dạng xpi2p nữa. Hãy sử dụng định dạng su3.

Cấu trúc thư mục chuẩn sẽ cho phép người dùng cài đặt các loại addon sau:

- Ứng dụng web Console
- Eepsite mới với cgi-bin, webapp
- Giao diện Console
- Bản dịch Console
- Chương trình Java
- Chương trình Java trong JVM riêng biệt
- Bất kỳ shell script hoặc chương trình nào

Một plugin sẽ cài đặt tất cả các tệp của nó trong `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` trên Windows). Trình cài đặt sẽ ngăn không cho cài đặt ở bất kỳ nơi nào khác, mặc dù plugin có thể truy cập các thư viện ở nơi khác khi đang chạy.

Điều này chỉ nên được xem như một cách để việc cài đặt, gỡ cài đặt và nâng cấp trở nên dễ dàng hơn, đồng thời giảm thiểu các xung đột cơ bản giữa các plugin.

Tuy nhiên, về cơ bản không có mô hình bảo mật nào khi plugin đang chạy. Plugin chạy trong cùng JVM và với các quyền tương tự như router, đồng thời có quyền truy cập đầy đủ vào hệ thống file, router, thực thi các chương trình bên ngoài, v.v.

## Chi tiết

foo.xpi2p là một tệp cập nhật có chữ ký (sud) chứa các nội dung sau:

Header .sud tiêu chuẩn được thêm vào đầu tệp zip, chứa các thông tin sau:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
File zip chứa các nội dung sau:

### tệp plugin.config

Tệp này là bắt buộc. Đây là tệp cấu hình I2P tiêu chuẩn, chứa các thuộc tính sau:

#### Thuộc Tính Bắt Buộc

Bốn thuộc tính sau đây là bắt buộc. Ba thuộc tính đầu tiên phải giống hệt với những thuộc tính trong plugin đã cài đặt để có thể cập nhật plugin.

-   **name** - Sẽ được cài đặt trong thư mục có tên này. Đối với native plugins, bạn có thể muốn sử dụng tên riêng biệt trong các gói khác nhau - ví dụ foo-windows và foo-linux.
-   **key** - Khóa công khai DSA dưới dạng 172 ký tự B64 kết thúc bằng '='. Bỏ qua đối với định dạng SU3.
-   **signer** - khuyến nghị dùng yourname@mail.i2p
-   **version** - Phải ở định dạng mà VersionComparator có thể phân tích, ví dụ 1.2.3-4. Tối đa 16 bytes (phải khớp với phiên bản sud). Các ký tự phân cách số hợp lệ là '.', '-', và '_'. Phiên bản này phải lớn hơn phiên bản trong plugin đã cài đặt để thực hiện cập nhật plugin.

#### Thuộc tính Hiển thị

Các giá trị cho những thuộc tính sau đây sẽ được hiển thị trên /configplugins trong bảng điều khiển router nếu có:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` được khuyến nghị
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - Trình kiểm tra cập nhật sẽ kiểm tra các byte 41-56 tại URL này để xác định xem có phiên bản mới hơn hay không. Từ phiên bản 1.7.0 (0.9.53), có thể sử dụng các biến `$OS` và `$ARCH` trong URL. Không khuyến nghị. Không sử dụng trừ khi bạn đã phân phối plugin trước đó ở định dạng xpi2p.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - Vị trí của tệp cập nhật định dạng su3, từ phiên bản 0.9.15. Từ phiên bản 1.7.0 (0.9.53), có thể sử dụng các biến `$OS` và `$ARCH` trong URL.
-   **description** - bằng tiếng Anh
-   **description_xx** - cho ngôn ngữ xx
-   **license** - Giấy phép plugin
-   **disableStop=true** - Mặc định false. Nếu true, nút dừng sẽ không được hiển thị. Sử dụng khi không có webapp và không có client nào với stopargs.

#### Thuộc tính Liên kết Thanh Tóm tắt Console

Các thuộc tính sau được sử dụng để thêm liên kết trên thanh tóm tắt console:

-   **consoleLinkName** - sẽ được thêm vào thanh tóm tắt
-   **consoleLinkName_xx** - cho ngôn ngữ xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - được hỗ trợ từ phiên bản 0.7.12-6
-   **consoleLinkTooltip_xx** - ngôn ngữ xx từ phiên bản 0.7.12-6

#### Thuộc tính Biểu tượng Console

Các thuộc tính tùy chọn sau có thể được sử dụng để thêm biểu tượng tùy chỉnh trên console:

-   **console-icon** - được hỗ trợ từ phiên bản 0.9.20. Chỉ dành cho webapps. Đường dẫn đến hình ảnh 32x32, ví dụ /icon.png. Từ phiên bản 1.7.0 (API 0.9.53), nếu consoleLinkURL được chỉ định, đường dẫn sẽ tương đối so với URL đó. Ngược lại, nó sẽ tương đối so với tên webapp. Áp dụng cho tất cả webapps trong plugin.
-   **icon-code** - được hỗ trợ từ phiên bản 0.9.25. Cung cấp biểu tượng console cho các plugin không có tài nguyên web. Một chuỗi B64 được tạo bằng cách gọi `net.i2p.data.Base64 encode FILE` trên một tệp hình ảnh png 32x32.

#### Thuộc tính Trình cài đặt

Các thuộc tính sau được sử dụng bởi trình cài đặt plugin:

-   **type** - app/theme/locale/webapp/... (chưa được triển khai, có thể không cần thiết)
-   **min-i2p-version** - Phiên bản I2P tối thiểu mà plugin này yêu cầu
-   **max-i2p-version** - Phiên bản I2P tối đa mà plugin này có thể chạy trên đó
-   **min-java-version** - Phiên bản Java tối thiểu mà plugin này yêu cầu
-   **min-jetty-version** - được hỗ trợ từ 0.8.13, sử dụng 6 cho webapps Jetty 6
-   **max-jetty-version** - được hỗ trợ từ 0.8.13, sử dụng 5.99999 cho webapps Jetty 5
-   **required-platform-OS** - chưa được triển khai - có thể sẽ chỉ hiển thị, không được xác minh
-   **other-requirements** - chưa được triển khai, ví dụ python x.y - không được xác minh bởi trình cài đặt, chỉ hiển thị cho người dùng
-   **dont-start-at-install=true** - Mặc định false. Sẽ không khởi động plugin khi nó được cài đặt hoặc cập nhật.
-   **router-restart-required=true** - Mặc định false. Điều này không khởi động lại router hoặc plugin khi cập nhật, nó chỉ thông báo cho người dùng rằng cần khởi động lại.
-   **update-only=true** - Mặc định false. Nếu true, sẽ thất bại nếu một cài đặt không tồn tại.
-   **install-only=true** - Mặc định false. Nếu true, sẽ thất bại nếu một cài đặt tồn tại.
-   **min-installed-version** - để cập nhật lên, nếu một cài đặt tồn tại
-   **max-installed-version** - để cập nhật lên, nếu một cài đặt tồn tại
-   **depends=plugin1,plugin2,plugin3** - chưa được triển khai
-   **depends-version=0.3.4,,5.6.7** - chưa được triển khai

#### Thuộc Tính Dịch Thuật

-   **langs=xx,yy,Klingon,...** - (chưa được triển khai) (yy là cờ quốc gia)

### Thư mục và Tệp Ứng dụng

Mỗi thư mục hoặc tệp sau đây là tùy chọn, nhưng phải có ít nhất một cái gì đó ở đó nếu không nó sẽ không làm gì cả:

**console/**

-   **locale/** - Chỉ các file jar chứa resource bundles mới (bản dịch) cho các ứng dụng trong bản cài đặt I2P cơ bản. Các bundles cho plugin này nên được đặt bên trong console/webapp/foo.war hoặc lib/foo.jar
-   **themes/** - Các theme mới cho router console. Đặt mỗi theme trong một thư mục con riêng.
-   **webapps/** - (Xem ghi chú quan trọng bên dưới về webapps) .wars - Các file này sẽ được chạy tại thời điểm cài đặt trừ khi bị vô hiệu hóa trong webapps.config. Tên war không cần phải giống với tên plugin. Không được trùng lặp tên war trong bản cài đặt I2P cơ bản.
-   **webapps.config** - Cùng định dạng với webapps.config của router. Cũng được sử dụng để chỉ định các jar bổ sung trong $PLUGIN/lib/ hoặc $I2P/lib cho classpath của webapp, với `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Lưu ý:** Trước phiên bản 1.7.0 (API 0.9.53), dòng classpath chỉ được tải nếu warname giống với tên plugin. Từ API 0.9.53 trở đi, thiết lập classpath sẽ hoạt động với bất kỳ warname nào.

> **Lưu ý:** Trước phiên bản router 0.7.12-9, router tìm kiếm `plugin.warname.startOnLoad` thay vì `webapps.warname.startOnLoad`. Để tương thích với các phiên bản router cũ hơn, một plugin muốn vô hiệu hóa một war nên bao gồm cả hai dòng.

**eepsite/**

(Xem các ghi chú quan trọng bên dưới về eepsite)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - Trình cài đặt sẽ phải thực hiện thay thế biến ở đây để thiết lập đường dẫn. Vị trí và tên của tệp này không thực sự quan trọng, miễn là nó được thiết lập trong clients.config - có thể sẽ thuận tiện hơn nếu đặt ở cấp trên một bậc so với vị trí này.

**lib/**

Đặt bất kỳ tệp jar nào ở đây, và chỉ định chúng trong dòng classpath trong console/webapps.config và/hoặc clients.config

### tệp clients.config

Tệp này là tùy chọn và chỉ định các client sẽ được chạy khi một plugin được khởi động. Nó sử dụng cùng định dạng với tệp clients.config của router. Xem đặc tả tệp cấu hình clients.config để biết thêm thông tin về định dạng và các chi tiết quan trọng về cách các client được khởi động và dừng.

-   **clientApp.0.stopargs=foo bar stop baz** - Nếu có, class sẽ được gọi với các tham số này để dừng client. Tất cả các tác vụ dừng được gọi với độ trễ bằng không. Lưu ý: Router không thể biết được các client không được quản lý của bạn có đang chạy hay không.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Nếu có, class sẽ được gọi với các tham số này ngay trước khi xóa $PLUGIN. Tất cả các tác vụ gỡ cài đặt được gọi với độ trễ bằng không.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - Trình chạy plugin sẽ thực hiện thay thế biến trong các dòng args và stopargs như sau:
    -   `$I2P` - Thư mục cài đặt cơ sở của I2P
    -   `$CONFIG` - Thư mục config của I2P (thường là ~/.i2p)
    -   `$PLUGIN` - Thư mục cài đặt của plugin này (thường là ~/.i2p/plugins/appname)
    -   `$OS` - Hệ điều hành máy chủ ở dạng `windows`, `linux`, `mac`
    -   `$ARCH` - Kiến trúc máy chủ ở dạng `386`, `amd64`, `arm64`

(Xem các ghi chú quan trọng bên dưới về việc chạy shell script hoặc các chương trình bên ngoài)

## Các Tác Vụ Cài Đặt Plugin

Điều này liệt kê những gì xảy ra khi một plugin được cài đặt bởi I2P.

1.  Tệp .xpi2p được tải xuống.
2.  Chữ ký .sud được xác minh đối với các khóa đã lưu trữ. Kể từ bản phát hành 0.9.14.1, nếu không có khóa nào khớp, việc cài đặt sẽ thất bại, trừ khi một thuộc tính router nâng cao được đặt để cho phép tất cả các khóa.
3.  Xác minh tính toàn vẹn của tệp zip.
4.  Trích xuất tệp plugin.config.
5.  Xác minh phiên bản I2P, để đảm bảo plugin sẽ hoạt động.
6.  Kiểm tra rằng các webapp không trùng lặp với các ứng dụng $I2P hiện có.
7.  Dừng plugin hiện có (nếu có).
8.  Xác minh rằng thư mục cài đặt chưa tồn tại nếu update=false, hoặc hỏi để ghi đè.
9.  Xác minh rằng thư mục cài đặt đã tồn tại nếu update=true, hoặc hỏi để tạo.
10. Giải nén plugin vào appDir/plugins/name/
11. Thêm plugin vào plugins.config

## Các Tác Vụ Khởi Động Plugin

Điều này liệt kê những gì xảy ra khi các plugin được khởi động. Đầu tiên, plugins.config được kiểm tra để xem plugin nào cần được khởi động. Đối với mỗi plugin:

1.  Kiểm tra clients.config, tải và khởi động từng mục (thêm các jar đã cấu hình vào classpath).
2.  Kiểm tra console/webapp và console/webapp.config. Tải và khởi động các mục cần thiết (thêm các jar đã cấu hình vào classpath).
3.  Thêm console/locale/foo.jar vào classpath dịch thuật nếu có.
4.  Thêm console/theme vào đường dẫn tìm kiếm theme nếu có.
5.  Thêm liên kết thanh tóm tắt.

## Ghi chú Console Webapp

Các webapp console với tác vụ chạy nền nên triển khai ServletContextListener (xem seedless hoặc i2pbote để tham khảo), hoặc ghi đè destroy() trong servlet, để chúng có thể được dừng lại. Kể từ phiên bản router 0.7.12-3, các webapp console sẽ luôn được dừng trước khi khởi động lại, vì vậy bạn không cần lo lắng về việc có nhiều instance, miễn là bạn làm điều này. Cũng kể từ phiên bản router 0.7.12-3, các webapp console sẽ được dừng khi router tắt.

Đừng gói các file jar thư viện trong webapp; hãy đặt chúng trong lib/ và đặt classpath trong webapps.config. Sau đó bạn có thể tạo các plugin cài đặt và cập nhật riêng biệt, trong đó plugin cập nhật không chứa các file jar thư viện.

Không bao giờ đóng gói Jetty, Tomcat, hoặc các servlet jar trong plugin của bạn, vì chúng có thể xung đột với phiên bản trong bản cài đặt I2P. Hãy cẩn thận không đóng gói bất kỳ thư viện xung đột nào.

Không bao gồm các tệp .java hoặc .jsp; nếu không Jetty sẽ biên dịch lại chúng khi cài đặt, điều này sẽ làm tăng thời gian khởi động. Mặc dù hầu hết các cài đặt I2P sẽ có trình biên dịch Java và JSP hoạt động trong classpath, điều này không được đảm bảo và có thể không hoạt động trong mọi trường hợp.

Hiện tại, một webapp cần thêm các file classpath trong $PLUGIN phải có cùng tên với plugin. Ví dụ, một webapp trong plugin foo phải được đặt tên là foo.war.

Mặc dù I2P đã hỗ trợ Servlet 3.0 từ phiên bản I2P 0.9.30, nhưng nó KHÔNG hỗ trợ quét annotation cho @WebContent (không có tệp web.xml). Một số tệp jar runtime bổ sung sẽ được yêu cầu, và chúng tôi không cung cấp những tệp này trong bản cài đặt tiêu chuẩn. Hãy liên hệ với các nhà phát triển I2P nếu bạn cần hỗ trợ cho @WebContent.

## Ghi chú về Eepsite

Không rõ cách để cài đặt một plugin vào một eepsite đã có. Router không có kết nối đến eepsite, và nó có thể đang chạy hoặc không, và có thể có nhiều hơn một eepsite. Tốt hơn là bắt đầu instance Jetty và instance I2PTunnel của riêng bạn, cho một eepsite hoàn toàn mới.

Nó có thể tạo một I2PTunnel mới (hơi giống như CLI i2ptunnel làm), nhưng nó sẽ không xuất hiện trong giao diện i2ptunnel tất nhiên, đó là một instance khác. Nhưng điều đó vẫn ổn. Sau đó bạn có thể khởi động và dừng i2ptunnel và jetty cùng nhau.

Vì vậy đừng trông chờ router sẽ tự động hợp nhất điều này với một eepsite hiện có nào đó. Có thể điều đó sẽ không xảy ra. Hãy khởi động một I2PTunnel và Jetty mới từ clients.config. Những ví dụ tốt nhất cho điều này là các plugin zzzot và pebble.

Làm thế nào để đưa thay thế đường dẫn vào jetty.xml? Xem các plugin zzzot và pebble để lấy ví dụ.

## Ghi Chú Khởi Động/Dừng Client

Kể từ phiên bản 0.9.4, router hỗ trợ các plugin client "được quản lý". Các plugin client được quản lý được khởi tạo và bắt đầu bởi `ClientAppManager`. ClientAppManager duy trì một tham chiếu đến client và nhận các cập nhật về trạng thái của client. Các plugin client được quản lý được ưu tiên, vì việc triển khai theo dõi trạng thái và bắt đầu cũng như dừng một client dễ dàng hơn nhiều. Nó cũng giúp tránh các tham chiếu tĩnh trong mã client có thể dẫn đến việc sử dụng bộ nhớ quá mức sau khi một client bị dừng. Xem đặc tả tệp cấu hình clients.config để biết thêm thông tin về cách viết một client được quản lý.

Đối với các plugin client "không được quản lý", router không có cách nào để giám sát trạng thái của các client được khởi động thông qua clients.config. Tác giả plugin nên xử lý các lệnh gọi start hoặc stop nhiều lần một cách nhẹ nhàng, nếu có thể, bằng cách giữ một bảng trạng thái tĩnh, hoặc sử dụng các file PID, v.v. Tránh ghi log hoặc exception khi start hoặc stop nhiều lần. Điều này cũng áp dụng cho lệnh gọi stop mà không có start trước đó. Kể từ phiên bản router 0.7.12-3, các plugin sẽ được dừng khi router tắt, có nghĩa là tất cả các client có stopargs trong clients.config sẽ được gọi, dù chúng có được khởi động trước đó hay không.

## Ghi chú về Shell Script và Chương trình Bên ngoài

Để chạy shell scripts hoặc các chương trình bên ngoài khác, hãy viết một Java class nhỏ kiểm tra loại hệ điều hành, sau đó chạy ShellCommand trên file .bat hoặc .sh mà bạn cung cấp. Một giải pháp tổng quát cho việc này đã được thêm vào I2P 1.7.0/0.9.53, đó là "ShellService" thực hiện theo dõi trạng thái cho một lệnh duy nhất và giao tiếp với ClientAppManager.

Các chương trình bên ngoài sẽ không được dừng lại khi router dừng hoạt động, và một bản sao thứ hai sẽ khởi chạy khi router khởi động. Điều này thường có thể được giảm thiểu bằng cách sử dụng ShellService để thực hiện theo dõi trạng thái. Nếu điều đó không phù hợp với trường hợp sử dụng của bạn, bạn có thể viết một lớp wrapper hoặc shell script thực hiện việc lưu trữ PID thông thường trong một file PID, và kiểm tra nó khi khởi động.

## Hướng dẫn Plugin khác

-   Xem nhánh monotone i2p.scripts hoặc bất kỳ plugin mẫu nào trên trang của zzz để tìm script shell makeplugin.sh. Script này tự động hóa hầu hết các tác vụ tạo khóa, tạo file su3 plugin và xác minh. Bạn nên tích hợp script này vào quy trình build plugin của mình.
-   Pack200 cho các file jar và war được khuyến khích mạnh mẽ cho plugin, nó thường giảm kích thước plugin xuống 60-65%. Xem bất kỳ plugin mẫu nào trên trang của zzz để có ví dụ. Pack200 unpacking được hỗ trợ trên các router 0.7.11-5 hoặc cao hơn, tức là về cơ bản tất cả các router hỗ trợ plugin.
-   Plugin không được cố gắng ghi vào bất kỳ đâu trong $I2P vì nó có thể là chỉ đọc, và đó không phải là chính sách tốt.
-   Plugin có thể ghi vào $CONFIG nhưng khuyến khích chỉ giữ file trong $PLUGIN. Tất cả file trong $PLUGIN sẽ bị xóa khi gỡ cài đặt.
-   $CWD có thể ở bất kỳ đâu; không giả định nó ở một vị trí cụ thể, không cố gắng đọc hoặc ghi file tương đối với $CWD. Đối với ShellService, nó luôn giống với $PLUGIN.
-   Các chương trình Java nên tìm hiểu vị trí của chúng bằng các directory getter trong I2PAppContext.
-   Thư mục plugin là `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, hoặc đặt tham số $PLUGIN trong dòng args trong clients.config.
-   Tất cả file config phải là UTF-8.
-   Để chạy trong JVM riêng biệt, sử dụng ShellCommand với `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Thay thế cho stopargs trong clients.config, một client Java có thể đăng ký shutdown hook với `I2PAppContext.addShutdownTask()`. Nhưng điều này sẽ không tắt plugin khi nâng cấp, vì vậy stopargs được khuyến khích. Ngoài ra, đặt tất cả thread được tạo về chế độ daemon.
-   Không bao gồm các class trùng lặp với những class trong cài đặt tiêu chuẩn. Mở rộng các class nếu cần thiết.
-   Cẩn thận với các định nghĩa classpath khác nhau trong wrapper.config giữa cài đặt cũ và mới.
-   Client sẽ từ chối các key trùng lặp với keyname khác nhau, và keyname trùng lặp với key khác nhau, và key hoặc keyname khác nhau trong gói nâng cấp. Bảo vệ key của bạn. Chỉ tạo chúng một lần.
-   Không sửa đổi file plugin.config khi runtime vì nó sẽ bị ghi đè khi nâng cấp. Sử dụng file config khác trong thư mục để lưu trữ cấu hình runtime.
-   Nói chung, plugin không nên yêu cầu truy cập vào $I2P/lib/router.jar. Không truy cập các router class, trừ khi bạn đang làm điều gì đó đặc biệt.
-   Vì mỗi phiên bản phải cao hơn phiên bản trước, bạn có thể cải tiến build script để thêm build number vào cuối phiên bản.
-   Plugin không bao giờ được gọi `System.exit()`.
-   Vui lòng tôn trọng giấy phép bằng cách đáp ứng các yêu cầu giấy phép cho bất kỳ phần mềm nào bạn đóng gói.
-   Router đặt múi giờ JVM thành UTC. Nếu plugin cần biết múi giờ thực tế của người dùng, nó được lưu trữ bởi router trong thuộc tính I2PAppContext `i2p.systemTimeZone`.

## Classpaths

Các tệp jar sau đây trong $I2P/lib có thể được coi là có trong classpath tiêu chuẩn cho tất cả các cài đặt I2P, bất kể cài đặt gốc cũ hay mới như thế nào.

Tất cả các API công khai gần đây trong các jar i2p đều có số phiên bản since-release được chỉ định trong Javadocs. Nếu plugin của bạn yêu cầu các tính năng chỉ có sẵn trong các phiên bản gần đây, hãy đảm bảo thiết lập các thuộc tính min-i2p-version, min-jetty-version, hoặc cả hai, trong tệp plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Các file jar sau trong $I2P/lib có thể được giả định là có mặt trong tất cả các cài đặt I2P, bất kể cài đặt gốc cũ hay mới như thế nào, nhưng không nhất thiết phải có trong classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Bất kỳ thứ gì không được liệt kê ở trên có thể không có mặt trong classpath của mọi người, ngay cả khi bạn có nó trong classpath trong phiên bản i2p của BẠN. Nếu bạn cần bất kỳ jar nào không được liệt kê ở trên, hãy thêm $I2P/lib/foo.jar vào classpath được chỉ định trong clients.config hoặc webapps.config trong plugin của bạn.

Trước đây, một mục classpath được chỉ định trong clients.config đã được thêm vào classpath cho toàn bộ JVM. Tuy nhiên, từ phiên bản 0.7.13-3, điều này đã được khắc phục bằng cách sử dụng class loaders, và giờ đây, như ban đầu dự định, classpath được chỉ định trong clients.config chỉ dành cho thread cụ thể đó. Do đó, hãy chỉ định đầy đủ classpath cần thiết cho mỗi client.

## Ghi chú về Phiên bản Java

I2P đã yêu cầu Java 7 kể từ phiên bản 0.9.24 (tháng 1 năm 2016). I2P đã yêu cầu Java 6 kể từ phiên bản 0.9.12 (tháng 4 năm 2014). Bất kỳ người dùng I2P nào đang sử dụng phiên bản mới nhất đều nên chạy JVM 1.7 (7.0).

Nếu plugin của bạn **không yêu cầu phiên bản 1.7**:

-   Đảm bảo rằng tất cả các file java và jsp được biên dịch với source="1.6" target="1.6".
-   Đảm bảo rằng tất cả các file jar thư viện đi kèm cũng dành cho phiên bản 1.6 trở xuống.

Nếu plugin của bạn **yêu cầu phiên bản 1.7**:

-   Lưu ý điều này trên trang tải xuống của bạn.
-   Thêm min-java-version=1.7 vào plugin.config của bạn

Trong mọi trường hợp, bạn **phải** thiết lập bootclasspath khi biên dịch với Java 8 để tránh lỗi runtime.

## JVM Bị Crash Khi Cập Nhật

Lưu ý - tất cả những vấn đề này giờ đây đã được khắc phục.

JVM có xu hướng bị crash khi cập nhật các file jar trong plugin nếu plugin đó đã chạy từ khi I2P được khởi động (ngay cả khi plugin đã được dừng sau đó). Điều này có thể đã được sửa với việc triển khai class loader trong phiên bản 0.7.13-3, nhưng cũng có thể chưa.

Cách an toàn nhất là thiết kế plugin của bạn với jar bên trong war (đối với webapp), hoặc yêu cầu khởi động lại sau khi cập nhật, hoặc không cập nhật các jar trong plugin của bạn.

Do cách thức hoạt động của class loader bên trong một webapp, có thể an toàn khi sử dụng các jar bên ngoài nếu bạn chỉ định classpath trong webapps.config. Cần thêm kiểm tra để xác nhận điều này. Đừng chỉ định classpath với một client 'giả' trong clients.config nếu nó chỉ cần thiết cho một webapp - thay vào đó hãy sử dụng webapps.config.

Ít an toàn nhất, và dường như là nguồn gốc của hầu hết các lỗi crash, là các client có plugin jar được chỉ định trong classpath trong clients.config.

Không có vấn đề gì trong quá trình cài đặt ban đầu - bạn không bao giờ cần phải khởi động lại cho việc cài đặt ban đầu của một plugin.

## Tham khảo

-   [Đặc tả Tệp Cấu hình](/docs/specs/configuration)
-   [Mật mã học DSA](/docs/specs/cryptography#DSA)
-   [Đặc tả Cập nhật](/docs/specs/updates)
