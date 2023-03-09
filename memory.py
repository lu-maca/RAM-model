class LocationRegistry:
    """Location registry implementation"""
    def __init__(self) -> None:
        self._loc_counter = 1
        
    # public methods
    def goto(self, new_loc_counter: int):
        if new_loc_counter <= 0:
            raise Exception("Trying to reach a negative location counter")
        self._loc_counter = new_loc_counter


class Registry:
    """Registry implementation: max number is 32 by default"""
    def __init__(self, num: int = 32) -> None:
        self._num = num

    # private method
    def _set_all(self) -> None:
        initial_value = 0
        for rnum in range (0, self._num):
            registry_name = f"R{rnum}"
            setattr(registry_name, initial_value)

    # public methods
    def read_reg_num(self, num: int) -> int:
        if num >= self._num:
            raise Exception("Trying to access to not existing error")
        registry_name = f"R{num}"
        return getattr(self, registry_name)


class Program:
    """Program class"""
    def __init__(self) -> None:
        self._program = list()

    # private methods
    def _unpack_operand(operand: str):
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
            lines = f.readlines()
        
        label = 0
        for line in lines:
            splitted_line = line.split(" ")
            
            instruction_dict = {
                "label": label,
                "opcode": splitted_line[0],
                "operand": self._unpack_operand(splitted_line[1])
            }
            label += 1
            self._program.append(instruction_dict)
    
    def get_instruction_at(self, label: int) -> tuple:
        if label > len(self._program):
            raise Exception("Not existing label")
        line = self._program[label]
        return (line["opcode"], line["operand"])