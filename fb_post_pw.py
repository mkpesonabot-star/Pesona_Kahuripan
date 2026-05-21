from playwright.sync_api import sync_playwright
import json
import time

def fb_post_playwright(message):
    with sync_playwright() as p:
        # Open browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Load cookies
        with open('fb_cookies.json', 'r') as f:
            cookies = json.load(f)
        
        # Format cookies for Playwright
        formatted_cookies = []
        for c in cookies:
            formatted_cookies.append({
                'name': c['name'],
                'value': c['value'],
                'domain': c['domain'],
                'path': c['path'],
                'secure': c['secure'],
                'httpOnly': c['httpOnly'],
                'sameSite': 'Lax' if c.get('sameSite') == 'unspecified' else c.get('sameSite', 'Lax').capitalize()
            })
            
        context.add_cookies(formatted_cookies)
        page = context.new_page()
        
        print("Navigating to Facebook...")
        page.goto('https://www.facebook.com/')
        time.sleep(5)
        
        # Take a screenshot to verify login state
        page.screenshot(path="fb_login_check.png")
        
        try:
            # Click the post box - finding the selector can be tricky on modern FB
            # We look for "What's on your mind" or similar
            print("Looking for post box...")
            post_trigger = page.get_by_text("What's on your mind", exact=False).first
            if post_trigger.is_visible():
                post_trigger.click()
                time.sleep(2)
                
                # Type the message
                # FB uses contenteditable divs, so we might need to use generic locator
                print(f"Typing message: {message}")
                page.keyboard.type(message)
                time.sleep(2)
                
                # Click Post button
                print("Clicking Post...")
                post_button = page.get_by_role("button", name="Post", exact=True)
                post_button.click()
                time.sleep(5)
                print("Done!")
                return True
            else:
                print("Post box not found. Maybe layout is different or login failed.")
                return False
        except Exception as e:
            print(f"Error during posting: {e}")
            return False
        finally:
            browser.close()

if __name__ == "__main__":
    fb_post_playwright("Halo dari Jeje Bot! Bang Rico mantap. [Test Post via Playwright]")
