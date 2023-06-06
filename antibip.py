import subprocess
import requests


def check_if_ipset_installed():
    try:
        subprocess.check_output(["sudo", "ipset", "list"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def check_if_iptables_installed():
    try:
        subprocess.check_output(["sudo", "iptables", "-L"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def create_ipset_blacklist():
    subprocess.run(
        ["sudo", "ipset", "create", "antibip-blacklist", "hash:ip", "hashsize", "8192"]
    )


def add_ip_to_blacklist(ip):
    subprocess.run(["sudo", "ipset", "add", "antibip-blacklist", ip])


def block_ipset_blacklist():
    subprocess.run(
        [
            "sudo",
            "iptables",
            "-I",
            "INPUT",
            "-m",
            "set",
            "--match-set",
            "antibip-blacklist",
            "src",
            "-j",
            "DROP",
        ]
    )

def block_ip(ip):
    subprocess.run(["sudo", "iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"])


def get_scanners_ips():
    url = "https://raw.githubusercontent.com/SilvrrGIT/IP-Lists/master/"
    files = ["binary_edge", "other", "shodan", "stretchoid"]
    scanners_ips = set()

    for file in files:
        response = requests.get(url + file)
        if response.status_code == 200:
            lines = response.text.split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    scanners_ips.add(line)

    return scanners_ips


def block_scanners_ips():
    confirmation = input(
        "Chức năng này sẽ tự động tải về danh sách các địa chỉ IP được đánh dấu là scanner như Censys, Shodan,... từ repo https://github.com/SilvrrGIT/IP-Lists/. Bạn muốn tiếp tục chứ? (y/n): "
    )

    if confirmation.lower() not in ["y", "yes"]:
        print("Đã thoát.")
        return

    print("Hãy đợi chút... (có thể mất từ 1-2 phút)")
    scanners_ips = get_scanners_ips()

    create_ipset_blacklist()

    for ip in scanners_ips:
        add_ip_to_blacklist(ip)

    block_ipset_blacklist()

    print("")
    print("Đã chặn thành công các địa chỉ IP từ danh sách.")
    print("Cảm ơn bạn vì đã sử dụng.")
    print("")


def uninstall_antibip():
    confirmation = input("Bạn có chắc chắn muốn gỡ bỏ antibip không? (y/n): ")

    if confirmation.lower() not in ["y", "yes"]:
        print("Đã thoát.")
        return

    subprocess.run(
        [
            "sudo",
            "iptables",
            "-D",
            "INPUT",
            "-m",
            "set",
            "--match-set",
            "antibip-blacklist",
            "src",
            "-j",
            "DROP",
        ]
    )
    subprocess.run(["sudo", "ipset", "flush", "antibip-blacklist"])
    subprocess.run(["sudo", "ipset", "destroy", "antibip-blacklist"])
    subprocess.run(["sudo", "ipset", "destroy", "antibip-blacklist"])

    print("Đã gỡ bỏ antibip.")
    print("")


def main():
    if not check_if_ipset_installed():
        print(
            "**ipset** chưa được cài đặt. Vui lòng cài đặt **ipset** và chạy lại script."
        )
        return

    if not check_if_iptables_installed():
        print(
            "**iptables** chưa được cài đặt. Vui lòng cài đặt **iptables** và chạy lại script."
        )
        return

    print(
        "Cảnh báo: Script này sẽ giúp bạn có thể hạn chế được một số công cụ quét mạng như Censys/Shodan (Censys và Shodan là công cụ tìm kiếm và quét mạng trực tuyến. Chúng giúp thu thập thông tin về các thiết bị kết nối với Internet. Tuy nhiên, khi được sử dụng bởi kẻ xấu, chúng có thể tìm lỗ hổng bảo mật và thông tin nhạy cảm để tấn công hoặc xâm nhập vào hệ thống). Bằng cách tải một danh sách các địa chỉ IPs của các scanners đã được tìm thấy và chặn chúng bằng iptables và ipset."
    )
    print(
        "Tuy nhiên, do script sử dụng iptables và ipset, bạn hãy chắc chắn rằng mình đã có một bản backup rules iptables để có thể revert lại nếu như script gây ra trục trặc. Cũng như, hãy đảm bảo rằng bạn đã cài đặt iptables, ipset và requests (pip install requests/pip3 install requests) để có thể sử dụng."
    )
    print("")
    print("Brought to you by hungaz")
    print("")
    confirmation = input("Bạn có chắc chắn muốn tiếp tục không? (y/n): ")

    if confirmation.lower() not in ["y", "yes"]:
        print("Đã thoát.")
        return

    print(" ")
    print("--------------- MENU --------------")
    print(" ")
    print("1. Chặn Censys/Shodan/Một số scanners khác")
    print("2. Gỡ bỏ antibip")
    print(" ")
    print("-----------------------------------")
    print(" ")
    choice = input("Chọn chức năng: ")

    if choice == "1":
        block_scanners_ips()
    elif choice == "2":
        uninstall_antibip()
    else:
        print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()