from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class EstatePropertyType(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _sql_constraints = [('check_price_is_possitive', 'check(price>0)', 'El precio debe ser mayor 0')]
    _order = 'sequence ASC, price DESC'
    
    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'), 
        ('refused', 'Refused')
        ], default='accepted') 
    
    partner_id = fields.Many2one(comodel_name ="res.partner")
    property_id = fields.Many2one(comodel_name ="estate.property")
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", readonly=False, inverse="_inverse_date_deadline")
    
    sequence = fields.Integer()
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date != False:
                offer.date_deadline = offer.create_date+relativedelta(days=offer.validity)
            else:
                offer.date_deadline = False
            
    @api.onchange('date_deadline')        
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline != False and offer.create_date != False:
                date_deadline = datetime.combine(offer.date_deadline, datetime.min.time())
                offer.validity = (date_deadline - offer.create_date).days
            
    def action_accepted(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "sold"
        return True
    
    def action_refused(self):
        self.status = 'refused'
        return True
    
    @api.model_create_multi
    def create(self, vals_list):        
        for vals in vals_list:
            lower_price = self.env["estate.property.offer"].search([("property_id", "=", vals["property_id"])], order="price ASC", limit=1 ).price
            if vals["price"] < lower_price:
                raise ValidationError("El precio de venta no puede ser menor el precio menor en la ofertas")
        res = super().create(vals_list)
        if res:
            res.property_id.state = "received"
        return res