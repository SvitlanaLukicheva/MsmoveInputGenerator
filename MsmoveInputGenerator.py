# -*-coding:Utf-8 -*

from datetime import datetime
import random
import re


parameters_file_name = "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\parameters.sv"
output_file_name = "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\fsc_introgression__" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".out"
number_of_samples = 10000


def ParseParameters(file_name):
    """
    Parses the parameters specified in the file "file_name" and returns them in a dictionary of the form
    {parameter_name,(val1, val2, val3)}
    """
    
    # if a parameter is bounded by a lower and a upper value, it has to be specified with 4 elements separated by tabs as follows:
    # param_name    is_int  lower_bound upper_bound
    # otherwise, if its value is a function of another parameter, it has to be specified with 3 elements separated by tabs as follows:
    # param_name    =   formula

    print(datetime.now().strftime("%H:%M:%S") + ": Reading file " + parameters_file_name + "...")

    parameters_file = open(file_name, "r")
    parameters = {}

    value_to_add = ()

    for line in parameters_file:
        line_parts = re.split(r'\t+', line)  # split elements of the line separated by tabs
        if(len(line_parts) == 3):
            value_to_add = (line_parts[1], line_parts[2])
        elif(len(line_parts) == 4):
            value_to_add = (line_parts[1], line_parts[2], line_parts[3])
        else:  # we want 3 or 4 elements per line
            raise Exception("Invalid format for the line " + line)
        if(line_parts[0] in parameters):
            raise("Duplicated parameter name: " + parameter[0])
        parameters[line_parts[0]] = value_to_add
           
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


def isFloat(string: str):
    """
    Indicates whether the provided string represents a float
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def GetParameterValue(value: str, known_values):
    """
    Returns the value for the provided parameter.
    If the parameter represents a float, returns this value.
    Otherwise, if the parameter represents the name of another parameter with a known value, returns the value of this parameter.
    Otherwise, returns "N/A"
    """
    result = "N/A"
    if(isFloat(value)):
        result = float(value)
    elif(value in known_values):
        result = known_values[value]
    return result


def EvaluateParameter(parameter: str, known_values):
    """
    Evaluates the value of the provided parameter.
    """

    result = "N/A"

    formula_parts = parameter.split()

    if(len(formula_parts) > 3):
        raise Exception("Invalid formula on line: " + line)

    if(len(formula_parts) == 1):  # the parameter is given as a value or equals another parameter
        result = GetParameterValue(formula_parts[0], known_values)
    else:  # this is a formula of type X ~ Y with ~ in the list [+,-,*,/]
        par1 = GetParameterValue(formula_parts[0], known_values)
        par2 = GetParameterValue(formula_parts[2], known_values)
        if(par1 == "N/A" or par2 == "N/A"):
            raise Exception("Invalid formula for " + parameter)
        if(formula_parts[1] == "+"):
            result = par1 + par2
        elif(formula_parts[1] == "-"):
            result = par1 - par2
        elif(formula_parts[1] == "*"):
            result = par1 * par2
        elif(formula_parts[1] == "/"):
            result = par1 / par2
        else:
            raise Exception("Invalid operation specified for parameter " + parameter)

    return result




parameters = ParseParameters(parameters_file_name)

output_file = open(output_file_name, "x")

print(datetime.now().strftime("%H:%M:%S") + ": Generating parameters...")
for i in range(number_of_samples):
    
    parameter_values = {}
    for parameter in parameters.items():
        try:
            if(parameter[1][0] == "="):  # this is a formula
                parameter_values[parameter[0]] = EvaluateParameter(parameter[1][1], parameter_values)
            else:  # this is a bounded parameters
                par1 = EvaluateParameter(parameter[1][0], parameter_values)
                par2 = EvaluateParameter(parameter[1][1], parameter_values)
                parameter_values[parameter[0]] = random.uniform(par1, par2)
        except ValueError:
            raise Exception("Invalid parameter type for parameter " + parameter)
    
    line = ""
    for parameter_value in parameter_values.values():
        line += str(parameter_value) + "\t"

    output_file.write(line + "\n")

print(datetime.now().strftime("%H:%M:%S") + ": Done.")

output_file.close()





