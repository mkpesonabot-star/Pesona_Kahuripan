import requests
import json
import os
import re

def post_to_fb_mbasic_v4(message):
    cookie_path = 'fb_cookies.json'
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    cookies = {c['name']: c['value'] for c in cookies_list}

    session = requests.Session()
    session.cookies.update(cookies)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    print("Navigating to profile to find post form...")
    # Using the UID from the cookies/previous check
    profile_url = 'https://mbasic.facebook.com/61586329972343'
    res = session.get(profile_url, headers=headers)
    
    with open('profile_debug.html', 'w') as f:
        f.write(res.text)

    # Look for any form that looks like a composer
    # Usually it's a textarea name="xc_message"
    fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
    jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text)
    post_match = re.search(r'action="(/composer/mbasic/.*?)"', res.text)

    if fb_dtsg and post_match:
        post_url = "https://mbasic.facebook.com" + post_match.group(1).replace("&amp;", "&")
        data = {
            "fb_dtsg": fb_dtsg.group(1),
            "jazoest": jazoest.group(1),
            "xc_message": message,
            "view_post": "Post"
        }
        print("Tokens found. Sending post...")
        post_res = session.post(post_url, data=data, headers=headers)
        if post_res.status_code == 200:
            print("Post successful!")
            return True
    
    print("Could not post via profile. Trying one more: /home.php")
    home_res = session.get('https://mbasic.facebook.com/home.php', headers=headers)
    fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', home_res.text)
    post_match = re.search(r'action="(/composer/mbasic/.*?)"', home_res.text)
    
    if fb_dtsg and post_match:
        post_url = "https://mbasic.facebook.com" + post_match.group(1).replace("&amp;", "&")
        data = {
            "fb_dtsg": fb_dtsg.group(1),
            "jazoest": jazoest.group(1),
            "xc_message": message,
            "view_post": "Post"
        }
        session.post(post_url, data=data, headers=headers)
        print("Post attempt via /home.php sent.")
        return True

    return False

if __name__ == "__main__":
    post_to_fb_mbasic_v4("Halo Bang Rico! Ini test post pertama Jeje dari VPS. Mantap! 🔥")
