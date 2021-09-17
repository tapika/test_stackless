import cffi
ffibuilder = cffi.FFI()

with open('cffi_interop.h') as f:
    # read plugin.h and pass it to embedding_api(), manually
    # removing the '#' directives and the CFFI_DLLEXPORT
    data = ''.join([line for line in f if not line.startswith('#') and 'initCffiModule' not in line])
    data = data.replace('CFFI_DLLEXPORT', '')
    #print(data)
    ffibuilder.embedding_api(data)


ffibuilder.set_source("cffiplugin", r"""
CFFI_DLLEXPORT int initCffiModule() {
    return cffi_start_python();
}
"""
)

ffibuilder.embedding_init_code("""
from cffiplugin import ffi
import stackless

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

def bootstrap_py(path):
    print('-> bootstrap_py(', path , ')')
    execfile(path)
    print('<- bootstrap_py(', path , ')')

@ffi.def_extern()
def taskletCreate(path):
    pathstr = ffi.string(path)
    print('startTasklet for', pathstr)
    t = stackless.tasklet(bootstrap_py)
    #print(t)
    t.setup(pathstr)
    #print('stackless task ok', t._task_id)
    #print(stackless._squeue)
    return t._task_id

@ffi.def_extern()
def taskletRun(taskId):
    t = taskletObject(taskId)
    if t is not None:
        t.run()

def taskletObject(taskid):
    for t in stackless._squeue:
        if t._task_id == taskid:
            return t
    return None

@ffi.def_extern()
def taskletIsAlive(taskId):
    #print('taskletIsAlive -> ')
    
    t = taskletObject(taskId)
    if t is None:
        r = False
    else:
        r = t.is_alive

    #print('taskletIsAlive(', t, 'isAlive:', r, ')')
    #print('<- taskletIsAlive')
    return r

@ffi.def_extern()
def taskletKill(taskId):
    t = taskletObject(taskId)
    if t is not None:
        try:
            print('Killing task #', t._task_id)
            t.kill()
            print('Removing task #', t._task_id)
            t.remove()
        except Exception as e:
            print('Cannot remove task #', taskId, str(e))
    else:
        print('Cannot kill task #', taskId, ' - does not exists')
        

@ffi.def_extern()
def stackless_run():
    print('-> stackless.run()')
    #print('task queue:', stackless._squeue)
    stackless.run()
    print('<- stackless.run()')
""")

ffibuilder.emit_c_code("cffiplugin.c")

