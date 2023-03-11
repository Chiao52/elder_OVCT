import pandas as pd
import numpy as np 
from functions import webcrawler

class update:
	def append_new():
		old_list = pd.read_csv("./resources/all_resources.csv")
		new_list = webcrawler.load_table()
		update_resource = old_list.merge(new_list, how='outer', indicator=True).loc[lambda x : x['_merge'] == 'right_only']
		update_resource = update_resource.drop(["_merge"], axis=1)
		update_resource.to_csv(r"./resources/all_resources.csv", mode = 'a', header = False, index = False)
		print("Successfully!")