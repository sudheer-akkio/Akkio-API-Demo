import numpy as np
import pandas as pd

ls = [25.7, 27.2, 29.7, 28.6, 30.7, 33.4, 35.8, 38.6, 3.7, 7.7]
val = np.std(ls)


# Calculate the standard deviation for the given values
std_deviation = pd.Series(ls).std()

print("Numpy answer: " + str(val))
print("Pandas answer: " + std_deviation)
