#!/usr/bin/env python3

import sys
import re
import requests


if len(sys.argv) != 2:
    print("[!] Usage: " + sys.argv[0] + " [File|URL]")
    exit(0)


def md5(data):
    if type(data) is str:
        data = bytes(data, encoding="utf-8")
    return __import__("hashlib").md5(data).hexdigest()


if sys.argv[1].startswith("http"):
    text = requests.get(sys.argv[1]).text
else:
    with open(sys.argv[1]) as file:
        text = file.read()

# PHP Version
php_version = re.search('<tr><td class="e">PHP Version </td><td class="v">(.*) </td></tr>', text)
if php_version == None:
    print("[!] No PHP version found, is this a phpinfo page/file?")
    exit(0)

php_version = php_version.group(1)

# Zend Extension Build ID
zend_extension_id = re.search('<tr><td class="e">Zend Extension Build </td><td class="v">(.*) </td></tr>', text)
if zend_extension_id == None:
    print("[!] No Zend Extension Build found")
    exit(0)

zend_extension_id = zend_extension_id.group(1)

# Zend Bin ID suffix
bin_id_suffix_arch = "4888(size_t)8"
bin_id_suffix_hooks = "\x02"

# Zend Bin ID
zend_bin_id = "BIN_" + bin_id_suffix_arch + bin_id_suffix_hooks

# Logging
print("[-] PHP version: " + repr(php_version))
print("[-] Zend Extension ID: " + repr(zend_extension_id))
print("[-] Zend Bin ID: " + repr(zend_bin_id))

# Get zend_system_id
digest = md5(php_version + zend_extension_id + zend_bin_id)
print("---------------------")
print("[+] System ID : " + digest)
