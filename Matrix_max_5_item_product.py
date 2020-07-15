import numpy as np
import pandas as pd

matrix = '''
30 90 80 36 44 66 42 34 65 52 88 26 79 81 55 92 37 37 04 84
93 04 92 03 37 87 93 84 94 62 55 07 88 86 09 33 70 78 09 61
72 02 02 37 38 88 57 19 22 82 71 53 14 60 73 05 45 77 76 57
32 34 77 55 39 93 36 95 65 32 95 90 53 71 97 70 85 38 72 37
37 53 33 97 41 01 77 07 68 10 01 45 21 94 09 80 98 45 89 87
19 12 58 02 27 83 70 12 75 12 36 43 15 79 40 90 91 74 58 84
45 34 34 29 14 89 51 65 87 24 78 26 94 82 64 75 14 09 76 26
86 30 86 21 30 00 57 90 11 00 41 48 08 38 37 41 85 84 46 74
61 83 37 84 98 44 10 32 08 18 68 36 43 49 26 28 47 37 81 23
39 74 01 51 73 83 85 41 82 25 03 32 16 15 66 51 37 68 47 28
78 68 27 37 58 88 63 54 89 11 56 47 20 57 58 07 07 36 26 20
11 36 87 84 82 68 12 16 37 16 00 50 96 25 53 00 27 78 00 57
04 70 06 96 92 00 96 15 24 32 13 49 61 52 30 38 03 77 43 17
45 78 70 45 10 61 60 71 00 18 91 27 00 04 66 72 07 74 89 73
94 97 29 25 89 67 91 65 17 27 51 61 86 21 95 79 01 54 89 80
59 90 72 94 60 03 39 61 69 49 52 89 50 74 84 56 50 86 68 26
66 47 67 78 68 65 20 83 78 37 19 52 16 76 12 25 35 81 26 81
67 03 31 26 27 61 36 84 19 53 77 69 40 13 91 78 00 54 94 02
20 59 70 91 74 39 90 55 53 74 12 79 48 40 01 73 06 68 56 40
07 33 59 64 84 25 89 38 19 29 93 77 46 86 45 93 63 96 53 29'''

maxProduct = 0
max_start_coordinates = None
max_navigation_direction = None

array = np.fromstring(matrix, sep='\n', dtype=int).reshape((20,20))
array_flipped = np.flip(array,0)                                                           # inversing the array to use the same logic as in "down_and_right" later
iterator = np.nditer(array, flags=['multi_index'])                                         # creatin an np iterator to access indexes

for matrix_element in iterator:
    starting_index = iterator.multi_index                                                  # getting the index coordinates from a nditer object with multi_index

    navi_list = {"top to bottom" : [(starting_index[0]+i, starting_index[1]) for i in range(5)],      # creating a collection of directions to check with their respective element coordinates
                 "left to right": [(starting_index[0], starting_index[1]+i) for i in range(5)],
                 "down and right": [(starting_index[0]+i, starting_index[1]+i) for i in range(5)],
                 "up and right": [(starting_index[0]+i, starting_index[1]+i) for i in range(5)]}

    for navigation_direction in navi_list:
        product_array = []                                                                      # storing the interim product value for comparison here
        for item in navi_list[navigation_direction]:
            try:                                                                                # using try/catch to ignore the out_of_range error on the matrix
                if navigation_direction == "up and right":                                      # using the vertically inversed matrix to avoid positioning complications for the up-and-right direction
                    product_array.append(array_flipped[item])
                else:
                    product_array.append(array[item])
            except:                                                                             # if coming to the border of the matrix, just checking next item in it
                break

        prod_pandas= int(pd.DataFrame(product_array).prod())                                    # Prod function in Numpy returns negative values when fed with an array of 3-digit integers, so I used Pandas instead.
        if maxProduct < prod_pandas:                                                            # I mean np.prod([199, 199, 199, 199, 199]) gives you -1453011609 funny, huh?
            maxProductArray = product_array                                                     # np.prod([199., 199., 199., 199., 199.]) works as expected though. Np precision quirks I guess?
            maxProduct = prod_pandas
            if navigation_direction == "up and right":
                max_start_coordinates = (19-starting_index[0], starting_index[1])                             # assumed we only work with a 20X20 matrix here
            else:
                max_start_coordinates = starting_index
            max_navigation_direction = navigation_direction

if maxProduct == 0:
    print(f"Maximum product = 0 since the matrix has no 5-item array with no zeros in it in any of the directions")
else:
    print(f"Maximum product = {maxProduct}, derived from array : {maxProductArray}, starts at {max_start_coordinates} (number {array[max_start_coordinates]}) when moving {max_navigation_direction}")

