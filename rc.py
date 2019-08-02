"""
An extensible RPN calculator for the command line.
"""

import os
import sys

import rpn_calc


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input('Press <Enter> to continue . . .')


def show_error(e, interactive):
    """
    Print an error message to stderr.

    show_error(e)

    Print the error message 'e' framed by '***' above and below to stderr.
    In interactive mode only (interactive == True), pauses after printing.
    """
    print('***', file=sys.stderr)
    print(e, file=sys.stderr)
    print('***', file=sys.stderr)
    if interactive:
        pause()


def show_operators(c):
    print("Available Operators\nopcode (arity): description\n")
    for op in c.operators:
        print(f'{op.opcode} ({op.arity}): {op.description} [{op.plugin}]')
    print()
    pause()


def print_help(c):
    print('Available commands:')
    for cmd, cmd_data in ui_commands.items():
        print(f'{cmd}: {cmd_data["description"]}')
    print()
    print('---')
    print('Aliases:')
    for alias, command in aliases.items():
        print(f'{alias} -> {command}')
    print("The empty command is an alias for 'dup'")
    print()
    print('---')
    show_operators(c)  # Operators must be last as it includes a pause() at the end


def get_new_stack_size(old_stack_size):
    stack_size = input('Enter new stack size: ')
    try:
        new_stack_size = int(stack_size)
    except:
        return old_stack_size
    return new_stack_size



def clear_stack(calculator):
    calculator.clear_stack()


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


def load_plugin(c):
    plugin = input('Enter plugin name: ')
    c.load_plugin(plugin)


def unload_plugin(c):
    plugin = input('Enter plugin name: ')
    c.unload_plugin(plugin)


def quit(c=None):
    exit(0)


aliases = {
    'd': 'drop',
    's': 'swap',
    'c': 'clear',
    'l': 'list',
    'h': 'help',
    'p': 'load',
    'u': 'unload',
    'q': 'quit',
    'ss': 'stacksize',
}

ui_commands = {
    'clear': {'description': 'Clear the stack', 'function': clear_stack},
    'list': {'description': 'List the available operators', 'function': show_operators},
    'help': {'description': 'Show this help message', 'function': print_help},
    'load': {'description': 'Load a plug-in', 'function': load_plugin},
    'unload': {'description': 'Unload a plug-in', 'function': unload_plugin},
    'quit': {'description': 'Exit the program', 'function': quit},
    # stacksize operates on a local variable, so it is intercepted as a special case in interactive
    # or ignored in CLI mode; therefore, it doesn't use the dispatching mechanism and has no
    # associated function; still, it is present for the 'help' command
    'stacksize': {'description': 'Define a new stack size', 'function': None},
}


def convert(txt):
    """
    Convert numeric elements to float or complex if possible.

    success, value = convert(txt)

    If txt can be converted into a number, return success = True and the
    converted value in value. Otherwise return success = False, and value
    contains the input argument.
    """
    try:
        res = float(txt)
        return True, res
    except:
        pass
    try:
        res = complex(txt)
        return True, res
    except:
        return False, txt


def parse(commands, calculator, interactive=True):
    if not commands:  # Empty command is alias for 'dup'
        yield 'dup'
        return

    for command in commands:
        if command in aliases:
            yield aliases[command]
        elif command in ui_commands:
            if interactive:
                yield command
        elif command in calculator._operators:
            yield command
        else:
            success, number = convert(command)
            if success:
                yield number
                continue
            show_error(f"Unknown command '{command}'", interactive)
            break


def run_command(cmd, calculator, interactive):
    if cmd in ui_commands:
        if interactive:  # ignore UI commands in non-interactive mode
            ui_commands[cmd]['function'](calculator)
        return None
    e = calculator.run_command(cmd)
    if e is not None:
        show_error(e, interactive)
        return e
    return None



def main_interactive(c):
    stack = []
    stack_size = 4

    while True:
        update_stack(stack)
        cmds = parse(input().strip().split(), calculator=c)
        for cmd in cmds:
            if cmd == 'stacksize':  # Special case: changes a local variable
                stack_size = get_new_stack_size(old_stack_size=stack_size)
                e = None
                continue
            e = run_command(cmd, calculator=c, interactive=True)
            if e is not None:
                break
        stack = c.read_stack(stack_size)


def main_cli(c, cli_cmds):
    cmds = parse(cli_cmds, calculator=c, interactive=False)
    for cmd in cmds:
        e = run_command(cmd, calculator=c, interactive=False)
        if e is not None:
            break

    if e is None:
        status_code = 0
        for n in c.read_stack():
            print(n)
    else:
        status_code = 1
    exit(status_code)


def main():
    c = rpn_calc.RPNCalculator()
    c.load_plugin('extra_ops')

    if len(sys.argv) == 1:
        main_interactive(c)
    else:
        main_cli(c, cli_cmds=sys.argv[1:])        


if __name__ == '__main__':
    main()
