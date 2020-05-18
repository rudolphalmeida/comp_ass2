from tweepy import OAuthHandler

_creds = {
    "RUD": {
        "RUD_CONS_KEY": "YiYRZRnFw6BmZ62JUQuRrJJ1V",
        "RUD_CONS_SECRET": "hQQUQIQqYxCwf9GD1k7E0v0uO3acPP3lxyJq6PkytNuMOqhivZ",
        "RUD_TOKEN": "132562597-zU3Z7EHp4Q3vJiXvKseL2ucVqALYldbI5B5l8IR0",
        "RUD_TOKEN_SECRET": "yaArEVX7I2d6TE9SX8toZjhzJsgvjfbKtcRDbZRGU9cB1",
    },
    "SAG": {
        "SAG_CONS_KEY": "n4IgjuZTLvAa9WXpJx7W0skch",
        "SAG_CONS_SECRET": "bRf2TZUbqFaDOZ4Y4EdQm8HHD783rthchtGs3D3317KalBRKGX",
        "SAG_TOKEN": "1254626494682238976-zT4eMwOCrzd9x1SUdq5y4OXSLsfnpf",
        "SAG_TOKEN_SECRET": "8wwXvZLEoESaJXGQ53kNTtslnZfMAhjE5aBAVhyBRTUPI",
    },
}


def _load_creds(username):
    assert username in ["RUD", "SAG", "SHA", "VIS", "SHE"]
    return _creds[username]


def authenticate(username):
    credentials = _load_creds(username)

    auth = OAuthHandler(
        credentials[f"{username}_CONS_KEY"], credentials[f"{username}_CONS_SECRET"]
    )
    auth.set_access_token(
        credentials[f"{username}_TOKEN"], credentials[f"{username}_TOKEN_SECRET"],
    )

    return auth
