import imap_tools
from pathlib import Path
import configparser
import os


secret_key = 'dsafdsafasfdddddddddsaewrwerweareawrwa645264654654234324'


def crypto_xor(message: str, secret: str) -> str:
    new_chars = list()
    i = 0
    for num_chr in (ord(c) for c in message):
        num_chr ^= ord(secret[i])
        new_chars.append(num_chr)
        i += 1
        if i >= len(secret):
            i = 0
    return ''.join(chr(c) for c in new_chars)


def decrypt_xor(message_hex: str, secret: str) -> str:
    decrypt_val = bytes.fromhex(message_hex).decode('utf-8')
    return crypto_xor(decrypt_val, secret)


def read_config():
    config = configparser.ConfigParser()
    if os.path.exists('config.ini'):
        config.read('config.ini')
        val_server = config['DEFAULT']['server']
        val_login = config['DEFAULT']['login']
        val_password = decrypt_xor(config['DEFAULT']['password'],secret_key)
        val_path_for_files = config['DEFAULT']['path_for_files']
        return {'server': val_server, 'login': val_login, 'password': val_password, 'path_for_files': val_path_for_files}


try:
    param = read_config()
    server = param.get('server')
    login = param.get('login')
    password = param.get('password')
    path_for_files = param.get('path_for_files')
    with imap_tools.MailBox(server).login(login, password, 'INBOX') as mailbox:
        for msg in mailbox.fetch(bulk=True):
            for att in msg.attachments:
                file_name = "".join(c for c in att.filename if c.isalnum() or c == '.')
                extension = Path(file_name).suffix.lower()
                if extension == ".xlsx" or extension == '.xls':
                    with open(path_for_files+format(file_name), 'wb') as f:
                        f.write(att.payload)
            mailbox.delete(msg.uid)
except Exception as e:
    message = str(e)
    print(message)