def defloop (the_list):
	for ilist in the_list:
		if isinstance(ilist, list):
			defloop(ilist)
		else:
			print(ilist)