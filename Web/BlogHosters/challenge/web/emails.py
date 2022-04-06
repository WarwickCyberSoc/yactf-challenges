# TODO: Get mail API access


import os


def send_email(email_type, support_member, info):
    email_content = ""

    from database import query_db

    # Update support member magic code
    magic_code = os.urandom(16).hex()
    query_db(
        "UPDATE users SET magic_code = ? WHERE username = ?",
        (magic_code, support_member),
        one=True,
    )

    if email_type == "password_reset":
        email_content = """Hi there! 

User {} has requested a reset of their password. Please reach out to them and ensure they are authorised to change this password, then click the link below.

{}
""".format(
            info["username"],
            "http://bloghosters.local/password_reset?magic_code={}&new_password={}".format(
                magic_code, info["new_password"]
            ),
        )
    elif email_type == "new_submission":
        email_content = """Hi there! 

User {user} has updated their blog. Please review their submission, then approve it on the website if appropiate.

http://bloghosters.local/blog/{user}?reviewing=1&magic_code={magic_code}
""".format(
            user=info["username"], magic_code=magic_code
        )

    print("Sending email to support: ")
    print(email_content)
