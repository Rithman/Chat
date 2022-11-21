import subprocess
import chardet
import re
from tabulate import tabulate
from ipaddress import ip_address


def ping(host, ip_range):
    host = ip_address(host)
    hosts = (host + i for i in range(ip_range))
    hosts_status = {"Reachable": [], "Unreachable": []}
    for host in list(hosts):
        with subprocess.Popen(["ping", f"{str(host)}"], creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE) as ping:
            print()

            for i, line in enumerate(ping.stdout):
                if i == 9:
                    res_line = chardet.detect(line)
                    text = line.decode(res_line['encoding'])
                    percent = re.search(r"(\d*)% потерь", text)
                    if int(percent.group(1)) < 100:
                        hosts_status["Reachable"].append(str(host))
                    else:
                        hosts_status["Unreachable"].append(str(host))
    print(tabulate(hosts_status, headers="keys"))
        
ping("127.0.0.1", 3)