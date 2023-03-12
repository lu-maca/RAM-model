from memory import Registry, Program, LocationRegistry
from ribbons import ReadRibbon, WriteRibbon

class Machine:
    def __init__(self, program: Program, read_ribbon: ReadRibbon) -> None:
        self._registry = Registry()
        self._program = program
        self._location_registry = LocationRegistry()
        self._read_ribbon = read_ribbon
        self._write_ribbon = WriteRibbon()
        self._value = None
        self._current_instr = None
        self._reg_zero = 0
        self.is_running = True

    # public methods
    def fetch_and_decode(self):
        line_idx = self._location_registry.get_line_counter()
        self._current_instr = self._program.get_instruction_at(line_idx)
        
    def execute(self):
        # execute
        self._reg_zero = int(self._registry.read_reg_num(0))
        try:
            self._get_value(self._current_instr[1])
        except:
            self.is_running = False

        opcode = self._current_instr[0]
        print("OPERATION CODE: " + opcode)
        opcode = "_{}".format(opcode.lower())

        try:
            call = getattr(self, opcode)
        except:
            raise Exception("Not existing opcode ({})".format(opcode))
        call()
    
    def get_result(self):
        return self._write_ribbon.get()

    # private methods (instruction set)
    def _get_value(self, argument: tuple):
        if argument[0] == "=":
            value = int(argument[1])
        elif argument[0] == "":
            value = self._registry.read_reg_num(int(argument[1]))
        elif argument[0] == "*":
            reg_i = self._registry.read_reg_num(int(argument[1]))
            value = self._registry.read_reg_num(reg_i)
        else:
            raise Exception("Error: operand at {} has a bad form".format(self._location_registry))
        self._value = value 

    def _load(self):
        self._registry.write_reg_num(0, self._value)
        self._location_registry.goto_next()

    def _store(self):
        self._registry.write_reg_num(self._value, self._reg_zero)
        self._location_registry.goto_next()

    def _add(self):
        sum = self._reg_zero + self._value
        self._registry.write_reg_num(0, sum)
        self._location_registry.goto_next()
        print(">> SUM RESULT: " + str(sum))

    def _sub(self):
        diff = self._reg_zero - self._value
        self._registry.write_reg_num(0, diff)
        self._location_registry.goto_next()

    def _mult(self):
        mult = self._reg_zero * self._value
        self._registry.write_reg_num(0, mult)
        self._location_registry.goto_next()

    def _div(self):
        if self._value == 0:
            raise ArithmeticError("Division by zero")
        div = self._reg_zero / self._value
        self._registry.write_reg_num(0, div)
        self._location_registry.goto_next()

    def _read(self):
        read_value = self._read_ribbon.read()
        self._read_ribbon.advance_position()
        self._registry.write_reg_num(self._value, read_value)
        self._location_registry.goto_next()
        print(">> READ VALUE: " + read_value)

    def _write(self):
        self._write_ribbon.write(self._value)
        self._write_ribbon.advance_position()
        self._location_registry.goto_next()

    def _jump(self):
        self._location_registry.goto(self._value)

    def _jgtz(self):
        if self._reg_zero > 0:
            self._location_registry.goto(self._value)
        else:
            self._location_registry.goto_next()

    def _jzero(self):
        if self._reg_zero == 0:
            self._location_registry.goto(self._value)
        else:
            self._location_registry.goto_next()

    def _jblank(self):
        if self._read_ribbon.read() == " ":
            self._location_registry.goto(self._value)
            print(">> JUMPING TO " + str(self._value))
        else:
            self._location_registry.goto_next()
            print(">> JUMP TO NEXT")

    def _halt(self):
        self.is_running = False
        print(">> HALT!")
