####                        ####
# \\\ SynergyStorm v.2.4.1 /// #
# ///      written by:     /// #
# \\\      sudo-matcha     \\\ #
####                        ####


from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import inquirer
import json
import requests
from pybetterloader.Loader import Loader
import re
import argparse
from time import sleep
from shutil import get_terminal_size

version_name = '2.4.1'
ROOT = __file__.removesuffix('synergystorm.py')

parser = argparse.ArgumentParser(
    prog="synergystorm",
    description=f"A command-line client for making some features of SynergyVue better (and for being a little evil).",
)
parser.add_argument(
    "--version",
    action="version",
    version=f"%(prog)s {version_name}",
    help="display the version number and exit",
)
parser.add_argument(
    "-id",
    nargs="?",
    type=int,
    help="Provide a student ID for authentication (requires --password)",
)
parser.add_argument(
    "--password",
    "-p",
    nargs="?",
    type=str,
    help="Provide a password for authentication (required by -id)",
)
parser.add_argument(
    "--show_webdriver",
    "-W",
    nargs='?',
    action='store_true',
    help='Show Selenium Webdriver instance (removes \'--headless\' argument)',
)
argv = parser.parse_args()
# def exit_gracefully(exit_code: int) -> None:
#     print('\x1b[?1049l]')
#     exit(exit_code)

loader = Loader(
    "Checking your connection, please wait...",
    anim="wifi",
    end="",
    color=(255, 255, 120),
    quips=False,
)
loader.start()
sleep(0.2)
try:
    online_check = requests.get("https://www.example.com")
except requests.exceptions.ConnectionError as e:
    loader.stop()
    print(
        f"\x1b[38;2;255;50;50m\uea87 \x1b[1mThere was trouble establishing a connection.\n  Please check your connection and try again.\x1b[0m"
    )
    print(f"\x1b[2m{e}\x1b[0m")
    exit(1)
loader.stop()

options = webdriver.ChromeOptions()
if not argv.show_webdriver:
    options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


def rgb_fg(r=0, g=0, b=0) -> str:
    if type(r) is tuple:
        r, g, b = r
    return f"\x1b[38;2;{r};{g};{b}m"


def rgb_bg(r=0, g=0, b=0) -> str:
    if type(r) is tuple:
        r, g, b = r
    return f"\x1b[48;2;{r};{g};{b}m"


def hex2rgb(h: str) -> tuple[int]:
    return tuple(int(h.strip("#")[i : i + 2], 16) for i in (0, 2, 4))


def rgb_brightness(rgb: tuple) -> float:
    r, g, b = rgb
    return (
        max(r / 255, g / 255, b / 255),
        max(r / 255, g / 255, b / 255),
        max(r / 255, g / 255, b / 255),
    )


def rgb2hsv(rgb: tuple) -> tuple:
    # https://www.rapidtables.com/convert/color/rgb-to-hsv.html
    r, g, b = rgb
    rgbP = rp, gp, bp = (r / 255, g / 255, b / 255)
    cmax = max(rgbP)
    cmin = min(rgbP)
    delta = cmax - cmin

    # hue
    if delta == 0:
        hue = 0
    elif cmax == rp:
        hue = 60 * (((gp - bp) / delta) % 6)
    elif cmax == gp:
        hue = 60 * (((bp - rp) / delta) + 2)
    elif cmax == bp:
        hue = 60 * (((rp - gp) / delta) + 4)

    # saturation
    if cmax == 0:
        saturation = 0
    else:
        saturation = delta / cmax

    # value
    value = cmax

    return (hue, saturation, value)


