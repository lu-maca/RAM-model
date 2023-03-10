from instruction_set import Machine
from memory import Program
from ribbons import ReadRibbon
import sys

def main():
    READ_RIBBON = ReadRibbon("123456789 ")
    program = Program()
    program.load_full_program("./algoritmo.txt")

    m = Machine(program, READ_RIBBON)

    while m.is_running:
        m.fetch_and_decode()
        m.execute()
    
    print("RESULT " + str(m.get_result()))
    
if __name__=="__main__":
    sys.exit(main())