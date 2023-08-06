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
    -D CMAKE_INSTALL_PREFIX=../../python-compadre-install \
    -D Compadre_USE_Trilinos:BOOL=ON \
    -D Compadre_USE_LAPACK:BOOL=ON \
    -D Compadre_USE_PYTHON:BOOL=ON \
    -D Trilinos_PREFIX:FILEPATH="$MY_TRILINOS_PREFIX" \
    -D Numpy_PREFIX:FILEPATH="$MY_NUMPY_PREFIX" \
    \
    ..
