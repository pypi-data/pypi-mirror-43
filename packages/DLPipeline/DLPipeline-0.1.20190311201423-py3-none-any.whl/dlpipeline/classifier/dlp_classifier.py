#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.utilities.dlp_base import DLPBase

__author__ = 'cnheider'


class DLPClassifier(DLPBase):

  def save(self, dataset, *, C):
    raise NotImplementedError

  def test(self, dataset, *, C):
    raise NotImplementedError
