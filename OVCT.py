from urllib.request import urlopen
import bs4, pandas


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

def askSaveOrNot(Filtered_source):
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

if __name__ == "__main__":
    source = webcrawler()
    filter_resource = filterCountry(source)
    filter_resource = filterSpeed(filter_resource)