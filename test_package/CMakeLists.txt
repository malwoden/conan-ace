project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS})

if(WITH_SSL)
    target_compile_definitions(example PRIVATE WITH_SSL)
endif()
