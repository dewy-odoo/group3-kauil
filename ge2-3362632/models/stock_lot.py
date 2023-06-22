from odoo import api, fields, models, exceptions


class StockLot(models.Model):
    _inherit = 'stock.lot'

    registry_id = fields.Many2one(string="Registry ID", comodel_name='motorcycle.registry')