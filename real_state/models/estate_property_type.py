from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    
    name = fields.Char(required=True)
    estate_property_ids = fields.One2many(comodel_name="estate.property", inverse_name="type_id")  
    estate_property_count = fields.Integer(compute="_compute_estate_property_count")
           
    def action_open_properties(self):
        return {
            "type":"ir.actions.act_window",
            "name":"Estate Property By Type",
            "res_model": "estate.property",
            "view_mode": "list,form",
            "views":[
                (self.env.ref('real_state.estate_property_view_list').id,"list"),
                (self.env.ref('real_state.estate_property_view_form').id,"form")
            ],
            "help":"""
                <p class="o_view_nocontent_smiling_face">
                    No has creado ninguna propiedad.
                </p>
            """,
            "search_view_id": [self.env.ref("real_state.estate_property_view_search").id],
            "domain": [("type_id", "=", self.id)],
            "context":{"default_type_id": self.id}
        }
    
    @api.depends('estate_property_ids')        
    def _compute_estate_property_count(self):
        for property_type in self:
            property_type.estate_property_count = len(property_type.estate_property_ids)
            