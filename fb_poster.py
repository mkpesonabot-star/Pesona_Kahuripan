import requests
import json
import os
import re

def post_to_fb(message):
    cookie_path = 'fb_cookies.json'
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    cookies = {c['name']: c['value'] for c in cookies_list}

    session = requests.Session()
    session.cookies.update(cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # Step 1: Get fb_dtsg and jazoest from the home page
    print("Fetching tokens...")
    res = session.get('https://mbasic.facebook.com/', headers=headers)
    
    # Simple regex to find tokens on mbasic
    fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
    jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text)
    
    # Find the post action URL
    post_url_match = re.search(r'action="(/composer/mbasic/.*?)"', res.text)

    if not fb_dtsg or not post_url_match:
        print("Error: Could not find post tokens or URL. Facebook might be blocking mbasic or layout changed.")
        return False

    post_url = 'https://mbasic.facebook.com' + post_url_match.group(1).replace('&amp;', '&')
    
    data = {
        'fb_dtsg': fb_dtsg.group(1),
        'jazoest': jazoest.group(1),
        'xc_message': message,
        'view_post': 'Post'
    }

    print(f"Posting message: {message}")
    response = session.post(post_url, data=data, headers=headers)
    
    if response.status_code == 200:
        print("Success! Message posted (check your profile).")
        return True
    else:
        print(f"Failed to post. Status code: {response.status_code}")
        return False

if __name__ == "__main__":
    post_to_fb("Halo dari Jeje Bot! Bang Rico mantap. [Test Post]")
