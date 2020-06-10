# -*-coding:Utf-8 -*

from datetime import datetime
import math
import random
import re



class MsmoveInputGenerator:

    def __init__(self, parameters_file_name, output_file_name, number_of_samples):
        """
        Constructor
        """

        # name of the file specifying parameters properties
        self.parameters_file_name = parameters_file_name
        # name of the output file
        self.output_file_name = output_file_name + "__" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".out"
        # minimum number of samples to generate
        self.number_of_samples = number_of_samples
        # dictionary {param_name -> (par_value_1, par_value_2, ...)}
        self.parameters = {}
        # number of steps for range of bounded parameters
        self.number_of_steps = 0


    def RunGenerator(self):
        """
        Parses parameters and generates the parameter values.
        """

        self.ParseParameters()

        output_file = open(self.output_file_name, "x")

        print(datetime.now().strftime("%H:%M:%S") + ": Generating parameters...")

        parameter_values = {}
        for i in range(self.number_of_steps):
            self.GenerateParameters(self.parameters.items(), 0, parameter_values, i, output_file)

        print(datetime.now().strftime("%H:%M:%S") + ": Done.")

        output_file.close()


    def ParseParameters(self):
        """
        Parses the parameters specified in the file "file_name" and returns them in a dictionary of the form {param_name -> (par_value_1, par_value_2, ...)}
        If a parameter is bounded by a lower and a upper value, it has to be specified as follows:
        param_name    lower_bound   upper_bound
        otherwise, if its value is a function of another parameter, it has to be specified as follows:
        param_name    =   formula
        """

        print(datetime.now().strftime("%H:%M:%S") + ": Reading file " + self.parameters_file_name + "...")

        parameters_file = open(self.parameters_file_name, "r")
        value_to_add = ()
        number_of_bounded_parameters = 0

        for line in parameters_file:
            line_parts = re.split(r'\t+', line)  # split elements of the line separated by tabs
            if(len(line_parts) == 3):
                value_to_add = (line_parts[1], line_parts[2])
                if(line_parts[1] != "="):  # this is a bounded parameter
                    number_of_bounded_parameters += 1
            else:  # we want 3 elements per line
                raise Exception("Invalid format for the line " + line)
            if(line_parts[0] in self.parameters):
                raise Exception("Duplicated parameter name: " + parameter[0])
            self.parameters[line_parts[0]] = value_to_add
           
        parameters_file.close()

        # the formula is "number_of_bounded_parameters root number_of_samples", we take the ceil in order to generate more samples than requested
        self.number_of_steps = math.ceil(self.number_of_samples ** ( 1.0 / number_of_bounded_parameters))

        print(datetime.now().strftime("%H:%M:%S") + ": Done.")


    def GenerateParameters(self, parameters, current_parameter_index, current_parameter_values, current_step, output_file):
        """
        Recursive method generating all the combination of parameters and writing them in the output file.
        """
        try:
            if(current_parameter_index < len(parameters)):
                parameter = list(parameters)[current_parameter_index]
                if(parameter[1][0] == "="):  # this is a formula
                    if(current_step > 0):  # there is only one value possible for formula parameters, no need to generate steps
                        return
                    current_parameter_values[parameter[0]] = self.EvaluateParameter(parameter[1][1], current_parameter_values)
                else:  # this is a bounded parameter
                    if(0 < self.number_of_steps):
                        min_bound = self.EvaluateParameter(parameter[1][0], current_parameter_values)
                        max_bound = self.EvaluateParameter(parameter[1][1], current_parameter_values)
                        values_range = max_bound - min_bound
                        if(values_range <= 0):
                            raise Exception("Invalid range for parameter " + parameter)
                        step_interval = values_range / (self.number_of_steps - 1)
                        current_parameter_values[parameter[0]] = min_bound + current_step * step_interval
                        
                for i in range(self.number_of_steps):
                    self.GenerateParameters(parameters, current_parameter_index + 1, current_parameter_values, i, output_file)

            elif(current_step == 0):
                line = ""
                for parameter_value in current_parameter_values.values():
                    line += str(parameter_value) + "\t"

                output_file.write(line + "\n")
                        
        except ValueError:
            raise Exception("Invalid parameter type for parameter " + parameter)


    def isFloat(self, string: str):
        """
        Indicates whether the provided string represents a float
        """
        try:
            float(string)
            return True
        except ValueError:
            return False


    def GetParameterValue(self, value: str, known_values):
        """
        Returns the value for the provided parameter.
        If the parameter represents a float, returns this value.
        Otherwise, if the parameter represents the name of another parameter with a known value, returns the value of this parameter.
        Otherwise, returns "N/A"
        """
        result = "N/A"
        if(self.isFloat(value)):
            result = float(value)
        elif(value in known_values):
            result = known_values[value]
        return result


    def EvaluateParameter(self, parameter: str, known_values):
        """
        Evaluates the value of the provided parameter.
        """

        result = "N/A"

        formula_parts = parameter.split()

        if(len(formula_parts) > 3):
            raise Exception("Invalid formula on line: " + line)

        if(len(formula_parts) == 1):  # the parameter is given as a value or equals another parameter
            result = self.GetParameterValue(formula_parts[0], known_values)
        else:  # this is a formula of type X ~ Y with ~ in the list [+,-,*,/]
            par1 = self.GetParameterValue(formula_parts[0], known_values)
            par2 = self.GetParameterValue(formula_parts[2], known_values)
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


msmove_input_generator = MsmoveInputGenerator("C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\parameters.sv", "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\fsc_introgression", 10000)
msmove_input_generator.RunGenerator()