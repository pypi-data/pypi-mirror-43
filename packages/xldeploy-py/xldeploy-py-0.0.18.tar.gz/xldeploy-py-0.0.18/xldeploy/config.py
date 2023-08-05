try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Config:
    def __init__(self, protocol="http", host="localhost", port="4516", context_path="deployit", username="admin",
                 password="admin", proxy_host=None, proxy_port=None, proxy_username=None, proxy_password=None, verify_ssl=True):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.context_path = context_path
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.verify_ssl = verify_ssl

    @classmethod
    def initialize(cls, url, username, password, proxy_host=None,
                   proxy_port=None, proxy_username=None, proxy_password=None, verify_ssl=True):
        parsed_url = urlparse(url)
        context_path = parsed_url.path.lstrip("/")
        # if no port given in url, send http over port 80 and https over port 443, fallback to 4516
        port = parsed_url.port if parsed_url.port else 443 if parsed_url.scheme == 'https' else 80 if parsed_url.scheme == 'http' else 4516
        return cls(parsed_url.scheme, parsed_url.hostname, port, context_path, username, password,
                   proxy_host, proxy_port, proxy_username, proxy_password, verify_ssl)
