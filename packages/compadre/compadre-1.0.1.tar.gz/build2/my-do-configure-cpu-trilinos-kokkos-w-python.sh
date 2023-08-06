#!/bin/bash
# 
#
# Script for invoking CMake using the CMakeLists.txt file in this directory. 

# following lines for build directory cleanup
find . ! -name '*.sh' -type f -exec rm -f {} +
find . -mindepth 1 -type d -exec rm -rf {} +

MY_TRILINOS_PREFIX="/Users/pakuber/Compadre/trilinos/openmp/install/"
MY_NUMPY_PREFIX="/System/Library/Frameworks/Python.framework/Versions//2.7/Extras/lib/python/numpy/core/include/"

cmake \
    -D CMAKE_CXX_COMPILER=mpic++ \
    -D CMAKE_INSTALL_PREFIX=../../canga-install \
    -D Compadre_USE_LAPACK:BOOL=ON \
    -D Compadre_USE_PYTHON:BOOL=ON \
    -D Compadre_USE_MATLAB:BOOL=ON \
    -D Numpy_PREFIX:FILEPATH="$MY_NUMPY_PREFIX" \
    -D LAPACK_DECLARED_THREADSAFE=ON \
    -D Trilinos_PREFIX:FILEPATH="$MY_TRILINOS_PREFIX" \
    \
    ..
    #-D KokkosCore_ARCH:STRING="SNB" \
    #-D Compadre_USE_Pthread:BOOL=ON \
    #-D Compadre_USE_OpenMP:BOOL=OFF \
