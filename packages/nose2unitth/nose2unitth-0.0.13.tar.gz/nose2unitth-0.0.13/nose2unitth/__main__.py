""" nose2unitth command line program

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2017-08-16
:Copyright: 2016, Karr Lab
:License: MIT
"""

from nose2unitth.core import Converter
import cement
import nose2unitth


class BaseController(cement.Controller):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        description = "Convert nose-style test reports into UnitTH-style test reports"
        arguments = [
            (['-v', '--version'], dict(action='version', version=nose2unitth.__version__)),
            (['in_file_nose'], dict(type=str, help='path to nose test report that should be converted')),
            (['out_dir_unitth'], dict(type=str, help='path where converted test report should be saved')),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs
        Converter.run(args.in_file_nose, args.out_dir_unitth)


class App(cement.App):
    """ Command line application """

    class Meta:
        label = 'nose2unitth'
        base_controller = 'base'
        handlers = [BaseController]


def main():
    with App() as app:
        app.run()
