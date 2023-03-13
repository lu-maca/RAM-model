class LocationRegistry:
    """Location registry implementation"""
    def __init__(self) -> None:
        self._loc_counter = 1
        
    # public methods
    def get_line_counter(self) -> int:
        return self._loc_counter

    def goto(self, new_loc_counter: int) -> None:
        if new_loc_counter <= 0:
            raise Exception("Trying to reach a negative location counter")
        self._loc_counter = new_loc_counter

    def goto_next(self) -> None:
        self._loc_counter += 1


class Registry:
    """Registry implementation: max number is 32 by default"""
    def __init__(self, num: int = 32) -> None:
        self._num = num
        self._set_all()

    # private method
    def _set_all(self) -> None:
        initial_value = 0
        for rnum in range (0, self._num):
            registry_name = f"R{rnum}"
            setattr(self, registry_name, initial_value)

    # public methods
    def read_reg_num(self, num: int) -> int:
        if num >= self._num:
            raise Exception("Trying to access to not existing error")
        registry_name = f"R{num}"
        return getattr(self, registry_name)

    def write_reg_num(self, num: int, value: str) -> None:
        if num >= self._num:
            raise Exception("Trying to access to not existing error")
        registry_name = f"R{num}"
        setattr(self, registry_name, int(value))


class Program:
    """Program class"""
    def __init__(self) -> None:
        self._program = list()
    
    def _remove_comments(self, lines) -> list:
        # remove # comments
        new_lines = []
        for line in lines:
            new_line = line.lstrip()
            if new_line.startswith("#") or new_line == "":
                continue
            new_line = new_line.split("#")[0]
            new_lines.append(new_line)
        return new_lines

    # private methods
    def _unpack_operand(self, operand: str):
        if operand.startswith("="):
            return ("=", operand.replace("=",""))
        elif operand.startswith("*"):
            return ("*", operand.replace("*",""))
        else:
            return ("", operand)
    
    # public methods
    def load_full_program(self, file: str) -> None:
        """Parser of the program"""
        with open(file, "r") as f:
            lines = self._remove_comments(f.readlines())
        
        for line in lines:
            splitted_line = line.split(" ")

            try:
                operand = splitted_line[2].replace("\n", "")
            except:
                operand = ""

            instruction_dict = {
                "label": int(splitted_line[0]),
                "opcode": splitted_line[1],
                "operand": self._unpack_operand(operand)
            }
            self._program.append(instruction_dict)
    
    def get_instruction_at(self, label: int) -> tuple:
        if label > len(self._program):
            raise Exception("Not existing label")
        line = self._program[label - 1]
        return (line["opcode"], line["operand"])