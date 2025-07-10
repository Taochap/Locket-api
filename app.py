from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import platform
import subprocess
import time
import json
import queue
import string
import random
import threading
import datetime
import re
import urllib3
from queue import Queue
from itertools import cycle
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.exceptions import ProxyError
from colorama import init, Fore, Style
from typing import Optional, List

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ==================================
# Copy zLocket class and helper functions here
# ==================================

PRINT_LOCK = threading.RLock()
def sfprint(*args, **kwargs):
    with PRINT_LOCK:
        print(*args, **kwargs)
        sys.stdout.flush()

class xColor:
    YELLOW='\033[38;2;255;223;15m'
    GREEN='\033[38;2;0;209;35m'
    RED='\033[38;2;255;0;0m'
    BLUE='\033[38;2;0;132;255m'
    PURPLE='\033[38;2;170;0;255m'
    PINK='\033[38;2;255;0;170m'
    MAGENTA='\033[38;2;255;0;255m'
    ORANGE='\033[38;2;255;132;0m'
    CYAN='\033[38;2;0;255;255m'
    PASTEL_YELLOW='\033[38;2;255;255;153m'
    PASTEL_GREEN='\033[38;2;153;255;153m'
    PASTEL_BLUE='\033[38;2;153;204;255m'
    PASTEL_PINK='\033[38;2;255;153;204m'
    PASTEL_PURPLE='\033[38;2;204;153;255m'
    DARK_RED='\033[38;2;139;0;0m'
    DARK_GREEN='\033[38;2;0;100;0m'
    DARK_BLUE='\033[38;2;0;0;139m'
    DARK_PURPLE='\033[38;2;75;0;130m'
    GOLD='\033[38;2;255;215;0m'
    SILVER='\033[38;2;192;192;192m'
    BRONZE='\033[38;2;205;127;50m'
    NEON_GREEN='\033[38;2;57;255;20m'
    NEON_PINK='\033[38;2;255;20;147m'
    NEON_BLUE='\033[38;2;31;81;255m'
    WHITE='\033[38;2;255;255;255m'
    RESET='\033[0m'

