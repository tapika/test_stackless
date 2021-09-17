#include <stdlib.h>
#include <filesystem>
#include <PyPy.h>
#include "python.h"
#include "cffi_interop.h"

using namespace std;
using namespace std::filesystem;

void runTaskUntilFinishes(int taskId, char* name)
{
    while (taskletIsAlive(taskId))
    {
        printf("* run %s\n", name);
        taskletRun(taskId);
    }

    printf("* task %s finished\n", name);
}

extern char* pythonPath;
extern char* sourcePath;

int main(int argc, char **argv) {

    // 1.
    rpython_startup_code();
    pypy_init_threads();

    int r;

    // 2.
    r = initCffiModule();
    if (r == -1)
    {
        PyErr_Print();
        return 0;
    }
    // 3.
    //pypy_setup_home(pythonPath, 1);
    
    path p = sourcePath;
    
    for (int loops = 0; loops < 100; loops++)
    {
        wstring s;
        s = (p / "test1.py").wstring();
        int t1 = taskletCreate(s.c_str());

        s = (p / "test2.py").wstring();
        int t2 = taskletCreate(s.c_str());

        //taskletKill(1);
        // Run all tasks simultaneously.
        //stackless_run();

        // Run only one task at the time
        runTaskUntilFinishes(t2, "task2");
        runTaskUntilFinishes(t1, "task1");

        taskletKill(t1);
        taskletKill(t2);
    }

    printf("end of app");
    return 0;
}

