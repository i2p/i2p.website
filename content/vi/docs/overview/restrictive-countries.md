---
title: "Các Quốc Gia Hạn Chế/Nghiêm Ngặt"
description: "Cách I2P hoạt động trong các khu vực pháp lý có hạn chế về công cụ định tuyến hoặc ẩn danh (Chế độ ẩn và danh sách nghiêm ngặt)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: tài liệu
reviewStatus: "needs-review"
---

Triển khai I2P này (triển khai Java được phân phối trên trang web này) bao gồm một "Danh sách Quốc gia Nghiêm ngặt" được sử dụng để điều chỉnh hành vi của router trong các khu vực mà việc tham gia định tuyến cho người khác có thể bị hạn chế bởi pháp luật. Mặc dù chúng tôi không biết các khu vực pháp lý cấm sử dụng I2P, một số có các quy định cấm rộng rãi đối với việc chuyển tiếp lưu lượng. Các router có vẻ nằm trong các quốc gia "nghiêm ngặt" sẽ tự động được đặt vào chế độ Ẩn.

Dự án tham khảo nghiên cứu từ các tổ chức quyền công dân và quyền kỹ thuật số khi đưa ra những quyết định này. Đặc biệt, nghiên cứu liên tục của Freedom House cung cấp thông tin cho các lựa chọn của chúng tôi. Hướng dẫn chung là bao gồm các quốc gia có điểm Tự do Dân sự (CL) từ 16 trở xuống, hoặc điểm Tự do Internet từ 39 trở xuống (không tự do).

## Tóm Tắt Chế Độ Ẩn

Khi một router được đặt vào chế độ Hidden, ba điều quan trọng thay đổi về hành vi của nó:

- Nó không công bố RouterInfo lên netDb.
- Nó không chấp nhận các tunnel tham gia.
- Nó từ chối các kết nối trực tiếp đến các router trong cùng quốc gia.

Các biện pháp phòng vệ này làm cho việc liệt kê các router một cách đáng tin cậy trở nên khó khăn hơn, và giảm thiểu rủi ro vi phạm các quy định địa phương về việc chuyển tiếp lưu lượng cho người khác.

## Danh sách các quốc gia có kiểm soát chặt chẽ (tính đến năm 2024)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
Nếu bạn cho rằng một quốc gia nên được thêm vào hoặc loại bỏ khỏi danh sách nghiêm ngặt, vui lòng mở một issue tại: https://i2pgit.org/i2p/i2p.i2p/

Tham khảo: Freedom House – https://freedomhouse.org/