class zLocket:
    def __init__(self, device_token: str="", target_friend_uid: str="", num_threads: int=1, note_target: str=""):
        self.FIREBASE_GMPID="1:641029076083:ios:cc8eb46290d69b234fa606"
        self.IOS_BUNDLE_ID="com.locket.Locket"
        self.API_LOCKET_URL="https://api.locketcamera.com"
        self.FIREBASE_AUTH_URL="https://www.googleapis.com/identitytoolkit/v3/relyingparty"
        self.FIREBASE_API_KEY="AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So"
        self.TOKEN_API_URL="https://thanhdieu.com/api/v1/locket/token"
        self.SHORT_URL="https://url.thanhdieu.com/api/v1"
        self.SV_FRQ_URL="https://thanhdieu-server.vercel.app/api/locket-friend-requests"
        self.TOKEN_FILE="token.json"
        self.TOKEN_EXPIRY_TIME=(20 + 9) * 60
        self.FIREBASE_APP_CHECK=None
        self.USE_EMOJI=True
        self.ACCOUNTS_PER_PROXY=random.randint(6,10)
        self.NAME_TOOL="zLocket Tool Pro"
        self.VERSION_TOOL="v1.0.7"
        self.TARGET_FRIEND_UID=target_friend_uid if target_friend_uid else None
        self.PROXY_LIST=[
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=20000&country=all&ssl=all&anonymity=all',
            'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt',
            'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt'
        ]
        self.print_lock=threading.Lock()
        self.successful_requests=0
        self.failed_requests=0
        self.total_proxies=0
        self.start_time=time.time()
        self.spam_confirmed=False
        self.telegram = 'wus_team'
        self.author = 'WsThanhDieu'
        self.request_timeout=15
        self.messages = []
        self.proxies = []
        self.proxy_load_time = 0
        self.proxy_expiry_interval = 15 * 60  # 15 minutes in seconds
        self._load_and_refresh_proxies()
        self.device_token=device_token
        self.num_threads=num_threads
        self.note_target=note_target
        self.session_id=int(time.time() * 1000)
        self._init_environment()
        self.FIREBASE_APP_CHECK=self._load_token_()
        if os.name=="nt":
            os.system(
                f"title 💰 {self.NAME_TOOL} {self.VERSION_TOOL} by Api.ThanhDieu.Com 💰"
         )

    def _print(self, *args, **kwargs):
        with PRINT_LOCK:
            timestamp=datetime.datetime.now().strftime("%H:%M:%S")
            message=" ".join(map(str, args))
            sm=message
            if "[+]" in message:
                sm=f"{xColor.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            elif "[✗]" in message:
                sm=f"{xColor.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            elif "[!]" in message:
                sm=f"{xColor.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            sfprint(
                f"{xColor.CYAN}[{timestamp}]{Style.RESET_ALL} {sm}", **kwargs)

    def _loader_(self, message, duration=3):
        spinner=cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        end_time=time.time() + duration
        while time.time() < end_time:
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.CYAN}{message} {next(spinner)} ")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            sys.stdout.write(f"\r{xColor.GREEN}{message} ✓     \n")
            sys.stdout.flush()

    def _sequence_(self, message, duration=1.5, char_set="0123456789ABCDEF"):
        end_time=time.time() + duration
        while time.time() < end_time:
            random_hex=''.join(random.choices(char_set, k=50))
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.GREEN}[{xColor.WHITE}*{xColor.GREEN}] {xColor.CYAN}{message}: {xColor.GREEN}{random_hex}")
                sys.stdout.flush()
            time.sleep(0.05)
        with PRINT_LOCK:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def _randchar_(self, duration=2):
        special_chars="#$%^&*()[]{}!@<>?/\\|~`-=+_"
        hex_chars="0123456789ABCDEF"
        colors=[xColor.GREEN, xColor.RED, xColor.YELLOW,
                  xColor.CYAN, xColor.MAGENTA, xColor.NEON_GREEN]
        end_time=time.time() + duration
        while time.time() < end_time:
            length=random.randint(20, 40)
            vtd=""
            for _ in range(length):
                char_type=random.randint(1, 3)
                if char_type==1:
                    vtd+=random.choice(special_chars)
                elif char_type==2:
                    vtd+=random.choice(hex_chars)
                else:
                    vtd+="xX0"
            status=random.choice([
                f"{xColor.GREEN}[ACCESS]",
                f"{xColor.RED}[DENIED]",
                f"{xColor.YELLOW}[BREACH]",
                f"{xColor.CYAN}[DECODE]",
                f"{xColor.MAGENTA}[ENCRYPT]"
            ])
            color=random.choice(colors)
            with PRINT_LOCK:
                sys.stdout.write(
                    f"\r{xColor.CYAN}[RUNNING TOOL] {color}{vtd} {status}")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            print()

    def _blinking_(self, text, blinks=3, delay=0.1):
        for _ in range(blinks):
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.WHITE}{text}")
                sys.stdout.flush()
            time.sleep(delay)
            with PRINT_LOCK:
                sys.stdout.write(f"\r{' ' * len(text)}")
                sys.stdout.flush()
            time.sleep(delay)
        with PRINT_LOCK:
            sys.stdout.write(f"\r{xColor.GREEN}{text}\n")
            sys.stdout.flush()

    def get_proxy_time_remaining(self):
        """Trả về thời gian còn lại trước khi proxy được làm mới (tính bằng giây)"""
        elapsed_time = time.time() - self.proxy_load_time
        remaining_time = self.proxy_expiry_interval - elapsed_time
        return max(0, int(remaining_time))

    def _load_and_refresh_proxies(self):
        self._print(f"{xColor.CYAN}[*] Loading new proxies...")
        self.proxies = self._load_proxies_from_urls()
        self.proxy_queue = Queue()
        for proxy in self.proxies:
            self.proxy_queue.put(proxy)
        self.proxy_load_time = time.time()
        self._print(f"{xColor.GREEN}[+] Proxies loaded and ready. Next refresh in {self.proxy_expiry_interval // 60} minutes.")

    def _load_proxies_from_urls(self):
        all_proxies = []
        for url in self.PROXY_LIST:
            try:
                self._print(f"{xColor.CYAN}[*] Fetching proxies from: {xColor.WHITE}{url}")
                response = requests.get(url, timeout=self.request_timeout)
                response.raise_for_status()
                # Assuming proxies are one per line
                proxies = [line.strip() for line in response.text.splitlines() if line.strip()]
                all_proxies.extend(proxies)
                self._print(f"{xColor.GREEN}[+] Fetched {len(proxies)} proxies from {xColor.WHITE}{url}")
            except requests.exceptions.RequestException as e:
                self._print(f"{xColor.RED}[!] Error fetching proxies from {xColor.WHITE}{url}: {str(e)}")
        if not all_proxies:
            self._print(f"{xColor.RED}[!] No proxies found from any source. Please check proxy URLs or add to proxy.txt.")
        else:
            self._print(f"{xColor.GREEN}[+] Total proxies loaded: {xColor.YELLOW}{len(all_proxies)}")
        return all_proxies

    def _init_environment(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        init(autoreset=True)

    def _load_token_(self):
        try:
            if not os.path.exists(self.TOKEN_FILE):
                return self.fetch_token()
            self._loader_(
                f"{xColor.YELLOW}Verifying token integrity{Style.RESET_ALL}", 0.5)
            with open(self.TOKEN_FILE, 'r') as file:
                token_data=json.load(file)
            if 'token' in token_data and 'expiry' in token_data:
                if token_data['expiry'] > time.time():
                    self._print(
                        f"{xColor.GREEN}[+] {xColor.CYAN}Loaded token from file token.json: {xColor.YELLOW}{token_data['token'][:10]}...{token_data['token'][-10:]}")
                    time.sleep(0.4)
                    time_left=int(token_data['expiry'] - time.time())
                    self._print(
                        f"{xColor.GREEN}[+] {xColor.CYAN}Token expires in: {xColor.WHITE}{time_left//60} minutes {time_left % 60} seconds")
                    return token_data['token']
                else:
                    self._print(
                        f"{xColor.RED}[!]{xColor.RED} Locket token expired, trying to fetch new token")
            return self.fetch_token()
        except Exception as e:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Error loading token from file: {str(e)}")
            return self.fetch_token()

    def save_token(self, token):
        try:
            token_data={
                'token': token,
                'expiry': time.time() + self.TOKEN_EXPIRY_TIME,
                'created_at': time.time()
            }
            with open(self.TOKEN_FILE, 'w') as file:
                json.dump(token_data, file, indent=4)

            self._print(
                f"{xColor.GREEN}[+] {xColor.CYAN}Token saved to {xColor.WHITE}{self.TOKEN_FILE}")
            return True
        except Exception as e:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Error saving token to file: {str(e)}")
            return False

    def fetch_token(self, retry=0, max_retries=3):
        if retry==0:
            self._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Initializing token authentication sequence")
            self._loader_("Establishing secure connection", 1)
        if retry >= max_retries:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Token acquisition failed after {max_retries} attempts")
            self._loader_("Emergency shutdown", 1)
            sys.exit(1)
        try:
            self._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Preparing to retrieve token [{retry+1}/{max_retries}]")
            response=requests.get(self.TOKEN_API_URL, timeout=self.request_timeout, proxies={
                                    "http": None, "https": None})
            response.raise_for_status()
            data=response.json()
            if not isinstance(data, dict):
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.WHITE}Invalid response format, retrying...")
                time.sleep(0.5)
                return self.fetch_token(retry + 1)
            if data.get("code")==200 and "data" in data and "token" in data["data"]:
                token=data["data"]["token"]
                self._print(
                    f"{xColor.GREEN}[+] {xColor.CYAN}Token acquired successfully")
                masked_token=token[:10] + "..." + token[-10:]
                self._print(
                    f"{xColor.GREEN}[+] {xColor.WHITE}Token: {xColor.YELLOW}{masked_token}")
                self.save_token(token)
                return token
            elif data.get("code") in (403, 404, 502, 503, 504, 429, 500):
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.RED}The Locket token server is no longer available, please contact us telegram @{self.author}, trying again...")
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
            else:
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.RED}{data.get('msg', 'Unknown error')}")
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
        except requests.exceptions.RequestException as e:
            self._print(
                f"{xColor.RED}[!] Warning: {xColor.YELLOW}Token unauthorized, retrying... {e}")
            self._loader_("Attempting to reconnect", 1)
            time.sleep(1.3)
            return self.fetch_token(retry + 1)

    def headers_locket(self):
        return {
            'Host': self.API_LOCKET_URL.replace('https://', ''),
            'Accept': '*/*',
            'baggage': 'sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket%401.121.1%2B1,sentry-trace_id=2cdda588ea0041ed93d052932b127a3e',
            'X-Firebase-AppCheck': self.FIREBASE_APP_CHECK,
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'sentry-trace': '2cdda588ea0041ed93d052932b127a3e-a3e2ba7a095d4f9d-0',
            'User-Agent': 'com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1',
            'Firebase-Instance-ID-Token': 'd7ChZwJHhEtsluXwXxbjmj:APA91bFoMIgxwf-2tmY9QLy82lKMEWL6S4d8vb9ctY3JxLLTQB1k6312TcgtqJjWFhQV1_J4wIFvE0Kfroztu1vbZDOFc65s0vvj68lNJM4XuJg1onEODiBG3r7YGrQLiHkBV1gEoJ5f',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
        }

    def firebase_headers_locket(self):
        base_headers=self.headers_locket()
        return {
            'Host': 'www.googleapis.com',
            'baggage': base_headers.get('baggage', ''),
            'Accept': '*/*',
            'X-Client-Version': 'iOS/FirebaseSDK/10.23.1/FirebaseCore-iOS',
            'X-Firebase-AppCheck': self.FIREBASE_APP_CHECK,
            'X-Ios-Bundle-Identifier': self.IOS_BUNDLE_ID,
            'X-Firebase-GMPID': '1:641029076083:ios:cc8eb46290d69b234fa606',
            'X-Firebase-Client': 'H4sIAAAAAAAAAKtWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA',
            'sentry-trace': base_headers.get('sentry-trace', ''),
            'Accept-Language': 'vi',
            'User-Agent': 'FirebaseAuth.iOS/10.23.1 com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1',
            'Connection': 'keep-alive',
            'X-Firebase-GMPID': self.FIREBASE_GMPID,
            'Content-Type': 'application/json',
        }

    def analytics_payload(self):
        return {
            "platform": "ios",
            "experiments": {
                "flag_4": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "43",
                },
                "flag_10": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "505",
                },
                "flag_6": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "2000",
                },
                "flag_3": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_22": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_18": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_17": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1010",
                },
                "flag_16": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "303",
                },
                "flag_15": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_14": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "551",
                },
                "flag_25": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "23",
                },
            },
            "amplitude": {
                "device_id": "57A54C21-B633-418C-A6E3-4201E631178C",
                "session_id": {
                    "value": str(self.session_id),
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                },
            },
            "google_analytics": {"app_instance_id": "7E17CEB525FA4471BD6AA9CEC2C1BCB8"},
            "ios_version": "1.121.1.1",
        }

    def excute(self, url, headers=None, payload=None, thread_id=None, step=None, proxies_dict=None):
        prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}{step}{Style.RESET_ALL}]" if thread_id is not None and step else ""
        try:
            response=requests.post(
                url,
                headers=headers or self.headers_locket(),
                json=payload,
                proxies=proxies_dict,
                timeout=self.request_timeout,
                verify=False
            )
            response.raise_for_status()
            self.successful_requests+=1
            return response.json() if response.content else True
        except ProxyError:
            self._print(
                f"{prefix} {xColor.RED}[!] Proxy connection terminated")
            self.failed_requests+=1
            return "proxy_dead"
        except requests.exceptions.RequestException as e:
            self.failed_requests+=1
            if hasattr(e, 'response') and e.response is not None:
                status_code=e.response.status_code
                try:
                    error_data=e.response.json()
                    error_msg=error_data.get(
                        'error', 'Remote server rejected request')
                    self._print(
                        f"{prefix} {xColor.RED}[!] HTTP {status_code}: {error_msg}")
                except:
                    self._print(
                        f"{prefix} {xColor.RED}[!] Server connection timeout")
                if status_code==429:
                    return "too_many_requests"
            # self._print(f"{prefix} {xColor.RED}[!] Network error: {str(e)[:50]}...")
            return None

    def _extract_uid_locket(self, url: str) -> Optional[str]:
        real_url=self._convert_url(url)
        if not real_url:
            self.messages.append(
                f"Locket account not found, please try again.")
            return None
        parsed_url=urlparse(real_url)
        if parsed_url.hostname != "locket.camera":
            self.messages.append(
                f"Locket URL không hợp lệ: {parsed_url.hostname}")
            return None
        if not parsed_url.path.startswith("/invites/"):
            self.messages.append(
                f"Link Locket Sai Định Dạng: {parsed_url.path}")
            return None
        parts=parsed_url.path.split("/")
        if len(parts) > 2:
            full_uid=parts[2]
            uid=full_uid[:28]
            return uid
        self.messages.append("Không tìm thấy UID trong Link Locket")
        return None

    def _convert_url(self, url: str) -> str:
        if url.startswith("https://locket.camera/invites/"):
            return url
        if url.startswith("https://locket.cam/"):
            try:
                resp=requests.get(
                    url,
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
                    },
                    timeout=self.request_timeout,
                )
                if resp.status_code==200:
                    match=re.search(
                        r'window\.location\.href\s*=\s*"([^"]+)"', resp.text)
                    if match:
                        parsed=urlparse(match.group(1))
                        query=parse_qs(parsed.query)
                        enc_link=query.get("link", [None])[0]
                        if enc_link:
                            return enc_link
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            except Exception as e:
                self.messages.append(
                    f"Failed to connect to the Locket server.")
                return ""
        payload={"type": "toLong", "kind": "url.thanhdieu.com", "url": url}
        headers={
            "Accept": "*/*",
            "Accept-Language": "vi",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            response=requests.post(
                self.SHORT_URL,
                headers=headers,
                data=urlencode(payload),
                timeout=self.request_timeout,
                verify=True,
            )
            response.raise_for_status()
            _res=response.json()
            if _res.get("status")==1 and "url" in _res:
                return _res["url"]
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""
        except requests.exceptions.RequestException as e:
            self.messages.append(
                "Lỗi kết nối tới API Url.ThanhDieu.Com " + str(e))
            return ""
        except ValueError:
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""

    def _cc_loader_(self, message, stop_event):
        spinner=cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not stop_event.is_set():
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.CYAN}{message} {next(spinner)} ")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
            sys.stdout.flush()

    def _xheader_(self):
        print(f"\n{xColor.CYAN}╔═══════════════════════════════════════════════════════╗")
        print(f"{xColor.CYAN}║ {xColor.YELLOW}             TOOL KHẮC CHẾ SPAM Y/C KẾT BẠN           {xColor.CYAN}║")
        print(f"{xColor.CYAN}║ {xColor.RED}                 [Telegram: @{self.telegram}]                {xColor.CYAN}║")
        print(f"{xColor.CYAN}╚═══════════════════════════════════════════════════════╝")

    def _zheader_(self):
        print(f"\n{xColor.CYAN}╔═══════════════════════════════════════════════════════╗")
        print(f"{xColor.CYAN}║ {xColor.YELLOW}              SPAM KẾT BẠN LOCKET WIDGET              {xColor.CYAN}║")
        print(f"{xColor.CYAN}║ {xColor.RED}                 [Telegram: @{self.telegram}]                {xColor.CYAN}║")
        print(f"{xColor.CYAN}╚═══════════════════════════════════════════════════════╝\n")

