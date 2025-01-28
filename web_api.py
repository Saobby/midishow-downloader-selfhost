import requests
import brotli
import json
from bs4 import BeautifulSoup
import time


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


def get_csrf_token(page_url: str, session: requests.Session):
    req_headers = gen_req_headers()
    rsp = session.get(page_url, headers=req_headers)
    bs = BeautifulSoup(rsp.text, "html.parser")
    csrf_tag = bs.find_all("meta", {"name": "csrf-token"})[0]
    return csrf_tag.attrs["content"], session


def login(identity: str, password: str, session: requests.Session):
    req_headers = gen_req_headers({"Cache-Control": "max-age=0", "Content-Type": "application/x-www-form-urlencoded",
                                   "Origin": "https://www.midishow.com", "Referer": "https://www.midishow.com/user/account/login"})
    csrf_token, session = get_csrf_token("https://www.midishow.com/user/account/login", session)
    req_data = {"_csrf": csrf_token, "LoginForm[identity]": identity, "LoginForm[password]": password, "login-button": ""}
    rsp = session.post("https://www.midishow.com/user/account/login", headers=req_headers, data=req_data, allow_redirects=False)
    if "Location" in rsp.headers:
        return session
    return None  # Failed to login


def download_midi(midi_id: str, session: requests.Session):
    req_url = "https://www.midishow.com/midi/download?id={}".format(midi_id)
    req_headers = gen_req_headers({"Cache-Control": "max-age=0", "Content-Type": "application/x-www-form-urlencoded",
                                   "Origin": "https://www.midishow.com", "Referer": req_url})
    csrf_token, session = get_csrf_token(req_url, session)
    req_data = {"_csrf": csrf_token}
    rsp = session.post(req_url, headers=req_headers, data=req_data)
    bs = BeautifulSoup(rsp.text, "html.parser")
    a_tags = bs.find_all("a")
    a_tag = None
    for tag in a_tags:
        if "/midi/download-file?t=" in tag.attrs["href"]:
            a_tag = tag
            break
    if a_tag is None:
        return None
    midi_url = "https://www.midishow.com"+a_tag.attrs["href"]
    req_headers = gen_req_headers({"Referer": req_url})
    rsp = session.get(midi_url, headers=req_headers)
    return rsp.content


def get_midi_info(page_url: str, session: requests.Session):
    rsp = session.get(page_url, headers=gen_req_headers({"Referer": "https://www.midishow.com/"}))
    bs = BeautifulSoup(rsp.text, "html.parser")
    rating_tags = bs.find_all("div", attrs={"id": "rating"})
    if len(rating_tags) == 0:
        return None
    midi_id = rating_tags[0].attrs["data-item-id"]
    container_tags = bs.find_all("div", attrs={"class": "ms-player-container"})
    if len(container_tags) == 0:
        return None
    h1_tags = container_tags[0].find_all("h1")
    if len(h1_tags) == 0:
        return None
    midi_title = h1_tags[0].get_text().strip()
    credit_a = bs.find("a", attrs={"href": "/help/credit.ab", "title": "积分规则"})
    if credit_a is None:
        return None
    credit_remaining = int(credit_a.get_text().split(":")[-1].strip())
    return midi_id, midi_title, credit_remaining


def gen_session(cookies: tuple = None, proxy: dict = None):
    ses = requests.session()
    if proxy is not None:
        ses.proxies.update(proxy)
    if cookies:
        for cookie in cookies:
            ses.cookies.set(*cookie)
    return ses


def comment_midi(session: requests.Session, midi_id: int, content: str):
    csrf_token, _ = get_csrf_token(f"https://www.midishow.com/midi/{midi_id}.html", session)
    req_payload = {"_csrf": csrf_token,
                   "MidiComment[content]": content,
                   "MidiComment[quote_id]": "0"}
    rsp = session.post(f"https://www.midishow.com/midi/add-comment?id={midi_id}",
                       headers=gen_req_headers({"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                                                "origin": "https://www.midishow.com",
                                                "referer": f"https://www.midishow.com/midi/{midi_id}.html",
                                                "x-csrf-token": csrf_token,
                                                "x-requested-with": "XMLHttpRequest"}),
                       data=req_payload)
    try:
        rsp = json.loads(rsp.text)
    except:
        print("Failed to comment")
        print(rsp.text)
        time.sleep(5)
        return False
    if rsp["result"]:
        return True
    print("Failed to comment")
    print(rsp)
    return False
