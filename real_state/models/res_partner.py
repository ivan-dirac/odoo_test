from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="seller_id")