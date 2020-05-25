from tweepy import OAuthHandler

_creds = {
    "RUD": {
        "CONS_KEY": "YiYRZRnFw6BmZ62JUQuRrJJ1V",
        "CONS_SECRET": "hQQUQIQqYxCwf9GD1k7E0v0uO3acPP3lxyJq6PkytNuMOqhivZ",
        "TOKEN": "132562597-zU3Z7EHp4Q3vJiXvKseL2ucVqALYldbI5B5l8IR0",
        "TOKEN_SECRET": "yaArEVX7I2d6TE9SX8toZjhzJsgvjfbKtcRDbZRGU9cB1",
    },
    "SAG": {
        "CONS_KEY": "n4IgjuZTLvAa9WXpJx7W0skch",
        "CONS_SECRET": "bRf2TZUbqFaDOZ4Y4EdQm8HHD783rthchtGs3D3317KalBRKGX",
        "TOKEN": "1254626494682238976-zT4eMwOCrzd9x1SUdq5y4OXSLsfnpf",
        "TOKEN_SECRET": "8wwXvZLEoESaJXGQ53kNTtslnZfMAhjE5aBAVhyBRTUPI",
    },
    "SHA": {
        "CONS_KEY": "s5JcGUsQsZbzztZglsKOAxp1g",
        "CONS_SECRET": "l59Hqb37lcqHrBvCE5ukfZAwCYazfOTjDO8vmkD1nj7TwNhRHI",
        "TOKEN": "1254385776176934913-uHCfy7ktByNDqHoXdDBLLtENXO6OkP",
        "TOKEN_SECRET": "pIUI2X1wWCAwK1UZIA97WZRL63mpLFxvgPDteaomnGOdz",
    },
    "VIS": {
        "CONS_KEY": "xX6K54mGcfcRrukhOkAQ9Uw8H",
        "CONS_SECRET": "UoVyfA7MUQg43rgVtfHuUGgQOCRx2tjgOTJ4y2INqX6uKuhrkZ",
        "TOKEN": "1254680534963240963-JE09HbFoivaeSMHOu1vbGSWbXKqOjG",
        "TOKEN_SECRET": "oErRHC0VZbTWbnLvpwEvqJMMuY5cKp0obKuVnkIiuhYcu",
    },
    "SHE": {
        "CONS_KEY": "IbVf6OKF149LvIaBaHLqATMcy",
        "CONS_SECRET": "UurXzYxD4az4mBNhZy3SYNMF9Ddmn4uAiEJxlwYWMivFoFtw5c",
        "TOKEN": "1251775148274839553-5XmofQVNiy09bCUchneleCfECGbrZ0",
        "TOKEN_SECRET": "hLrif1SabrixfwlsDCszGotoMxHoQoEIiPrTRHJnVHknS",
    },
}


def _load_creds(username):
    assert username in ["RUD", "SAG", "SHA", "VIS", "SHE"]
    return _creds[username]


def authenticate(username):
    credentials = _load_creds(username)

    auth = OAuthHandler(credentials["CONS_KEY"], credentials["CONS_SECRET"])
    auth.set_access_token(credentials["TOKEN"], credentials["TOKEN_SECRET"])

    return auth
