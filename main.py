import platform
import pandas
import os
import sys

import set_init
set_init.init_file_name()
from functions import *

if __name__ == "__main__":
    set_init.init_file_name()
    result = pandas.read_csv("./resources/all_resources.csv")

    while(True):
    
        print("\n======================================================================\n\n【 Public VPN 10 records 】\n")
        print(result[['#HostName', 'CountryLong', 'IP', 'Speed']].head(10)) # List the first 10 rows of the PublicVPN list
        print('\n======================================================================\n')

        function_chioce = input("Choose a Function: \n\n 1. Update the public VPN list \n 2. Filter the public VPN list \n 3. Connection \n 0. Exit\n\n=> ")
        
        if function_chioce == '1':
            result = webcrawler.load_table()
            file_storage.file_update(result)

        elif function_chioce == '2':
            print('\n-----------------------------------\n')
            filtered_csv_path = vpnfilter.filter(result)

        elif function_chioce == '3':
            print('\n-----------------------------------\n')
            file_name = input("【 Please enter your VPN list name:】\n\n=> ")
            filtered_csv_path = "./resources/" + file_name + ".csv"
            while (filtered_csv_path.strip() == '') or (os.path.exists(filtered_csv_path) == False):
                print("[Sorry, this path information is necessary, please input again.]")
                print('\n-----------------------------------\n')
                file_name = input("【 Please enter your VPN list name:】\n\n=> ")
                filtered_csv_path = "./resources/" + file_name + ".csv"

            vpn_hostname, vpn_ip, vpn_country = vpnselection.select_one(filtered_csv_path, show_list = "y")
            ovpn_file_content = decode.vpn(filtered_csv_path, vpn_hostname)

            if platform.system() == "Linux":
                connection.ubuntu(ovpn_file_content, vpn_hostname, vpn_ip, vpn_country)
            elif platform.system() == "Darwin":
                connection.macos(ovpn_file_content, vpn_hostname, vpn_ip, vpn_country)
            elif platform.system() == "Windows":
                connection.windows(ovpn_file_content, vpn_hostname, vpn_ip, vpn_country)
            else:
                print("Sorry, your operating system is not supported!")
                sys.exit()
            sys.exit()
        
        elif function_chioce == '0':
            sys.exit()

        else:
            pass
