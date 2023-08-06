python setup.py bdist_wheel sdist && rm -rf build/ && rm -rf python_src/CMakeFiles && rm -rf python_src/CMakeCache.txt && cd dist && tar -xzvf compadre-1.0.17.tar.gz && cd compadre-1.0.17 && cp PKG-INFO ../.. && cp setup.cfg ../.. && cd ../.. && rm -rf dist && tar -czvf compadre-1.0.17.tar.gz *

mkdir dist && mv compadre-1.0.17.tar.gz dist && python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose


python -m pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade compadre

