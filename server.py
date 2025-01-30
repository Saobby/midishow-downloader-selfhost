from flask import Flask, render_template, request, abort
import json
import random
import redis_api
import web_api_v2
import base64
import re
from config import MIDISHOW_ACCOUNTS, SERVER_PORT, SERVER_HOST
import webbrowser

app = Flask(__name__)


def gen_returns(success=True, message="OK", data=None, **kwargs):
    ret = {"success": success, "message": message, "data": data}
    for k, v in kwargs.items():
        ret[k] = v
    return json.dumps(ret)


def get_api_instance(username: str, password: str):
    db_session = redis_api.get_session()
    cookies = db_session.get(f"midishow_downloader_cookies_{username}")
    if cookies:
        cookies = tuple(json.loads(cookies))
        api_instance = web_api_v2.MidiShowAPI()
        api_instance.login_by_cookies(cookies)
        db_session.close()
        return api_instance
    else:
        api_instance = web_api_v2.MidiShowAPI()
        res = api_instance.login_by_password(username, password)
        if not res:
            db_session.close()
            return None
        db_session.setex(
            f"midishow_downloader_cookies_{username}",
            24 * 3600,
            json.dumps(api_instance.export_cookies())
        )
        db_session.close()
        return api_instance


@app.route("/api/download_midi", methods=["post"])
def api_download_midi():
    if request.json is None:
        return abort(400)
    url = request.json.get("url")
    if url is None:
        return abort(400)
    if re.match("^https://www\\.midishow\\.com/(en/|zh-tw/)?midi/.+$", url) is None:
        return gen_returns(False, "请输入有效的页面地址"), 400
    api_instance = get_api_instance(*random.choice(MIDISHOW_ACCOUNTS))
    if api_instance is None:
        return gen_returns(False, "登录失败! 请检查用户名和密码是否设置正确!"), 500
    try:
        data, midi_title = api_instance.download_midi(url)
    except:
        return gen_returns(False, "无法下载 midi , 请检查链接是否正确!"), 500
    if data is None:
        return gen_returns(False, "你的账户被风控，请重新注册一个账户并设置好账户密码后重试!"), 500
    data_b64 = base64.b64encode(data).decode()
    return gen_returns(True, "OK", {"file": data_b64, "title": midi_title})


@app.errorhandler(400)
def error_400(err):
    return gen_returns(False, "参数错误"), 400


@app.errorhandler(404)
def error_404(err):
    return gen_returns(False, "你要访问的页面不存在"), 404


@app.errorhandler(500)
def error_500(err):
    return gen_returns(False, "服务器内部错误! 请携带错误日志前往 Github Issues 报告问题!"), 500


@app.after_request
def add_header(r):
    if request.headers.get("origin") is not None:
        r.headers["Access-Control-Allow-Origin"] = request.headers.get("origin")
    r.headers["Access-Control-Allow-Headers"] = "Content-Type"
    r.headers["Access-Control-Allow-Credentials"] = "true"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    r.headers["Access-Control-Max-Age"] = "600"
    if "/api/" in request.path:
        r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


@app.route("/", methods=["get"])
def index():
    return render_template("index.html")


def main():
    port = random.randint(10000, 20000) if SERVER_PORT == -1 else SERVER_PORT
    webbrowser.open(f"http://{SERVER_HOST}:{port}")
    app.run(port=port, host=SERVER_HOST)


if __name__ == '__main__':
    main()
