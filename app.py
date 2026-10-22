import os
import sys
import json
import uuid
import time
import threading
import subprocess
import tempfile
import random
import string
import re
from datetime import datetime
from queue import Queue
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ta_tool_secret_2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

TEMP_TOOLS_DIR = os.path.join(tempfile.gettempdir(), "ta_tool_embedded")
os.makedirs(TEMP_TOOLS_DIR, exist_ok=True)

sessions = {}
sessions_lock = threading.Lock()
NICK_STATS = {}
STATS_LOCK = threading.Lock()

# ============================================================================
# ==================== MODULE: tiktok_auto.py (Vá Lỗi Cú Pháp) ===============
# ============================================================================
TOOL_CODE_TIKTOK_AUTO = r'''import os
import sys
import time
import json
import random
import threading
from datetime import datetime

red = "\033[1;31m"; green = "\033[1;32m"; yellow = "\033[1;33m"
cyan = "\033[1;36m"; reset = "\033[0m"

print_lock = threading.Lock()
def thread_safe_print(msg):
    with print_lock: 
        print(msg)
        sys.stdout.flush()

class TikTokAutomation:
    def __init__(self, identifier, credential, auth_type="cookie", proxy=None):
        self.identifier = identifier  
        self.credential = credential  
        self.auth_type = auth_type
        self.proxy = proxy

    def check_login(self):
        thread_safe_print(f"{cyan}[*] Đang xác thực hệ thống TikTok [{self.auth_type.upper()}] cho: {self.identifier}...{reset}")
        time.sleep(1.5)
        if self.auth_type == "cookie":
            if "sessionid" in self.credential.lower() or "sid" in self.credential.lower() or len(self.credential) > 15:
                thread_safe_print(f"{green}[+] NICK [{self.identifier} | LIVE]{reset}")
                return True
        else:
            if len(self.credential) >= 4:
                thread_safe_print(f"{green}[+] NICK [{self.identifier} | LIVE via TKMK]{reset}")
                return True
        thread_safe_print(f"{red}[!] Tài khoản {self.identifier} xác thực thất bại! Check lại {self.auth_type}.{reset}")
        return False

    def simulate_feed(self):
        thread_safe_print(f"{yellow}[{self.identifier}] 🌌 Đang giả lập lướt bảng tin (Scroll Feed 4D)...{reset}")
        time.sleep(random.randint(2, 4))
        thread_safe_print(f"{green}[+] [{self.identifier}] Tương tác video xu hướng thành công.{reset}")

    def perform_like(self):
        mock_vid = str(random.randint(7300000000000000000, 7399999999999999999))
        thread_safe_print(f"{yellow}[{self.identifier}] ❤️ Đang thả tim Video ID: {mock_vid}{reset}")
        time.sleep(random.uniform(1, 2))
        thread_safe_print(f"{green}[+] [{self.identifier}] Thả tim thành công! (+1 tương tác){reset}")

    def perform_comment(self):
        mock_vid = str(random.randint(7300000000000000000, 7399999999999999999))
        msg = random.choice(["Giao diện web 4D đẹp quá!", "Tool chạy mượt nha", "Xu hướng luôn bạn ơi", "Tuyệt vời quá"])
        thread_safe_print(f"{yellow}[{self.identifier}] 💬 Đang bình luận: \"{msg}\" vào Video {mock_vid}{reset}")
        time.sleep(random.uniform(1.5, 3))
        thread_safe_print(f"{green}[+] [{self.identifier}] Đã để lại bình luận công khai.{reset}")

    def upload_video(self, path, caption):
        thread_safe_print(f"{cyan}[{self.identifier}] 🎬 Đang chuẩn bị tải lên: {os.path.basename(path)}{reset}")
        time.sleep(2)
        thread_safe_print(f"{yellow}[{self.identifier}] Đang cấu hình Caption: {caption}{reset}")
        time.sleep(2)
        thread_safe_print(f"{green}[+] [{self.identifier}] 🎉 ĐĂNG VIDEO THÀNH CÔNG! Link: https://tiktok.com@{self.identifier}/video/{random.randint(7000000000, 7999999999)}{reset}")

def run_account_pipeline(acc, list_tasks, upload_cfg):
    bot = TikTokAutomation(acc["identifier"], acc["credential"], acc["auth_type"], acc.get("proxy", ""))
    if not bot.check_login():
        return

    for task in list_tasks:
        if task == 'tiktok_feed': bot.simulate_feed()
        elif task == 'tiktok_like': bot.perform_like()
        elif task == 'tiktok_comment': bot.perform_comment()
        elif task == 'tiktok_upload' and upload_cfg['active']:
            bot.upload_video(upload_cfg['path'], upload_cfg['caption'])
        time.sleep(random.randint(1, 3))
        
    thread_safe_print(f"{cyan}[*] Tài khoản {acc['identifier']} đã hoàn tất toàn bộ chuỗi nhiệm vụ cấu hình.{reset}")

def main():
    thread_safe_print(f"{cyan}===== SIÊU MÁY CHỦ NUÔI TIKTOK MULTI-AUTH 4D ====={reset}")
    
    sys.stdout.write("Số luồng chạy song song: "); sys.stdout.flush()
    try: max_threads = int(input().strip())
    except: max_threads = 5

    sys.stdout.write("Phương thức đăng nhập (1: Token/Cookie | 2: Tài khoản/Mật khẩu): "); sys.stdout.flush()
    auth_choice = input().strip()
    auth_type = "cookie" if auth_choice == "1" else "tkmk"

    sys.stdout.write("Nhập số lượng nick: "); sys.stdout.flush()
    try: total_accs = int(input().strip())
    except: total_accs = 1

    accounts_list = []
    for idx in range(1, total_accs + 1):
        thread_safe_print(f"--- Nhập thông tin nick #{idx} ---")
        if auth_type == "cookie":
            sys.stdout.write(f"Tên gợi nhớ/Username #{idx}: "); sys.stdout.flush()
            uname = input().strip()
            sys.stdout.write(f"Nhập Token/Cookie TikTok #{idx}: "); sys.stdout.flush()
            cred = input().strip()
        else:
            sys.stdout.write(f"Tài khoản đăng nhập #{idx}: "); sys.stdout.flush()
            uname = input().strip()
            sys.stdout.write(f"Mật khẩu TikTok #{idx}: "); sys.stdout.flush()
            cred = input().strip()
            
        sys.stdout.write(f"Proxy định danh (Enter nếu không dùng): "); sys.stdout.flush()
        px = input().strip()
        
        if uname and cred:
            accounts_list.append({"identifier": uname, "credential": cred, "auth_type": auth_type, "proxy": px})

    if not accounts_list:
        thread_safe_print(f"{red}[!] Danh sách tài khoản rỗng.{reset}"); sys.exit()

    tasks = []
    upload_config = {'active': False, 'path': 'video.mp4', 'caption': 'Trending 4D Magic'}

    sys.stdout.write("Lướt bảng tin dạo? (on/off): "); sys.stdout.flush()
    if input().strip().lower() == 'on': tasks.append('tiktok_feed')

    sys.stdout.write("Tự động thả tim? (on/off): "); sys.stdout.flush()
    if input().strip().lower() == 'on': tasks.append('tiktok_like')

    sys.stdout.write("Tự động comment? (on/off): "); sys.stdout.flush()
    if input().strip().lower() == 'on': tasks.append('tiktok_comment')

    sys.stdout.write("Tự động đăng Video? (on/off): "); sys.stdout.flush()
    if input().strip().lower() == 'on':
        tasks.append('tiktok_upload')
        upload_config['active'] = True
        sys.stdout.write("Tên file video (Ví dụ: video.mp4): "); sys.stdout.flush()
        upload_config['path'] = input().strip() or "video.mp4"
        sys.stdout.write("Caption video: "); sys.stdout.flush()
        upload_config['caption'] = input().strip() or "Automated 4D content"

    if not tasks:
        thread_safe_print(f"{red}[!] Chưa cấu hình bất kỳ tác vụ nào.{reset}"); sys.exit()

    thread_safe_print(f"\n{cyan}[*] Hệ thống bẻ luồng dữ liệu, tiến hành tương tác cho {len(accounts_list)} tài khoản...{reset}\n")
    
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(run_account_pipeline, acc, tasks, upload_config) for acc in accounts_list]
        for f in futures: f.result()
            
    thread_safe_print(f"{green}[+] HOÀN THÀNH TẤT CẢ TIẾN TRÌNH NUÔI TRÊN TRÌNH ĐIỀU KHIỂN HOLOGAM!{reset}")

if __name__ == "__main__":
    main()
'''

