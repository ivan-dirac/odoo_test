from odoo import models, fields, api, Command

class AccountMove(models.Model):
    _inherit = "account.move"
    
    property_id = fields.Many2one(comodel_name="estate.property")
    
    