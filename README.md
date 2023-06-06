# antibip

Censys và Shodan là công cụ tìm kiếm và quét mạng trực tuyến. Chúng giúp thu thập thông tin về các thiết bị kết nối với Internet. Tuy nhiên, khi được sử dụng bởi kẻ xấu, chúng có thể tìm lỗ hổng bảo mật và thông tin nhạy cảm để tấn công hoặc xâm nhập vào hệ thống. Vì vậy, script này được tạo ra để giúp mọi người có thể giảm thiểu khả năng bị quét bằng cách script sẽ tự động tải xuống một danh sách các địa chỉ IP đã được phát hiện là scanners của Censys/Shodan/... và DROP chúng bằng iptables.


## Cài đặt

Để sử dụng, bạn cần phải cài module ``request`` và IPTables (bạn có thể tra Google để xem cách cài cho distro của bạn) để có thể lấy danh sách các địa chỉ IPs của scanners và chặn chúng:

Cài đặt module requests
```bash
  pip (hoặc pip3) install requests
```
Cài đặt ipset
```bash
  DEB based systems: sudo apt-get install ipset
  RPM based systems: sudo dnf install ipset
```
Cài đặt iptables (nhớ tắt firewall mặc định của OS trước)
```bash
  DEB based systems: sudo apt-get install iptables
  RPM based systems: sudo dnf install iptables
```
Sau đó, chỉ cần khởi động script và sử dụng
```bash
  python3 (hoặc python) antibip.py
```
Bạn có thể lưu vĩnh viễn các rules IPTables bằng cách sử dụng ``iptables-persistent``
```bash
  DEB based systems: sudo apt-get install iptables-persistent
  
  RPM based systems: sudo dnf install iptables-services
```

## Tác giả
- [@hungnguyennaz](https://github.com/hungnguyennaz) - Script này
- [@SilvrrGIT](https://github.com/SilvrrGIT) - IP Lists
