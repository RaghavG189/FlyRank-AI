#Class for NotFoundError
class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


#Class for ValidationError
class ValidationError(Exception):
    def __init__(self, message):
        self.message = message