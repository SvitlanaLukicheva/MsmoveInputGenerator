# -*-coding:Utf-8 -*

from datetime import datetime
import random
import re


parameters_file_name = "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\parameters.sv"
output_file_name = "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\output__" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".out"
number_of_samples = 1000


def ParseParameters(file_name):
    print(datetime.now().strftime("%H:%M:%S") + ": Reading file " + parameters_file_name + "...")
    
    parameters_file = open(file_name, "r")
    parameters = []

    for line in parameters_file:
        line_parts = re.split(r'\t+', line)  # split elements of the line separated by tabs
        if(len(line_parts) != 3):  # we want exactly 2 elements per line
            raise Exception("Invalid format for the line " + line)
        if(line_parts[0] == "0"):  # this is a float
            try:
                parameters.append((int(line_parts[0]), float(line_parts[1]), float(line_parts[2])))
            except ValueError:
                raise Exception("Invalid parameters on line " + line + ", should be float")
        elif(line_parts[0] == "1"):  # this is an integer
            try:
                parameters.append((int(line_parts[0]), float(line_parts[1]), float(line_parts[2])))
            except ValueError:
                raise Exception("Invalid parameters on line " + line + ", should be float")
        else:
            raise Exception("Invalid first parameter on line " + line + ", should be 0 or 1")
            
    parameters_file.close()

    print(datetime.now().strftime("%H:%M:%S") + ": Done.")
    return parameters



def GenerateRandomValuesForParameter(min_value, max_value, is_int: bool, count: int):
    print(datetime.now().strftime("%H:%M:%S") + ": Reading file " + parameters_file_name + "...")

    result = []

    if(is_int):
        for i in range(count):
            result.append(random.randint(min_value, max_value))
    else:
        result.append(random.uniform(min_value, max_value))

    print(datetime.now().strftime("%H:%M:%S") + ": Reading file " + parameters_file_name + "...")

    return result



parameters = ParseParameters(parameters_file_name)

output_file = open(output_file_name, "x")

print(datetime.now().strftime("%H:%M:%S") + ": Generating parameters...")
for i in range(number_of_samples):
    line = ""
    for parameter in parameters:
        if(parameter[0] == 0):  # this is a float
            line += str(random.uniform(parameter[1], parameter[2]))
        else:
            line += str(random.randint(parameter[1], parameter[2]))
        line += "\t"
    output_file.write(line + "\n")
print(datetime.now().strftime("%H:%M:%S") + ": Done.")

output_file.close()





