from playwright.sync_api import sync_playwright
import json
import time
import os

def fb_post_playwright(message):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        # Using a more standard desktop UA
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        
        # Load cookies from EditThisCookie format
        with open('fb_cookies.json', 'r') as f:
            cookies = json.load(f)
        
        formatted_cookies = []
        for c in cookies:
            ss = c.get('sameSite', 'Lax')
            if ss.lower() not in ['strict', 'lax', 'none']:
                ss = 'Lax'
            
            formatted_cookies.append({
                'name': c['name'],
                'value': c['value'],
                'domain': c['domain'],
                'path': c['path'],
                'secure': c['secure'],
                'httpOnly': c['httpOnly'],
                'sameSite': ss.capitalize()
            })
            
        context.add_cookies(formatted_cookies)
        page = context.new_page()
        
        print("Navigating to Facebook...")
        # Reduce wait intensity to avoid timeout on slow networks
        page.goto('https://www.facebook.com/', wait_until="domcontentloaded", timeout=60000)
        time.sleep(10) # Wait for JS to settle manually
        
        # Take a screenshot to verify login state
        page.screenshot(path="fb_login_check.png")
        print("Screenshot saved to fb_login_check.png")
        
        try:
            # Look for the post box trigger
            # It usually has text like "What's on your mind, Rico?"
            print("Looking for post box trigger...")
            # Try multiple selectors because FB layout changes often
            post_trigger = None
            selectors = [
                "text=What's on your mind", 
                "text=Apa yang Anda pikirkan", 
                "[role='button']:has-text('What\\'s on your mind')",
                "div[aria-label*='What\\'s on your mind']",
                "div[aria-label*='Apa yang Anda pikirkan']"
            ]
            
            for s in selectors:
                try:
                    el = page.locator(s).first
                    if el.is_visible():
                        post_trigger = el
                        break
                except:
                    continue
            
            if post_trigger:
                print("Clicking post box...")
                post_trigger.click()
                time.sleep(3)
                
                # The actual input area appears after clicking the trigger
                print(f"Typing message: {message}")
                # FB uses a contenteditable div for the post body
                page.keyboard.type(message)
                time.sleep(2)
                
                # Find and click the Post button
                print("Clicking Post button...")
                # The button is usually [aria-label='Post'] or has text 'Post'
                post_button = page.locator("[role='button'][aria-label='Post'], [role='button']:has-text('Post'), [role='button']:has-text('Kirim')").first
                if post_button.is_enabled():
                    post_button.click()
                    print("Post button clicked. Waiting for confirmation...")
                    time.sleep(10) # Wait for post to finish
                    print("Process finished.")
                    page.screenshot(path="fb_after_post.png")
                    return True
                else:
                    print("Post button found but not enabled.")
                    page.screenshot(path="fb_post_error.png")
                    return False
            else:
                print("Could not find post box trigger. Check fb_login_check.png")
                return False
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="fb_exception.png")
            return False
        finally:
            browser.close()

if __name__ == "__main__":
    fb_post_playwright("Halo Bang Rico! Ini test post pertama Jeje dari VPS. Mantap! 🔥 [Sent via Playwright]")
