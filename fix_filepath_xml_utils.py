#!/usr/bin/env python3
"""This script contains all of the modules used in fix_filepath_xml.py"""

from raspberry_pi_libraries import multi_wrapper

class FixFilepathXML(multi_wrapper.Packages):
    """Class that adapts parent's modules for FixFilepathXML"""
    class InitBashArgs(multi_wrapper.Packages.InitBashArgs):
        """Initalizes the arguements present for bash execution which will be different for each
        application of this wrapper"""
        @classmethod
        def get_arg_params(cls):
            """Returns the argument paramters"""
            cls._parser.add_argument("--xml-dir", default=None, type=str,
                                     help="directory with xmls")
            cls._parser.add_argument("--images-dir", default=None, type=str,
                                     help="directory with images")

        @classmethod
        def get_args(cls):
            """Returns data inputted from bash"""
            if not cls._args.xml_dir:
                raise multi_wrapper.Packages.ArguementError(f"No input directory specified." \
                                                             + " Please specify '--xml-dir'" \
                                                             + "arguement")
            if not cls._args.images_dir:
                raise multi_wrapper.Packages.ArguementError(f"No input directory specified." \
                                                             + " Please specify '--images-dir'" \
                                                             + "arguement")
            return cls._args
