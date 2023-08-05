#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

'''
This module contains ontologies and annotation corpora embedded in fastsemsim,
and the code for keeping track, browsing and load the desired datasets.
The file data/dataset.txt contains the list of ontologies and annotation corpora currently embedded in the fastsemsim package.
Dataset handling and API functions are entirely included in the Dataset class.
'''

__all__ = ['Dataset']


from .Dataset import *
dataset = Dataset()
