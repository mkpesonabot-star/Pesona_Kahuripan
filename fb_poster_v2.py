import requests
import json
import os
import re

def post_to_fb_mbasic(message):
    cookie_path = 'fb_cookies.json'
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    cookies = {c['name']: c['value'] for c in cookies_list}

    session = requests.Session()
    session.cookies.update(cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    print("Checking mbasic connectivity...")
    res = session.get('https://mbasic.facebook.com/', headers=headers)
    
    # Debug: Save the HTML to see why it fails
    with open('mbasic_debug.html', 'w') as f:
        f.write(res.text)
        
    if "Log In" in res.text and "c_user" not in session.cookies:
        print("Error: Cookies didn't work for mbasic.")
        return False

    # Look for the form action and tokens
    fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
    jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text)
    
    # On mbasic, the post form is usually the first one
    # We look for the action URL specifically for /composer/mbasic/
    post_match = re.search(r'action="(/composer/mbasic/.*?)"', res.text)

    if fb_dtsg and post_match:
        post_url = "https://mbasic.facebook.com" + post_match.group(1).replace("&amp;", "&")
        data = {
            "fb_dtsg": fb_dtsg.group(1),
            "jazoest": jazoest.group(1),
            "xc_message": message,
            "view_post": "Post"
        }
        print(f"Tokens found. Sending post to {post_url}...")
        post_res = session.post(post_url, data=data, headers=headers)
        if post_res.status_code == 200:
            print("Post sent! Check your profile.")
            return True
        else:
            print(f"Failed to post. Status: {post_res.status_code}")
    else:
        print("Could not find tokens or post URL. Trying alternative...")
        # Sometimes it's /a/cp.php
        alt_match = re.search(r'action="(/a/cp\.php.*?)"', res.text)
        if alt_match:
             print("Found alternative post URL. Trying...")
             # This requires more complex form handling. 
             # Let's just report the failure for now to avoid mess.
        
    return False

if __name__ == "__main__":
    post_to_fb_mbasic("Halo Bang Rico! Ini test post pertama Jeje dari VPS. Mantap! 🔥")
