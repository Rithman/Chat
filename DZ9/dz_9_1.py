import subprocess
import chardet
import re
from ipaddress import ip_address


def ping(host):
    ip_obj = ip_address(host) # не понятен смысл задания содавать объект ip_address, чтобы потом порсто использовать его строковое представление
    with subprocess.Popen(["ping", f"{str(ip_obj)}"], creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE) as ping:
        is_alive = False
        for i, line in enumerate(ping.stdout):
            if i == 9:
                res_line = chardet.detect(line)
                text = line.decode(res_line['encoding'])
                percent = re.search(r"(\d*)% потерь", text)
                if int(percent.group(1)) < 100:
                    is_alive = True
        print(f"{host}: Узел {('' if is_alive else 'не ')}доступен")
        
ping("127.0.0.1")