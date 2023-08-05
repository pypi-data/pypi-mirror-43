# -*- coding: iso-8859-1 -*-

# Copyright 2011-2013 Marco Mina. All rights reserved.

# This file is part of fastSemSim

# fastSemSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# fastSemSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with fastSemSim.  If not, see <http://www.gnu.org/licenses/>.

# @mail marco.mina.85@gmail.com
# @version 2.0
# @desc Parser module: load/store ontologies


"""
Set of functions to parse and handle ontologies.
"""

from __future__ import print_function


try:
	unicode
except (NameError, AttributeError):
	unicode = str #For python3

from .AnnotationCorpus import AnnotationCorpus
from .AnnotationCorpus import AnnotationCorpusFormat

# import sys
# import os
# import copy
# import pandas
# import types
# from xml.sax import make_parser
# from xml.sax.handler import ContentHandler
# import gzip

# from fastsemsim import data
# INT_DEBUG = True # remove?

def load_ac(ontology, source_file, file_type, params={}):
	ac = AnnotationCorpus(ontology)
	ac.load(source_file, file_type, params)
	return(ac)
#


# load embedded dataset
# builtin_dataset = data.dataset
