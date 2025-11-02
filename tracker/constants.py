CHARACTER_MAP = {
    0x00: "Kevin",
    0x01: "Mark",
    0x02: "Jim",
    0x03: "George",
    0x04: "Cindy",
    0x05: "Alyssa",
    0x06: "Yoko",
    0x07: "David"
}

OFFSETS = {
    "SLPM-65428": {
        "signature": {
            "address": 0x2036D5F0,
            "expected": b'\x00' * 16
        },
        "lobby_flag": 0x2036D5F0,  # same offset used in Windows tracker
        "player_structs": [
            0x7f76f6e16640,
            0x7f76f6e16bc0,
            0x7f76f6e17140,
            0x7f76f6e176c0
        ],
        "char_id_offset": 0x00
    }
}
