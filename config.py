import toml

conf = toml.load("./config.toml")

REDIS_HOST = conf["redis"]["host"]
REDIS_PORT = conf["redis"]["port"]
REDIS_PASSWD = conf["redis"]["password"]

MIDISHOW_ACCOUNTS = [(i["username"], i["password"]) for i in conf["midishow"]["accounts"]]

SERVER_HOST = conf["server"]["host"]
SERVER_PORT = conf["server"]["port"]
