from playwright.sync_api import sync_playwright
import json
import time
import os

def fb_post_listing(message, image_path=None):
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
            print("Looking for post box...")
            # Common selectors for the post trigger
            selectors = [
                "text=What's on your mind", 
                "text=Apa yang Anda pikirkan", 
                "div[role='button']:has-text('What\\'s on your mind')",
                "div[aria-label*='What\\'s on your mind']",
                "div[aria-label*='Apa yang Anda pikirkan']"
            ]
            
            post_trigger = None
            for s in selectors:
                try:
                    el = page.locator(s).first
                    if el.is_visible():
                        post_trigger = el
                        break
                except: continue
            
            if not post_trigger:
                print("Trigger not found. Checking if already in composer...")
                # Sometimes clicking a 'Photo/video' button is better
                photo_button = page.locator("div[aria-label='Photo/video'], div[aria-label='Foto/video']").first
                if photo_button.is_visible():
                    post_trigger = photo_button

            if post_trigger:
                post_trigger.click()
                time.sleep(5)
                
                # If we have an image, upload it
                if image_path and os.path.exists(image_path):
                    print(f"Uploading image: {image_path}")
                    # FB uses hidden file inputs
                    file_input = page.locator("input[type='file'][accept*='image']").first
                    file_input.set_input_files(image_path)
                    time.sleep(5)

                print("Typing listing details...")
                # Type the message into the active element or the known composer div
                page.keyboard.type(message)
                time.sleep(3)
                
                print("Clicking Post button...")
                # Wait for the button to be clickable (upload might take time)
                post_button = page.locator("[role='button'][aria-label='Post'], [role='button']:has-text('Post'), [role='button']:has-text('Kirim')").first
                post_button.wait_for(state="visible", timeout=30000)
                
                if post_button.is_enabled():
                    post_button.click()
                    print("Sent! Waiting for upload/process...")
                    time.sleep(15)
                    page.screenshot(path="fb_listing_result.png")
                    return True
                else:
                    print("Post button disabled.")
                    page.screenshot(path="fb_listing_fail.png")
            else:
                print("Could not start post.")
                page.screenshot(path="fb_no_trigger.png")
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="fb_listing_error.png")
        finally:
            browser.close()
    return False

if __name__ == "__main__":
    msg = """SIAP HUNI GAK PAKAI RIBET! RUMAH SUBSIDI DOUBLE DINDING DI CILEUNGSI 🏠✨

Bagi Bapak/Ibu yang sedang cari rumah subsidi tapi spesifikasinya semi-komersil, Pesona Kahuripan 12 bisa jadi pilihan terbaik. Lokasinya sangat strategis di pinggir Jalan Raya Provinsi Cileungsi - Jonggol.

Peningkatan Spesifikasi dari PK 12:
✅ Sudah ada dapur & tembok belakang
✅ Ceiling/Plafon lebih tinggi
✅ Double Dinding antar rumah

Rincian Biaya (Type 30/60):
• Booking Fee: Rp 500.000
• Total Bayar: Rp 6.500.000
• Biaya ALL-IN Sampai Terima Kunci: Rp 7.000.000

Estimasi Angsuran KPR BTN (Flat/Tetap):
• 10 Tahun: Rp 1.933.400 / bulan
• 15 Tahun: Rp 1.438.400 / bulan
• 20 Tahun: Rp 1.198.000 / bulan

🎁 PROMO KHUSUS: Free Internet selama 6 Bulan!

Hubungi sekarang:
📞 Abang Rico - 08211979791"""
    fb_post_listing(msg)