def _rand_str_(length=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def _rand_name_():
    return _rand_str_(8, chars=string.ascii_lowercase)

def _rand_email_():
    return f"{_rand_str_(15)}@thanhdieu.com"

def _rand_pw_():
    return 'zlocket' + _rand_str_(7)

def _clear_():
    try:
        os.system('cls' if os.name=='nt' else 'clear')
    except:
        with PRINT_LOCK:
            print("\033[2J\033[H", end="")
            sys.stdout.flush()

def typing_print(text, delay=0.02):
    with PRINT_LOCK:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def _flush_():
    sys.stdout.write('\033[F\033[K') 
    sys.stdout.write('\033[F\033[K')
    sys.stdout.flush()

def _cd_(message, count=5, delay=0.2):
    for i in range(count, 0, -1):
        binary=bin(i)[2:].zfill(8)
        sys.stdout.write(
            f"\r{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}{message} {xColor.RED}{binary}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(
        f"\r{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}{message} {xColor.GREEN}READY      \n")
    sys.stdout.flush()

def step1b_sign_in(email, password, thread_id, proxies_dict, zlocket_instance):
    if not email or not password:
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed: Invalid credentials")
        return None, None
    payload={
        "email": email,
        "password": password,
        "clientType": "CLIENT_TYPE_IOS",
        "returnSecureToken": True
    }
    vtd=zlocket_instance.excute(
        f"{zlocket_instance.FIREBASE_AUTH_URL}/verifyPassword?key={zlocket_instance.FIREBASE_API_KEY}",
        headers=zlocket_instance.firebase_headers_locket(),
        payload=payload,
        thread_id=thread_id,
        step="Auth",
        proxies_dict=proxies_dict
    )
    if vtd and 'idToken' in vtd and 'localId' in vtd:
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.GREEN}[✓] Authentication successful")
        return vtd.get('idToken'), vtd.get('localId')
    zlocket_instance._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed")
    return None, None

