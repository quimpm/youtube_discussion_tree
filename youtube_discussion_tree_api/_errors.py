class Error(Exception):
    pass

class SearchBoundsExceded(Error):
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class NoEnglishTranscription(Error):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
