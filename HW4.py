# import random module
import random
import re

# HW1 refactoring
# Task 1: create a list of random number of dicts (from 2 to 10)
def random_list(list_min, list_max, dict_min, dict_max, value_min, value_max):
    #  step 1: define an empty list
    list_dict = []
    # step 2: loop for random number of dicts
    for i in range(random.randint(list_min, list_max)):
        # step 3: define an empty dictionary
        dict_for_list = {}
        # step 4: loop for random number of key-value pairs
        for j in range(random.randint(dict_min, dict_max)):
            # step 5: random key generation
            dict_key = chr(random.randint(ord('a'), ord('z')))
            # step 6: random value generation
            dict_value = random.randint(value_min, value_max)
            # step 7: update dictionary with key-value pairs
            dict_for_list.update({dict_key: dict_value})
        # step 8: update list with dictionaries
        list_dict.append(dict_for_list)
    return list_dict


# step 9: print generated list
generated_list = random_list(2, 10, 2, 10, 1, 100)
print(generated_list)


# Task 2: get previously generated list of dicts and create one common dict:
def common_dict(list_of_dict):
    #  step 1: define an empty dictionary
    common_dict_draft = {}
    l = 0
    k = 0
    # step 2: loop for all elements of the list
    for l in range(len(list_of_dict)):
        # step 3: loop for all elements of the dictionary
        for k in range(len(list_of_dict[l])):
            # step 4: method to return all keys
            key = list(list_of_dict[l].keys())[k]
            # step 4: method to return all values
            value = list(list_of_dict[l].values())[k]
            #  step 5: check if key-value pair already exists in common_dict
            if key in common_dict_draft:
                # step 6: change value to list of values [1, 2, 3],
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
        # step 8: define an empty dictionary
    common_dictionary = {}
    # step 9: loop for all elements of common_dict_draft
    for i in range(len(common_dict_draft)):
        # step 10: method to return all keys
        key = list(common_dict_draft.keys())[i]
        # step 11: method to return all values
        value = list(common_dict_draft.values())[i]
        # step 12: if key is only in one dict - take it as is
        if value[2] == 0:
            common_dictionary.update({key: value[1]})
            # step 13: if key in 2 or more dictionaries, add in new dictionary pair with max value and modified key
        else:
            new_key = f"{key}_{value[0] + 1}"
            common_dictionary.update({new_key: value[1]})
    return common_dictionary


# step 14 print generated list
new_dict = common_dict(generated_list)
print(new_dict)


# HW2 refactoring
HW_string = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""
# Task 1: Normalize letter case
def normalized_text(text):
    # step 1: Converts HW_string into lower case
    text_mod1 = text.lower()
    # step 2: Use regular expression to split HW_string into sentences
    text_mod2 = re.split(r'\.\s+', text_mod1)
    # step 3: Use capitalize() method to convert the first character to upper case
    text_mod3 = [sentence.capitalize() for sentence in text_mod2]
    # step 4: Join the sentences with normalized case
    text_normalized = ". ".join(text_mod3)
    return text_normalized
# step 5: print
HW_string_normalized = normalized_text(HW_string)
print(HW_string_normalized)

# Task 2: Create new sentence
def sentence_from_last_words(text):
    # step 1: define an empty list
    last_words = []
    i = 0
    # step 2: loop for searching dot (end of the sentence, right border of the word)
    while i < len(text):
        if text[i] == '.':
            j = i-1
            # step 3: loop for searching the closest whitespace (left border of the word)
            while j >= 0 and not text[j].isspace():
                j -= 1
            # step 4: add last word to the list
            last_words.append(text[j+1:i])
        i += 1
    # step 5: Join all last words from HW_string_normalized into one sentence
    sentence = ' '.join(last_words).capitalize() + '.'
    return sentence

# step 5: print
new_sentence = sentence_from_last_words(HW_string_normalized)
print(f"Sentence made of the last words: {new_sentence}")

# Task 3: Fix the mistakes
fixing_rules = {" iz ": " is "}
def fix_mistakes(text, replacements):
    fixed_text = text
    # step 1: loop for all fixing rules
    for old_value, new_value in replacements.items():
        # step 2: replace words according to the rules
        fixed_text = fixed_text.replace(old_value, new_value)
    return fixed_text

# step 3: print
text_without_mistakes = fix_mistakes(HW_string_normalized, fixing_rules)
print(text_without_mistakes)

# Task 4: Calculate whitespaces
def whitespaces_count(text):
    # step 1: define variable for counting
    whitespace_count = 0
    # step 2: loop for searching whitespaces in text
    for i in range(len(text)):
        if text[i].isspace():
            whitespace_count += 1
        else:
            i += 1
    return (f"Number of whitespace characters: {whitespace_count}")

# step 3: print
cnt = whitespaces_count(HW_string)
print(cnt)