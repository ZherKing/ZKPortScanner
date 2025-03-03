import tkinter as tk
from tkinter import messagebox, scrolledtext

import assets.scan_ports
from assets.scan_ports import *


def gui():
    # 创建主窗口
    root = tk.Tk()
    root.title("ZKPortScanner - 端口扫描工具 by ZherKing")

    # 创建并放置标签和输入框
    tk.Label(root, text="目标IP地址或域名:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entry_target = tk.Entry(root, width=50)
    entry_target.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="端口（例如80、80，443或者10-20）:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    entry_ports = tk.Entry(root, width=50)
    entry_ports.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="线程数:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    entry_max_workers = tk.Entry(root, width=50)
    entry_max_workers.grid(row=2, column=1, padx=5, pady=5)

    # 创建并放置扫描按钮
    text_result = scrolledtext.ScrolledText(root, width=80, height=20)
    text_result.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    btn_scan = tk.Button(root, text="开始扫描",
                         command=lambda: start_scan(entry_target, entry_ports, entry_max_workers, text_result))
    btn_scan.grid(row=3, column=0, columnspan=2, pady=10)

    # 创建并放置滚动文本框用于显示结果
    text_result = scrolledtext.ScrolledText(root, width=80, height=20)
    text_result.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # 运行主循环
    root.mainloop()