import socket
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
import re
from tkinter import messagebox


def parse_ports(port_input):
    """
    解析端口输入，可以是单个端口、多个端口和端口范围的组合。
    返回一个包含所有要扫描的端口号的列表。
    """
    ports = set()
    parts = port_input.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def resolve_domain(domain):
    """
    将域名解析为IP地址。
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def scan_port(ip, port):
    """
    尝试连接指定的IP地址和端口。
    如果连接成功，则认为端口是开放的。
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
    except:
        return False
    else:
        return True
    finally:
        sock.close()

def scan_ports(ip, ports, max_workers=100):
    """
    扫描指定IP地址的端口列表。
    """
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in future_to_port:
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)

    return open_ports


def start_scan(entry_target, entry_ports, entry_max_workers, text_result):
    target = entry_target.get().strip()
    port_input = entry_ports.get().strip()
    max_workers_input = entry_max_workers.get().strip()

    if not target or not port_input or not max_workers_input:
        messagebox.showwarning("输入错误", "请输入目标IP地址或域名、端口和线程数。")
        return

    try:
        max_workers = int(max_workers_input)
    except ValueError:
        messagebox.showwarning("输入错误", "线程数必须是一个整数。")
        return

    # 解析域名（如果输入的不是IP地址）
    if not re.match(r'^\d{1,3}(\.\d{1,3}){3}$', target):
        ip = resolve_domain(target)
        if ip is None:
            messagebox.showerror("解析错误", f"无法解析域名 {target}")
            return
    else:
        ip = target

    ports = parse_ports(port_input)
    if not ports:
        messagebox.showwarning("输入错误", "请输入有效的端口。")
        return

    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, f"开始扫描 {ip} 的端口: {', '.join(map(str, ports))}，使用线程数: {max_workers}...\n")

    open_ports = scan_ports(ip, ports, max_workers)

    if open_ports:
        result = f"开放的端口: {', '.join(map(str, open_ports))}\n"
    else:
        result = "没有发现开放的端口。\n"

    text_result.insert(tk.END, result)