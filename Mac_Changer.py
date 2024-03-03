import subprocess
import winreg
import re
import smtplib
import os
import time
import colorama
from colorama import Fore

os.system("cls")

Logo = (Fore.LIGHTCYAN_EX + r"""
    __=============================================================================================_
    ||                                                                                             ||            
    ||               ___            ___        __         __________                               ||  
    ||               ||\\          //||       //\\       ||=========|      Wrote By:               ||            
    ||               || \\        // ||      //  \\      ||                   Getahun -- Alta      ||        
    ||               ||  \\      //  ||     //____\\     ||                                        ||            
    ||               ||   \\    //   ||    //======\\    ||                                        ||          
    ||               ||    \\  //    ||   //        \\   ||__________                              ||         
    ||               ||     \\//     ||  //          \\  ||==========|                             ||
    ||<------------------------------------------------------------------------------------------->||             
    ||  _________                     __       ___      __  __________     _________    _______    ||        
    || |=========|  ||     ||        //\\      ||\\     ||  ||========|    ||======||  ||     ||   ||        
    || ||           ||     ||       //  \\     || \\    ||  ||             ||          ||_____||   ||              
    || ||           ||=====||      //____\\    ||  \\   ||  ||    ________ ||=======|  ||==== //   ||                
    || ||           ||     ||     //======\\   ||   \\  ||  ||       | |   ||          ||     \\   ||                 
    || ||_________  ||     ||    //        \\  ||    \\ ||  ||_______| |   ||______||  ||      \\  ||                   
    || |==========| ||     ||   //          \\ ||     \\||  ||=========|   ||=======|  ||       \\ ||
    ||=============================================================================================||

""" + "\n")
print(Logo)
print("\n* Writen by Getahun Atla, 2016 // 2023" + "\n")


time.sleep(7)
os.system("cls")

print(Fore.LIGHTGREEN_EX +
      "##############################################################")
print("1) Make sure you run this script with administrator privileges")
print("2) Make sure that the WiFi adapter is connected to a network")
print("##############################################################\n")


def Coment():
    os.system("cls")

    print(Fore.LIGHTYELLOW_EX + """
                                                ## My Address ##
                    __=================================================================================__      
                    ||                                                                                 ||
                    ||      Phone =  +251 969 141 695 / +251 909 739 087                               || 
                    ||      Email Address = getahunalta09@gmail.com                                    ||
                    ||      Telegram Username = @LocalHost127                                          ||   
                    ||      Github = https://github.com/N3T-H4NT3R                                     ||    
                    ||      Linkedin = https://www.linkedin.com/in/getahun-alta-082473279/             ||
                    ||                                                                                 ||
                    ||---------------------------------------------------------------------------------||
                GOOD BY
          """)
    time.sleep(15)


mac_to_change_to = ["0A1111111111", "0E2222222222", "023333333333", "064444444444",
                    "0A1122334455", "0E1122334455", "021122334455", "061122334455", "021122334455", "061122334455"]
mac_addresses = list()

macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")

transportName = re.compile("({.+})")
adapterIndex = re.compile("([0-9]+)")
getmac_output = subprocess.run(
    "getmac", capture_output=True).stdout.decode().split('\n')

for macAdd in getmac_output:
    macFind = macAddRegex.search(macAdd)
    transportFind = transportName.search(macAdd)
    if macFind == None or transportFind == None:
        continue
    mac_addresses.append((macFind.group(0), transportFind.group(0)))

print("       "*7 + "Chooice Your Network Card !" + "\n")
for index, item in enumerate(mac_addresses):
    print(
        f"Card > [{index}] || Current Mac: > {item[0]} || Transport Name > [{item[1]}]")
option = input("\n" + "Select Your Interface ==>>: ")

while True:
    print("\n" + "Which [Mac Address] Do You Want To Use ?" + "\n")
    for index, item in enumerate(mac_to_change_to):
        print(f"{index} - Mac Address: {item}")
    update_option = input(
        "\n" + "Select the menu item number corresponding to the new MAC address that you want to use:")
    if int(update_option) >= 0 and int(update_option) < len(mac_to_change_to):
        print(
            f"Your Mac Address will be Changing To: {mac_to_change_to[int(update_option)]}")
        break

    else:
        print("\n" + "You didn't select a valid option. Please try again!" + "\n")
