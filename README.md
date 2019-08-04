# RPN Calculator

An extensible Reverse Polish Notation (RPN) calculator for the command line.


## Usage

### Calculator Usage

An RPN calculator holds values in a stack, and applies operators by popping the required arguments and pushing the results. Therefore, the specification to add 2 and 2 is ``2 2 +``: the first 2 is pushed to the stack, then the other 2; the ``+`` operation pops both 2's, adds them to yield 4 as a result, and pushes the 4 to the stack. A subsequent ``1 +`` command would build on the existing stack, to give 5 as a result. All the operations are sequential, so ``2 2 + <enter>`` and ``2 <enter> 2 <enter> + <enter>`` are equivalent. Executing an operation that requires more arguments than are available in the stack results in an error.

This calculator shows a partial view of the stack, including the top elements (4 by default), and accepts commands consisting of numbers and operators. Numbers, expressed in any format that Python understands as a literal, are pushed to the stack, and operators executed.

There are several calculator commands available; one of them is ``help`` (or just ``h``), which shows all available commands. They are:

*   h, help: print this help message
*   ss, stacksize: change stack size (for visualization)
*   p, load: load a plugin file
*   dup: duplicate first level of the stack - empty command is an alias for dup
*   c, clear: clear stack
*   d: alias for drop - drop one value
*   l, list: list available operators and their opcodes
*   s: alias for swap - swap levels 1 and 2 of the stack
*   q, quit: exit

Some of these commands correspond to default operators, or are aliases for them. The default list of operators is:

*   \+ (2): addition [std]
*   \- (2): addition [std]
*   \* (2): addition [std]
*   / (2): division [std]
*   drop (1): pop and lose element on top level of stack [std]
*   swap (2): swap the two topmost elements of stack [std]
*   dup (1): duplicate topmost level of stack [std]
*   ** (2): power [extra_ops]
*   // (2): integer division [extra_ops]
*   mod (2): modulo or remainder [extra_ops]
*   % (2): percent [extra_ops]
*   neg (1): sign reversal [extra_ops]
*   inv (1): inverse [extra_ops]

The list is presented as in the calculator in the form: operator (arity): description [plugin]. Arity is the number of arguments that the operator takes, and plugin is the extension that loaded the operator. ``std`` (standard operations) and ``extra_ops`` are provided and loaded by default. ``std`` is built-in, and ``extra_ops`` is given in the form of a plug-in as an example. See below in extensions for more about plug-in use.

Commands can be supplied one by one, or several at a time, separated with spaces.


### Errors

Certain commands may cause an error: an undefined command, a division by zero, a command that requires more arguments than are available in the stack, etc. The calculator will report the error and pause, and then revert the stack to the previous state. The command causing the error, and any subsequent commands supplied, are lost.


### Extensions

The ``extra_ops`` module is an example of a plug-in. A plug-in just requires to export under the name ``operators`` a list of dictionaries, each describing an operator with the following fields:

*   ``opcode``: the command to use
*   ``arity``: the number of arguments taken by the operator
*   ``function``: the function that performs the calculation
*   ``description``: a short description of the operator to be shown in the operators listing
*   ``plugin``: the name of the plug-in the operator is associated to

The plug-in name supplied does not need to be the name of the plug-in module. Rather, this is a way of grouping related operators mainly for the purpose of removing the operators from the calculator.

The operator functions should return a scalar value for a single result, a sequence (such as a list) for multiple results, or in case of an error a string describing the error (it will be displayed to the user).

This allows the introduction of arbitrary code, and is not meant for casual use, especially with files from unknown sources. The mechanism is designed for developers to create their custom extensions.


## RPN Calculator Library

The description above refers to the calculator application. The calculator engine is provided as a library ``rpn_calc.py``, which can be used independently. The library defines the ``RPNCalculator`` class, which is the calculator engine proper, and an ``Operator`` class for defining new operations.

The calculator application ``rc.py`` is actually a user interface that relies on an ``RPNCalculator`` instance, and serves as an example for building applications on top of the library, such as a GUI-based calculator, or a calculator component inside a larger application.


## Interactive and CLI modes

When called without arguments, the calculator runs in interactive mode as described above.

CLI mode is activated by passing arguments when running the calculator. The arguments that are passed are interpreted as a sequence of commands, and the calculator performs the operations and prints out the final state of the stack, one item per line ordered bottom to top. This is intended to work in the UNIX style of composable programs or for quick calculations on the command line.

Some examples:

    $ python rc.py 3 3 +
    6.0
    $

    $ python rc.py 3 2 5 +
    3.0
    7.0
    $

    $ python rc.py 3 drop
    $

    $ python rc.py 3 +
    ***
    Not enough arguments for operator '+'
    ***

In this mode, errors are output to stderr, and nothing is written to stdout to avoid passing on an incoherent state of the stack.


## Why develop this calculator

I have used RPN calculators for years, especially the HP 48GX. After that, it is difficult for me to return to the more usual infix-notation calculators and forgo the flexibility of stack manipulation (as opposed e.g. to the use of parentheses or memory registers). For some time I used an emulator of the HP 48GX, but this was only developed for older versions of Windows, and had no Linux support at all.

As I could not find a good option for an RPN calculator that I could use, I decided to develop my own, and this is the result. It is of course loosely inspired in the working of the calculator I have used for a long time.
