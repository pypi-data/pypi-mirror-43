# python-autologs
Auto generate logs for functions based on function docstring

Decorator to generate log info and log error for function.
The log contain the first line from the function docstring and resolve
names from function docstring by function args, any args that not
resolved from the docstring will be printed after.
In some cases only info or error log is needed, the decorator can be
called with @generate_logs(error=False) to get only log INFO and vice versa


Example:
@generate_logs()
def my_test(test, cases):
    '''
    Run test with cases
    '''
    return

my_test(test='my-test-name', cases=['case01', 'case02']
Will generate:
    INFO Run test my-test-name with cases case01, case02
    ERROR Failed to Run test my-test-name with cases case01, case02
    if step is True:
        Test Step   1: Run test my-test-name with cases case01, case02
