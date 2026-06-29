import os
import time
import re
import urllib.request
import json
import ssl
import random
import sys

# =====================================================================
# --- CẤU HÌNH HỆ THỐNG TOOL CÀO VIDEO TIKTOK NÉT HƠN SNAPTIK 69 LẦN---
# =====================================================================
FILE_DANH_SACH = "kenh.txt"
# =====================================================================

ssl._create_default_https_context = ssl._create_unverified_context

# --- MÃ MÀU TERMINAL ANSI ---
C_YELLOW = "\033[93m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_RESET = "\033[0m"

def doc_danh_sach_kenh(file_path):
    """Đọc danh sách kênh từ file txt, bỏ qua dòng trống hoặc comment"""
    urls = []
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# Ném link TikTok vào đây, mỗi dòng 1 link. Kênh mới đưa lên đầu list.\n")
        print(f"⚠️ Đã tạo file {file_path}. Bro hãy điền link kênh vào đó nhé!")
        return urls
        
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls

def clean_filename(text, username, video_id, ext_type=".mp4"):
    if not text or text.strip() == "": 
        text = f"Video review chia se kien thuc cham soc da skin care cosmee"
    else:
        text = text.replace('#', ' ')
        
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYy'
    s = ''
    for char in text: s += s0[s1.index(char)] if char in s1 else char
            
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    words = s.split()
    s = "-".join(words).lower()
    s = s[:55].strip('-')
    if not s: s = "video-review"
    s = s[0].upper() + s[1:]
    return f"{s}-{video_id}-@{username.lower()}{ext_type}"

def get_channel_name(url):
    match = re.search(r'@([a-zA-Z0-9_\.]+)', url)
    return match.group(1) if match else "unknown"

def get_video_urls(channel_url):
    username = get_channel_name(channel_url)
    print(f"\n🔍 [TOÀN DIỆN] Đang quét TẤT CẢ video từ kênh: @{username}...")
    urls = []
    cursor = "0"  # Vị trí bắt đầu (0 nghĩa là đầu trang)
    has_more = True
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    while has_more:
        try:
            # Gắn thêm tham số cursor để API biết cần lấy block video tiếp theo
            api_user_url = f"https://www.tikwm.com/api/user/posts?unique_id={username}&count=50&cursor={cursor}"
            req = urllib.request.Request(api_user_url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                if data.get('code') == 0 and 'data' in data:
                    res_data = data['data']
                    videos = res_data.get('videos', [])
                    
                    for video in videos:
                        video_id = video.get('video_id')
                        if video_id:
                            urls.append(f"https://www.tiktok.com/@{username}/video/{video_id}")
                    
                    print(f"   ↳ Đã thu thập được {len(urls)} video...")
                    
                    # Kiểm tra xem còn video để tải tiếp không
                    has_more = res_data.get('hasMore', False)
                    if has_more:
                        cursor = res_data.get('cursor', '0')
                        time.sleep(random.uniform(1.5, 3.0))  # Nghỉ ngắn giữa các lần lật trang để bảo vệ luồng mạng
                    else:
                        has_more = False
                else:
                    print("⚠️ API không trả về thêm dữ liệu hoặc hết danh sách.")
                    has_more = False
                    
        except Exception as e: 
            print(f"⚠️ Gián đoạn khi cào danh sách trang: {e}")
            has_more = False  # Gặp lỗi thì dừng vòng lặp tránh treo tool

    print(f"✅ TỔNG KẾT: Đã quét sạch hoàn toàn {len(urls)} link video của kênh @{username}!")
    return urls

def download_tiktok_api(video_url, folder_save, username, current_idx, total_count):
    try:
        api_url = f"https://www.tikwm.com/api/?url={video_url}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if data.get('code') == 0:
            video_data = data['data']
            video_id = video_data['id']
            title = video_data.get('title', '')
            
            video_filename = clean_filename(title, username, video_id, ext_type=".mp4")
            json_filename = clean_filename(title, username, video_id, ext_type=".json")
            final_video_path = os.path.join(folder_save, video_filename)
            final_json_path = os.path.join(folder_save, json_filename)
            
            seo_metadata = {
                "video_id": video_id,
                "author_channel": username,
                "tiktok_url": video_url,
                "mo_ta_goc_video": title,
                "hashtags": [tag.strip() for tag in re.findall(r'#\w+', title)] if title else [],
                "thong_ke_tuong_tac": {
                    "luot_xem_views": video_data.get('play_count', 0),
                    "luot_thich_likes": video_data.get('digg_count', 0),
                    "luot_binh_luan_comments": video_data.get('comment_count', 0),
                    "luot_chia_se_shares": video_data.get('share_count', 0)
                },
                "am_nhac_background": {
                    "music_id": video_data.get('music_info', {}).get('id', ''),
                    "music_title": video_data.get('music_info', {}).get('title', ''),
                    "music_author": video_data.get('music_info', {}).get('author', '')
                },
                "thoi_gian_dang_timestamp": video_data.get('create_time', 0)
            }
            
            with open(final_json_path, 'w', encoding='utf-8') as f:
                json.dump(seo_metadata, f, ensure_ascii=False, indent=4)
            
            # --- NẾU ĐÃ CÓ VIDEO CŨ ---
            if os.path.exists(final_video_path):
                print(f"{C_YELLOW}⏭️  [{current_idx}/{total_count}] Đã có sẵn MP4 ➔ Chỉ cập nhật file JSON SEO: {json_filename}{C_RESET}")
                return True
                
            # --- NẾU LÀ VIDEO MỚI TINH ---
            print(f"{C_CYAN}⚡ [{current_idx}/{total_count}] Phát hiện Video MỚI ĐĂNG ➔ Đang xử lý tải về...{C_RESET}")
            download_url = video_data.get('hdplay') or video_data.get('play')
            if not download_url: return True
            if not download_url.startswith('http'): download_url = f"https://www.tikwm.com{download_url}"
                
            video_req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(video_req) as video_resp:
                total_size = int(video_resp.info().get('Content-Length', 0))
                downloaded = 0
                block_size = 1024 * 64
                
                with open(final_video_path, 'wb') as out_file:
                    while True:
                        buffer = video_resp.read(block_size)
                        if not buffer: break
                        downloaded += len(buffer)
                        out_file.write(buffer)
                        
                        percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                        bar_length = 15
                        filled_length = int(round(bar_length * downloaded / float(total_size))) if total_size > 0 else 0
                        loading_bar = '█' * filled_length + '-' * (bar_length - filled_length)
                        
                        short_name = video_filename if len(video_filename) <= 40 else f"{video_filename[:37]}..."
                        sys.stdout.write(f"\r📥 |{loading_bar}| {percent:.1f}% : {short_name}      ")
                        sys.stdout.flush()
            print()
            print(f"{C_GREEN}✨ [COMPLETED] Đã lưu Video mới & JSON SEO: {video_filename}{C_RESET}")
            return False 
        else:
            return True
    except Exception as e:
        return True

def process_channel(url_kenh):
    username = get_channel_name(url_kenh)
    folder_save = f"{username.capitalize()}_Cosmee"
    if not os.path.exists(folder_save): os.makedirs(folder_save)
        
    video_links = get_video_urls(url_kenh)
    if not video_links: return

    total_count = len(video_links)
    print(f"🚀 Tìm thấy {total_count} bài đăng. Tiến hành đồng bộ (Ưu tiên video MỚI NHẤT)...")
    
    for i, link in enumerate(video_links, 1):
        is_old = download_tiktok_api(link, folder_save, username, i, total_count)
        
        # Nghỉ thông minh: Video cũ lướt nhanh 1s, video mới vừa tải xong nghỉ 5-15s phá dấu vết máy móc
        if is_old:
            time.sleep(random.uniform(1.0, 1.5)) 
        else:
            sleep_time = random.randint(5, 15)
            print(f"☕ [Nghỉ ngắn] Giả lập lướt xem tiếp trong {sleep_time}s...")
            time.sleep(sleep_time)

if __name__ == "__main__":
    print("=== HỆ THỐNG FAST-RECOVERY: CHẠY THỦ CÔNG KHI CÓ NHU CẦU ===")
    
    # 1. Đọc danh sách kênh từ file txt
    danh_sach_kenh = doc_danh_sach_kenh(FILE_DANH_SACH)
    
    if not danh_sach_kenh:
        print("❌ Không có kênh nào trong list. Hãy kiểm tra lại file kenh.txt!")
        sys.exit()
        
    print(f"📂 Đã tải thành công {len(danh_sach_kenh)} kênh từ file cấu hình. Bắt đầu quét dữ liệu...")
    
    # 2. Duyệt tuần tự qua từng kênh (Kênh mới ở đầu file chạy trước)
    for url in danh_sach_kenh:
        process_channel(url)
        
        # Nghỉ ngẫu nhiên giữa các kênh để hạ nhiệt luồng mạng
        delay_kenh = random.randint(10, 30)
        print(f"\n☕ Đã quét xong kênh. Nghỉ ngơi {delay_kenh}s trước khi chuyển kênh tiếp theo...")
        time.sleep(delay_kenh)
        
    print("\n🏁 [HOÀN THÀNH LƯỢT QUẾT]")
    print("✨ Toàn bộ video mới đã được tải, file JSON SEO đã đồng bộ hoàn chỉnh.")
    print("👉 Bro có thể tắt Terminal an toàn rồi nhé!")