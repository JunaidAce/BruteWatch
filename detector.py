import time
from collections import defaultdict
from config import MAX_ATTEMPTS, TIME_WINDOW, BLOCK_TIME

failed_attempts = defaultdict(list)
blocked_ips = {}

def is_ip_blocked(ip):
    if ip in blocked_ips:
        if time.time() < blocked_ips[ip]:
            return True
        else:
            del blocked_ips[ip]
    return False

def record_failed_attempt(ip):
    now = time.time()
    failed_attempts[ip].append(now)

    failed_attempts[ip] = [
        t for t in failed_attempts[ip]
        if now - t <= TIME_WINDOW
    ]

    if len(failed_attempts[ip]) >= MAX_ATTEMPTS:
        blocked_ips[ip] = now + BLOCK_TIME

def validate_login(ip, username, password, users):
    if is_ip_blocked(ip):
        return "blocked"

    if username in users and users[username] == password:
        failed_attempts[ip].clear()
        return "success"
    else:
        record_failed_attempt(ip)
        return "failed"
