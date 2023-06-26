from odoo import api, models, fields, exceptions

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'

    lot_id = fields.One2many('stock.lot', 'registry_id', string="Lot ID")
    sale_order = fields.Char()
    owner_id = fields.Many2one('res.partner')
    owner_phone = fields.Char(related='owner_id.phone')
    owner_email = fields.Char(related='owner_id.email')

    # constrain to enforce one2one relation on lot_id
    @api.constrains('lot_id')
    def _enforce_one2one_lot_id(self):
        for record in self:
            if (len(record.lot_id)) > 1:
                raise exceptions.ValidationError("You can only add one lot_id!!")
