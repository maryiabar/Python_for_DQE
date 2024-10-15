import re
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
