from odoo import api, models, fields, excpetions


class MotorcycleRegistry(models.Model):

    _inherit = 'motorcycle.registry'

    repair_ids = fields.One2Many('Repair Orders', comodel_name='repair.order', inverse_name='registry_id')