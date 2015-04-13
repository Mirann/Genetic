
class Function(object):
    def __init__(self, function_name):
        self.function_name = function_name

    def execute(self, var1, var2):
        pass


class TwoVariableFunction(Function):
    def __init__(self, function_name):
        Function.__init__(self, function_name)

    def execute(self, var1, var2):
        self.function_name(var1, var2)


class OneVariableFunction(Function):
    def __init__(self, function_name):
        Function.__init__(self, function_name)

    def execute(self, var1, var2=None):
        self.function_name(var1)