def step2_finalize_user(id_token, thread_id, proxies_dict, zlocket_instance):
    if not id_token:
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed: Invalid token")
        return False
    first_name=zlocket_instance.NAME_TOOL
    last_name=' '.join(random.sample([
        '😀', '😂', '😍', '🥰', '😊', '😇', '😚', '😘', '😻', '😽', '🤗',
        '😎', '🥳', '😜', '🤩', '😢', '😡', '😴', '🙈', '🙌', '💖', '🔥', '👍',
        '✨', '🌟', '🍎', '🍕', '🚀', '🎉', '🎈', '🌈', '🐶', '🐱', '🦁',
        '😋', '😬', '😳', '😷', '🤓', '😈', '👻', '💪', '👏', '🙏', '💕', '💔',
        '🌹', '🍒', '🍉', '🍔', '🍟', '☕', '🍷', '🎂', '🎁', '🎄', '🎃', '🔔',
        '⚡', '💡', '📚', '✈️', '🚗', '🏠', '⛰️', '🌊', '☀️', '☁️', '❄️', '🌙',
        '🐻', '🐼', '🐸', '🐝', '🦄', '🐙', '🦋', '🌸', '🌺', '🌴', '🏀', '⚽', '🎸'
    ], 5))
    username=_rand_name_()
    payload={
        "data": {
            "username": username,
            "last_name": last_name,
            "require_username": True,
            "first_name": first_name
        }
    }
    headers=zlocket_instance.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=zlocket_instance.excute(
        f"{zlocket_instance.API_LOCKET_URL}/finalizeTemporaryUser",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Profile",
        proxies_dict=proxies_dict
    )
    if result:
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.GREEN}[✓] Profile created: {xColor.YELLOW}{username}")
        return True
    zlocket_instance._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed")
    return False

