from odoo import api, fields, models, exceptions


class Repair(models.Model):

    _inherit = 'repair.order'

    registry_id = fields.Many2one(comodel_name='motorcycle.registry', string='Registry Number', required=True)

    vin = fields.Char(string='Motorcycle VIN', compute='_compute_vin_from_registry_id')
    
    mileage = fields.Float(string='Current Mileage')

    # overriding partner_id, sale_order_id, product_id. Making them related to registry_id
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer', compute='_compute_partner_id', states={'confirmed': [('readonly', False)]})

    sale_order_id = fields.Many2one(
        'sale.order', 'Sale Order', check_company=True,
        copy=False, help="Sale Order from which the product to be repaired comes from.", compute='_compute_sale_order_id')


    product_id = fields.Many2one(
            'product.product', string='Product to Repair',
            domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
            readonly=True, required=True, states={'draft': [('readonly', False)]}, check_company=True,
            compute='_compute_product_id')

    @api.model
    def _validate_registry_id(registry_id):

        if len(registry_id) > 1:
            raise exceptions.ValidationError("You can only have one VIN for a repair order!")
        else:
            return True

    @api.depends('registry_id')
    def _compute_vin_from_registry_id(self):
        for record in self:
            # check to enforce one registry_id for a repair order
            if Repair._validate_registry_id(record.registry_id): 
                for registry in record.registry_id:
                    record.vin = registry.vin
                    return
        record.vin = False


    @api.depends('registry_id')
    def _compute_partner_id(self):
        for record in self:
            if Repair._validate_registry_id(record.registry_id):
                for registry in record.registry_id:
                    registry_partner_ids = self.env['motorcycle.registry'].search(domain=[('vin', '=', registry.vin)])
                    record.partner_id = registry_partner_ids.owner_id
                    return
        record.partner_id = False

    @api.depends('registry_id')
    def _compute_sale_order_id(self):
        for record in self:
            for registry in record.registry_id:
                registry_sale_orders = self.env['sale.order'].search(domain=[('name', '=', registry.sale_order)])
                record.sale_order_id = registry_sale_orders
                return
        record.sale_order_id = False

    @api.depends('registry_id')
    def _compute_product_id(self):
        for record in self:
            for registry in record.registry_id:
                sale_order_id = self.env['sale.order.line'].search(domain=[('order_id', '=', registry.sale_order)])
                record.product_id = sale_order_id.product_id
                return
        record.product_id = False

