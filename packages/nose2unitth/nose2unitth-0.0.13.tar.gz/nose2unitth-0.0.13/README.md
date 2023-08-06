[![PyPI package](https://img.shields.io/pypi/v/nose2unitth.svg)](https://pypi.python.org/pypi/nose2unitth)
[![Documentation](https://readthedocs.org/projects/nose2unitth/badge/?version=latest)](http://docs.karrlab.org/nose2unitth)
[![Test results](https://circleci.com/gh/KarrLab/nose2unitth.svg?style=shield)](https://circleci.com/gh/KarrLab/nose2unitth)
[![Test coverage](https://coveralls.io/repos/github/KarrLab/nose2unitth/badge.svg)](https://coveralls.io/github/KarrLab/nose2unitth)
[![Code analysis](https://api.codeclimate.com/v1/badges/e3ee777af72076166232/maintainability)](https://codeclimate.com/github/KarrLab/nose2unitth)
[![License](https://img.shields.io/github/license/KarrLab/nose2unitth.svg)](LICENSE)
![Analytics](https://ga-beacon.appspot.com/UA-86759801-1/nose2unitth/README.md?pixel)

# nose2unitth
Convert [nose](http://nose.readthedocs.io)-style XML test reports to [UnitTH](http://junitth.sourceforge.net/)-compatible XML reports

## Example
* [nose-style XML report](examples/nose.xml)
* [UnitTH-style XML report](examples/unitth/1)
* [UnitTH HTML test history report](https://cdn.rawgit.com/KarrLab/nose2unitth/master/examples/html/index.html)

## Installation
* Latest release from PyPI
  ```
  pip install nose2unitth
  ```

* Latest revision from GitHub
  ```
  pip install git+https://github.com/KarrLab/nose2unitth.git#egg=nose2unitth
  ```

## Usage
```
# convert nose-style reports to UnitTH-style reports
nosetests <package-to-test> --with-xunit --xunit-file=examples/nose.xml

mkdir -p examples/unitth
nose2unitth examples/nose.xml examples/unitth/1
nose2unitth examples/nose.xml examples/unitth/2

junit2html examples/nose.xml examples/unitth/1/index.html
junit2html examples/nose.xml examples/unitth/2/index.html

# generate HTML test report
java \
    -Dunitth.generate.exectimegraphs=true \
    -Dunitth.xml.report.filter= \
    -Dunitth.html.report.path=. \
    -Dunitth.report.dir=examples/html \
    -jar unitth.jar examples/unitth/*
```

## Documentation
Please see the documentation at [Read the Docs](http://docs.karrlab.org/nose2unitth).

## Tests
### Running the tests
`nose` can be used to run the tests:
```
nosetests tests \
  --with-xunit --xunit-file=test-report.xml \
  --with-coverage --cover-package=nose2unitth
```

Please note that additional packages are required for testing (see [tests/requirements.txt](tests/requirements.txt)).

## License
The example model is released under the [MIT license](LICENSE).

## Development team
`nose2unitth` was developed by [Jonathan Karr](http://www.karrlab.org) at the Icahn School of Medicine at Mount Sinai in New York, USA.

## Questions and comments
Please contact the [Jonathan Karr](http://www.karrlab.org) with any questions or comments.
