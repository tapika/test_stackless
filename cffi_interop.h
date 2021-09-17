#ifndef CFFI_DLLEXPORT
#define CFFI_DLLEXPORT extern "C" __declspec(dllimport)
#endif

CFFI_DLLEXPORT int initCffiModule();
CFFI_DLLEXPORT void stackless_run();
CFFI_DLLEXPORT int taskletCreate(const wchar_t* pyfile);
CFFI_DLLEXPORT void taskletRun(int task);
CFFI_DLLEXPORT bool taskletIsAlive(int task);
CFFI_DLLEXPORT void taskletKill(int task);

