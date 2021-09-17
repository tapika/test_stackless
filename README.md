# test_stackless

Test application for pypy's `stackless` features:

https://doc.pypy.org/en/latest/stackless.html

# Prerequisites (installed once)

1. Install choco using instructions from here: https://chocolatey.org/install
2. Run elevated command line prompt and run following commands:

* `choco feature disable -n=allowGlobalConfirmation`

=> Supresses yes prompt (https://stackoverflow.com/a/30428182/2338477)

3. Install pypy

* `choco install python.pypy`

=> Install pypy with python 2 extension

# Build

- Checkout this git into pypy's folder.

- From Visual studio (2019), select File > Open > CMake > select `CMakeLists.txt`

- From Solution Explorer, select switch between views, right click on `CMake Targets View`, Open.

- Right click on `pytest_runner`, Set as startup item.

- Compile project / debug

