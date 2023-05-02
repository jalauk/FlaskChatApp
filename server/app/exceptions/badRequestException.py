class BadRequestException(Exception):
    def __init__(self,errors:str):
        Exception.__init__(self, errors)
        self.errors = errors    