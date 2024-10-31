# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class InsuranceSubCategory(models.Model):
    """Insurance Sub Category"""
    _name = 'insurance.sub.category'
    _description = __doc__
    _rec_name = 'name'

    insurance_category_id = fields.Many2one(
        'insurance.category', string="Category", required=True)
    name = fields.Char(string="Name", required=True)


class InsuranceCategory(models.Model):
    """Insurance Category"""
    _name = 'insurance.category'
    _description = __doc__
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    category = fields.Selection(
        [('life', "Life Insurance"), ('health', "Health Insurance"), ('property', "Property Insurance"),
         ('liability', "Liability Insurance"), ('disability',
                                                "Disability Insurance"), ('travel', "Travel Insurance"),
         ('pet', "Pet Insurance"), ('business', "Business Insurance"), ('auto', "Auto Insurance")], string="Category",
        required=True)
    category_code = fields.Char(string="Code")
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, string="Company")
    currency_id = fields.Many2one(
        'res.currency', string='Currency', related="company_id.currency_id")

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
        [('accident', "Accident"), ('illness', "Illness"), ('routine_care', "Routine Care")], string="Coverage Type")
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
