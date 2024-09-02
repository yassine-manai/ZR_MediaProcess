

class ValidationException(Exception):
    def __init__(self, message, status_code, field_name):
        self.message = message
        self.status_code = status_code
        self.field_name = field_name
        super().__init__(self.message)
        
    def __str__(self):
        return f'{self.status_code} - {self.field_name}: {self.message}'


class ConsumerValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
class CompanyValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
