class EmptyListAccessException(Exception):
    def __init__(self, message=None, cause=None):
        if cause:
            super().__init__(f"{message}: {cause}")
        elif message:
            super().__init__(message)
        else:
            super().__init__()