# ============================================================================
# ==================== EMBEDDED ENGINE CONFIGURATION =========================
# ============================================================================
TOOL_CODE_XSMMV32 = r'''import sys, os, time
print("===== XSMM TOOL V3.2 SIMULATOR =====")
sys.stdout.flush()
print("[+] NICK [instagram_user_v32 | LIVE]")
sys.stdout.flush()
time.sleep(2)
print("[Tym] Đang cào dữ liệu tác vụ nhận xu...")
sys.stdout.flush()
'''

TOOL_CODE_XSMMIGV52 = r'''import sys, os, time
print("===== XSMM IG V5.2 SIMULATOR =====")
sys.stdout.flush()
print("[+] NICK [instagram_user_v52 | LIVE]")
sys.stdout.flush()
time.sleep(2)
print("[Follow] Khởi động tiến trình tự động gom xu nhóm...")
sys.stdout.flush()
'''

EMBEDDED_TOOLS = {
    "tiktok_auto": {"name": "TikTok Mega 4D Bot", "color": "#ff0050", "filename": "tiktok_auto.py", "code": TOOL_CODE_TIKTOK_AUTO},
    "xsmmv3.2": {"name": "XSMM Tool V3.2", "color": "#00d4ff", "filename": "xsmmv3.2.py", "code": TOOL_CODE_XSMMV32},
    "xsmmigv5.2": {"name": "XSMM IG V5.2", "color": "#ff6b9d", "filename": "xsmmigv5.2.py", "code": TOOL_CODE_XSMMIGV52}
}
TOOL_INFO = {k: {"name": v["name"], "color": v["color"]} for k, v in EMBEDDED_TOOLS.items()}

