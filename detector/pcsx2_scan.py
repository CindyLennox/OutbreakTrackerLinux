import psutil

def get_pcsx2_pid():
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            name = proc.info.get('name', '') or ''
            exe = proc.info.get('exe', '') or ''
            cmdline = proc.info.get('cmdline') or []
            if "pcsx2" in name.lower() or "pcsx2" in exe.lower() or any("pcsx2" in arg.lower() for arg in cmdline):
                return proc.info['pid']
        except Exception:
            continue
    return None

def read_memory(pid, address, size):
    try:
        with open(f"/proc/{pid}/mem", "rb") as mem:
            mem.seek(address)
            return mem.read(size)
    except Exception:
        return None


def get_ps2_base_address(pid):
    try:
        with open(f"/proc/{pid}/maps", "r") as maps:
            for line in maps:
                parts = line.split()
                if len(parts) >= 2 and 'r' in parts[1]:
                    addr_range = parts[0]
                    start_str, end_str = addr_range.split('-')
                    start = int(start_str, 16)
                    end = int(end_str, 16)
                    if end - start >= 0x1000000 and start >= 0x20000000:
                        return start
    except Exception as e:
        print(f"[DEBUG] Failed to find PS2 base address: {e}")
    return None
