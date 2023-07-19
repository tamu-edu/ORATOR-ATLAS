# cmake needs this line
cmake_minimum_required(VERSION 3.10)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_CXX_STANDARD 17)
# Define project name
project(atlas_project C CXX)



find_package(OpenCV  REQUIRED)
find_package(PkgConfig REQUIRED)

include_directories( ${OpenCV_INCLUDE_DIRS} )


link_libraries(jsoncpp ${OpenCV_LIBS})


add_executable(main main.cpp)

