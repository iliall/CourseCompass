cmake_minimum_required(VERSION 3.10)
project(CourseCompass)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the include directory
include_directories(include)

# Add the executable
add_executable(courseCompass src/main.cpp)

# Link necessary libraries (e.g., Boost, if used by Crow)
find_package(Boost REQUIRED)
if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
    target_link_libraries(courseCompass ${Boost_LIBRARIES})
endif()
