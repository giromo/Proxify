import os
import requests
import re
from base64 import b64decode
from concurrent.futures import ThreadPoolExecutor
import time
import shutil
import multiprocessing

MT_PROTO_LINKS = [
    'https://mtpro.xyz/api/?type=mtproto',
    'https://mtpro.xyz/api/?type=socks'
]

V2RAY_LINKS = list(set([
    "https://raw.githubusercontent.com/MrPooyaX/VpnsFucking/main/BeVpn.txt",
    "",
    "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "",
    "",
    "",
    "",
    "",
    "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://mrpooya.top/SuperApi/BE.php"
]))

PROXY_LINKS = {
    'socks5': [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/socks5.txt',
        'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt',
        'https://raw.githubusercontent.com/r00tee/Proxy-List/refs/heads/main/Socks5.txt',
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks5/data.txt',
        'https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt',
        'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt',
        'https://raw.githubusercontent.com/elliottophellia/proxylist/refs/heads/master/results/socks5/global/socks5_checked.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/socks5.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/generated/socks5_proxies.txt',
        'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks5.txt'
    ],
    'socks4': [
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks4/data.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/generated/socks4_proxies.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/socks4.txt',
        'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks4.txt',
        'https://proxyspace.pro/socks4.txt'
    ],
    'http': [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/http.txt',
        'https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/http/data.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt',
        'https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/generated/http_proxies.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt',
        'https://api.openproxylist.xyz/http.txt',
        'https://alexa.lr2b.com/proxylist.txt',
        'https://rootjazz.com/proxies/proxies.txt',
        'https://proxy-spider.com/api/proxies.example.txt',
        'https://multiproxy.org/txt_all/proxy.txt',
        'https://proxyspace.pro/http.txt'
    ],
    'https': [
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt',
        'https://raw.githubusercontent.com/claude89757/free_https_proxies/refs/heads/main/https_proxies.txt',
        'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt',
        'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt',
        'https://raw.githubusercontent.com/SevenworksDev/proxy-list/refs/heads/main/proxies/https.txt',
        'https://proxyspace.pro/https.txt'
    ],
    'mtproto': [
        'https://raw.githubusercontent.com/Argh94/telegram-proxy-scraper/refs/heads/main/proxy.txt'
    ]
}

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist and check write permissions."""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.access(directory, os.W_OK):
            raise PermissionError(f"No write permission for directory {directory}")
    except Exception as e:
        print(f"Failed to create directory {directory}: {e}")
        raise

def fetch_url(url):
    """Fetch content from a given URL with a timeout."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def clean_proxy_line(line):
    """Clean proxy line by removing protocol prefixes using regex."""
    line = line.strip()
    if not line:
        return None
    pattern = r'^(socks5|socks4|http|https)://'
    cleaned = re.sub(pattern, '', line)
    return cleaned if cleaned else None

def get_metadata_headers():
    """Return metadata headers for subscription files."""
    return """#profile-title: base64:8J+GkyBHaXQ6IEBGaXJtZm94IOKbk++4j+KAjfCfkqU=
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/firmfox/Proxify
#profile-web-page-url: https://github.com/giromo/Proxify\n"""

def organize_configs(configs):
    """Organize configs by protocol."""
    protocol_map = {
        'vmess': [],
        'vless': [],
        'trojan': [],
        'shadowsocks': [],
        'wireguard': [],
        'warp': [],
        'reality': [],
        'tuic': [],
        'hysteria2': [],
        'other': []
    }
    
    for config in configs:
        if not config.strip():
            continue
            
        config_lower = config.lower()
        if re.match(r'vmess://', config_lower):
            protocol_map['vmess'].append(config)
        elif re.match(r'vless://', config_lower):
            protocol_map['vless'].append(config)
        elif re.match(r'trojan://', config_lower):
            protocol_map['trojan'].append(config)
        elif re.match(r'ss://|shadowsocks://', config_lower):
            protocol_map['shadowsocks'].append(config)
        elif re.match(r'ssr://', config_lower):
            protocol_map['shadowsocks'].append(config)  # ShadowSocksR as shadowsocks
        elif re.match(r'wireguard://', config_lower):
            protocol_map['wireguard'].append(config)
        elif re.match(r'warp', config_lower):
            protocol_map['warp'].append(config)
        elif re.match(r'reality', config_lower):
            protocol_map['reality'].append(config)
        elif re.match(r'tuic://|tuic5://', config_lower):
            protocol_map['tuic'].append(config)
        elif re.match(r'hy2://|hysteria2://', config_lower):
            protocol_map['hysteria2'].append(config)
        else:
            protocol_map['other'].append(config)
    
    return protocol_map

