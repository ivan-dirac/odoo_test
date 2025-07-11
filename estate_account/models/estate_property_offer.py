from odoo import models, fields, api, Command

class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"
    
    def action_accepted(self):
        res = super().action_accepted()
        invoice = self.env["account.move"].create(
            {
                "partner_id" : self.property_id.buyer_id.id, 
                "move_type" : 'out_invoice',
                "invoice_line_ids": [
                    (Command.CREATE, 0, {"name" : self.property_id.name, "quantity": 1, "price_unit":  (self.property_id.selling_price * 1.06) }),
                    (Command.CREATE, 0, {"name" : "Comision", "quantity": 1, "price_unit": 100})
                ],
                "property_id" : self.property_id.id
            }
        )
       #invoice = self.env["account.move"].search([("property_id","=", self.property_id.id)], limit=1)
        self.property_id.account_move_id = invoice
        return res