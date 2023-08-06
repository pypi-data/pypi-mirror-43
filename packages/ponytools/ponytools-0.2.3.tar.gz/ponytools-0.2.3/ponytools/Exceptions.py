class PonyToolsError(Exception):
    pass

class TriAllelicError(PonyToolsError):
    def __init__(self,expr,message=''):
        self.expr = expr
        self.message = message

class MissingChromosomeError(PonyToolsError):
    def __init__(self,expr,message=''):
        self.expr = expr
        self.message = message

class InfoKeyError(PonyToolsError):
    def __init__(self,expr,message=''):
        self.expr = expr
        self.message = message
