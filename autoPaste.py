# AutoPaste v1.0
import win32con
import win32clipboard as clip
import requests


def get_clipboard() -> str:
    clip.OpenClipboard()
    contents = clip.GetClipboardData(win32con.CF_UNICODETEXT)
    clip.CloseClipboard()
    return contents


def set_clipboard(data: str) -> None:
    clip.OpenClipboard()
    clip.EmptyClipboard()
    if data != "":
        clip.SetClipboardData(win32con.CF_UNICODETEXT, data)
    clip.CloseClipboard()


def requestPaste(data: str) -> str:
    d = {
        "poster": "autoPaste",
        "syntax": "text",
        "expiration": None,
        "content": data,
    }
    if "#include" in data:
        d["syntax"] = "cpp"
    response = requests.post("https://paste.ubuntu.com/", d)
    if response.status_code != 200:
        raise Exception("Network Error")
    his = response.history[0]
    return his.headers["location"]
    pass


def main():
    s = get_clipboard()
    url = requestPaste(s)
    set_clipboard(url)
    print("Paste completed, the url was copied to your clipboard")
    pass


if __name__ == '__main__':
    print("AutoPaste to paste.ubuntu.com by smz")
    try:
        main()
    except TypeError:
        print("Error: The Clipboard's content is not text data or it's empty")
    except Exception as e:
        print("Error: " + str(e))
    finally:
        input("press Enter to quit")
