# Given the desired total weight of a barbell with weights, return the combination of plates needed to reach that weight
# E.g. if I want to lift 150 lbs, I would need a 45 plate, a 5 plate, and a 2.5 plate on each side of the 45 lbs barbell

def getPlatesHelper(curr_weight, curr_plates):
	if curr_weight == 0:
		return curr_plates
	else:
		for plate in [45, 35, 25, 10, 5, 2.5]:
			if plate <= curr_weight:
				return getPlatesHelper(curr_weight - plate, curr_plates + [plate])

def getPlates(weight):
	return getPlatesHelper((weight - 45) / 2, [])
