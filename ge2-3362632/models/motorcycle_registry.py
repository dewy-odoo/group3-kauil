from odoo import api, models, fields

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'

    lot_id = fields.One2many('stock.lot', 'registry_id', string="Lot ID")