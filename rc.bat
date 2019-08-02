rem Launcher for rc.py RPN Calculator
rem
rem Should work both in interactive and CLI modes; for interactive mode
rem a subshell is spawned so that it can also be used directly from the
rem Run dialog.
rem
rem Copy this file somewhere in your %PATH% and set the right path for
rem the rpn_calc folder below, and you will be able to use the
rem calculator by running 'rc [commands]' from the CLI. Running 'rc' in
rem the Run dialog will open the calculator in a new cmd window that
rem will close automatically when you exit the calculator.

@echo off

rem Set here the location of rpn_calc
pushd c:\temp\rpn_calc
if [%1] == [] goto interactive

:cli-mode
python rc.py %*
set RETURN_VAL = %ERRORLEVEL%
popd
exit /B %RETURN_VAL%

:interactive
cmd /c "python rc.py"
popd
