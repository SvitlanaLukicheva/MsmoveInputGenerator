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
PARAM_NAME  LOWER_BOUND UPPER_BOUND
PARAM_NAME  = FORMULA
```

The first line specifies a parameter which is bounded by a lower and a upper value.
The second line specifies a parameter which is computed by a formula.
Formulas are of type `X ~ Y`, where ´X´ and ´Y´ are parameter names (defined previously) or numbers and ´~´ is an operator from the list `+, -, *, /`.
Lower and upper bounds can also be specified as formulas, possibly using parameters (defined previously).

See below an example.

```
POP_RAT	0.02282 0.068475
T_DIV1	0.046	0.138
T_DIV2	=	TDIV1
T_INTR	0	TDIV1 / 4
```
