from playwright.sync_api import sync_playwright
import json
import time
import os

def fb_post_option_c(message, image_paths):
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
        
        print("Navigating to Facebook...")
        page.goto('https://www.facebook.com/', wait_until="domcontentloaded", timeout=60000)
        time.sleep(10)
        
        try:
            print("Looking for Photo/video button...")
            photo_trigger = page.locator("div[aria-label='Photo/video'], div[aria-label='Foto/video'], div:has-text('Photo/video')").first
            
            if photo_trigger.is_visible():
                photo_trigger.click()
                time.sleep(5)
                
                print(f"Uploading {len(image_paths)} images...")
                file_input = page.locator("input[type='file'][accept*='image']").first
                file_input.set_input_files(image_paths)
                time.sleep(12) 

                print("Typing Option C description...")
                page.keyboard.type(message)
                time.sleep(3)
                
                print("Clicking Post button...")
                post_button = page.locator("[role='button'][aria-label='Post'], [role='button']:has-text('Post'), [role='button']:has-text('Kirim')").first
                post_button.wait_for(state="visible", timeout=60000)
                
                if post_button.is_enabled():
                    post_button.click()
                    print("Sent! Waiting for upload/process...")
                    time.sleep(20) 
                    page.screenshot(path="fb_option_c_result.png")
                    return True
                else:
                    print("Post button disabled.")
            else:
                print("Could not find photo trigger.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
    return False

if __name__ == "__main__":
    msg = """BONUS INTERNET 6 BULAN! 🎁 

Miliki rumah subsidi idaman di Pesona Kahuripan 12 Cileungsi. Spesifikasi gila-gilaan: 
✅ Double Dinding 
✅ Sudah ada Dapur & Tembok Belakang (Gak perlu renovasi!)
✅ Plafon Tinggi (Sejuk & Luas)

💰 Biaya ALL-IN cuma 7 Juta sampai terima kunci!
Booking Fee cuma 500rb. Cicilan flat mulai 1,1 Juta/bulan.

Slot terbatas, siapa cepat dia dapat! 🏃💨

Hubungi sekarang untuk konsultasi & share lokasi survei:
📞 Abang Rico - 08211979791 (WA/Telp)"""

    images = [
        "/root/.openclaw/media/inbound/file_14---def020b2-c726-4d56-99e4-b7b02e113a10.jpg",
        "/root/.openclaw/media/inbound/file_15---38e8b133-099f-4626-80bb-1ba703f3d50b.jpg",
        "/root/.openclaw/media/inbound/file_16---6696cce4-1748-4741-b82c-035143d041e5.jpg",
        "/root/.openclaw/media/inbound/file_17---ca1a64a1-f948-4361-ba3b-d45541e36c88.jpg",
        "/root/.openclaw/media/inbound/file_18---ce60adad-9c76-43ff-8c43-ed7a11884a62.jpg",
        "/root/.openclaw/media/inbound/file_19---7d96f790-d326-4466-83f5-285d1fe48720.jpg",
        "/root/.openclaw/media/inbound/file_20---661599be-945c-4173-aec6-a26f01fe04ea.jpg"
    ]
    fb_post_option_c(msg, images)
