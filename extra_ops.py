operators = (
    {'opcode': '**', 'arity': 2,'function': lambda x, y: x ** y, 'description': 'power', 'plugin': 'extra_ops'},
    {'opcode': '//', 'arity': 2, 'function': lambda x, y: x//y if y != 0 else 'error: division by zero', 'description': 'integer division', 'plugin': 'extra_ops'},
    {'opcode': 'mod', 'arity': 2, 'function': lambda x, y: x % y, 'description': 'modulo or remainder', 'plugin': 'extra_ops'},
    {'opcode': '%', 'arity': 2, 'function': lambda x, y: x * y / 100, 'description': 'percent', 'plugin': 'extra_ops'},
    {'opcode': 'neg', 'arity': 1, 'function': lambda x: -x, 'description': 'sign reversal', 'plugin': 'extra_ops'},
    {'opcode': 'inv', 'arity': 1, 'function': lambda x: 1/x if x != 0 else 'error: division by zero', 'description': 'inverse', 'plugin': 'extra_ops'}
)
