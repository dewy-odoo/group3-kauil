from odoo import api, fields, models

class StockLot(models.Model):
    _inherit = 'stock.lot'

    @api.model
    def _get_next_serial(self, company, product):
        if product.detailed_type == 'motorcycle' and product.tracking != "none":
            if product.make and product.model and product.year and product.battery_capacity:
                return (product.make + product.model + str(product.year % 100) + product.battery_capacity.upper() + str(self.env['ir.sequence'].next_by_code('stock.lot.serial'))[1:])
        return super(StockLot, self)._get_next_serial(company, product)