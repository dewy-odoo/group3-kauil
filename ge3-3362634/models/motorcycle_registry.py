from odoo import models, fields

class MotorcycleRegistry(models.Model):
    _name = 'motorcycle.registry'
    _inherit = ['portal.mixin', 'motorcycle.registry']

    public = fields.Boolean('Public', default=True)

    # portal.mixin override
    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = f'/my/registry/{record.id}'