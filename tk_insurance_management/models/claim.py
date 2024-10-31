# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ClaimInformation(models.Model):
    """Claim Information"""
    _name = "claim.information"
    _description = __doc__
    _rec_name = 'claim_number'

    claim_number = fields.Char(
        string='Claim', required=True, readonly=True, default=lambda self: _('New'))
    insurance_id = fields.Many2one(
        'insurance.information', string="Insurance", required=True)
    insured_id = fields.Many2one(
        related='insurance_id.insured_id', string='Insured')
    dob = fields.Date(related='insurance_id.dob', string='Date of Birth')
    age = fields.Char(related='insurance_id.age', string='Age')
    phone = fields.Char(related="insured_id.phone")
    insurance_nominee_id = fields.Many2one(
        related="insurance_id.insurance_nominee_id", string="Nominee")
    your_nominee_is_your = fields.Selection(related="insurance_nominee_id.your_nominee_is_your",
                                            string="Your Nominee is Your")
    nominee_dob = fields.Date(
        related="insurance_nominee_id.nominee_dob", string=" Date of Birth")

    insurance_policy_id = fields.Many2one(
        related='insurance_id.insurance_policy_id', string='Insurance Policy')
    insurance_category_id = fields.Many2one(related='insurance_id.insurance_category_id', string="Policy Category",
                                            required=True)
    insurance_sub_category_id = fields.Many2one(
        related='insurance_id.insurance_sub_category_id', string="Sub Category")

    insurance_time_period = fields.Char(
        related="insurance_policy_id.insurance_time_period_id.t_period")
    agent_id = fields.Many2one(
        related='insurance_id.agent_id', string='Agent', readonly=True)
    policy_amount = fields.Monetary(
        related="insurance_id.total_policy_amount", string="Policy Amount")
    amount_paid = fields.Monetary(string="Amount Paid")
    company_id = fields.Many2one(related="insurance_id.company_id")
    currency_id = fields.Many2one(
        'res.currency', string='Currency', related="company_id.currency_id")
    claim_date = fields.Date(string='Date', required=True)
    policy_terms_and_conditions = fields.Text(string="Terms & Conditions")
    invoice_id = fields.Many2one('account.move', string="Claim Bill")
    payment_status = fields.Selection(
        related='invoice_id.payment_state', string="Payment Status")
    amount_residual = fields.Monetary(
        related='invoice_id.amount_residual', string="Claim Amount")
    maturity_of_the_policy = fields.Boolean(string="Maturity of the Policy")
    surrender_of_the_policy = fields.Boolean(string="Surrender of the Policy")
    discounted_value_in_policy = fields.Boolean(
        string="Discounted Value in Policy")
    death_of_the_insured = fields.Boolean(string="Death of the Insured")
    paid_up_of_lapsed_policy = fields.Boolean(
        string="Paid up of Lapsed Policy")
    other = fields.Boolean(string="Other")
    furnish_date_of_death = fields.Date(string="Date of Death")

    claim_documents_ids = fields.One2many(
        'claim.documents', 'claim_information_id', string="Claim Documents")

    state = fields.Selection(
        [('draft', "Draft"), ('submit', "Submit"),
         ('approved', "Approved"), ('not_approved', "Not Approved")],
        default='draft')

    def draft_to_submit(self):
        self.state = 'submit'

    def submit_to_approved(self):
        documents_verified = True
        for rec in self.claim_documents_ids:
            if not rec.state == 'verified':
                documents_verified = False
                break
        if not documents_verified:
            message = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'danger',
                    'title': ('Claim Documents'),
                    'message': "Please complete claim documents",
                    'sticky': True,
                }
            }
            return message
        else:
            self.state = 'approved'

    def approved_to_not_approved(self):
        self.state = 'not_approved'

    @api.model
    def create(self, vals):
        if vals.get('claim_number', 'New') == 'New':
            vals['claim_number'] = self.env['ir.sequence'].next_by_code(
                'claim.information') or 'New'
        return super(ClaimInformation, self).create(vals)

    def action_claim_settlement_amount(self):
        for record in self:
            if record.amount_paid == 0:
                raise ValidationError("Please claim amount can not be zero")
            else:
                claim_record = {
                    'name': 'Claim Settlement Amount',
                    'quantity': 1,
                    'price_unit': self.amount_paid,
                }
                invoice_lines = [(0, 0, claim_record)]
                data = {
                    'partner_id': self.agent_id.id,
                    'move_type': 'in_invoice',
                    'invoice_date': fields.Datetime.now(),
                    'invoice_line_ids': invoice_lines,
                }
                invoice_id = self.env['account.move'].sudo().create(data)
                invoice_id.action_post()
                self.invoice_id = invoice_id.id
