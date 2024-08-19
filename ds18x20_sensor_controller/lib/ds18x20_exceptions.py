class Ds18x20Error(BaseException):
    def __init__(self, message):
        super().__init__(f"Failed to read sensor: {message}")
