#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Experiments Tests for Prismic library"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import json
import prismic
import unittest
from prismic.experiments import Experiments

experiments_json = """
{
    "draft": [
        {
            "id": "xxxxxxxxxxoGelsX",
            "name": "Exp 2",
            "variations": [
                {
                    "id": "VDUBBawGAKoGelsZ",
                    "label": "Base",
                    "ref": "VDUBBawGALAGelsa"
                },
                {
                    "id": "VDUE-awGALAGemME",
                    "label": "var 1",
                    "ref": "VDUUmHIKAZQKk9uq"
                }
            ]
        }
    ],
    "running": [
        {
            "googleId": "_UQtin7EQAOH5M34RQq6Dg",
            "id": "VDUBBawGAKoGelsX",
            "name": "Exp 1",
            "variations": [
                {
                    "id": "VDUBBawGAKoGelsZ",
                    "label": "Base",
                    "ref": "VDUBBawGALAGelsa"
                },
                {
                    "id": "VDUE-awGALAGemME",
                    "label": "var 1",
                    "ref": "VDUUmHIKAZQKk9uq"
                }
            ]
        }
    ]
}"""


class ExperimentsTestCase(unittest.TestCase):

    def setUp(self):
        self.experiments = Experiments.parse(json.loads(experiments_json))

    def test_parsing(self):
        first = self.experiments.current()
        self.assertEqual(first.id, 'VDUBBawGAKoGelsX')
        self.assertEqual(first.google_id, '_UQtin7EQAOH5M34RQq6Dg')
        self.assertEqual(first.name, 'Exp 1')

    def test_cookie_parsing(self):
        self.assertIsNone(self.experiments.ref_from_cookie(''), 'Empty cookie')
        self.assertIsNone(self.experiments.ref_from_cookie('Ponies are awesome'), 'Invalid content')

        self.assertEqual('VDUBBawGALAGelsa',
                         self.experiments.ref_from_cookie('_UQtin7EQAOH5M34RQq6Dg%200'),
                         'Actual running variation')
        self.assertEqual('VDUUmHIKAZQKk9uq',
                         self.experiments.ref_from_cookie('_UQtin7EQAOH5M34RQq6Dg%201'),
                         'Actual running variation')

        self.assertIsNone(self.experiments.ref_from_cookie('_UQtin7EQAOH5M34RQq6Dg%209'), 'Index overflow')
        self.assertIsNone(self.experiments.ref_from_cookie('_UQtin7EQAOH5M34RQq6Dg%20-1'), 'Negative index overflow')
        self.assertIsNone(self.experiments.ref_from_cookie('NotAGoodLookingId%200'), 'Unknown Google ID')
        self.assertIsNone(self.experiments.ref_from_cookie('NotAGoodLookingId%201'), 'Unknown Google ID')
