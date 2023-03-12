from instruction_set import Machine
from memory import Program
from ribbons import ReadRibbon
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

HELP = \
""" \
path of the program file. it shall be a text file in the following form: 
LABEL COMMAND ARGUMENT

LABEL       :   int (program line starting from 1)
COMMAND     :   str (listed below)
ARGUMENT    :   i, =i, *i where i is int 

=========================================================================

Commands list:
READ
WRITE
LOAD
STORE

ADD
SUB
MULT
DIV

JUMP
JGTZ
JZERO
JBLANK

HALT
"""

def get_options():
    parser = ArgumentParser(
        "simple and probably not very accurate model of a RAM",
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("program", type=str, help=HELP)
    parser.add_argument("input_string", type=str, help="string of int. it ends with a blank space")

    return parser.parse_args()

def main():
    args = get_options()

    program = Program()
    program.load_full_program(args.program)
    read_ribbon = ReadRibbon(args.input_string)
    
    m = Machine(program, read_ribbon)

    print("[Input] '{}'".format(args.input_string))
    print("------------------------")

    # run the machine
    while m.is_running:
        m.fetch_and_decode()
        m.execute()
    
    print("------------------------")
    print("[Result] {}".format(m.get_result()))
    
if __name__=="__main__":
    sys.exit(main())