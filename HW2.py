# import
import random
from turtle import update

#Task 1: create a list of random number of dicts (from 2 to 10)
#  step 1: define an empty list
list_dict = []
# step 2: loop for random number of dicts
for i in range(random.randint(2, 10)):
    # step 3: define an empty dictionary
    dict_for_list = {}
    # step 4: loop for random number of key-value pairs
    for j in range(random.randint(2, 10)):
        # step 5: random key generation
        dict_key = chr(random.randint(ord('a'), ord('z')))
        # step 6: random value generation
        dict_value = random.randint(0, 100)
        # step 7: update dictionary with key-value pairs
        dict_for_list.update({dict_key: dict_value})
    # step 8: update list with dictionaries
    list_dict.append(dict_for_list)
# step 9: print generated list
print(list_dict)

# Task 2: get previously generated list of dicts and create one common dict:

#  step 1: define an empty dictionary
common_dict_draft = {}
l = 0
k = 0
# step 2: loop for all elements of the list
for l in range(len(list_dict)):
    # step 3: loop for all elements of the dictionary
    for k in range(len(list_dict[l])):
        # step 4: method to return all keys
        key = list(list_dict[l].keys())[k]
        # step 4: method to return all values
        value = list(list_dict[l].values())[k]
        #  step 5: check if key-value pair already exists in common_dict
        if key in common_dict_draft:
            #step 6: change value to list of values [1, 2, 3],
            # where 1 - number of dictionary, 2 - max value, 3 - number of loop
            dval = common_dict_draft.get(key)
            dval[2] += 1
            if value > dval[1]:
                dval[0] = l
                dval[1] = value
        # step 7: otherwise add new key-value pair in common_dict with 0 as number of loop
        else:
            common_dict_draft.update({key: [l, value, 0]})
        k += 1
    l += 1
#print(common_dict_draft)

# step 8: define an empty dictionary
common_dict = {}
# step 9: loop for all elements of common_dict_draft
for i in range(len(common_dict_draft)):
    # step 10: method to return all keys
    key = list(common_dict_draft.keys())[i]
    # step 11: method to return all values
    value = list(common_dict_draft.values())[i]
    # step 12: if key is only in one dict - take it as is
    if value[2] == 0:
        common_dict.update({key: value[1]})
        # step 13: if key in 2 or more dictionaries, add in new dictionary pair with max value and modified key
    else:
        new_key = f"{key}_{value[0]+1}"
        common_dict.update({new_key: value[1]})
# print
print(common_dict)

