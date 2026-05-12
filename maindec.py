import os
import time

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

ENCRYPTED_FILE = "encrypted.txt"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════════════╗
  ║                                                  ║
  ║     ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗  ║
  ║    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝  ║
  ║    ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║     ║
  ║    ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║     ║
  ║    ╚██████╗██║  ██║   ██║   ██║        ██║     ║
  ║     ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝     ║
  ║                                                  ║
  ║          {YELLOW}File Encryptor & Decryptor{CYAN}             ║
  ║          {DIM}Secure your messages with XOR{CYAN}            ║
  ╚══════════════════════════════════════════════════╝
{RESET}""")

def divider():
    print(f"{DIM}{CYAN}  ──────────────────────────────────────────────────{RESET}")

def success(msg):
    print(f"\n  {GREEN}✔  {msg}{RESET}")

def error(msg):
    print(f"\n  {RED}✘  {msg}{RESET}")

def info(msg):
    print(f"\n  {YELLOW}ℹ  {msg}{RESET}")

def xor_encrypt(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result

def xor_decrypt(cipher, key):
    return xor_encrypt(cipher, key)

def to_hex(text):
    return text.encode("latin-1").hex()

def from_hex(hex_text):
    return bytes.fromhex(hex_text).decode("latin-1")

def encrypt_message():
    print(f"\n{BOLD}{CYAN}  [ ENCRYPT MESSAGE ]{RESET}")
    divider()
    message = input(f"\n  {WHITE}Enter your message : {RESET}").strip()
    key = input(f"  {WHITE}Enter secret key   : {RESET}").strip()

    if not message or not key:
        error("Message and key cannot be empty.")
        return

    encrypted = xor_encrypt(message, key)
    hex_output = to_hex(encrypted)

    print(f"\n  {GREEN}Encrypted (HEX):{RESET}")
    print(f"\n  {YELLOW}{hex_output}{RESET}")

    save = input(f"\n  {WHITE}Save to file? (y/n) : {RESET}").strip().lower()
    if save == "y":
        with open(ENCRYPTED_FILE, "w") as f:
            f.write(hex_output)
        success(f"Saved to '{ENCRYPTED_FILE}'")
    else:
        info("Not saved.")

def decrypt_message():
    print(f"\n{BOLD}{CYAN}  [ DECRYPT MESSAGE ]{RESET}")
    divider()
    hex_input = input(f"\n  {WHITE}Enter encrypted HEX : {RESET}").strip()
    key = input(f"  {WHITE}Enter secret key    : {RESET}").strip()

    if not hex_input or not key:
        error("Input and key cannot be empty.")
        return

    try:
        cipher = from_hex(hex_input)
        decrypted = xor_decrypt(cipher, key)
        print(f"\n  {GREEN}Decrypted message:{RESET}")
        print(f"\n  {YELLOW}{decrypted}{RESET}")
    except Exception:
        error("Invalid HEX input or wrong key.")

def encrypt_to_file():
    print(f"\n{BOLD}{CYAN}  [ ENCRYPT & SAVE TO FILE ]{RESET}")
    divider()
    message = input(f"\n  {WHITE}Enter your message : {RESET}").strip()
    key = input(f"  {WHITE}Enter secret key   : {RESET}").strip()

    if not message or not key:
        error("Message and key cannot be empty.")
        return

    encrypted = xor_encrypt(message, key)
    hex_output = to_hex(encrypted)

    with open(ENCRYPTED_FILE, "w") as f:
        f.write(hex_output)

    success(f"Message encrypted and saved to '{ENCRYPTED_FILE}'")

def decrypt_from_file():
    print(f"\n{BOLD}{CYAN}  [ DECRYPT FROM FILE ]{RESET}")
    divider()

    if not os.path.exists(ENCRYPTED_FILE):
        error(f"File '{ENCRYPTED_FILE}' not found. Encrypt something first.")
        return

    with open(ENCRYPTED_FILE, "r") as f:
        hex_input = f.read().strip()

    info(f"Loaded encrypted data from '{ENCRYPTED_FILE}'")
    print(f"\n  {DIM}HEX: {hex_input[:60]}{'...' if len(hex_input) > 60 else ''}{RESET}")

    key = input(f"\n  {WHITE}Enter secret key : {RESET}").strip()

    if not key:
        error("Key cannot be empty.")
        return

    try:
        cipher = from_hex(hex_input)
        decrypted = xor_decrypt(cipher, key)
        print(f"\n  {GREEN}Decrypted message:{RESET}")
        print(f"\n  {YELLOW}{decrypted}{RESET}")
    except Exception:
        error("Could not decrypt. Check your key or file content.")

def show_menu():
    print(f"\n{BOLD}{WHITE}  MAIN MENU{RESET}")
    divider()
    print(f"\n  {CYAN}[1]{RESET}  Encrypt a message")
    print(f"  {CYAN}[2]{RESET}  Decrypt a message")
    print(f"  {CYAN}[3]{RESET}  Encrypt & save to file")
    print(f"  {CYAN}[4]{RESET}  Decrypt from file")
    print(f"  {RED}[5]{RESET}  Exit\n")

def main():
    clear()
    banner()

    while True:
        show_menu()
        choice = input(f"  {WHITE}Select option [1-5] : {RESET}").strip()

        if choice == "1":
            encrypt_message()
        elif choice == "2":
            decrypt_message()
        elif choice == "3":
            encrypt_to_file()
        elif choice == "4":
            decrypt_from_file()
        elif choice == "5":
            print(f"\n  {CYAN}Goodbye! Stay secure.{RESET}\n")
            time.sleep(1)
            break
        else:
            error("Invalid choice. Please enter 1 to 5.")

        input(f"\n  {DIM}Press Enter to continue...{RESET}")
        clear()
        banner()

main()