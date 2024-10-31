# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class InsuranceTimePeriod(models.Model):
    """Insurance Time Period"""
    _name = 'insurance.time.period'
    _description = __doc__
    _rec_name = 't_period'

    t_period = fields.Char(string="Policy Term", required=True)
    duration = fields.Integer(string="Duration (Months)")


class InsurancePolicy(models.Model):
    """Insurance Policy"""
    _name = 'insurance.policy'
    _description = __doc__
    _rec_name = 'policy_name'

    policy_name = fields.Char(string="Name", required=True)
    insurance_category_id = fields.Many2one(
        'insurance.category', string="Policy Category", required=True)
    category = fields.Selection(
        related="insurance_category_id.category", string='Category')
    insurance_sub_category_id = fields.Many2one('insurance.sub.category', string="Sub Category",
                                                domain="[('insurance_category_id', '=', insurance_category_id)]", required=True)

    insurance_time_period_id = fields.Many2one(
        'insurance.time.period', string="Policy Terms", required=True)
    duration = fields.Integer(
        related="insurance_time_period_id.duration", string="Duration (Months)")
    file_name = fields.Char(string="filename")
    avatar = fields.Binary(string="Document")
    policy_terms_and_conditions = fields.Text(string="Terms & Conditions")
    phone = fields.Char(related='company_id.phone', string="Phone")
    street = fields.Char(related="company_id.street",
                         string="Street", translate=True)
    street2 = fields.Char(related="company_id.street2",
                          string="Street 2", translate=True)
    city = fields.Char(related="company_id.city",
                       string="City", translate=True)
    state_id = fields.Many2one(related="company_id.state_id", string="State")
    country_id = fields.Many2one(
        related="company_id.country_id", string="Country")
    zip = fields.Char(related="company_id.zip", string="Zip", size=6)

    policy_amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', related="company_id.currency_id")
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, string="Company", required=True)

    # Life Insurance:
    life_insured_age = fields.Selection(
        [('five_to_twenty', "Between 5 to 20 Years"), ('twenty_to_fifty', "Between 20 to 50 Years"),
         ('fifty_to_seventy', "Between 50 to 70 Years"), ('above_seventy', "Above 70 Years")], string="Insured Age")
    desired_death_amount = fields.Monetary(string="Death Amount")
    length_of_coverage_term = fields.Text(string="Length of Coverage Terms")
    life_health_history = fields.Text(string="Insured Health History")
    occupation_and_hobbies = fields.Text(string="Occupation and Hobbies")
    family_medical_history = fields.Text(string="Family Medical History")
    # Health Insurance:
    health_insured_age = fields.Selection(
        [('five_to_twenty', "Between 5 to 20 Years"), ('twenty_to_fifty', "Between 20 to 50 Years"),
         ('fifty_to_seventy', "Between 50 to 70 Years"), ('above_seventy', "Above 70 Years")], string="Insured Age")
    desired_coverage_type = fields.Selection([('individual', "Individual"), ('family', "Family"), ('group', "Group")],
                                             string="Coverage Type")
    out_of_pocket_maximum = fields.Text(string="Out-of-Pocket Maximum")
    health_history_of_insured = fields.Text(string="Health History")
    drug_coverage = fields.Text(string="Prescription Drug Coverage")
    healthcare_provider_network = fields.Text(
        string="Preferred Healthcare Provider Network")
    # Property Insurance:
    construct_year = fields.Integer(string="Construct Year")
    property_value = fields.Monetary(string="Estimated Value")
    property_coverage_limits = fields.Text(string="Property Coverage Limits")
    construction_type_and_materials = fields.Text(
        string="Construction Type and Materials")
    special_features_of_the_property = fields.Text(
        string="Special Features of the Property")
    personal_property_inventory = fields.Text(
        string="Personal Property Inventory")
    # Liability Insurance:
    type_of_liability_risk = fields.Selection(
        [('auto', "Auto"), ('homeowner', "HomeOwner's"), ('business', "Business")], string="Liability Risk")
    liability_coverage_type = fields.Selection(
        [('general_liability', "General Liability"),
         ('professional_liability', "Professional Liability")],
        string="Coverage Type")
    desired_coverage_limits = fields.Text(string="Desired Coverage Limits")
    business_type_and_operations = fields.Text(
        string="Business Type and Operations")
    # Disability Insurance:
    income = fields.Monetary(string="Income")
    length_coverage_disability_period = fields.Text(
        string="Length of Coverage Period")
    disability_health_history = fields.Text(string="Health History")
    occupation_and_hobbies = fields.Text(string="Occupation and Hobbies")
    # Travel Insurance:
    types_of_coverage = fields.Selection(
        [('trip_cancellation', "Trip Cancellation"), ('medical_emergency', "Medical Emergency"),
         ('lost_luggage', "Lost Luggage")], string="Type of Coverage")
    traveler_health_history = fields.Text(string="Traveler Health History")
    # Pet Insurance:
    pet_desired_coverage_type = fields.Selection(
        [('accident', "Accident"), ('illness', "Illness"), ('routine_care', "Routine Care")], string="Coverage Type ")
    exclusions = fields.Selection(
        [('pre_existing_conditions', "Pre-Existing Conditions"),
         ('certain_breeds', "Certain Breeds")],
        string="Exclusions")
    pet_coverage_limits = fields.Text(string="Coverage Limits")
    # Business Insurance:
    business_desired_coverage_type = fields.Selection(
        [('property_damage', "Property Damage"), ('liability',
                                                  "Liability"), ('workers', "Workers Compensation")],
        string="Coverage Type")
    business_property_value = fields.Monetary(string="Estimated Value")
    business_type_operation = fields.Text(
        string="Business Type and Operations")
    business_coverage_limits = fields.Text(string="Business Coverage Limits")
    industry_specific_risks = fields.Text(string=" Industry-Specific Risks")
    # Auto Insurance:
    coverage_type = fields.Selection(
        [('liability', "Liability"), ('collision', "Collision"),
         ('comprehensive', "Comprehensive")],
        string="Coverage Type")
    driving_history = fields.Text(string="Driving History of the Insured")
    coverage_limits = fields.Text(string="Auto Coverage Limits")

    @api.constrains('policy_amount')
    def _check_policy_amount(self):
        for record in self:
            if record.policy_amount == 0:
                raise ValidationError("Please policy amount can not be zero")

    @api.onchange('insurance_category_id')
    def get_insurance_policy(self):
        for rec in self:
            if rec.insurance_category_id:
                # Life Insurance:
                rec.life_insured_age = rec.insurance_category_id.life_insured_age
                rec.desired_death_amount = rec.insurance_category_id.desired_death_amount
                rec.length_of_coverage_term = rec.insurance_category_id.length_of_coverage_term
                rec.life_health_history = rec.insurance_category_id.life_health_history
                rec.occupation_and_hobbies = rec.insurance_category_id.occupation_and_hobbies
                rec.family_medical_history = rec.insurance_category_id.family_medical_history
                # Health Insurance:
                rec.health_insured_age = rec.insurance_category_id.health_insured_age
                rec.desired_coverage_type = rec.insurance_category_id.desired_coverage_type
                rec.out_of_pocket_maximum = rec.insurance_category_id.out_of_pocket_maximum
                rec.health_history_of_insured = rec.insurance_category_id.health_history_of_insured
                rec.drug_coverage = rec.insurance_category_id.drug_coverage
                rec.healthcare_provider_network = rec.insurance_category_id.healthcare_provider_network
                # Property Insurance:
                rec.construct_year = rec.insurance_category_id.construct_year
                rec.property_value = rec.insurance_category_id.property_value
                rec.property_coverage_limits = rec.insurance_category_id.property_coverage_limits
                rec.construction_type_and_materials = rec.insurance_category_id.construction_type_and_materials
                rec.special_features_of_the_property = rec.insurance_category_id.special_features_of_the_property
                rec.personal_property_inventory = rec.insurance_category_id.personal_property_inventory
                # Liability Insurance:
                rec.type_of_liability_risk = rec.insurance_category_id.type_of_liability_risk
                rec.liability_coverage_type = rec.insurance_category_id.liability_coverage_type
                rec.desired_coverage_limits = rec.insurance_category_id.desired_coverage_limits
                rec.business_type_and_operations = rec.insurance_category_id.business_type_and_operations
                # Disability Insurance:
                rec.income = rec.insurance_category_id.income
                rec.length_coverage_disability_period = rec.insurance_category_id.length_coverage_disability_period
                rec.disability_health_history = rec.insurance_category_id.disability_health_history
                rec.occupation_and_hobbies = rec.insurance_category_id.occupation_and_hobbies
                # Travel Insurance:
                rec.types_of_coverage = rec.insurance_category_id.types_of_coverage
                rec.traveler_health_history = rec.insurance_category_id.traveler_health_history
                # Pet Insurance:
                rec.pet_desired_coverage_type = rec.insurance_category_id.pet_desired_coverage_type
                rec.exclusions = rec.insurance_category_id.exclusions
                rec.pet_coverage_limits = rec.insurance_category_id.pet_coverage_limits
                # Business Insurance:
                rec.business_desired_coverage_type = rec.insurance_category_id.business_desired_coverage_type
                rec.business_property_value = rec.insurance_category_id.business_property_value
                rec.business_type_operation = rec.insurance_category_id.business_type_operation
                rec.business_coverage_limits = rec.insurance_category_id.business_coverage_limits
                rec.industry_specific_risks = rec.insurance_category_id.industry_specific_risks
                # Auto Insurance:
                rec.coverage_type = rec.insurance_category_id.coverage_type
                rec.driving_history = rec.insurance_category_id.driving_history
                rec.coverage_limits = rec.insurance_category_id.coverage_limits


class InsuranceBuyingFor(models.Model):
    """Insurance Buying For"""
    _name = 'insurance.buying.for'
    _description = __doc__
    _rec_name = 'buying_for'

    buying_for = fields.Char(string="Buying For", required=True)
    insurance_category_id = fields.Many2one(
        'insurance.category', string="Policy Category", required=True)
