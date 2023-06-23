from odoo import api, models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()

        if res is True and self.location_dest_id.get_xml_id()[5] == 'stock.stock_location_customers':
            for el in self.move_line_ids:
                print("testing")
                registry = self.env['motorcycle.registry'].create({
                    "vin": el.lot_id.name
                })

        return res