def save_protocol_files(protocol_map):
    """Save configs to files by protocol."""
    ensure_directory_exists('v2ray_configs/seperated_by_protocol')
    metadata = get_metadata_headers()
    
    for protocol, configs in protocol_map.items():
        if configs:
            with open(f'v2ray_configs/seperated_by_protocol/{protocol}.txt', 'w') as f:
                f.write(metadata)
                f.write('\n'.join(configs) + '\n')

def save_subscription_files(configs, chunk_size=500):
    """Save configs to subscription files in chunks."""
    ensure_directory_exists('v2ray_configs/mixed')
    metadata = get_metadata_headers()
    
    for i in range(0, len(configs), chunk_size):
        chunk = configs[i:i + chunk_size]
        with open(f'v2ray_configs/mixed/subscription-{i//chunk_size + 1}.txt', 'w') as f:
            f.write(metadata)
            f.write('\n'.join(chunk) + '\n')

def get_proxy(proxy_type):
    """Fetch and save proxies of a specific type."""
    proxies = set()
    max_workers = min(15, multiprocessing.cpu_count() * 2)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_url, url): url for url in PROXY_LINKS[proxy_type]}
        
        for future in futures:
            data = future.result()
            if data:
                for line in data.splitlines():
                    cleaned = clean_proxy_line(line)
                    if cleaned:
                        proxies.add(cleaned)
    
    if proxies:
        ensure_directory_exists('proxies')
        with open(f'proxies/{proxy_type}.txt', 'w') as f:
            f.write('\n'.join(proxies) + '\n')

def get_v2ray():
    """Fetch and process V2Ray configs."""
    configs = set()
    max_workers = min(15, multiprocessing.cpu_count() * 2)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_url, url): url for url in V2RAY_LINKS}
        
        for future in futures:
            data = future.result()
            if data:
                try:
                    decoded = b64decode(data).decode('utf-8')
                    configs.update(line.strip() for line in decoded.splitlines() if line.strip())
                except:
                    configs.update(line.strip() for line in data.splitlines() if line.strip())
    
    if configs:
        configs = list(configs)
        protocol_map = organize_configs(configs)
        save_protocol_files(protocol_map)
        save_subscription_files(configs)

def get_mtproto(link_index):
    """Fetch and save MTProto proxies."""
    try:
        response = requests.get(MT_PROTO_LINKS[link_index], timeout=20)
        response.raise_for_status()
        data = response.json()
        
        ensure_directory_exists('telegram_proxies')
        
        if link_index == 0:
            filename = 'telegram_proxies/mtproto.txt'
            with open(filename, 'w') as f:
                if isinstance(data, list):
                    for proxy in data:
                        f.write(f"https://t.me/proxy?server={proxy['host']}&port={proxy['port']}&secret={proxy['secret']}\n")
                elif isinstance(data, dict):
                    f.write(f"https://t.me/proxy?server={data['host']}&port={data['port']}&secret={data['secret']}\n")
        else:
            filename = 'telegram_proxies/socks5.txt'
            with open(filename, 'w') as f:
                if isinstance(data, list):
                    for proxy in data:
                        host = proxy.get('ip', proxy.get('host', ''))
                        f.write(f"https://t.me/proxy?server={host}&port={proxy['port']}\n")
                elif isinstance(data, dict):
                    host = data.get('ip', data.get('host', ''))
                    f.write(f"https://t.me/proxy?server={host}&port={data['port']}\n")
    except Exception as e:
        print(f"Error in get_mtproto: {e}")

def cleanup_old_files():
    """Remove old directories before processing."""
    for dir_path in ['Seperated_by_protocol', 'proxy', 'telegram_proxy', 'mix']:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

def main():
    """Main function to orchestrate proxy fetching."""
    if os.path.basename(os.getcwd()) == 'app':
        os.chdir('..')
    start_time = time.time()
    cleanup_old_files()
    
    ensure_directory_exists('telegram_proxies')
    ensure_directory_exists('proxies')
    ensure_directory_exists('v2ray_configs/mixed')
    ensure_directory_exists('v2ray_configs/seperated_by_protocol')
    
    max_workers = min(7, multiprocessing.cpu_count() * 2)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.submit(get_proxy, 'socks4')
        executor.submit(get_proxy, 'socks5')
        executor.submit(get_proxy, 'http')
        executor.submit(get_proxy, 'https')
        executor.submit(get_mtproto, 0)
        executor.submit(get_mtproto, 1)
        executor.submit(get_v2ray)
    
    print(f"Execution completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