def step3_send_friend_request(id_token, thread_id, proxies_dict, zlocket_instance):
    if not id_token:
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed: Invalid token")
        return False
    payload={
        "data": {
            "user_uid": zlocket_instance.TARGET_FRIEND_UID,
            "source": "signUp",
            "platform": "iOS",
            "messenger": "Messages",
            "invite_variant": {"value": "1002", "@type": "type.googleapis.com/google.protobuf.Int64Value"},
            "share_history_eligible": True,
            "rollcall": False,
            "prompted_reengagement": False,
            "create_ofr_for_temp_users": False,
            "get_reengagement_status": False
        }
    }
    headers=zlocket_instance.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=zlocket_instance.excute(
        f"{zlocket_instance.API_LOCKET_URL}/sendFriendRequest",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Friend",
        proxies_dict=proxies_dict
    )
    if result:
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.GREEN}[✓] Connection established with target")
        return True
    zlocket_instance._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed")
    return False

def format_proxy(proxy_str):
    if not proxy_str:
        return None
    try:
        if not proxy_str.startswith(('http://', 'https://')):
            proxy_str=f"http://{proxy_str}"
        return {"http": proxy_str, "https": proxy_str}
    except Exception as e:
        print(f"Proxy format error: {e}") # Use print for now, replace with proper logging
        return None

