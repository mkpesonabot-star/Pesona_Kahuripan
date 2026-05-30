import requests
import json
import os
import re

def post_to_fb_mbasic_v5(message):
    cookie_path = 'fb_cookies.json'
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    cookies = {c['name']: c['value'] for c in cookies_list}

    session = requests.Session()
    session.cookies.update(cookies)
    
    # Use the Desktop UA to bypass the "Browser not supported" screen on mbasic
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    print("Fetching mbasic home page with Desktop UA...")
    res = session.get('https://mbasic.facebook.com/', headers=headers)
    
    # Save for debug
    with open('mbasic_v5_debug.html', 'w') as f:
        f.write(res.text)

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
            print("Post success!")
            return True
    else:
        print("Still blocked or tokens not found. Facebook might be forcing Desktop view or blocking mbasic for this account.")
            
    return False

if __name__ == "__main__":
    post_to_fb_mbasic_v5("Halo Bang Rico! Ini test post pertama Jeje dari VPS. Mantap! 🔥")
