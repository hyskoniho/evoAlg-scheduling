
import sys, io
function_buffer = io.StringIO()

def trace_calls(frame, event, arg, buffer=globals()['function_buffer']):
    if event == 'call':
        buffer.write('\n'*3)
        buffer.write(f'Calling function: {frame.f_code.co_name}\n')
    elif event == 'line':
        buffer.write(f'[L{frame.f_lineno}] {frame.f_locals}\n')
    elif event == 'return':
        buffer.write(f'Returning from function: {frame.f_code.co_name}\n')
    return trace_calls

def track_execution(func, *args, **kwargs):
    sys.settrace(trace_calls)
    func(*args, **kwargs)
    global function_buffer
    with open('trace_output.txt', 'w') as f:
        f.write(function_buffer.getvalue())
    function_buffer = io.StringIO()
    sys.settrace(None)

