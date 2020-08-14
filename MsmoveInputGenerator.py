# -*-coding:Utf-8 -*

from datetime import datetime
import math
import random
import re

from ParametersSet import ParametersSet



class MsmoveInputGenerator:

    def __init__(self, parameters_file_name, output_file_name, number_of_samples):
        """
        Constructor
        """

        # name of the file specifying parameters properties
        self.parameters_file_name = parameters_file_name
        # output file
        self.output_file = open(output_file_name + "__" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".out", "x")
        # minimum number of samples to generate
        self.number_of_samples = number_of_samples
        # dictionary {param_name -> (par_value_1, par_value_2, ...)}
        self.parameters = ParametersSet()
        # number of steps to generate for each parameter
        self.number_of_steps = 0
        # total number of samples to generate = number_of_steps * number_of_parameters
        self.total_number_of_samples_to_generate = 0
        # counts the number of generated samples
        self.generated_samples_count = 0



    def RunGenerator(self):
        """
        Parses parameters and generates the parameter values.
        """

        self.parameters.ParseParameters(self.parameters_file_name)

        # the formula is "number_of_parameters root number_of_samples", we take the ceil in order to generate more samples than requested
        self.number_of_steps = math.ceil(self.number_of_samples ** ( 1.0 / self.parameters.number_of_parameters))
        self.total_number_of_samples_to_generate = self.number_of_steps ** self.parameters.number_of_parameters

        print("Number of steps for parameters: " + str(self.number_of_steps) + ".")
        print("Number of samples to generate: " + str(self.total_number_of_samples_to_generate) + ".")
        
        print(datetime.now().strftime("%H:%M:%S") + ": Generating parameters...")

        param_step_dict ={
            "NPOP1_1": 0,
            "NPOP1_2": 0,
            "NPOP2_1": 0,
            "NPOP2_2": 0,
            "T_DIV": 0,
            "NPOP_A": 0,
            "MU": 0
            }

        # introgression-related parameters have to be also generated
        if(self.parameters.number_of_parameters == 9):
            param_step_dict["T_I"] = 0
            param_step_dict["P_I"] = 0

        self.GenerateOuput(param_step_dict, 0, -1)

        print(datetime.now().strftime("%H:%M:%S") + ": Done. Generated " + str(self.generated_samples_count) + " samples.")

        self.output_file.close()



    def GenerateOuput(self, param_step_dict, step_index, param_index):
        """
        Recursive function assigning all the possible combinations of the parameters
        to the parameters step dictionary and generating msmove output for each combination
        """
        if(param_index < len(param_step_dict)):
            for i in range(self.number_of_steps):
                param_name = list(param_step_dict.keys())[param_index]
                param_step_dict[param_name] = step_index
                self.GenerateOuput(param_step_dict, i, param_index + 1)

        # compute a new parameters set
        if(param_index == len(param_step_dict) and step_index == 0):
            self.generated_samples_count = self.generated_samples_count + 1
            self.output_file.write(self.parameters.GetOutputLineForParameterSet(param_step_dict, self.number_of_steps - 1) + "\n")
            if(self.generated_samples_count % 2000 == 0):
                print(str(self.generated_samples_count) + " out of " + str(self.total_number_of_samples_to_generate), "current parameters vector:", param_step_dict)

