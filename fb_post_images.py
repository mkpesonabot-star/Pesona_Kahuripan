from playwright.sync_api import sync_playwright
import json
import time
import os

def fb_post_with_images(message, image_paths):
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
            # Clicking Photo/video usually opens the composer with the upload field ready
            photo_trigger = page.locator("div[aria-label='Photo/video'], div[aria-label='Foto/video'], div:has-text('Photo/video')").first
            
            if photo_trigger.is_visible():
                photo_trigger.click()
                time.sleep(5)
                
                print(f"Uploading {len(image_paths)} images...")
                # Find the hidden file input
                file_input = page.locator("input[type='file'][accept*='image']").first
                file_input.set_input_files(image_paths)
                time.sleep(10) # Wait for previews to load

                print("Typing description...")
                # The text box is usually a div with contenteditable="true"
                # Playwright's keyboard.type works on focused elements
                page.keyboard.type(message)
                time.sleep(3)
                
                print("Clicking Post button...")
                # Button might take time to become enabled while images upload
                post_button = page.locator("[role='button'][aria-label='Post'], [role='button']:has-text('Post'), [role='button']:has-text('Kirim')").first
                post_button.wait_for(state="visible", timeout=60000)
                
                if post_button.is_enabled():
                    post_button.click()
                    print("Sent! Waiting for upload/process...")
                    time.sleep(20) # Significant wait for multiple images
                    page.screenshot(path="fb_listing_images_result.png")
                    return True
                else:
                    print("Post button disabled.")
                    page.screenshot(path="fb_images_fail.png")
            else:
                print("Could not find photo trigger.")
                page.screenshot(path="fb_no_photo_trigger.png")
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="fb_images_error.png")
        finally:
            browser.close()
    return False

if __name__ == "__main__":
    msg = """SIAP HUNI GAK PAKAI RIBET! RUMAH SUBSIDI DOUBLE DINDING DI CILEUNGSI 🏠✨

Bagi Bapak/Ibu yang sedang cari rumah subsidi tapi spesifikasinya semi-komersil, Pesona Kahuripan 12 bisa jadi pilihan terbaik. Lokasinya sangat strategis di pinggir Jalan Raya Provinsi Cileungsi - Jonggol.

Peningkatan Spesifikasi dari PK 12:
✅ Sudah ada dapur & tembok belakang (tidak perlu keluar biaya renovasi lagi!)
✅ Ceiling/Plafon lebih tinggi (ruangan jadi lebih sejuk dan kelihatan luas)
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

Hubungi sekarang untuk konsultasi data & share lokasi survei:
📞 Abang Rico - 08211979791"""

    images = [
        "/root/.openclaw/media/inbound/file_14---def020b2-c726-4d56-99e4-b7b02e113a10.jpg",
        "/root/.openclaw/media/inbound/file_15---38e8b133-099f-4626-80bb-1ba703f3d50b.jpg",
        "/root/.openclaw/media/inbound/file_16---6696cce4-1748-4741-b82c-035143d041e5.jpg",
        "/root/.openclaw/media/inbound/file_17---ca1a64a1-f948-4361-ba3b-d45541e36c88.jpg",
        "/root/.openclaw/media/inbound/file_18---ce60adad-9c76-43ff-8c43-ed7a11884a62.jpg",
        "/root/.openclaw/media/inbound/file_19---7d96f790-d326-4466-83f5-285d1fe48720.jpg",
        "/root/.openclaw/media/inbound/file_20---661599be-945c-4173-aec6-a26f01fe04ea.jpg"
    ]
    fb_post_with_images(msg, images)
