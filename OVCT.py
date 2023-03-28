from urllib.request import urlopen
import bs4, pandas, os, base64, re


def webcrawler():
    html = urlopen('https://www.vpngate.net/cn/')
    root = bs4.BeautifulSoup(html, 'html.parser')

    strong_word = root.find_all('strong')

    link_list = []
    for csv_list_link in strong_word:
        if csv_list_link.a != None:
            link_list.append(csv_list_link.a.get('href'))

    vpngate_url = link_list[6]
    source = pandas.read_csv(vpngate_url, header=1)
    source['Speed'] = source['Speed'] / 1000000
    source = source[['#HostName', 'CountryLong', 'IP', 'Speed', 'OpenVPN_ConfigData_Base64']]
    source.to_csv('vpn_list.csv', sep=',', index=False)
    print("\n======================================================================\n\n【 Public VPN 10 records 】\n")
    print(source[['#HostName', 'CountryLong', 'IP', 'Speed']].head(10))
    print('\n======================================================================\n')
    return source

def append_new_list():
    old_list = pandas.read_csv('vpn_list.csv')
    new_list = webcrawler()
    update_list = old_list.merge(new_list, how='outer', indicator=True).loc[lambda x : x['_merge'] == 'right_only']
    update_list = update_list.drop(["_merge"], axis=1)
    update_list.to_csv('vpn_list.csv', mode = 'a', header = False, index = False)
    print("[ The publicVPN have been updated! ]")
    print('\n-----------------------------------\n')

def filterCountry(source):
    country_list = source.filter(items=['CountryLong'])
    country_list = country_list.astype(str)
    country_list = country_list['CountryLong'].values.tolist()
    country_set = set(country_list)
    country_set.remove('nan')
    while(True):
        print('\n-----------------------------------\n')
        print('There are some countries you can choose: \n')
        for c in country_set:
            print(c.replace(',', ''))
        input_country = input("\n\n【 Please enter the country 】 \n\n=> ")
        if (input_country in country_set):
            break
        else:
            print('\n[Your input is not in the list, please enter it again.]')
            
    source = source[source.CountryLong.eq(input_country)]
    return source

def filterSpeed(source):
    speed_list = source.filter(items=['Speed'])
    speedmax = speed_list.max()  
    speedmin = speed_list.min()
    print('\n-----------------------------------\n')
    print('The Speed Range: ' + speedmin.to_string(index=False) + ' Mbps' + ' ~ ' + speedmax.to_string(index=False) + ' Mbps')
    speed = int(input("\n【 How fast the VPN would you prefer 】\n\n=> "))
    
    source = source.query('Speed >= {}'.format(speed))
    askSaveOrNot(source)
    return source

def askSaveOrNot(filtered_source):
    print('\n-----------------------------------\n')
    save_or_not = input("【 Save as another list.(Y/N) 】 \n\n=> ")
    if save_or_not == "Y" or save_or_not == "y":
        Filtered_source.to_csv('filtered_vpn_list.csv', sep=',', index=False)
        print("\n[ the list has been saved successfully. ]")
    else:
        pass
    print('\n-----------------------------------\n\n【 Public VPN 10 filtered records 】\n')
    print(Filtered_source[['#HostName', 'CountryLong', 'IP', 'Speed']].head(10))
    print('\n-----------------------------------\n')

def selectOne(selected_file_name):
    Source = pandas.read_csv(selected_file_name)

    print('\n-----------------------------------\n\n【 Public VPN 10 filtered records 】\n')
    print(Source[['#HostName', 'CountryLong', 'IP', 'Speed']].head(10))
    print('\n-----------------------------------\n')

    vpn_hostname = input("【 Please input VPN ISP hostname 】\n\n=> ")
    
    while(vpn_hostname not in list(Source['#HostName'])):
        print("\n[Sorry, this Hostname isn't in the file, please input again.]")
        print('\n-----------------------------------\n')
        vpn_hostname = input("【 Please input VPN ISP hostname 】\n\n=> ")        
    
    print('\n-----------------------------------\n')

    filter = Source['#HostName'] == vpn_hostname
    vpn_data = Source[(filter)].values.tolist()[0]
    vpn_ip = vpn_data[2]
    vpn_country = vpn_data[1]
    
    if " " in vpn_country:
        vpn_country = vpn_country.replace(" ", "_")
    else:
        pass
    return vpn_hostname, vpn_ip, vpn_country

def decodeSelectedVpn(selected_file_name, vpn_hostname):
    list_file = pandas.read_csv(selected_file_name)
    filter = list_file['#HostName'] == vpn_hostname
    vpn_data = list_file[(filter)]

    base64_message = str(vpn_data['OpenVPN_ConfigData_Base64'].values)
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    ovpn_file_content = message_bytes.decode('ascii')

    return ovpn_file_content

def Connection(ovpn_file_content, vpn_hostname, vpn_ip, vpn_country):
    openvpn_path = "/etc/openvpn"
    ovpn_file_path = os.path.join(openvpn_path, 'client', 'vpngate_{}_{}_{}.ovpn'.format(vpn_hostname, vpn_country, vpn_ip))
    print(ovpn_file_path)
    ovpn_file_path = re.sub("\[|\]|\'","",ovpn_file_path)
    print(ovpn_file_path)
    # with open(ovpn_file_path, mode="w") as file:
    #     file.write(ovpn_file_content)
    # print("\n===== ## Now, the public VPN (Country: {}, Hostname: {}, IP: {}) is connecting. ===== \n\n".format(vpn_hostname, vpn_country, vpn_ip))
    # os.system('sudo openvpn --config {}'.format(ovpn_file_path))

if __name__ == "__main__":
    #webcrawler()
    while(True):
        function_chioce = input("Choose a Function: \n\n 1. Update the public VPN list \n 2. Filter the public VPN list \n 3. Connection \n 0. Exit\n\n=> ")
        if function_chioce == "1":
            append_new_list()
        
        elif function_chioce == "2":
            source = pandas.read_csv('vpn_list.csv')
            filter_resource = filterCountry(source)
            filter_resource = filterSpeed(filter_resource)
            askSaveOrNot(filter_resource)
        
        elif function_chioce == '3':
            print('\n-----------------------------------\n')
            print('You can enter a csv file name of these...\n')
            for i in range(len(os.listdir())):
                if os.listdir()[i].endswith(".csv"):
                    print(os.listdir()[i].replace('.csv', ''))
            print('\n-----------------------------------\n')
            
            selected_file_name = input("【 Please enter the VPN list name 】\n\n=> ")
            selected_file_name = selected_file_name + ".csv"
            while (selected_file_name.strip() == '') or (os.path.exists(selected_file_name) == False):
                print("\n[Sorry, this path information is necessary, please input again.]")
                print('\n-----------------------------------\n')
                selected_file_name = input("【 Please enter the VPN list name 】\n\n=> ")
                selected_file_name = selected_file_name + ".csv"
            

            vpn_hostname, vpn_ip, vpn_country = selectOne(selected_file_name)
            ovpn_file_content = decodeSelectedVpn(selected_file_name, vpn_hostname)
            Connection(ovpn_file_content, vpn_hostname, vpn_ip, vpn_country)