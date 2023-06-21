from odoo import api, fields, models
import random

class aname(models.Model):
    _inherit = 'stock.lot'

    name = fields.Char(
        'Lot/Serial Number', default=lambda self: self.env['ir.sequence'].next_by_code('stock.lot.serial'),
        required=True, help="Unique Lot/Serial Number", index='trigram', compute='_compute_motorcycle_vin')
    
    @api.depends("product_id")
    def _compute_motorcycle_vin(self):
        for record in self:
            if record.product_id.product_tmpl_id.detailed_type == 'motorcycle':
                name = ""
                name += record.product_id.make[:2].upper()
                name += record.product_id.model[:2].upper()
                name += str(record.product_id.year % 100)
                name += record.product_id.battery_capacity.upper()
                for i in range(0, 6):
                    name += str(random.randint(0, 9))
                record.name = name
            else:
                record.name = self.env['ir.sequence'].next_by_code('stock.lot.serial')