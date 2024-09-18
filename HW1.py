#import random module
import random

# Task 1: create list of 100 random numbers from 0 to 1000
# step 1: create an empty list
random_numbers = []
# step 2: use a loop to limit number of elements in the list (100)
for i in range(1, 101):
    # step 3: use a module to generate random numbers from 0 to 1000
    num = random.randint(0, 1000)
    # step 4: add each generated number to the list
    random_numbers.append(num)
# step 5: print list of 100 random numbers from 0 to 1000
print('List of random numbers: ', random_numbers)

# Task 2: sort the list from min to max (using bubble sort)
# step 1: define length of the list
last_index = len(random_numbers)
# step 2: use loop for all elements in the list
for i in range(last_index):
    # step 3: use inner loop to compare numbers
    for j in range(0, last_index - i - 1):
        # step 4: compare 2 adjacent numbers
        if random_numbers[j] > random_numbers[j + 1]:
            # step 5: swap if left number is greater than right
            random_numbers[j], random_numbers[j + 1] = random_numbers[j + 1], random_numbers[j]
# step 6: print sorted list
print('Sorted list of random numbers: ', random_numbers)

# Task 3: calculate average for even and odd numbers
# step 1: define variables for further calculation
even_sum = 0
even_count = 0
odd_sum = 0
odd_count = 0
# step 2: use loop to check each value in the list
for i in range(last_index):
    # step 3: if the value is even, add it to the even_sum and increase even_count by 1
    if random_numbers[i] % 2 == 0:
        even_sum += random_numbers[i]
        even_count += 1
    # step 3: if the value is odd, add it to the odd_sum and increase odd_count by 1
    elif random_numbers[i] % 2 != 0:
        odd_sum += random_numbers[i]
        odd_count += 1
#step 4: calculate average values for even numbers
try:
    even_avg = even_sum / even_count
# except to cath ZeroDivisionError
except ZeroDivisionError:
    print('Error while calculating even average value')
    even_avg = None
# finally moving to the next calculation
finally:
    pass
#step 4: calculate average values for odd numbers
try:
    odd_avg = odd_sum / odd_count
# except to cath ZeroDivisionError
except ZeroDivisionError:
    print('Error while calculating odd average value')
    odd_avg = None
# finally moving to the next command
finally:
    pass
# step 5: print results
print('Even average value: ', even_avg)
print('Odd average value: ', odd_avg)

