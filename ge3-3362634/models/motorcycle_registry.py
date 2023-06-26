from odoo import models, fields

class MotorcycleRegistry(models.Model):
    _name = 'motorcycle.registry'
    _inherit = ['portal.mixin', 'motorcycle.registry']

    public = fields.Boolean('Public', default=True)