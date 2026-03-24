import os
import requests
import hashlib
import time

URL_LIST_FILE = 'siteurl.txt'
BASE_DIR = 'favicon'
SIZES = [32, 64, 128, 256] 
API_TEMPLATE = "https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&size={size}&url={url}"

def get_md5(data):
    return hashlib.md5(data).hexdigest()

def download_favicons():
    for size in SIZES:
        os.makedirs(os.path.join(BASE_DIR, str(size)), exist_ok=True)

    if not os.path.exists(URL_LIST_FILE):
        return

    with open(URL_LIST_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in urls:
        domain = url.split('//')[-1].split('/')[0]
        filename = f"{domain}.png"
        print(f"Processing: {domain}")

        for size in SIZES:
            filepath = os.path.join(BASE_DIR, str(size), filename)
            target_api = API_TEMPLATE.format(size=size, url=url)
            try:
                response = requests.get(target_api, headers=headers, timeout=20)
                if response.status_code == 200 and len(response.content) > 100:
                    new_content = response.content
                    new_md5 = get_md5(new_content)
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            if get_md5(f.read()) == new_md5:
                                continue
                    with open(filepath, 'wb') as f:
                        f.write(new_content)
                    print(f"  [+] {size}px updated")
                time.sleep(0.2)
            except Exception as e:
                print(f"  [!] {size}px error: {e}")

if __name__ == "__main__":
    download_favicons()