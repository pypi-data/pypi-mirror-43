# Install script for directory: /Users/pakuber/Compadre/barebone_toolkit/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/Users/pakuber/Compadre/barebone_toolkit/python_src/src/libcompadre.dylib")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Users/pakuber/Compadre/barebone_toolkit/python_src/KokkosCore-install/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "@loader_path/"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -add_rpath "/Users/pakuber/Compadre/barebone_toolkit/python_src/KokkosCore-install/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -add_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -add_rpath "@loader_path/"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcompadre.dylib")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Compadre/compadre-target.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Compadre/compadre-target.cmake"
         "/Users/pakuber/Compadre/barebone_toolkit/python_src/src/CMakeFiles/Export/lib/cmake/Compadre/compadre-target.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Compadre/compadre-target-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Compadre/compadre-target.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Compadre" TYPE FILE FILES "/Users/pakuber/Compadre/barebone_toolkit/python_src/src/CMakeFiles/Export/lib/cmake/Compadre/compadre-target.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Compadre" TYPE FILE FILES "/Users/pakuber/Compadre/barebone_toolkit/python_src/src/CMakeFiles/Export/lib/cmake/Compadre/compadre-target-noconfig.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tpl" TYPE FILE FILES "/Users/pakuber/Compadre/barebone_toolkit/src/tpl/nanoflann.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "/Users/pakuber/Compadre/barebone_toolkit/python_src/src/Compadre_Config.h"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_GMLS.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_GMLS_ApplyTargetEvaluations.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_GMLS_Basis.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_GMLS_Quadrature.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_GMLS_Targets.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_LinearAlgebra_Declarations.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_LinearAlgebra_Definitions.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_Misc.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_Operators.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_PointCloudSearch.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_Typedefs.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/Compadre_Evaluator.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/USER_StandardTargetFunctionals.hpp"
    "/Users/pakuber/Compadre/barebone_toolkit/src/USER_ManifoldTargetFunctionals.hpp"
    )
endif()

