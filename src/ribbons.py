class Ribbon:
    """Ribbon implementation"""
    def __init__(self) -> None:
        self._position = 1

    # public methods
    def advance_position(self) -> None:
        self._position += 1
    
    def get_position(self) -> int:
        return self._position


class ReadRibbon(Ribbon):
    """An implementation of a readable ribbon"""
    def __init__(self, init_cond: str) -> None:
        super().__init__()
        self._init_cond = init_cond
        self._max_len = len(init_cond) - 1
    
    # public methods
    def read(self) -> str:
        pos = self.get_position()
        return self._init_cond[pos - 1]


class WriteRibbon(Ribbon):
    """An implementation of a ribbon on which you can write"""
    def __init__(self) -> None:
        super().__init__()
        self._result = ""

    # public methods
    def write(self, new_char: str) -> None:
        self._result += str(new_char)

    def get(self) -> str:
        return self._result