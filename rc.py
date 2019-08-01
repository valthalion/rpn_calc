"""
An extensible RPN calculator for the command line.
"""

import os

import rpn_calc


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input('Press <Enter> to continue . . .')
    # os.system('pause')


def print_help():
    print("""Available commands:
    h, help: print this help message
    ss, stacksize: change stack size (for visualization)
      you will be prompted for the new size
    p, load: load a plugin file
    dup: duplicate top level of the stack - empty command is an alias for dup
    c, clear: clear stack
    d: alias for drop - drop one value
    l, list: list available operators and their opcodes
    s: alias for swap - swap levels 1 and 2 of the stack
    q, quit: exit
    """)


def update_stack(stack):
    clear_screen()
    print("STACK:")
    if not stack:
        print('Empty stack\n')
        return
    stacksize = len(stack)
    for value, position in zip(stack, range(stacksize, 0, -1)):
        print(f'{position}: {value}')
    print()


def main():
    c = rpn_calc.RPNCalculator()
    c.load_plugin('extra_ops')
    stack = []
    stack_size = 4

    while True:
        update_stack(stack)
        cmds = input().strip().split()
        if not cmds:  # Empty command is an alias for 'dup'
            cmds.append('dup')

        for cmd in cmds:
            # UI Commands
            if cmd == 'q' or cmd == 'quit':
                exit()
            if cmd == 'h' or cmd == 'help':
                print_help()
                pause()
                continue
            if cmd == 'p' or cmd == 'load': # TODO: Guard for non-existent plugin
                plugin = input('Enter plugin name: ')
                c.load_plugin(plugin)
                continue
            if cmd == 'u' or cmd == 'unload': # TODO: Guard for non-existent plugin
                plugin = input('Enter plugin name: ')
                c.unload_plugin(plugin)
                continue
            if cmd == 'c' or cmd == 'clear':
                c.clear_stack()
                stack = c.read_stack(stack_size)
                continue
            if cmd == 'l' or cmd == 'list':
                print("Available Operators\nopcode (arity): description\n")
                for op in c.operators:
                    print(f'{op.opcode} ({op.arity}): {op.description} [{op.plugin}]')
                print()
                pause()
                continue
            if cmd == 'ss' or cmd == 'stacksize':
                ss = input('Enter new stack size: ')
                try:
                    stack_size = int(ss)
                except:
                    pass
                continue
            # Calculator Commands
            elif cmd == 'd': # alias for 'drop'
                cmd = 'drop'
            elif cmd == 's': # alias for 'swap'
                cmd = 'swap'
            e = c.run_command(cmd)
            if e is not None:
                print("***\n{}\n***".format(e))
                pause()
                break
        stack = c.read_stack(stack_size)


if __name__ == '__main__':
    main()
