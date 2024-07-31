# Instructions for developers

## Testing

### Test suite

The tests use the builtin `unittest` module and can be run like `./venv/bin/python -m unittest discover -s tests -v`

### Testing across versions

The development is usually done in the latest python version, which means that it could contain non-backwards compatible code.

You can use Docker to run the test in different versions of python by doing `docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.X-slim python -m unittest discover -s tests` by changin the `X` in the `python:3.X-slim` part of it to cover the version in question.

## Releasing

The releases are pushed to pypi using twine (`./venv/bin/pip install twine`). The config file is supposed to live in the `conf/` subdirectory (not part of the git repo)

### Build

A wheel build is expected for which the `wheel` package is required (`./venv/bin/pip install wheel`)

First the source distribution `./venv/bin/python setup.py sdist`

Then the wheel `./venv/bin/python setup.py bdist_wheel`

### pytest

Cleanup the dist folder, remove all the betas, rcs, etc. (everything there will end up in pypi)

To deploy into pytest:

`./venv/bin/python -m twine upload --config-file conf/pypirc.ini --repository testpypi dist/*`

### Production

Then the production version

`./venv/bin/python -m twine upload --config-file conf/pypirc.ini dist/*`
