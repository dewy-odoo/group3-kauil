from odoo import models, fields, api

class MotorcycleRegistry(models.Model):
    _name = 'motorcycle.registry'
    _inherit = ['portal.mixin', 'motorcycle.registry']

    public = fields.Boolean('Public', default=True)

        # Vehicles fields
    brand = fields.Char(compute='_compute_from_vin', store = True)
    make = fields.Char(compute='_compute_from_vin', store = True)
    model = fields.Char(compute='_compute_from_vin', store = True)

    # portal.mixin override
    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = f'/my/registry/{record.id}'

    @api.depends('vin')
    def _compute_from_vin(self):
        registries_with_vin = self.filtered(lambda r: r.vin)
        registries_with_vin._check_vin_pattern()
        for registry in registries_with_vin:
            registry.brand = registry.vin[:2]
            registry.make = registry.vin[2:4]
            registry.model = registry.vin[4:6]
        for registry in (self - registries_with_vin):
            registry.brand = False
            registry.make = False
            registry.model = False