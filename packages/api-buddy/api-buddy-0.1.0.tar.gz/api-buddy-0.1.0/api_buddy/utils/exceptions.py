import random
from colorama import Fore, Style
from typing import NoReturn
from api_buddy.utils import PREFS_FILE

EXAMPLE_PREFS = """
api_url: https://api.url.com
auth_type: oauth2
oauth2:
  client_id: your_client_id
  client_secret: your_client_secret
  scopes:
    - one_scope
    - another_scope
auth_test_status: 401
api_version: 2
verify_ssl: false
timeout: 100
headers:
  Cookie: flavor=chocolate-chip; milk=please;
  Origin: your-face
verboseness:
  request: true
  response: true
indent:
  4
theme: paraiso-dark
variables:
  user_id: ab12c3d
  email: me@email.com
"""


class APIBuddyException(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message


def exit_with_exception(err: APIBuddyException) -> NoReturn:
    emoji = random.choice((
        '⚠️',
        '😭',
        '😮',
        '🙊',
        '🐛',
        '🔥',
    ))
    pleasantry = random.choice((
        'Oh no',
        'Whoops',
        'Oops',
        'Crikey',
        'Dang',
        'Bruh',
        'Woah',
    ))
    print(
        f'{Fore.YELLOW}{Style.BRIGHT}{pleasantry}! {emoji}\n'
        f'{Style.NORMAL}{err.title}{Style.RESET_ALL}\n\n'
        f'{err.message}\n'
    )
    exit(1)


class PrefsException(APIBuddyException):
    TITLE_HEADERS = (
        'There\'s a problem with your preferences',
        'Your preferences appear to be borked',
        'Your preferences aren\'t quite right',
        'Your preferences are a bit off',
        'It looks like your preferences are messed up',
    )
    MESSAGE_FOOTERS_1 = (
        f'Open up',
        f'Crack open',
        f'Check out',
    )
    MESSAGE_FOOTERS_2 = (
        'and have a look',
        'and fix it up',
        'and make it right',
    )

    def __init__(self, title: str, message: str) -> None:
        header = random.choice(self.TITLE_HEADERS)
        footer_1 = random.choice(self.MESSAGE_FOOTERS_1)
        footer_2 = random.choice(self.MESSAGE_FOOTERS_2)
        prefs_title = f'{header}\n{title}'
        prefs_msg = (
            f'{message}\n\n{footer_1} '
            f'{Fore.MAGENTA}{PREFS_FILE}{Style.RESET_ALL} '
            f'{footer_2} -- here\'s an example with all the prefs:\n'
            f'{EXAMPLE_PREFS}'
        )
        return super().__init__(prefs_title, prefs_msg)


class ConnectionException(APIBuddyException):
    TITLES = (
        'There was a problem connecting that url',
        'I can\'t reach that url',
        'I can\'t find that url in the interwebs',
    )
    MESSAGES = (
        'Are you on WiFi?',
        'Is that even a real API?',
        'Maybe try again?',
        'Do you have a hotspot or something?',
        'I think your WiFi is busted',
    )

    def __init__(self) -> None:
        msg = random.choice(self.MESSAGES)
        return super().__init__(
            title=random.choice(self.TITLES),
            message=(
                f'{msg}\n\nCheck your {Fore.MAGENTA}api_url{Style.RESET_ALL} '
                'setting in your preferences and make sure you\'r connected to'
                ' the internet'
            ),
        )


class TimeoutException(APIBuddyException):
    TITLES = (
        'This is taking forever',
        'I can\'t wait for this response anymore',
        'Yo what\'s taking so long',
    )

    def __init__(self, timeout: int) -> None:
        return super().__init__(
            title=random.choice(self.TITLES),
            message=(
                'Your request timed out. I waited '
                f'{Fore.MAGENTA}{Style.BRIGHT}{timeout}{Style.RESET_ALL} '
                'seconds.\n\n'
                'If you want to wait longer, you should update the '
                f'{Fore.MAGENTA}timeout{Style.RESET_ALL} setting in your '
                'preferences.'
            ),
        )
