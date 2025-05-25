from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


def apply_proxy_settings(proxy_host, proxy_port, proxy_username=None, proxy_password=None):
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = f"{proxy_host}:{proxy_port}"
    proxy.ssl_proxy = f"{proxy_host}:{proxy_port}"

    if proxy_username and proxy_password:
        proxy.socks_username = proxy_username
        proxy.socks_password = proxy_password

    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)

    return webdriver.Chrome(desired_capabilities=capabilities)