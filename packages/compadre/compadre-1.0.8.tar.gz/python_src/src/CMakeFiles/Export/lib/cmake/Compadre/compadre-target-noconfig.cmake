#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Compadre::compadre" for configuration ""
set_property(TARGET Compadre::compadre APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Compadre::compadre PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libcompadre.so"
  IMPORTED_SONAME_NOCONFIG "libcompadre.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS Compadre::compadre )
list(APPEND _IMPORT_CHECK_FILES_FOR_Compadre::compadre "${_IMPORT_PREFIX}/lib/libcompadre.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
