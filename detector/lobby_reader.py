from detector.pcsx2_scan import get_pcsx2_pid, read_memory, get_ps2_base_address
from tracker.constants import CHARACTER_MAP, OFFSETS


def read_lobby_and_characters(file_id):
    pid = get_pcsx2_pid()
    if not pid:
        return None

    offsets = OFFSETS.get(file_id)
    if not offsets:
        return None

    # Check lobby flag
    flag_addr = offsets["lobby_flag"]
    base = 0x20000000  # PS2 memory base
    real_addr = flag_addr - base + get_ps2_base_address(pid)
    flag = read_memory(pid, real_addr, 1)

    if not flag or flag[0] == 0x00:
        print("[DEBUG] Lobby not ready. Waiting…")
        return None

    # Read all player structs
    characters = []
    for addr in offsets["player_structs"]:
        char = read_memory(pid, addr + offsets["char_id_offset"], 1)
        name = "Unknown (?)"
        if char:
            char_id = char[0]
            name = CHARACTER_MAP.get(char_id, f"Unknown ({char_id})")
        characters.append(name)

    return characters



