#
# MIT License
#
# Copyright (c) 2024 Stellacore Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

##
## -- CMake build system description
##

cmake_minimum_required(VERSION 3.13)

set(aProjName "pycallc")
set(aProjVersion "0.1.0") # Set this based on features, updates and patches
set(aProjLib "${aProjName}_clib")

project(
	${aProjName}
	VERSION ${aProjVersion}
	DESCRIPTION "pycallc - Example Python calling C/C++ code (with ctypes) "
	LANGUAGES CXX C
	)

include(CTest)
enable_testing()


message("### CMAKE_MAJOR_VERSION: " ${CMAKE_MAJOR_VERSION})
message("### CMAKE_MINOR_VERSION: " ${CMAKE_MINOR_VERSION})
message("### CMAKE_PATCH_VERSION: " ${CMAKE_PATCH_VERSION})
message("### CMAKE_TWEAK_VERSION: " ${CMAKE_TWEAK_VERSION})
message("### PROJECT: " ${PROJECT})
message("### PROJECT_VERSION: " ${PROJECT_VERSION})


set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ===
# === Environment specific flags
# ===

set(BUILD_FLAGS_FOR_CLANG
	""
	)
set(BUILD_FLAGS_FOR_GCC
	#
	-pthread
	-fomit-frame-pointer
	#
	-Wall
	-Wextra
	-Wuninitialized
	-Winit-self
	-pedantic-errors
	#
	-fPIC  ## Important for python callable library creation
	)
set(BUILD_FLAGS_FOR_VISUAL
	""
	)

# ===
# === Library
# ===

# Note library must be SHARED to be called by python
# Could use default cmake settings, such as
# option(BUILD_SHARED_LIBS "Build using shared libraries [off]" OFF)
# but, more clear to create explicit SHARED lib. ref the add_library()
# function in src/CMakeLists.txt file.
add_subdirectory(src)

# ===
# === Tests
# ===

add_subdirectory(test)

