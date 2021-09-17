cmake_minimum_required(VERSION 3.19)

set(Python_DIR "${CMAKE_CURRENT_SOURCE_DIR}/..")
# or change directory to pypy install folder as following:
#set(Python_DIR "C:/...absolute path.../pypy")

#set(PythonMajorVer 7)
set(PythonMajorVer 8)

set(Python_EXECUTABLE "${Python_DIR}/pypy3.exe")
set(Python_LIBRARIES "${Python_DIR}/libs/python3${PythonMajorVer}.lib")
set(Python_INCLUDE_DIRS "${Python_DIR}/include")

string(REPLACE "/" "\\\\" PythonDir "${Python_DIR}")
string(REPLACE "/" "\\\\" SourceDir "${CMAKE_CURRENT_SOURCE_DIR}")

file(WRITE ${CMAKE_CURRENT_SOURCE_DIR}/appPaths.cpp 
    "char* pythonPath = \"${PythonDir}\";\n"
    "char* sourcePath = \"${SourceDir}\";\n"
)

project(test_python)

add_library(cffiplugin SHARED 
    ${CMAKE_CURRENT_SOURCE_DIR}/cffiplugin.c
    cffi_interop.h
    cffiplugin.py
)
target_include_directories(cffiplugin PRIVATE ${Python_INCLUDE_DIRS})
target_link_libraries(cffiplugin PRIVATE ${Python_LIBRARIES})

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/cffiplugin.c
    COMMAND pypy
    ARGS cffiplugin.py
    DEPENDS cffiplugin.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "pypy cffiplugin.py => Generating ${file}..."
    VERBATIM
)

add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
add_compile_definitions(pytest_runner Py_NO_ENABLE_SHARED)
add_executable(
   pytest_runner
   ${CMAKE_CURRENT_SOURCE_DIR}/appPaths.cpp
   pypytest_runner.cpp
   test1.py
   test2.py
)

target_include_directories(pytest_runner PRIVATE ${Python_INCLUDE_DIRS})
target_link_libraries(pytest_runner PRIVATE ${Python_LIBRARIES})
target_link_libraries(pytest_runner PRIVATE cffiplugin)
# delay load specific dll
target_link_libraries(pytest_runner PRIVATE delayimp.lib)

target_compile_features(pytest_runner PRIVATE cxx_std_17)

add_custom_command(TARGET pytest_runner POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${Python_DIR}/libpypy3-c.dll"
        "${Python_DIR}/libffi-7.dll"
        $<TARGET_FILE_DIR:pytest_runner>)    

# delay load specific dll
set_target_properties(pytest_runner PROPERTIES LINK_FLAGS "/DELAYLOAD:cffiplugin.dll")

