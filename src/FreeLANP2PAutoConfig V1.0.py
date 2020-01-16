import shutil, os, subprocess, glob

def GenerateKeyCert():
    subprocess.call(OSSLExePath + " req -new -newkey rsa:4096 -days 358000 -nodes -x509 -subj \"/C=US/ST=Denial/L=Springfield/O=Dis/CN=" + PCName + "\" -keyout " + PCName + ".key  -out " + PCName + ".crt")

def CheckOpenSSL():
    if os.path.isfile(r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe") == False:
        input('You do not have OpenSSL installed or it is not in "C:\Program Files\OpenSSL-Win64\bin\openssl.exe"')
        exit()

def CheckKeyCert():
    if os.path.isfile(glob.glob("*.crt")[0]) and os.path.isfile(glob.glob("*.key")[0]) == False:
        input("Something went wrong with certificate and key generation.")
        exit()

def MoveKeyCert():
    shutil.move(cert, r"C:\Program Files\FreeLAN\config")
    shutil.move(key, r"C:\Program Files\FreeLAN\config")

def DeleteOldConfig():
    if os.path.isfile(r"C:\Program Files\FreeLAN\config\freelan.cfg") == True:
        os.remove(r"C:\Program Files\FreeLAN\config\freelan.cfg")

def WriteNewConfig():
    file = open("freelan.cfg", "w")

    file.write('dynamic_contact_file="' + cert + '"\n')
    file.write('ipv4_address_prefix_length=' + ipv4pl + '\n')
    file.write('ipv4_dhcp=false' + '\n')
    file.write('ipv6_address_prefix_length=' + ipv6pl + '\n')
    file.write('relay_mode_enabled=no' + '\n')
    file.write('signature_certificate_file="' + cert + '"' + '\n')
    file.write('signature_private_key_file="' + key + '"' + '\n')
    file.write('authority_certificate_file="' + cert + '"' + '\n')

    file.close

CheckOpenSSL()

OSSLExePath = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"
PCName = os.environ["COMPUTERNAME"]

GenerateKeyCert()

CheckKeyCert()

cert = glob.glob("*.crt")[0]
key = glob.glob("*.key")[0]

MoveKeyCert()

DeleteOldConfig()

ipv4pl = input("Enter: ipv4_address_prefix_length=")
ipv6pl = input("Enter: ipv6_address_prefix_length=")

os.chdir(r"C:\Program Files\FreeLAN\config")

WriteNewConfig()

print("Done.")
