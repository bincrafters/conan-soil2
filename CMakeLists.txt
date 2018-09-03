cmake_minimum_required(VERSION 2.8.11)

# Project Name and start working in project scope (some things just work until now, some just work after this command)
project(SOIL2)

# Add Conan dependencies (our C++ dependency manager)
# include(conanbuildinfo.cmake)
# conan_basic_setup()


# Error if paths aren't set well
get_filename_component(MAINDIR "${CMAKE_SOURCE_DIR}" REALPATH)  # Main inexor folder
get_filename_component(BINDIR "${CMAKE_BINARY_DIR}" REALPATH)   # Where it generates the projects into
if(${MAINDIR} STREQUAL ${BINDIR})
    message(FATAL_ERROR "Keep your directories clean, don't generate the project-files in the main directory! ${MAINDIR} ${BINDIR}")
endif()

set(sources "source_subfolder/src/SOIL2/etc1_utils.c"
            "source_subfolder/src/SOIL2/image_DXT.c"
            "source_subfolder/src/SOIL2/image_helper.c"
            "source_subfolder/src/SOIL2/SOIL2.c")
add_library(SOIL2 ${sources})
