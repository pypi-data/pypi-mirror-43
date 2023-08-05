#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Copyright 2011 Marco Mina. All rights reserved.

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
'''
This module contains the classes for the evaluation of the Semantic Similarity.
Please refer to the single classes for details on the implemented measures.
'''

# __all__ = ["SemSimUtils", "ObjSemSim", "SemSimMeasures", "TermSemSim", "MixSemSim", "ObjSetSemSim"]

from .ObjSemSim import ObjSemSim
from .ObjSetSemSim import ObjSetSemSim
from .SetSemSim import SetSemSim
from .SemSimUtils import SemSimUtils

# from .ObjSemSim import *
# from .TermSemSim import *

from ._libs import *