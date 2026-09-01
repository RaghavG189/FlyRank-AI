#Class for NotFoundError - if content not found
class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


#Class for ValidationError - if content is not in right format or null
class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


#Class for InvalidCredentials - if supabase rejected user login information
class InvalidCredentials(Exception):
    def __init__(self, message):
        self.message = message

#Class for LLMQuarantineError - if LLM response fails to be validated
class LLMQuarantineError(Exception):
    def __init__(self, message):
        self.message = message

#Class for LLMDisabled - if .env variable - LLMDisabled is set to FALSE
class LLMDisabled(Exception):
    def __init__(self, message):
        self.message = message