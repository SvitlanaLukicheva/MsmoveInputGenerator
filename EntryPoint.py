# -*-coding:Utf-8 -*

from MsmoveInputGenerator import MsmoveInputGenerator

msmove_input_generator = MsmoveInputGenerator("C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\gadma_parameters_no_introgression.sv", "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\gadma_no_introgression", 10000)
msmove_input_generator.RunGenerator()

msmove_input_generator = MsmoveInputGenerator("C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\gadma_parameters_introgression.sv", "C:\\Users\\svitl\\Desktop\\Git\\MsmoveInputGenerator\\data\\gadma_introgression", 10000)
msmove_input_generator.RunGenerator()