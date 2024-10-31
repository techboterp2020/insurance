# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class InsuranceNominee(models.Model):
    """Insurance Nominee"""
    _name = 'insurance.nominee'
    _description = __doc__
    _rec_name = 'nominee_name'

    nominee_name = fields.Char(string="Nominee", required=True)
    your_nominee_is_your = fields.Selection(
        [('grand_daughter', "Grand Daughter"), ('grand_mother', "Grand Mother"), ('niece', "Niece"),
         ('sister', "Sister"), ('aunt', "Aunt"), ('daughter', "Daughter"), ('mother', "Mother")],
        string="Your Nominee is Your")
    nominee_dob = fields.Date(string="Date of Birth")
