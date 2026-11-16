import sys

SCENARIOS = {
    "login": (
        "https://the-internet.herokuapp.com/login",
        [
            "type tomsmith into the username field",
            "type SuperSecretPassword! into the password field",
            "click login",
            "click logout",
        ],
    ),
    "wikipedia": (
        "https://www.wikipedia.org",
        [
            "type Chromium web browser into the search box",
            "press Enter in the search box",
            "click the Blink link",
        ],
    ),
}

NAME = sys.argv[1] if len(sys.argv) > 1 else "login"
URL, STEPS = SCENARIOS[NAME]