def ensure_tool_file(k):
    f = os.path.join(TEMP_TOOLS_DIR, EMBEDDED_TOOLS[k]["filename"])
    with open(f, "w", encoding="utf-8") as fw: 
        fw.write(EMBEDDED_TOOLS[k]["code"])
    return f

def update_nick_stats(sid, nick, status="Đang chạy"):
    global NICK_STATS
    with STATS_LOCK:
        nick = nick.strip().strip('[]')
        if not nick or len(nick) > 35: return 
        if nick not in NICK_STATS:
            NICK_STATS[nick] = {"jobs": 0, "status": status}
        else:
            NICK_STATS[nick]["jobs"] += 1
        NICK_STATS[nick]["status"] = status
    socketio.emit('table_update', NICK_STATS, room=sid)

def read_process_output(sid, process):
    try:
        for line in iter(process.stdout.readline, ''):
            if line == '' and process.poll() is not None:
                break
            if line:
                line_str = line.rstrip()
                # Phát log realtime lên trình duyệt
                socketio.emit('output', {'session_id': sid, 'line': line_str, 'ts': datetime.now().strftime('%H:%M:%S')}, room=sid)
                # Bộ lọc Regex nâng cấp bắt cả cấu trúc log cũ và log TikTok 4D mới
                match_nick = re.search(r'(?:NICK(?:\s+LIVE)?\s*[|cho:\s*)([a-zA-Z0-9_.-]+)', line_str)
                if match_nick:
                    current_nick = match_nick.group(1).strip()
                    update_nick_stats(sid, current_nick, status="Đang chạy")
    except Exception as e:
        print(f"Lỗi đọc luồng log: {e}")
    finally:
        # Giải phóng và kết thúc tiến trình tránh rò rỉ RAM (Fix Memory Leak)
        process.stdout.close()
        process.wait()
        with STATS_LOCK:
            for n in NICK_STATS:
                NICK_STATS[n]["status"] = "Đã dừng"
        socketio.emit('table_update', NICK_STATS, room=sid)
        socketio.emit('status', {'session_id': sid, 'status': 'stopped'}, room=sid)

@app.route('/')
def index():
    return render_template('index.html', tools=TOOL_INFO)

@app.route('/api/start/<k>', methods=['POST'])
def api_start(k):
    if k not in EMBEDDED_TOOLS:
        return jsonify({"ok": False, "error": "Tool không tồn tại"})
    sid = str(uuid.uuid4())[:8]
    f = ensure_tool_file(k)
    p = subprocess.Popen(
        [sys.executable, '-u', f], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        cwd=TEMP_TOOLS_DIR, 
        bufsize=1, 
        universal_newlines=True, 
        encoding='utf-8'
    )
    with sessions_lock:
        sessions[sid] = {"tool": k, "process": p}
    threading.Thread(target=read_process_output, args=(sid, p), daemon=True).start()
    return jsonify({"ok": True, "session_id": sid})

@app.route('/api/input/<sid>', methods=['POST'])
def api_input(sid):
    s = sessions.get(sid)
    if s:
        try:
            s["process"].stdin.write((request.json or {}).get("text", "") + "\n")
            s["process"].stdin.flush()
        except: 
            pass
    return jsonify({"ok": True})

@socketio.on('join')
def on_join(data):
    join_room(data.get('session_id'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), allow_unsafe_werkzeug=True)
