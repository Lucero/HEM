cmake_minimum_required(VERSION 3.8)

project(bme680)

aux_source_directory(. SRCs)

include_directories(.)

if (CMAKE_SYSTEM_NAME MATCHES "Linux")
	set(LIB_FILENAME Linux_x64)
	#set(LIB_FILENAME Linux_x86)
elseif (CMAKE_SYSTEM_NAME MATCHES "Windows")
	IF(CMAKE_CL_64)
		set(LIB_FILENAME win_x64)
	ELSE(CMAKE_CL_64)
		set(LIB_FILENAME win_x86)
	ENDIF(CMAKE_CL_64)
elseif (CMAKE_SYSTEM_NAME MATCHES "Darwin")
	set(LIB_FILENAME Macos)
else ()
	MESSAGE(STATUS "other platform: ${CMAKE_SYSTEM_NAME}")
endif (CMAKE_SYSTEM_NAME MATCHES "Linux")

MESSAGE(STATUS "lib path: ${PROJECT_SOURCE_DIR}/libs/${LIB_FILENAME}")
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/libs/${LIB_FILENAME}) #设置库文件的输出目录

#创建共享库
add_library(BME680 SHARED ${SRCs})
