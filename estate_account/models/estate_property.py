from odoo import models, fields, api, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    account_move_id = fields.Many2one(comodel_name="account.move")
    
    def action_open_invoice(self):
        return {
            "type":"ir.actions.act_window",
            "name":"Invoice of Property",
            "res_model": "account.move",
            "view_mode": "form",
            "views":[
                (self.env.ref('account.view_move_form').id,"form")
            ],
            "res_id": self.account_move_id.id
        }