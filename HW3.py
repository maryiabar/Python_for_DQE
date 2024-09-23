#import
import re

HW_string = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# Task 1: Normalize letter case
# step 1: Converts HW_string into lower case
HW_mod1 = HW_string.lower()
# step 2: Use regular expression to split HW_string into sentences
HW_mod2 = re.split(r'\.\s+', HW_mod1)
# step 3: Use capitalize() method to convert the first character to upper case
HW_mod3 = [sentence.capitalize() for sentence in HW_mod2]
# step 4: Join the sentences with normalized case
HW_string_normalized = ". ".join(HW_mod3)
# step 5: print
print(HW_string_normalized)

# Task 2: Create new sentence
# step 1: define an empty list
last_words = []
i = 0
# step 2: loop for searching dot (end of the sentence, right border of the word)
while i < len(HW_string_normalized):
    if HW_string_normalized[i] == '.':
        j = i-1
        # step 3: loop for searching the closest whitespace (left border of the word)
        while j >= 0 and not HW_string_normalized[j].isspace():
            j -= 1
        # step 4: add last word to the list
        last_words.append(HW_string_normalized[j+1:i])
    i += 1
# step 5: Join all last words from HW_string_normalized into one sentence
new_sentence = ' '.join(last_words).capitalize() + '.'
# step 5: print
print(f"Sentence made of the last words: {new_sentence}")

# Task 3: Fix the mistakes
# step 1: replase words iz->is and thiz->this
HW_string_without_mistakes = HW_string_normalized.replace(" iz ", " is ").replace("Thiz", "this")
# step 2: print
print(HW_string_without_mistakes)

# Task 4: Calculate whitespaces
# step 1: define variable for counting
whitespace_count = 0
# step 2: loop for searching whitespaces in HW_string
for i in range(len(HW_string)):
    if HW_string[i].isspace():
        whitespace_count += 1
    else:
        i += 1
# step 3: print
print(f"Number of whitespace characters: {whitespace_count}")