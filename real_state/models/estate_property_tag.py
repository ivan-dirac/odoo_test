from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _sql_constraints = [('id', 'unique(name)', 'Es imposible crear 2 tags con el mismo nombre')]
    
    name = fields.Char(required=True)