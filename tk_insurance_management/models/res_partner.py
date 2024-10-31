# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string="Customer")
    is_agent = fields.Boolean(string="Agent")

    insurance_information_ids = fields.One2many(
        'insurance.information', 'agent_id', string="Insurance")
    agent_total_commission = fields.Monetary(
        string="Total Commission", compute="_total_agent_commission", store=True)

    @api.depends('insurance_information_ids')
    def _total_agent_commission(self):
        for rec in self:
            agent_total_commission = 0.0
            if rec.insurance_information_ids:
                for commission in rec.insurance_information_ids:
                    agent_total_commission = agent_total_commission + commission.total_commission
                    rec.agent_total_commission = agent_total_commission
            else:
                rec.agent_total_commission = 0.0

    def action_agent_commission(self):
        return True
