import requests
import brotli
from bs4 import BeautifulSoup
import base64

static_headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.midishow.com/",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def gen_req_headers(args=None):
    if args is None:
        args = {}
    req_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd", "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive", "Host": "www.midishow.com",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": '"Windows"', "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    for k, v in args.items():
        req_headers[k] = v
    return req_headers


def decode_base64(encoded_str: str, chr_set: str):
    standard_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    translation_table = str.maketrans(chr_set, standard_charset)
    standard_encoded_str = encoded_str.translate(translation_table)
    return base64.b64decode(standard_encoded_str)


def hex2str(hex_str: str):
    result = ""
    for i in range(0, len(hex_str), 2):
        if hex_str[i:i + 2] == "00":
            break
        result += chr(int(hex_str[i:i + 2], 16))
    return result


class MidiShowAPI:
    def __init__(self):
        self.session = requests.session()

    def login_by_cookies(self, cookies: tuple):
        for cookie in cookies:
            self.session.cookies.set(*cookie)

    def login_by_password(self, username: str, password: str):
        req_headers = gen_req_headers({
            "Cache-Control": "max-age=0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.midishow.com",
            "Referer": "https://www.midishow.com/user/account/login"
        })
        csrf_token = self._get_csrf_token("https://www.midishow.com/user/account/login")
        req_data = {
            "_csrf": csrf_token,
            "LoginForm[identity]": username,
            "LoginForm[password]": password,
            "login-button": ""
        }
        rsp = self.session.post("https://www.midishow.com/user/account/login",
                                headers=req_headers,
                                data=req_data,
                                allow_redirects=False)
        if "Location" in rsp.headers:
            return True
        return False  # Failed to login

    def _get_csrf_token(self, page_url: str):
        req_headers = gen_req_headers()
        rsp = self.session.get(page_url, headers=req_headers)
        bs = BeautifulSoup(rsp.text, "html.parser")
        csrf_tag = bs.find_all("meta", {"name": "csrf-token"})[0]
        return csrf_tag.attrs["content"]

    def download_midi(self, page_url: str):
        rsp = self.session.get(page_url, headers=gen_req_headers({"Referer": "https://www.midishow.com/"}))
        bs = BeautifulSoup(rsp.text, "html.parser")
        midi_title = bs.find("div", attrs={"class": "ms-player-container"}).find("h1").get_text().strip()
        div0 = bs.find_all(lambda tag: tag.has_attr("data-mid"))[0]
        fake_midi_url = div0.attrs["data-mid"]
        csrf_token = bs.find_all("meta", {"name": "csrf-token"})[0].attrs["content"]
        midi_id = div0.attrs["data-id"]
        rsp1 = self.session.post(f"https://www.midishow.com/midi/new-file?id={midi_id}",
                                 headers=gen_req_headers({
                                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                     "Origin": "https://www.midishow.com",
                                     "Referer": page_url,
                                     "X-Csrf-Token": csrf_token,
                                     "X-Requested-With": "XMLHttpRequest"
                                 }),
                                 data={"id": midi_id})
        if rsp1.status_code != 200:
            print(rsp1.text)
            return None
        rsp2 = self.session.get(fake_midi_url
                                .replace("https://www.midishow.com", "https://s.midishow.net")
                                .replace(".mid?", ".js?"),
                                headers=static_headers)
        chr_set = hex2str(rsp1.headers.get("Etag")) + rsp1.text[56:]
        midi_file = decode_base64(rsp1.text[28: 56], chr_set) + decode_base64(rsp2.text[3: -3], chr_set) + decode_base64(rsp1.text[: 28], chr_set)
        return midi_file, midi_title

    def export_cookies(self):
        return self.session.cookies.items()
