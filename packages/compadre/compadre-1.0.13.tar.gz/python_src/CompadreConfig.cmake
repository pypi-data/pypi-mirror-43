set(Compadre_VERSION 1.0.1)
#The definition of this macro is really inconvenient prior to CMake
#commit ab358d6a859d8b7e257ed1e06ca000e097a32ef6
#we'll just copy the latest code into our Config.cmake file
macro(latest_find_dependency dep)
  if (NOT ${dep}_FOUND)
    set(cmake_fd_quiet_arg)
    if(${CMAKE_FIND_PACKAGE_NAME}_FIND_QUIETLY)
      set(cmake_fd_quiet_arg QUIET)
    endif()
    set(cmake_fd_required_arg)
    if(${CMAKE_FIND_PACKAGE_NAME}_FIND_REQUIRED)
      set(cmake_fd_required_arg REQUIRED)
    endif()

    get_property(cmake_fd_alreadyTransitive GLOBAL PROPERTY
      _CMAKE_${dep}_TRANSITIVE_DEPENDENCY
    )

    find_package(${dep} ${ARGN}
      ${cmake_fd_quiet_arg}
      ${cmake_fd_required_arg}
    )

    if(NOT DEFINED cmake_fd_alreadyTransitive OR cmake_fd_alreadyTransitive)
      set_property(GLOBAL PROPERTY _CMAKE_${dep}_TRANSITIVE_DEPENDENCY TRUE)
    endif()

    if (NOT ${dep}_FOUND)
      set(${CMAKE_FIND_PACKAGE_NAME}_NOT_FOUND_MESSAGE "${CMAKE_FIND_PACKAGE_NAME} could not be found because dependency ${dep} could not be found.")
      set(${CMAKE_FIND_PACKAGE_NAME}_FOUND False)
      return()
    endif()
    set(cmake_fd_required_arg)
    set(cmake_fd_quiet_arg)
    set(cmake_fd_exact_arg)
  endif()
endmacro(latest_find_dependency)

set(Compadre_EXPORTED_TARGETS "compadre;gmls_module")
foreach(tgt IN LISTS Compadre_EXPORTED_TARGETS)
  include(${CMAKE_CURRENT_LIST_DIR}/${tgt}-target.cmake)
endforeach()
set(Compadre_DEBUG "ON")
set(Compadre_USE_CUDA "OFF")
set(Compadre_USE_KokkosCore "ON")
set(Compadre_USE_LAPACK "ON")
set(Compadre_USE_OPENBLAS "ON")
set(Compadre_USE_MPI "OFF")
set(Compadre_USE_OpenMP "ON")
set(Compadre_USE_PYTHON "ON")
set(Compadre_USE_Trilinos "")
set(LAPACK_DECLARED_THREADSAFE "ON")
set(Compadre_VERSION_MAJOR "1")
set(Compadre_VERSION_MINOR "0")
set(Compadre_VERSION_PATCH "1")
set(Compadre_SEMVER "1.0.1-sha.137ed89+1011101101")
set(Compadre_COMMIT "137ed891deae1d0a0a3ae0929c38972dc7ed6ba1")
set(Compadre_CXX_FLAGS " -fopenmp ")
set(Compadre_CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX:BOOL=\"/usr/local\" -DPYTHON_CALLING_BUILD:BOOL=\"ON\" -DCompadre_USE_MPI:BOOL=\"OFF\" -DCompadre_USE_PYTHON:BOOL=\"ON\" -DCompadre_USE_MATLAB:BOOL=\"ON\" -DCompadre_EXAMPLES:BOOL=\"OFF\"")
set(GMLS_Module_DEST "lib/python/dist-packages")
set(Compadre_INSTALL_PREFIX "/usr/local")
