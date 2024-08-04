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

# Find and link PostgreSQL libraries
find_package(PostgreSQL REQUIRED)
if(PostgreSQL_FOUND)
    include_directories(${PostgreSQL_INCLUDE_DIRS})
    target_link_libraries(courseCompass ${PostgreSQL_LIBRARIES})
else()
    message(FATAL_ERROR "PostgreSQL not found")
endif()

# Include libpqxx headers and link libpqxx library
include_directories($ENV{LIBPQXX_INCLUDE_DIR})

find_library(PQXX_LIB pqxx REQUIRED PATHS $ENV{LIBPQXX_LIB_DIR})
if(PQXX_LIB)
    target_link_libraries(courseCompass ${PQXX_LIB})
else()
    message(FATAL_ERROR "libpqxx not found")
endif()
