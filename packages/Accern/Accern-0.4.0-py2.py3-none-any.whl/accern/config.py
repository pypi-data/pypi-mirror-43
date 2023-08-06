import json
import copy

CONFIG = {
    "file": None,
    "content": None,
}
CONFIG_DEFAULT = {
    "io": {
        "production": "https://io.accern.com/api/io/jobs",
        "staging": "https://io-staging.accern.com/api/io/jobs",
    },
    "v4_api": "https://feed.accern.com/v4/alphas",
    "v4_stream": "https://feed.accern.com/v4/stream",
}


def set_config_file(config_file):
    if config_file is None and CONFIG["file"] is None:
        return
    if config_file != CONFIG["file"]:
        CONFIG["file"] = config_file
        CONFIG["content"] = None


def get_config_file():
    return CONFIG["file"]


def get_config():
    # type: () -> dict
    res = CONFIG["content"]
    if res is None:
        if CONFIG["file"] is None:
            res = copy.deepcopy(CONFIG_DEFAULT)
        else:
            with open(CONFIG["file"], "r") as f_in:
                res = json.load(f_in)
        CONFIG["content"] = res  # type: ignore
    return res  # type: ignore