def get_proxy(proxy_queue, thread_id, stop_event=None, zlocket_instance=None):
    try:
        if stop_event is not None and stop_event.is_set():
            return None
        
        # Check if proxies need to be refreshed
        if zlocket_instance and (time.time() - zlocket_instance.proxy_load_time) > zlocket_instance.proxy_expiry_interval:
            zlocket_instance._print(f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.YELLOW}[!] Proxy list expired, refreshing...")
            zlocket_instance._load_and_refresh_proxies()

        proxy_str=proxy_queue.get_nowait()
        return proxy_str
    except queue.Empty:
        if stop_event is None or not stop_event.is_set():
            print(f"[Thread-{thread_id:03d}] Proxy pool exhausted") # Use print for now, replace with proper logging
        return None

def step1_create_account(thread_id, proxy_queue, stop_event, zlocket_instance):
    while not stop_event.is_set():
        current_proxy=get_proxy(proxy_queue, thread_id, stop_event, zlocket_instance)
        proxies_dict=format_proxy(current_proxy)
        proxy_usage_count=0
        failed_attempts=0
        max_failed_attempts=10
        if not current_proxy:
            zlocket_instance._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy pool depleted, waiting for refill (1s)")
            time.sleep(1)
            continue
        zlocket_instance._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Thread activated with proxy: {xColor.YELLOW}{current_proxy}")
        if thread_id < 3:
            _cd_(f"Thread-{thread_id:03d} initialization", count=3)
        while not stop_event.is_set() and proxy_usage_count < zlocket_instance.ACCOUNTS_PER_PROXY and failed_attempts < max_failed_attempts:
            if stop_event.is_set():
                return
            if not current_proxy:
                current_proxy=get_proxy(proxy_queue, thread_id, stop_event, zlocket_instance)
                proxies_dict=format_proxy(current_proxy)
                if not current_proxy:
                    zlocket_instance._print(
                        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy unavailable, will try again")
                    time.sleep(1) # Wait a bit before retrying to get a proxy
                    continue
                zlocket_instance._print(
                    f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Switching to new proxy: {xColor.YELLOW}{current_proxy}")

            prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Register{Style.RESET_ALL}]"
            email=_rand_email_()
            password=_rand_pw_()
            zlocket_instance._print(
                f"{prefix} {xColor.CYAN}● Initializing new identity: {xColor.YELLOW}{email[:8]}...@...")
            payload={
                "data": {
                    "email": email,
                    "password": password,
                    "client_email_verif": True,
                    "client_token": _rand_str_(40, chars=string.hexdigits.lower()),
                    "platform": "ios"
                }
            }
            if stop_event.is_set():
                return
            response_data=zlocket_instance.excute(
                f"{zlocket_instance.API_LOCKET_URL}/createAccountWithEmailPassword",
                headers=zlocket_instance.headers_locket(),
                payload=payload,
                thread_id=thread_id,
                step="Register",
                proxies_dict=proxies_dict
            )
            if stop_event.is_set():
                return
            if response_data=="proxy_dead":
                zlocket_instance._print(
                    f"{prefix} {xColor.RED}[!] Proxy terminated, acquiring new endpoint")
                current_proxy=None
                failed_attempts += 1
                continue
            if response_data=="too_many_requests":
                zlocket_instance._print(
                    f"{prefix} {xColor.RED}[!] Connection throttled, switching endpoint")
                current_proxy=None
                failed_attempts += 1
                continue
            if isinstance(response_data, dict) and response_data.get('result', {}).get('status')==200:
                zlocket_instance._print(
                    f"{prefix} {xColor.GREEN}[✓] Identity created: {xColor.YELLOW}{email}")
                proxy_usage_count += 1
                failed_attempts=0
                if stop_event.is_set():
                    return
                id_token, local_id=step1b_sign_in(
                    email, password, thread_id, proxies_dict, zlocket_instance)
                if stop_event.is_set():
                    return
                if id_token and local_id:
                    if step2_finalize_user(id_token, thread_id, proxies_dict, zlocket_instance):
                        if stop_event.is_set():
                            return
                        first_request_success=step3_send_friend_request(
                            id_token, thread_id, proxies_dict, zlocket_instance)
                        if first_request_success:
                            zlocket_instance._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.YELLOW}🚀 Boosting friend requests: Sending 15 more requests")
                            for _ in range(15):
                                if stop_event.is_set():
                                    return
                                step3_send_friend_request(
                                    id_token, thread_id, proxies_dict, zlocket_instance)
                            zlocket_instance._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.GREEN}[✓] Boost complete: 101 total requests sent")
                    else:
                        zlocket_instance._print(
                            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failure")
                else:
                    zlocket_instance._print(
                        f"{prefix} {xColor.RED}[✗] Identity creation failed")
                failed_attempts += 1
        if failed_attempts >= max_failed_attempts:
            zlocket_instance._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Thread restarting: Excessive failures ({failed_attempts})")
        else:
            zlocket_instance._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.YELLOW}● Proxy limit reached ({proxy_usage_count}/{zlocket_instance.ACCOUNTS_PER_PROXY}), getting new proxy")


