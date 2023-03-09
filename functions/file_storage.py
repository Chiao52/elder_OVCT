import pandas, csv

def file_update(Source):
    Path = './resources/all_resources.csv'
    # columns = ['HostName', 'Country', 'IP', 'Speed (Mbps)', 'OpenVPN_ConfigData_Base64']
    # source_CSV = Source.reindex(columns=columns)
    Source.to_csv(Path, sep=',', index=False)
    print("\n[ The result has outputted ! ]\n")
    return Path

def save_file(Source):
    print('\n-----------------------------------\n')
    file_name = input("【 Please input the CSV file name that you want to save. 】 \n\nPlease enter the absolute file name\n\n=> ")
    Path = './resources/' + file_name +'.csv'
    # columns = ['HostName', 'Country', 'IP', 'Speed (Mbps)', 'OpenVPN_ConfigData_Base64']
    # source_CSV = Source.reindex(columns=columns)
    Source.to_csv(Path, sep=',', index=False)
    print("\n[ The result has outputted ! ]\n")
    return Path
