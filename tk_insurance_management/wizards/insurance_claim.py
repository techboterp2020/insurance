# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, api, models, _


class InsuranceClaim(models.TransientModel):
    _name = 'insurance.claim'
    _description = "Insurance Claim"

    insurance_id = fields.Many2one(
        'insurance.information', string="Insurance", required=True)
    insured_id = fields.Many2one(
        related='insurance_id.insured_id', string='Insured')
    claim_date = fields.Date(string='Date')

    def insurance_claim_create(self):
        data = {
            'insurance_id': self.insurance_id.id,
            'claim_date': self.claim_date,
        }
        claim = self.env['claim.information'].create(data)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Claim',
            'res_model': 'claim.information',
            'res_id': self.insurance_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