# Initialize zLocket instance globally or pass it around
z_locket_instance = zLocket()

@app.route('/')
def home():
    return "zLocket API is running!"

@app.route('/spam_friend_request', methods=['POST'])
def spam_friend_request():
    data = request.get_json()
    target_url = data.get('target_url')
    custom_username = data.get('custom_username', z_locket_instance.NAME_TOOL)
    use_emoji = data.get('use_emoji', True)
    num_threads = data.get('num_threads', 1)

    if not target_url:
        return jsonify({'status': 'error', 'message': 'Missing target_url'}), 400

    z_locket_instance.TARGET_FRIEND_UID = z_locket_instance._extract_uid_locket(target_url)
    if not z_locket_instance.TARGET_FRIEND_UID:
        return jsonify({'status': 'error', 'message': z_locket_instance.messages}), 400

    z_locket_instance.NAME_TOOL = custom_username
    z_locket_instance.num_threads = num_threads
    proxies = z_locket_instance._load_proxies_from_urls()
    if not proxies:
        return jsonify({"status": "error", "message": "No proxies available from configured URLs."}), 500

    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)
    stop_event = threading.Event()
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=step1_create_account,
            args=(i, proxy_queue, stop_event, z_locket_instance)
        )
        threads.append(thread)
        thread.daemon = True # Allow main program to exit even if threads are running
        thread.start()

    # Thêm thông tin thời gian proxy vào response
    proxy_time_remaining = z_locket_instance.get_proxy_time_remaining()
    proxy_refresh_time = z_locket_instance.proxy_expiry_interval // 60  # Chuyển đổi sang phút

    # In a real API, you might want to manage these threads more robustly
    # and provide a way to query their status or stop them.
    # For now, we'll just start them and return a success message.
    return jsonify({
        'status': 'success', 
        'message': 'Friend request spamming initiated.',
        'proxy_info': {
            'total_proxies': len(proxies),
            'proxy_refresh_interval_minutes': proxy_refresh_time,
            'proxy_time_remaining_seconds': proxy_time_remaining,
            'proxy_time_remaining_minutes': proxy_time_remaining // 60,
            'next_proxy_refresh': f"Proxy sẽ được làm mới sau {proxy_time_remaining // 60} phút {proxy_time_remaining % 60} giây"
        }
    })

