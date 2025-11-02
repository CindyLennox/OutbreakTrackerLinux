from detector.pcsx2_scan import get_pcsx2_pid, read_memory, get_ps2_base_address
from tracker.constants import OFFSETS

def detect_game_version():
    pid = get_pcsx2_pid()
    base = get_ps2_base_address(pid)
    if not pid or not base:
        print("[DEBUG] PCSX2 not running or base address not found.")
        return None

    for file_id, data in OFFSETS.items():
        sig = data.get("signature")
        if not sig:
            continue

        real_addr = base + (sig["address"] - 0x20000000)
        result = read_memory(pid, real_addr, len(sig["expected"]))
        print(f"[DEBUG] Raw signature at {hex(sig['address'])}: {result.hex() if result else 'unreadable'}")

        if result and any(b != 0x00 for b in result) and result.startswith(sig["expected"]):
            print(f"[DEBUG] Signature matched → {file_id}")
            return file_id


    print("[DEBUG] No signature match found.")
    return None
