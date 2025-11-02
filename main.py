import time
import psutil
from detector.outbreak_check import detect_game_version
from detector.lobby_reader import read_lobby_and_characters
from detector.pcsx2_scan import get_pcsx2_pid

def main_loop():
    print("Outbreak Tracker for Linux started.")

    pcsx2_found = False
    pid = None
    file_id = None
    lobby_detected = False

    while True:
        if not pcsx2_found:
            pid = get_pcsx2_pid()
            if pid:
                print(f"[DEBUG] PCSX2 process found: PID {pid}")
                pcsx2_found = True
            else:
                print("[DEBUG] PCSX2 not running. Retrying…")
                time.sleep(2)
                continue

        if pcsx2_found and not psutil.pid_exists(pid):
            print("[DEBUG] PCSX2 closed. Resetting tracker.")
            pcsx2_found = False
            pid = None
            file_id = None
            lobby_detected = False
            time.sleep(2)
            continue

        if not file_id:
            file_id = detect_game_version()
            if file_id:
                print(f"[TRACKER] Game version detected → {file_id}. Sync milestone logged.")
                print("Waiting for online lobby to start…")
            else:
                print("[DEBUG] Outbreak not detected. Retrying…")
                time.sleep(2)
                continue

        if not lobby_detected:
            characters = read_lobby_and_characters(file_id)
            if characters:
                print("Lobby detected. Players and characters:")
                for i, name in enumerate(characters, 1):
                    print(f"Player {i}: {name}")
                lobby_detected = True
            else:
                print("[DEBUG] Lobby not ready. Waiting…")
        else:
            print("[DEBUG] Tracker is idle. Monitoring…")

        time.sleep(2)

if __name__ == "__main__":
    main_loop()
