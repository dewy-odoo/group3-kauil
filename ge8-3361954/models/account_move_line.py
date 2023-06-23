import random
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    vin = fields.Char(string='VIN', compute='_compute_vin', store=True, readonly=True)

    @api.depends('product_id')
    def _compute_vin(self):
        for line in self:
            if line.product_id.product_tmpl_id.detailed_type == 'motorcycle':
                line.vin = line.product_id.product_tmpl_id.make[:2].upper()
                line.vin += line.product_id.product_tmpl_id.model[:2].upper()
                line.vin += str(line.product_id.product_tmpl_id.year % 100)
                line.vin += line.product_id.product_tmpl_id.battery_capacity.upper()
                for i in range(0, 6):
                    line.vin += str(random.randint(0, 9))
            else:
                line.vin = ""