def hsv2rgb(hsv: tuple) -> tuple:
    # https://www.rapidtables.com/convert/color/hsv-to-rgb.html
    h, s, v = hsv

    C = v * s
    X = C * (1 - abs(h / 60 % 2 - 1))
    m = v - C

    if 0 <= h < 60:
        rgbP = (C, X, 0)
    elif 60 <= h < 120:
        rgbP = (X, C, 0)
    elif 120 <= h < 180:
        rgbP = (0, C, X)
    elif 180 <= h < 240:
        rgbP = (0, X, C)
    elif 240 <= h < 300:
        rgbP = (X, 0, C)
    elif 300 <= h < 360:
        rgbP = (C, 0, X)

    rp, gp, bp = rgbP
    rgb = ((rp + m) * 255, (gp + m) * 255, (bp + m) * 255)
    return rgb


def print_splash() -> None:
    term_h, term_w = get_terminal_size()
    if term_w >= 29:
        with open(f"{ROOT}/splash", "r") as f:
            splash = f.read()
        splash_lines = splash.split("\n")
        for i, line in enumerate(splash_lines):
            for char in line:
                if char in ["_", "/", "\\", ",", "`"]:
                    print(f"{rgb_fg(160,160,255)}{char}", end="")
                else:
                    print(f"{rgb_fg(255,90,90)}{char}", end="")

            if i == 9:
                print(f"   \x1b[7m v{version_name} \x1b[0m", end="")
            print()
    else:
        with open(f"{ROOT}/splash_small", "r") as f:
            splash = f.read()
        splash_lines = splash.split("\n")
        for i, line in enumerate(splash_lines):
            for char in line:
                if char in ["_", "/", "\\", ",", "`"]:
                    print(f"{rgb_fg(160,160,255)}{char}", end="")
                else:
                    print(f"{rgb_fg(255,90,90)}{char}", end="")

            if i == 4:
                print(f"   \x1b[7m v{version_name} \x1b[0m", end="")
            print()


def prompt_login(student_id: str = None, password: str = None) -> None:
    flag = True
    loader = Loader(
        "Requesting Login Page...",
        color=(50, 181, 144),
        timeout=0.25,
        quips=False,
        end="",
        anim="wifi",
    )
    loader.start()
    while flag:
        driver.get(
            "https://synergypvue.kentwoodps.org/PXP2_Login_Student.aspx?regenerateSessionId=True"
        )
        loader.stop()
        if not (student_id or password):
            creds = [
                inquirer.Text(name="student_id", message="Enter your Student ID"),
                inquirer.Password(name="password", message="Password"),
            ]
            creds = inquirer.prompt(creds)
            if not creds:
                exit(0)
        else:
            creds = {"student_id": student_id, "password": password}

        driver.find_element(By.ID, "ctl00_MainContent_username").send_keys(
            creds["student_id"]
        )
        driver.find_element(By.ID, "ctl00_MainContent_password").send_keys(
            creds["password"]
        )
        loader = Loader(
            "Logging you in...",
            color=(255, 255, 255),
            timeout=0.25,
            anim="hourglass",
            quips=False,
            end="",
        )
        loader.start()
        driver.find_element(By.ID, "ctl00_MainContent_Submit1").click()
        if (
            driver.current_url
            == "https://synergypvue.kentwoodps.org/PXP2_Login_Student.aspx?regenerateSessionId=True"
        ):
            loader.stop()
            print(
                f"\x1b[1m{rgb_fg(255,50,50)}Invalid Username or Password, Try again.\x1b[0m"
            )
        elif driver.current_url == "https://synergypvue.kentwoodps.org/Home_PXP2.aspx":
            loader.stop()
            print(f"\x1b[1m{rgb_fg(50,255,50)}\uf058 Logged in Succesfully!\x1b[0m")
            name = driver.find_element(By.ID, "Greeting").text
            print(
                f"{rgb_fg(120,120,255)}\ueb99 \x1b[1m{name}\x1b[0m".encode(
                    "utf-16"
                ).decode("utf-16")
            )
            flag = False


def get_session_id() -> str:
    if driver.current_url != "https://synergypvue.kentwoodps.org/Home_PXP2.aspx":
        return None

    print("Getting Session ID...")
    return driver.get_cookies()[1]["value"]


