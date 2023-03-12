from memory import Registry, Program, LocationRegistry
from ribbons import ReadRibbon, WriteRibbon


class Style:
   BOLD = '\033[1m'
   END = '\033[0m'

class Logger:
    def __init__(self) -> None:
        pass
    
    def log_instruction(self, instruction) -> None:
        print("{}[Instruction] {}{}".format(Style.BOLD, instruction, Style.END))

    def log_instruction_info(self, instr_info) -> None:
        print(">> {}".format(instr_info))

class Machine:
    def __init__(self, program: Program, read_ribbon: ReadRibbon) -> None:
        self._registry = Registry()
        self._write_ribbon = WriteRibbon()
        self._location_registry = LocationRegistry()
        self._log = Logger()
        self._program = program
        self._read_ribbon = read_ribbon
        self._value = None
        self._current_instr = None
        self._line_idx = 0
        self._reg_zero = 0
        self.is_running = True
        

    # public methods
    def fetch_and_decode(self):
        self._line_idx = self._location_registry.get_line_counter()
        self._current_instr = self._program.get_instruction_at(self._line_idx)
        
    def execute(self):
        # execute
        self._reg_zero = int(self._registry.read_reg_num(0))
        try:
            self._get_value(self._current_instr[1])
        except:
            self.is_running = False

        opcode = self._current_instr[0]

        # log
        self._log.log_instruction("{} (line {})".format(opcode, self._line_idx))

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
            raise Exception(
                "Error: operand at {} has a bad form".format(self._location_registry)
            )
        self._value = value 

    def _load(self):
        self._registry.write_reg_num(0, self._value)
        self._location_registry.goto_next()
        self._log.log_instruction_info("Write {} to R0".format(self._value))

    def _store(self):
        self._registry.write_reg_num(self._value, self._reg_zero)
        self._location_registry.goto_next()
        self._log.log_instruction_info(
            "Store the content of R0 ({}) in R{}".format(self._reg_zero, self._value)
        )

    def _add(self):
        sum = self._reg_zero + self._value
        self._registry.write_reg_num(0, sum)
        self._location_registry.goto_next()
        self._log.log_instruction_info(
            "Sum: {} + {} = {}".format(self._reg_zero, self._value, sum)
        )

    def _sub(self):
        diff = self._reg_zero - self._value
        self._registry.write_reg_num(0, diff)
        self._location_registry.goto_next()
        self._log.log_instruction_info(
            "Sub: {} - {} = {}".format(self._reg_zero, self._value, diff)
        )

    def _mult(self):
        mult = self._reg_zero * self._value
        self._registry.write_reg_num(0, mult)
        self._location_registry.goto_next()
        self._log.log_instruction_info(
            "Mult: {} * {} = {}".format(self._reg_zero, self._value, mult)
        )

    def _div(self):
        if self._value == 0:
            raise ArithmeticError("Division by zero")
        div = self._reg_zero / self._value
        self._registry.write_reg_num(0, div)
        self._location_registry.goto_next()
        self._log.log_instruction_info(
            "Div: {} / {} = {}".format(self._reg_zero, self._value, div)
        )

    def _read(self):
        read_value = self._read_ribbon.read()
        self._read_ribbon.advance_position()
        self._registry.write_reg_num(self._value, read_value)
        self._location_registry.goto_next()
        self._log.log_instruction_info("Read input: {}".format(read_value))

    def _write(self):
        self._write_ribbon.write(self._value)
        self._write_ribbon.advance_position()
        self._location_registry.goto_next()
        self._log.log_instruction_info("Write on output: {}".format(self._value))

    def _jump(self):
        self._location_registry.goto(self._value)
        self._log.log_instruction_info("Jump to line: {}".format(self._value))

    def _jgtz(self):
        if self._reg_zero > 0:
            self._location_registry.goto(self._value)
            self._log.log_instruction_info("Jump to: {}".format(self._value))
        else:
            self._location_registry.goto_next()
            self._log.log_instruction_info("Jump to next")

    def _jzero(self):
        if self._reg_zero == 0:
            self._location_registry.goto(self._value)
            self._log.log_instruction_info("Jump to: {}".format(self._value))    
        else:
            self._location_registry.goto_next()
            self._log.log_instruction_info("Jump to next")

    def _jblank(self):
        if self._read_ribbon.read() == " ":
            self._location_registry.goto(self._value)
            self._log.log_instruction_info("Jump to: {}".format(self._value))
        else:
            self._location_registry.goto_next()
            self._log.log_instruction_info("Jump to next")

    def _halt(self):
        self.is_running = False
        self._log.log_instruction_info("Halt!")

