from playwright.sync_api import sync_playwright
import json
import time
import os

def check_profile_feed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        
        with open('fb_cookies.json', 'r') as f:
            cookies = json.load(f)
        
        formatted_cookies = []
        for c in cookies:
            ss = c.get('sameSite', 'Lax')
            if ss.lower() not in ['strict', 'lax', 'none']:
                ss = 'Lax'
            formatted_cookies.append({
                'name': c['name'], 'value': c['value'], 'domain': c['domain'], 'path': c['path'],
                'secure': c['secure'], 'httpOnly': c['httpOnly'], 'sameSite': ss.capitalize()
            })
            
        context.add_cookies(formatted_cookies)
        page = context.new_page()
        
        print("Navigating to Profile...")
        # Direct link to the user's timeline
        page.goto('https://www.facebook.com/61586329972343', wait_until="domcontentloaded", timeout=60000)
        time.sleep(10)
        
        # Take a high-res screenshot of the timeline
        page.screenshot(path="fb_timeline_check.png", full_page=False)
        print("Screenshot of timeline saved to fb_timeline_check.png")
        
        # Check for privacy settings or "Only Me" icon on recent posts
        # This is harder to do via script, but the screenshot will tell the truth
        
        browser.close()

if __name__ == "__main__":
    check_profile_feed()
