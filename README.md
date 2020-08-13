# MsmoveInputGenerator
Generates ranges of input values for msmove

## How to run
Edit `EntryPoint.py` file with the following commands:
```
msmove_input_generator = MsmoveInputGenerator("input_file_name", "output_file_name", min_number_of_entries_to_generate)
msmove_input_generator.RunGenerator()
```

## Input file

The syntax of the input file is the following:
```
NPOP1_1	VALUE
NPOP1_2	VALUE
NPOP2_1	VALUE
NPOP2_2	VALUE 
T_DIV	VALUE
NPOP_A	VALUE
MU	VALUE
T_I	0
P_I	0
```

All these parameters must be provided (but not necessarily in this order).

In order to generate a parameters set without introgression, the `T_I` and `P_I` parameters have to be set to 0. To add introgression, both of these parameters have to be set to 1.

The program estimates the minimum number of steps for each parameters in order to achieve the desired number of entries to generate and then generates `number_of_steps ^ number of parameters` entries.
