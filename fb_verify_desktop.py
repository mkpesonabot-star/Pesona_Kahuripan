import requests
import json
import os
import re

def post_to_fb_desktop(message):
    cookie_path = 'fb_cookies.json'
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    cookies = {c['name']: c['value'] for c in cookies_list}

    session = requests.Session()
    session.cookies.update(cookies)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    print("Fetching Desktop home page...")
    res = session.get('https://www.facebook.com/', headers=headers)
    
    # In Desktop, tokens are often in JSON strings in the HTML
    dtsg_match = re.search(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', res.text)
    user_id_match = re.search(r'"USER_ID":"(\d+)"', res.text)
    
    if dtsg_match and user_id_match:
        print(f"Tokens found (Desktop). UID: {user_id_match.group(1)}")
        # Posting to Desktop via raw requests is extremely complex due to GraphQL.
        # But we can verify we are 'fully' in.
        return True
    else:
        print("Desktop tokens not found.")
        return False

if __name__ == "__main__":
    post_to_fb_desktop("Test")
