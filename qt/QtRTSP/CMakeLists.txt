cmake_minimum_required(VERSION 3.5)

project(QtRTSP LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# QtCreator supports the following variables for Android, which are identical to qmake Android variables.
# Check http://doc.qt.io/qt-5/deployment-android.html for more information.
# They need to be set before the find_package(Qt5 ...) call.

#if(ANDROID)
#    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
#    if (ANDROID_ABI STREQUAL "armeabi-v7a")
#        set(ANDROID_EXTRA_LIBS
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libcrypto.so
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libssl.so)
#    endif()
#endif()

find_package(QT NAMES Qt6 Qt5 COMPONENTS Widgets REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Widgets REQUIRED)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ffmpeg REQUIRED IMPORTED_TARGET libavcodec libavformat libavutil libswscale)

#find_package(FFmpeg COMPONENTS AVCODEC AVFORMAT AVUTIL AVDEVICE REQUIRED)

include_directories(thirdparty/live555)
link_directories(thirdparty/live555/build)



add_executable(QtRTSP
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
    VideoDecoder.cpp
    VideoDecoder.hpp
    VideoGrabber.cpp
    VideoGrabber.hpp
    VideoImageWidget.cpp
    VideoImageWidget.hpp
)


target_link_libraries(QtRTSP PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
target_link_libraries(QtRTSP PRIVATE PkgConfig::ffmpeg)
target_link_libraries(QtRTSP PRIVATE liveMedia)
