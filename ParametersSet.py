# -*-coding:Utf-8 -*


from datetime import datetime
import math
import numpy
import re



class ParametersSet:

    def __init__(self):
        """
        Constructor
        """

        self.npop1_1 = "N/A"
        self.npop1_2 = "N/A"
        self.npop2_1 = "N/A"
        self.npop2_2 = "N/A"
        self.t_div = "N/A"
        self.npop_a = "N/A"
        self.mu = "N/A"
        self.t_i = "N/A"
        self.p_i = "N/A"

        # represents the number of parsed parameters, can be 7 (no introgression) or 9 (introgression)
        self.number_of_parameters = 0



    def ParseParameters(self, parameters_file_name):
        """
        Reads the parameters file name and assigns the values of parameters from it.
        The format of parameters file is a line for each parameter of the following form:
        PARAM_NAME  PARAM_VALUE
        """

        print(datetime.now().strftime("%H:%M:%S") + ": Reading file " + parameters_file_name + "...")

        parameters_file = open(parameters_file_name, "r")

        for line in parameters_file:
            line_parts = re.split(r'\t+', line)  # split elements of the line separated by tabs
            if(len(line_parts) == 2):
                self.AddParameter(line_parts[0], float(line_parts[1].strip()))
            else:  # we want 2 elements per line
                raise Exception("Invalid format for the line " + line)
           
        parameters_file.close()

        # check that all the mandatory parameters are correctly set
        if(self.npop1_1 == "N/A" or
           self.npop1_2 == "N/A" or
           self.npop2_1 == "N/A" or
           self.npop2_2 == "N/A" or
           self.t_div == "N/A" or
           self.npop_a == "N/A" or
           self.mu == "N/A"):
            raise Exception("One of mandatory parameters is missing!")

        # check that introgression-related parameters are correctly set (either both equal 1 or both equal 0)
        if(self.t_i == 1 and self.p_i == 1):  # introgression
            self.number_of_parameters = 9
        elif(self.t_i == 0 and self.p_i == 0):  # no introgression
            self.number_of_parameters = 7
        else:
            raise Exception("Inconsistent values provided for parameters T_I and P_I!")

        print(datetime.now().strftime("%H:%M:%S") + ": Reading file done.")



    def AddParameter(self, param_name, param_value):
        """
        Assigns the provided value to the parameter with the provided name
        """
        if(param_name == "NPOP1_1"):
            if(self.npop1_1 != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.npop1_1 = param_value
        elif(param_name == "NPOP1_2"):
            if(self.npop1_2 != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.npop1_2 = param_value
        elif(param_name == "NPOP2_1"):
            if(self.npop2_1 != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.npop2_1 = param_value
        elif(param_name == "NPOP2_2"):
            if(self.npop2_2 != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.npop2_2 = param_value
        elif(param_name == "T_DIV"):
            if(self.t_div != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.t_div = param_value
        elif(param_name == "NPOP_A"):
            if(self.npop_a != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.npop_a = param_value
        elif(param_name == "MU"):
            if(self.mu != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.mu = param_value
        elif(param_name == "T_I"):
            if(self.t_i != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.t_i = param_value
        elif(param_name == "P_I"):
            if(self.p_i != "N/A"):
                raise Exception("Duplicated value specified for the parameter " + param_name + "!")
            else:
                self.p_i = param_value
        else:
            raise Exception("Invalid parameter name: " + param_name + "!")




    def GetLowerBoundOfParameter(self, param_value):
        return param_value - (param_value / 2)



    def GetOutputLineForParameterSet(self, param_step_dict, total_number_of_steps):
        """
        Evaluates the parameter values for the provided combination of parameter steps.
        """

        # first, evaluate the model parameter values for the provided combination of parameter steps
        current_npop1_1 = self.GetLowerBoundOfParameter(self.npop1_1) + (self.npop1_1 / total_number_of_steps) * param_step_dict["NPOP1_1"]
        current_npop1_2 = self.GetLowerBoundOfParameter(self.npop1_2) + (self.npop1_2 / total_number_of_steps) * param_step_dict["NPOP1_2"]
        current_npop2_1 = self.GetLowerBoundOfParameter(self.npop2_1) + (self.npop2_1 / total_number_of_steps) * param_step_dict["NPOP2_1"]
        current_npop2_2 = self.GetLowerBoundOfParameter(self.npop2_2) + (self.npop2_2 / total_number_of_steps) * param_step_dict["NPOP2_2"]
        current_t_div = self.GetLowerBoundOfParameter(self.t_div) + (self.t_div / total_number_of_steps) * param_step_dict["T_DIV"]
        current_npop_a = self.GetLowerBoundOfParameter(self.npop_a) + (self.npop_a / total_number_of_steps) * param_step_dict["NPOP_A"]
        current_mu = self.GetLowerBoundOfParameter(self.mu) + (self.mu / total_number_of_steps) * param_step_dict["MU"]

        # then, evaluate msmove parameter values from the model values
        n2_init = current_npop2_1 / current_npop1_1
        t_div = current_t_div / (4 * current_npop1_1)
        resize = current_npop_a / current_npop1_1
        theta = 4 * current_npop1_1 * current_mu * 10000
        alpha_1 = (-4 * current_npop1_1 / current_t_div) * numpy.log(current_npop1_2 / current_npop1_1)
        alpha_2 = (-4 * current_npop1_1 / current_t_div) * numpy.log(current_npop2_2 / current_npop2_1)

        output_line = str(n2_init) + "\t" + str(t_div) + "\t" + str(t_div) + "\t" + str(resize) + "\t" + str(theta) + "\t" + str(alpha_1) + "\t" + str(alpha_2)

        # introgression-related parameters
        if(self.number_of_parameters == 9):
            t_i = 0 + ((current_t_div / 4) / total_number_of_steps) * param_step_dict["T_I"]
            p_i = max(0.01, (1 / total_number_of_steps) * param_step_dict["P_I"])
            output_line = output_line + "\t" + str(t_i) + "\t" + str(p_i)

        debug = False
        if(debug):
            print("Model parameters:", current_npop1_1, current_npop1_2, current_npop2_1, current_npop2_2, current_t_div, current_npop_a, current_mu)
            print("msmove parameters", output_line)

        return output_line