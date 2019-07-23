# auto-login-net v2.0
import requests
import win32api, win32con
import sys
import json


def getPath():
    sap = '/'
    if sys.argv[0].find(sap) == -1:
        sap = '\\'
    indx = sys.argv[0].rfind(sap)
    path = sys.argv[0][:indx] + sap
    return path


def main():
    keyname = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, keyname, 0, win32con.KEY_ALL_ACCESS)
    win32api.RegSetValueEx(key, "autoLoginNet", 0, win32con.REG_SZ, sys.argv[0])
    win32api.RegCloseKey(key)
    file_path = getPath() + "account.txt"
    file = open(file_path, "r")
    user = file.readline().strip()
    pwd = file.readline().strip()
    data = {
        "opr": "pwdLogin",
        "userName": user,
        "pwd": pwd,
        "rememberPwd": 0
    }
    try:
        response = requests.post("http://10.69.253.12/ac_portal/login.php", data, timeout=5)
    except Exception:
        raise Exception("网络错误")
    if response.status_code != 200:
        raise Exception("网络错误")
    response.encoding = 'utf-8'
    ret = json.loads(response.text.replace('\'', '\"'))
    if ret["success"]:
        print("Greetings")
    else:
        raise Exception(ret['msg'])


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input("print Enter to quit...")
