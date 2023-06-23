from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_new_customer = fields.Boolean(string = "Is New Customer", 
                                     compute = "_compute_is_new_customer")
    
    


    ##when its not new customer, deactive the coupon


            
        
            
        
    
    @api.onchange("partner_id")
    def _compute_is_new_customer(self):
        sale_order_ids = self.partner_id.sale_order_ids
        for sale_order in sale_order_ids.filtered(lambda so: so.state in ['sale', 'done']):
            for order_line in sale_order.order_line:
                if order_line.product_template_id and order_line.product_template_id.detailed_type == 'motorcycle':
                    self.is_new_customer = False
                    self.env.ref('ge9-3363106.new_customer_coupon').active = False
                    self.pricelist_id = self.env.ref('ge9-3363106.no_coupon')
                    super()._recompute_prices()
                    return
        # check res partner
        self.is_new_customer = True
        self.env.ref('ge9-3363106.new_customer_coupon').active = True

        
    @api.depends("pricelist_id")
    def action_apply_discount(self):
        self.pricelist_id = self.env.ref('ge9-3363106.new_customer_coupon')
        super().action_update_prices()
        return True
    


    


    
    

