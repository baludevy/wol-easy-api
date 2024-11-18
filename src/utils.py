import re


def validate_ip(ip: str) -> bool:
    regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip):
        return True
    return False


def validate_mac(mac: str) -> bool:
    regex = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    if re.search(regex, mac):
        return True
    return False
