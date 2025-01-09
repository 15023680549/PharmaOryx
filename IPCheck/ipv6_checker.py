import socket


def check_ipv6_support(url):
    try:
        # 获取主机名的IP地址信息
        ip_addresses = socket.getaddrinfo(url, None)
        ipv6_support = False
        for addr_info in ip_addresses:
            # 检查是否包含IPv6地址
            if addr_info[0] == socket.AF_INET6:
                ipv6_support = True
                break

        if ipv6_support:
            print(f"{url} 支持IPv6")
        else:
            print(f"{url} 不支持IPv6")
    except socket.gaierror as e:
        print(f"无法解析域名或域名不可达: {e}")


if __name__ == "__main__":
    website_url = input("请输入网站链接：")
    check_ipv6_support(website_url)
