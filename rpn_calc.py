"""
Provides RPNCalculator, an extensible RPN calculator; and Operator, a class to
define new operators to extend the calculator.
"""


from collections import namedtuple
from operator import add, sub, mul


Operator = namedtuple('Operator', ['opcode', 'arity', 'function', 'description', 'plugin'])
Operator.__doc__ = """
    An operator to extend RPNCalculator.

    Operator('opcode', 'arity', 'function', 'description', 'plugin')

    *   opcode is the string that will be used as identifier for the
        operator.

    *   arity is the number of arguments used by the operator.

    *   function is the function implementing the operator; it should
        take a number of arguments equal to arity and return None for
        no results, a scalar for a single result value or a list for
        multiple result values. If an error occurs, it should return a
        string describing it.

    *   description is a string documenting the operator; it can be
        used by the calculators using this module to describe the
        available operators

    *   plugin is the name of the plugin that loads the operator; it is
        only an identifier to group operators for the unload_plugin
        functionality
"""


_std_operators = [
    Operator(opcode='+', arity=2, function=add, description='addition', plugin='std'),
    Operator(opcode='-', arity=2, function=sub, description='addition', plugin='std'),
    Operator(opcode='*', arity=2, function=mul, description='addition', plugin='std'),
    Operator(opcode='/', arity=2,
             function=lambda x, y: x/y if y != 0 else 'error: division by zero',
             description='division', plugin='std'),
    Operator(opcode='drop', arity=1, function=lambda x: None,
             description='pop and lose element on top level of stack', plugin='std'),
    Operator(opcode='swap', arity=2, function=lambda x,y: [y, x],
             description='swap the two topmost elements of stack', plugin='std'),
    Operator(opcode='dup', arity=1, function=lambda x: [x, x],
             description='duplicate topmost level of stack', plugin='std'),
]


class RPNCalculator:
    """
    Implements an RPN calculator.

    This provides the stack management and calculation engine with basic
    operators (+, -, *, /). Additional operators can be added afterwards
    through the add_operator or load_plugin method.
    """

    def __init__(self):
        self.stack = []
        self._operators = {op.opcode: op for op in _std_operators}
   
    @property
    def operators(self):
        """Return an iterator over the registered operators as Operator instances."""
        return self._operators.values()

    def add_operator(self, operator):
        """
        Allows to add a new operator or update (redefine) an existing one.

        Takes an operator argument, expected to be an instance of the
        rpn_calc.Operator class. If the opcode is already defined, this will
        overwrite it.
        """
        self._operators[operator.opcode] = operator

    def load_plugin(self, plugin_name):
        """
        Import operators from a plugin.

        A plugin file is a Python module from which an iterable of operators can
        be imported as <plugin>.operators; each operator should be a dictionary
        with the fields needed for an Operator instance (opcode, arity,
        function, description, and plugin). This method expects a file named
        plugin.py that can be imported directly.

        A plugin containing an operator with an opcode that clashes with one
        that is already loaded will override it.
        """
        exec(f'import {plugin_name} as plugin', globals())
        for operator in plugin.operators:
            op = Operator(**operator)
            self._operators[op.opcode] = op

    def unload_plugin(self, plugin):
        """Unload a plugin"""
        if plugin == 'std':
            return "Error: Standard plugin cannot be removed"
        plugin_ops = [opcode for opcode, op in self._operators.items() if op.plugin == plugin]
        for opcode in plugin_ops:
            self._operators.pop(opcode)

    def run_command(self, cmd):
        """
        Execute a command.
        
        None is returned for success, an error message (a string) otherwise; if
        an error happens, the state of the calculator does not change.
        """
        if isinstance(cmd, (int, float, complex)):
            self.stack.append(cmd)
            return None

        if cmd not in self._operators:
            return f"Operator '{cmd}' undefined"

        op = self._operators[cmd]
        if len(self.stack) < op.arity:
            return f"Not enough arguments for operator '{cmd}'"
        self.stack, args = self.stack[:-op.arity], self.stack[-op.arity:]
        res = op.function(*args)
        if res is None:
            pass
        elif isinstance(res, (int, float, complex)):
            self.stack.append(res)
        elif isinstance(res, list):
            self.stack.extend(res)
        else: # error string
            self.stack.extend(args)  # restore state before error
            return res  # pass on error message
        return None  # all happy paths end here

    def read_stack(self, n=None):
        """
        Get up to n elements from the stack, returned as a list.

        If n is None, the full stack is returned
        """
        return self.stack[-n:] if n is not None else self.stack[:]

    def clear_stack(self):
        """Remove all elements from the stack"""
        self.stack = []
