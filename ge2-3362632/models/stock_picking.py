from odoo import api, models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()

        if res is True and 'stock.stock_location_customers' in self.location_dest_id.get_external_id().values():
            for el in self.move_line_ids:
                if el.product_id.detailed_type == "motorcycle":
                    self.env['motorcycle.registry'].create({
                        "lot_id": el.lot_id,
                        "vin": el.lot_id.name,
                        "sale_order": self.origin,
                        "owner_id": self.partner_id.id
                    })

        return res