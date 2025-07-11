from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Property"
    _sql_constraints = [
        ('check_selling_price_possitive', 'check(selling_price>=0)', 'El precio debe ser mayor a 0'),
        ('check_expected_price_possitive', 'check(expected_price>0)', 'El precio debe ser mayor a 0')]
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West'), 
        ], default='west')
    active = fields.Boolean(default="True")
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancel')
    ], default='new')
    
    type_id = fields.Many2one(comodel_name="estate.property.type")
    tag_ids = fields.Many2many(comodel_name="estate.property.tag")    
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")    
    expected_price_iva = fields.Float(compute="_compute_expected_price_iva", search="_search_expected_price_iva")
    total_area = fields.Integer(compute="_compute_total_area")    
    best_price = fields.Float(compute="_compute_best_price")
    
    buyer_id = fields.Many2one(comodel_name="res.partner")
    seller_id = fields.Many2one(comodel_name="res.partner")
    
    @api.depends('expected_price')
    def _compute_expected_price_iva(self):
        for estate_property in self:
            estate_property.expected_price_iva = estate_property.expected_price * 1.16
    
    @api.depends('living_area', 'garden_area')        
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area
            
    @api.depends('offer_ids.price')        
    def _compute_best_price(self):
        for estate_property in self:
            accepted_offers = estate_property.offer_ids.filtered(lambda offer: offer.status == "accepted") 
            if len(accepted_offers) > 0:                
                estate_property.best_price = max(accepted_offers.mapped("price"))
            else:
                estate_property.best_price = 0
                
    @api.onchange('garage')              
    def _onchangeTest(self):
        for estate_property in self:
            estate_property.description = _("Descripcion de: %s", estate_property.name)
            
    @api.onchange('bedrooms')              
    def _onchangeTest2(self):
        for estate_property in self:
            estate_property.garage = True
            estate_property.garden_area = 123
            
    def _search_expected_price_iva(self, operator, value):
        #[("expected_price_iva", ">", 1100)]
        #expected_price = 1000, expected_price_iva = 1160
        #expected_price = 900, expected_price_iva = 1044
        return [("expected_price", operator, value/1.16)] 
    
    def action_set_sold(self):
        if self.state != "cancel":
            self.state = "sold"
        else:
            raise UserError(_("Una vez cancelado no lo puedes vender"))
        return True
    
    def action_set_cancel(self):
        if self.state != "sold":
            self.state = "cancel"
        else:
            raise UserError("Una vez vendido no se puede cancelar")
        return True
    
    @api.constrains('selling_price', 'expected_price', 'state')
    def _check_date_end(self):
        for estate_property in self:
            if estate_property.state == "sold":
                cantidad = (estate_property.expected_price * 90)/100
                if float_compare(estate_property.selling_price, cantidad, precision_digits = 2) == -1:
                    raise ValidationError("El precio de venta no puede ser menor al 90 porciento del precio sugerido")
                
    def unlink(self):
        blocked_properties = self.filtered(lambda property: property.state not in ["new", "cancel"])
        if blocked_properties:
            raise ValidationError(_("%s : solo se puede eliminar un a propiedad con estatus nuevo y/o cancelado", ', '.join(blocked_properties.mapped('name'))))
        return super().unlink() 
    
    
    def copy(self, default=None):
        res = super().copy(default)
        res.name = self.name+" (copy)"
        return res
                