@app.route('/delete_friend_request', methods=['POST'])
def delete_friend_request():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    limit = data.get('limit')
    num_threads = data.get('num_threads', 1)

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required.'}), 400

    # Simplified login process for API
    try:
        _res_ = requests.post(
            f"{z_locket_instance.FIREBASE_AUTH_URL}/verifyPassword?key={z_locket_instance.FIREBASE_API_KEY}",
            headers=z_locket_instance.firebase_headers_locket(),
            json={
                "email": email,
                "password": password,
                "clientType": "CLIENT_TYPE_IOS",
                "returnSecureToken": True
            },
            timeout=z_locket_instance.request_timeout,
            verify=False
        )
        _res_.raise_for_status()
        _auth_ = _res_.json()
        if 'idToken' not in _auth_ or 'localId' not in _auth_:
            error_msg = _auth_.get('error', {}).get('message', 'Authentication failed')
            return jsonify({'status': 'error', 'message': error_msg}), 401
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Authentication failed: {str(e)}'}), 500

    id_token = _auth_['idToken']
    local_id = _auth_['localId']

    # Fetch friend requests
    try:
        loader_stop = threading.Event()
        vtd_loader = threading.Thread(
            target=z_locket_instance._cc_loader_,
            args=(f"{xColor.YELLOW}Đang lấy danh sách Y/C kết bạn, hãy kiên nhẫn chờ đợi...", loader_stop)
        )
        vtd_loader.daemon = True
        vtd_loader.start()

        vtd = requests.post(
            z_locket_instance.SV_FRQ_URL,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                "action": 'thanhdieu_get_friends',
                "idToken": id_token,
                "localId": local_id
            },
            timeout=z_locket_instance.request_timeout + 200,
            verify=True
        )
        cmm = vtd.json()
        loader_stop.set()
        vtd_loader.join()

        if cmm.get('code') != 200:
            return jsonify({'status': 'error', 'message': cmm.get('msg', 'Failed to fetch friend requests')}), 500

        friend_list = cmm['data']['list']
        total_friends = cmm['total']

        if limit is None or limit > total_friends:
            limit = total_friends

    except requests.exceptions.RequestException as e:
        loader_stop.set()
        vtd_loader.join()
        return jsonify({'status': 'error', 'message': f'Failed to fetch friend requests: {str(e)}'}), 500
    except Exception as e:
        loader_stop.set()
        vtd_loader.join()
        return jsonify({'status': 'error', 'message': f'Unexpected error fetching friend requests: {str(e)}'}), 500

    deleted_count = 0
    thread_semaphore = threading.Semaphore(num_threads)
    delete_lock = threading.Lock()

    def delete_friend_request_thread(friend):
        nonlocal deleted_count
        with thread_semaphore:
            if deleted_count >= limit:
                return
            headers = z_locket_instance.headers_locket()
            headers['Authorization'] = f"Bearer {id_token}"
            _payload = {
                "data": {
                    "analytics": z_locket_instance.analytics_payload(),
                    "direction": "incoming",
                    "user_uid": friend['userId']
                }
            }
            result = z_locket_instance.excute(
                f"{z_locket_instance.API_LOCKET_URL}/deleteFriendRequest",
                headers=headers,
                payload=_payload
            )
            with delete_lock:
                if result and deleted_count < limit:
                    deleted_count += 1
                    # In a real API, you'd log this or send updates, not print to console
                    # print(f"Deleted: {friend['userId']}")

    threads = []
    for friend in friend_list[:limit]: # Only process up to the limit
        thread = threading.Thread(target=delete_friend_request_thread, args=(friend,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Thêm thông tin thời gian proxy vào response
    proxy_time_remaining = z_locket_instance.get_proxy_time_remaining()
    proxy_refresh_time = z_locket_instance.proxy_expiry_interval // 60  # Chuyển đổi sang phút

    return jsonify({
        'status': 'success', 
        'message': f'Successfully deleted {deleted_count} friend requests.',
        'proxy_info': {
            'total_proxies': len(z_locket_instance.proxies),
            'proxy_refresh_interval_minutes': proxy_refresh_time,
            'proxy_time_remaining_seconds': proxy_time_remaining,
            'proxy_time_remaining_minutes': proxy_time_remaining // 60,
            'next_proxy_refresh': f"Proxy sẽ được làm mới sau {proxy_time_remaining // 60} phút {proxy_time_remaining % 60} giây"
        }
    })

@app.route('/proxy_status', methods=['GET'])
def proxy_status():
    """Endpoint để kiểm tra trạng thái proxy hiện tại"""
    proxy_time_remaining = z_locket_instance.get_proxy_time_remaining()
    proxy_refresh_time = z_locket_instance.proxy_expiry_interval // 60  # Chuyển đổi sang phút
    
    return jsonify({
        'status': 'success',
        'proxy_info': {
            'total_proxies': len(z_locket_instance.proxies),
            'proxy_refresh_interval_minutes': proxy_refresh_time,
            'proxy_time_remaining_seconds': proxy_time_remaining,
            'proxy_time_remaining_minutes': proxy_time_remaining // 60,
            'next_proxy_refresh': f"Proxy sẽ được làm mới sau {proxy_time_remaining // 60} phút {proxy_time_remaining % 60} giây",
            'proxy_load_time': z_locket_instance.proxy_load_time,
            'current_time': time.time()
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


