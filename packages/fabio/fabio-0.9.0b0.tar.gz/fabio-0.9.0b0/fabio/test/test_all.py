#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Fable Input Output
#             https://github.com/silx-kit/fabio
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Test suite for all fabio modules."""
from __future__ import print_function, with_statement, division, absolute_import

import sys
import logging
import unittest

logger = logging.getLogger(__name__)

from . import testfabioimage
from . import testedfimage
from . import testcbfimage
from . import testfilenames
from . import test_file_series
from . import test_filename_steps
from . import testadscimage
from . import testfit2dmaskimage
from . import testGEimage
from . import testheadernotsingleton
from . import testmar345image
from . import testbrukerimage
from . import testbruker100image
from . import testmccdimage
from . import testopenheader
from . import testopenimage
from . import testOXDimage
from . import testkcdimage
from . import testtifimage
from . import testXSDimage
from . import testraxisimage
from . import testpnmimage
from . import test_flat_binary
from . import testnumpyimage
from . import testcompression
from . import testpilatusimage
from . import test_nexus
from . import testeigerimage
from . import testhdf5image
from . import testfit2dimage
from . import testspeimage
from . import testfabioconvert
from . import testjpegimage
from . import testjpeg2kimage
from . import testmpaimage
from . import testdm3image
from . import test_failing_files
from . import test_formats
from . import test_image_convert
from . import testmrcimage
from . import test_pixi_image
from . import test_tiffio
from . import test_frames
from . import test_fabio


def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(testfabioimage.suite())
    testSuite.addTest(testedfimage.suite())
    testSuite.addTest(testcbfimage.suite())
    testSuite.addTest(testfilenames.suite())
    testSuite.addTest(test_file_series.suite())
    testSuite.addTest(test_filename_steps.suite())
    testSuite.addTest(testadscimage.suite())
    testSuite.addTest(testfit2dmaskimage.suite())
    testSuite.addTest(testGEimage.suite())
    testSuite.addTest(testheadernotsingleton.suite())
    testSuite.addTest(testmar345image.suite())
    testSuite.addTest(testbrukerimage.suite())
    testSuite.addTest(testbruker100image.suite())
    testSuite.addTest(testmccdimage.suite())
    testSuite.addTest(testopenheader.suite())
    testSuite.addTest(testopenimage.suite())
    testSuite.addTest(testOXDimage.suite())
    testSuite.addTest(testkcdimage.suite())
    testSuite.addTest(testtifimage.suite())
    testSuite.addTest(testXSDimage.suite())
    testSuite.addTest(testraxisimage.suite())
    testSuite.addTest(testpnmimage.suite())
    testSuite.addTest(test_flat_binary.suite())
    testSuite.addTest(testnumpyimage.suite())
    testSuite.addTest(testcompression.suite())
    testSuite.addTest(testpilatusimage.suite())
    testSuite.addTest(test_nexus.suite())
    testSuite.addTest(testeigerimage.suite())
    testSuite.addTest(testhdf5image.suite())
    testSuite.addTest(testfit2dimage.suite())
    testSuite.addTest(testspeimage.suite())
    testSuite.addTest(testfabioconvert.suite())
    testSuite.addTest(testjpegimage.suite())
    testSuite.addTest(testjpeg2kimage.suite())
    testSuite.addTest(testmpaimage.suite())
    testSuite.addTest(testdm3image.suite())
    testSuite.addTest(test_failing_files.suite())
    testSuite.addTest(test_formats.suite())
    testSuite.addTest(test_image_convert.suite())
    testSuite.addTest(testmrcimage.suite())
    testSuite.addTest(test_pixi_image.suite())
    testSuite.addTest(test_tiffio.suite())
    testSuite.addTest(test_frames.suite())
    testSuite.addTest(test_fabio.suite())
    return testSuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    if not runner.run(suite()).wasSuccessful():
        sys.exit(1)
