import requests
import json
import os
import re

def post_to_fb_mbasic_final(message):
    cookie_path = 'fb_cookies.json'
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    cookies = {c['name']: c['value'] for c in cookies_list}

    session = requests.Session()
    session.cookies.update(cookies)
    
    # Using a common Mobile User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    }

    print("Fetching mbasic home page...")
    res = session.get('https://mbasic.facebook.com/', headers=headers)
    
    # Try to find the "What's on your mind" link/form
    # On mbasic, the post form is usually right there if you are logged in
    fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
    jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text)
    post_match = re.search(r'action="(/composer/mbasic/.*?)"', res.text)

    if not fb_dtsg or not post_match:
        print("Tokens not found on home page. Trying to navigate to composer directly...")
        composer_res = session.get('https://mbasic.facebook.com/composer/mbasic/', headers=headers)
        fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', composer_res.text)
        jazoest = re.search(r'name="jazoest" value="(.*?)"', composer_res.text)
        post_match = re.search(r'action="(/composer/mbasic/.*?)"', composer_res.text)

    if fb_dtsg and post_match:
        post_url = "https://mbasic.facebook.com" + post_match.group(1).replace("&amp;", "&")
        data = {
            "fb_dtsg": fb_dtsg.group(1),
            "jazoest": jazoest.group(1),
            "xc_message": message,
            "view_post": "Post"
        }
        print(f"Tokens found. Sending post...")
        post_res = session.post(post_url, data=data, headers=headers)
        if post_res.status_code == 200:
            print("Success! Post should be live.")
            return True
        else:
            print(f"Failed. Status: {post_res.status_code}")
    else:
        print("Critical Error: Could not find post form even on composer page.")
        # Save HTML for debugging
        with open('composer_debug.html', 'w') as f:
            f.write(res.text)
            
    return False

if __name__ == "__main__":
    post_to_fb_mbasic_final("Halo Bang Rico! Ini test post pertama Jeje dari VPS. Mantap! 🔥")
