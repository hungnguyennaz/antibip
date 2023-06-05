# antibip

Script Python chặn IP của các hệ thống scanners như Censys, Shodan


## Cài đặt

Để sử dụng, bạn cần phải cài module ``request`` và IPTables (bạn có thể tra Google để xem cách cài cho distro của bạn) để có thể lấy danh sách các địa chỉ IPs của scanners và chặn chúng bằng cách sử dụng lệnh

```bash
  pip (hoặc pip3) install requests
```
Sau đó, chỉ cần khởi động script và sử dụng
```bash
  python3 (hoặc python) antibip.py
```
Bạn có thể lưu vĩnh viễn các rules IPTables bằng cách sử dụng ``iptables-persistent``
```bash
  DEB based systems: sudo apt install iptables-persistent
  
  RPM based systems: sudo dnf install iptables-services
```

## Tác giả
- [@hungnguyennaz](https://github.com/hungnguyennaz) - Script này
- [@SilvrrGIT](https://github.com/SilvrrGIT) - IP Lists