controller_key_part = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
    controller_key_folders = [
        ("\\000" + str(item) if item < 10 else "\\00" + str(item)) for item in range(0, 21)]
    for key_folder in controller_key_folders:
        try:
            with winreg.OpenKey(hkey, controller_key_part + key_folder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                try:
                    count = 0
                    while True:
                        name, value, type = winreg.EnumValue(regkey, count)
                        count = count + 1
                        if name == "NetCfgInstanceId" and value == mac_addresses[int(option)][1]:
                            new_mac_address = mac_to_change_to[int(
                                update_option)]
                            winreg.SetValueEx(
                                regkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac_address)
                            print("Successly matched Transport Number")
                            break
                except WindowsError:
                    pass
        except:
            pass

run_disable_enable = input(
    "\n" + "Do you Want To Disable and Reenable your wireless device(s). Type [yes] to Continue or [no] to Exit:")

if run_disable_enable.lower() == 'yes':
    run_last_part = True
else:
    run_last_part = False
while run_last_part:
    network_adapters = subprocess.run(["wmic", "nic", "get", "name,index"], capture_output=True).stdout.decode(
        'utf-8', errors="ignore").split('\r\r\n')
    for adapter in network_adapters:
        adapter_index_find = adapterIndex.search(adapter.lstrip())

        if adapter_index_find and "Wireless" in adapter:
            disable = subprocess.run(["wmic", "path", "win32_networkadapter", "where",
                                     f"index={adapter_index_find.group(0)}", "call", "disable"], capture_output=True)

            if (disable.returncode == 0):
                os.system("cls")
                print(f"Disabled {adapter.lstrip()}")
            enable = subprocess.run(["wmic", "path", f"win32_networkadapter", "where",
                                    f"index={adapter_index_find.group(0)}", "call", "enable"], capture_output=True)

            if (enable.returncode == 0):
                print(f"Enabled {adapter.lstrip()}")
    getmac_output = subprocess.run(
        "getmac", capture_output=True).stdout.decode()
    mac_add = "-".join([(mac_to_change_to[int(update_option)][i:i+2])
                       for i in range(0, len(mac_to_change_to[int(update_option)]), 2)])
    if mac_add in getmac_output:
        for index, item in enumerate(mac_addresses):
            print("\n" + f"Your old [Mac Address] is > {item[0]}" + "\n")
            print(
                "\n" + f"Your New [Mac Address] is > {mac_to_change_to[int(update_option)]}" + "\n")
    break

Feed_Back = str(
    input("\n" + "if You Have any Question or Feed Back!! Say [Yes] or [No]: "))

if Feed_Back == "yes" or Feed_Back == "YES":
    os.system("cls")
    Email_or_Phone = str(input("Enter Your Email or Phone Number: "))

    while not Email_or_Phone:
        os.system("cls")
        print(5 * "     " + "Email or Phone Number is required!" + "\n")
        Email_or_Phone = input("Enter Your Email or Phone Number: ")

    Comment = str(input("Feed Back: "))

    while not Comment:
        os.system("cls")
        print(5*"     " + "The Feed Back Filed can not be Empty!")
        Comment = str(input("Feed Back: "))

    Output = "Email Address = " + \
        str(Email_or_Phone) + "\n" \
        "Feed Back =  " + str(Comment)

    Email_Address = "Enter Your Email Address"
    Email_Address_Password = "Enter Your Password"

    Send_To_Email = smtplib.SMTP("smtp.gmail.com", 587)
    Send_To_Email.starttls()
    Send_To_Email.login(Email_Address, Email_Address_Password)
    Send_To_Email.sendmail(Email_Address, Email_Address, Output)
    Send_To_Email.quit()

    print("\n" "Thank You" + "\n")

    time.sleep(2)

    Coment()


elif Feed_Back == "NO" or Feed_Back == "no" or Feed_Back == "exit":
    Coment()

elif Feed_Back == "":
    Feed_Back = str(input("\n" + "Say [Yes] or [No]: "))

else:
    print("Invalid Key !!!")
