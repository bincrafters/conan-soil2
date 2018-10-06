cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

# Error if paths aren't set well
get_filename_component(MAINDIR "${CMAKE_SOURCE_DIR}" REALPATH)  # Main folder
get_filename_component(BINDIR "${CMAKE_BINARY_DIR}" REALPATH)   # Where it generates the projects into

set(sources "source_subfolder/src/SOIL2/etc1_utils.c"
            "source_subfolder/src/SOIL2/image_DXT.c"
            "source_subfolder/src/SOIL2/image_helper.c"
            "source_subfolder/src/SOIL2/SOIL2.c")
add_library(SOIL2 ${sources})