def generate_headers(session_id: str) -> dict:
    # Making our own headers with grabbed session_id >:3
    headers = {
        "Host": "synergypvue.kentwoodps.org",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://synergypvue.kentwoodps.org/Home_PXP2.aspx",
        "Content-Type": "application/json",
        "Origin": "https://synergypvue.kentwoodps.org",
        "Connection": "keep-alive",
        "Cookie": f"PVUE=eng; ASP.NET_SessionId={session_id}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
    }
    return headers


def create_hall_pass(headers: dict, roomGU: str, minutes: int) -> None:
    url = "https://synergypvue.kentwoodps.org/api/v1/components/pxp/svue-hallpass/SvueHallPass/CreateHallPass"
    body = {"roomGU": roomGU, "minutes": minutes}
    num = [
        inquirer.Text(name="num", message="Number of Passes to Send"),
    ]
    num = inquirer.prompt(num)
    if not num:
        exit(0)
    else:
        num = int(num["num"])
    for _ in range(num):
        resp = requests.post(url=url, json=body, headers=headers)
        with open("resp.json", "w") as f:
            json.dump(resp.json(), f)
        try:
            if resp.json()["error"]:
                print(
                    f"\x1b[1m{rgb_fg(255,50,50)}\uea87 {resp.json()['error']['message']}"
                )
                exit(1)
        except KeyError:
            print(
                f"\x1b[1m{rgb_fg(50,255,50)}\uf058 Hallpass Created Succesfully!\x1b[0m"
            )


def get_hall_pass_rooms(headers: dict) -> dict:
    url = "https://synergypvue.kentwoodps.org/api/v1/components/pxp/svue-hallpass/SvueHallPass/GetHallPassRooms"
    resp = requests.post(url, headers=headers)
    return resp.json()


def prompt_roomGU(hall_pass_rooms: dict) -> str:
    rooms_dicts = hall_pass_rooms["data"]
    rooms = {}
    roomGU_name = {}
    for room in rooms_dicts:
        rooms[room["roomName"]] = {
            "roomGU": room["roomGU"],
            "color": hex2rgb(room["color"]),
            "maxTime": room["maxTime"],
        }
        roomGU_name[room["roomGU"]] = room["roomName"]
    choices = [
        f"{rgb_fg(tuple(int(i)+100 for i in data['color']))}{name}  \x1b[2;3m{data['roomGU']}\x1b[0m"
        for name, data in rooms.items()
    ]

    questions = [
        inquirer.List(
            name="room_name", message="Choose a room", choices=choices, carousel=True
        )
    ]
    answer = inquirer.prompt(questions=questions)
    if not answer:
        exit(0)
    room_name = answer["room_name"]
    room_name = re.match(
        "^\\x1b\[38;2;(?:\d{1,3};?){3}m(.+)\s{2}\\x1b\[2;3m.+\\x1b\[0m$", room_name
    ).groups()[0]
    max_time = rooms[room_name]["maxTime"]
    roomGU = rooms[room_name]["roomGU"]
    return roomGU, max_time


def get_future_passes(headers: dict):
    resp = requests.get(
        "https://synergypvue.kentwoodps.org/api/v1/components/pxp/svue-hallpass/SvueHallPass/GetFuturePasses",
        headers=headers,
    )
    num_passes = len(resp.json()["data"])
    print(len)


def main() -> None:
    # print('\x1b[?1049h')
    print_splash()
    prompt_login(student_id=argv.id, password=argv.password)
    session_id = get_session_id()
    driver.close()
    headers = generate_headers(session_id=session_id)
    hall_pass_rooms = get_hall_pass_rooms(headers=headers)
    roomGU, max_time = prompt_roomGU(hall_pass_rooms=hall_pass_rooms)
    create_hall_pass(headers=headers, roomGU=roomGU, minutes=max_time)


if __name__ == "__main__":
    main()
