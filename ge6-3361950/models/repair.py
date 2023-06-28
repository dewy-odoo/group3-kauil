from odoo import api, models, fields, exceptions



class Repair(models.Model):

    _inherit = ['portal.mixin', 'repair.order']

    def _compute_repair_order_portal_url(self):
        super()._compute_access_url()

        for record in self:
            record.access_url = f'/my/repair-order/{record.id}'
    