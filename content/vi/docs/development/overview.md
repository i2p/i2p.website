---
title: "Mục lục Tài liệu Kỹ thuật"
description: "Mục lục tài liệu kỹ thuật I2P"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/vi/docs/develop/overview"
  - "/vi/docs/develop/overview/"
---


## Tổng quan {#overview}

- [Giới thiệu kỹ thuật](/docs/overview/intro)
- [Giới thiệu ít kỹ thuật hơn](/docs/overview/intro/)
- [Mô hình mối đe dọa và phân tích](/docs/overview/threat-model)
- [So sánh với các mạng ẩn danh khác](/docs/overview/comparison)
- [Sơ đồ ngăn xếp giao thức](/docs/development/protocol-stack)
- [Các bài báo về I2P](/papers/)
- [Bài thuyết trình, bài viết, hướng dẫn, video và phỏng vấn](/about/media/)
- [Tổng quan Dự án Internet Vô hình (I2P) - 28 tháng 8, 2003 (PDF)](/docs/historical/i2p_philosophy.pdf)


## Chủ đề Tầng Ứng dụng {#applications}

- [Tổng quan và Hướng dẫn Phát triển Ứng dụng](/docs/development/applications)
- [Đặt tên và Sổ địa chỉ](/docs/overview/naming)
- [Lệnh Feed Đăng ký Sổ địa chỉ](/docs/specs/subscription)
- [Tổng quan về Plugin](/docs/guides/plugins)
- [Đặc tả Plugin](/docs/specs/plugin)
- [Client được Quản lý](/docs/applications/managed-clients)
- [Nhúng router vào ứng dụng của bạn](/docs/applications/embedding)
- [Bittorrent qua I2P](/docs/applications/bittorrent)
- [API Plugin I2PControl](/docs/api/i2pcontrol)
- [Định dạng hostsdb.blockfile](/docs/specs/blockfile)
- [Định dạng Tệp Cấu hình](/docs/specs/configuration)


## API và Giao thức Tầng Ứng dụng {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [Cấu hình I2PTunnel](/docs/specs/configuration)
- [Proxy SOCKS](/docs/api/socks)
- [Giao thức SAMv3](/docs/api/samv3)
- [Giao thức SAM](/docs/legacy/sam) (Không dùng nữa)
- [Giao thức SAMv2](/docs/legacy/samv2) (Không dùng nữa)
- [Giao thức BOB](/docs/legacy/bob) (Không dùng nữa)


## API và Giao thức Truyền tải Đầu cuối {#transport-api}

- [Tổng quan Giao thức Streaming](/docs/api/streaming)
- [Đặc tả Giao thức Streaming](/docs/specs/streaming)
- [Datagram](/docs/api/datagrams)
- [Đặc tả Datagram](/docs/specs/datagrams)


## API và Giao thức Giao diện Client-Router {#i2cp}

- [Tổng quan I2CP](/docs/specs/i2cp)
- [Đặc tả I2CP](/docs/specs/i2cp)
- [Đặc tả Cấu trúc Dữ liệu Chung](/docs/specs/common-structures)


## Mã hóa Đầu cuối {#encryption}

- [Mã hóa ECIES-X25519-AEAD-Ratchet cho đích](/docs/specs/ecies)
- [Mã hóa lai ECIES-X25519](/docs/specs/ecies-hybrid)
- [Mã hóa ECIES-X25519 cho router](/docs/specs/ecies-routers)
- [Mã hóa ElGamal/AES+SessionTag](/docs/specs/elgamal-aes)
- [Chi tiết mật mã ElGamal và AES](/docs/specs/cryptography)


## Cơ sở Dữ liệu Mạng {#netdb}

- [Tổng quan cơ sở dữ liệu mạng, chi tiết và phân tích mối đe dọa](/docs/overview/network-database)
- [Hash mật mã](/docs/specs/cryptography#hashes)
- [Chữ ký mật mã](/docs/specs/cryptography#signatures)
- [Chữ ký Red25519](/docs/specs/red25519)
- [Đặc tả reseed router](/docs/misc/reseed)
- [Địa chỉ Base32 cho Leaseset được Mã hóa](/docs/specs/b32encrypted)


## Giao thức Tin nhắn Router {#i2np}

- [Tổng quan I2NP](/docs/specs/i2np)
- [Đặc tả I2NP](/docs/specs/i2np)
- [Đặc tả Cấu trúc Dữ liệu Chung](/docs/specs/common-structures)
- [Đặc tả Leaseset được Mã hóa](/docs/specs/encryptedleaseset)


## Đường hầm {#tunnels}

- [Lập hồ sơ và chọn peer](/docs/overview/peer-selection)
- [Tổng quan định tuyến đường hầm](/docs/overview/tunnel-routing)
- [Định tuyến garlic và thuật ngữ](/docs/overview/garlic-routing)
- [Xây dựng và mã hóa đường hầm](/docs/specs/tunnel-creation)
- [ElGamal/AES cho mã hóa yêu cầu xây dựng](/docs/specs/elgamal-tunnel-creation)
- [Chi tiết mật mã ElGamal và AES](/docs/specs/cryptography)
- [Đặc tả xây dựng đường hầm (ElGamal)](/docs/specs/tunnel-creation)
- [Đặc tả xây dựng đường hầm (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [Đặc tả tin nhắn đường hầm cấp thấp](/docs/specs/tunnel-message)
- [Đường hầm Một chiều](/docs/legacy/unidirectional)
- [Lập hồ sơ và Chọn Peer trong Mạng Ẩn danh I2P - 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## Tầng Truyền tải {#transports}

- [Tổng quan tầng truyền tải](/docs/overview/transport)
- [Đặc tả NTCP2](/docs/specs/ntcp2)
- [Đặc tả SSU2](/docs/specs/ssu2)
- [NTCP (Cũ)](/docs/legacy/ntcp)
- [Tổng quan SSU (Cũ)](/docs/legacy/ssu-overview)


## Chủ đề Router Khác {#router}

- [Cập nhật phần mềm router](/docs/specs/updates)
- [Đặc tả reseed router](/docs/misc/reseed)
- [Hiệu suất](/docs/overview/performance)
- [Định dạng Tệp Cấu hình](/docs/specs/configuration)
- [Định dạng Tệp GeoIP](/docs/legacy/geoip)
- [Các cổng được I2P sử dụng](/docs/overview/ports)


## Hướng dẫn và Tài nguyên cho Nhà phát triển {#develop}

- [Hướng dẫn cho Nhà phát triển Mới](/docs/development/new-developers)
- [Hướng dẫn cho Người dịch Mới](/docs/development/new-translators)
- [Hướng dẫn cho Nhà phát triển](/docs/development/dev-guidelines)
- [Đề xuất](/proposals/)
- [Nhúng router vào ứng dụng của bạn](/docs/applications/embedding)
- [Cách Thiết lập Máy chủ Reseed](/docs/guides/reseed-server)
- [Các cổng được I2P sử dụng](/docs/overview/ports)
- [Lộ trình Dự án](/get-involved/roadmap/)
- [Tài liệu invisiblenet I2P cổ - 2003](/docs/historical/)
