"""WebView2 桌面窗口启动器"""
import socket
import time


def _wait_for_server(host: str, port: int, timeout: float = 10.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def launch_gui(host: str, port: int, title: str = "PyPitravel"):
    """启动桌面窗口"""
    try:
        import webview
    except ImportError:
        print("错误: 需要安装 pywebview，请运行: pip install pypitravel[gui]")
        return

    url = f"http://{host}:{port}"

    if not _wait_for_server(host, port):
        print(f"错误: 服务未在 {url} 就绪")
        return

    webview.create_window(
        title,
        url,
        width=1100,
        height=720,
        min_size=(900, 600),
        text_select=True,
    )
    webview.start()
