from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', compute="_compute_closest")

    
    @api.onchange('partner_id')
    def _compute_closest(self):
        for record in self:
            wID = 3
            caDeliveries = ['CA', 'NV', 'OR', 'ID', 'UT', 'AZ']
            if self.partner_id.state_id.code in caDeliveries:
                wID = 4
            warehouse = self.env['stock.warehouse'].search_read([('id', '=', wID)])
            if len(warehouse) == 1:
                record.warehouse_id = warehouse[0]