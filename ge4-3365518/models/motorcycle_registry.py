from odoo import api, models, fields, exceptions


class MotorcycleRegistry(models.Model):

    _inherit = 'motorcycle.registry'

    repair_ids = fields.One2many(
        string='Repair Orders', comodel_name='repair.order', inverse_name='registry_id')

    def action_display_repairs(self):
        self.ensure_one()
        return {
            'name': ('Repair Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'repair.order',
            'view_mode': 'tree',
            'domain': [('registry_id', '=', self.registry_number)],
        }
