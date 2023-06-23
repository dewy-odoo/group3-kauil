from odoo import api, fields, models, tools

class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, compute = "_calc_detailed_type", group_expand='_read_group_categ_id',
        required=True, search = "_search_categ_id")
    
    @api.depends("detailed_type")
    def _calc_detailed_type(self):
         for s in self:     
            if s.detailed_type == "motorcycle":
                s.categ_id = s.env.ref('ge9-3365528.moto_category')
                return
            elif s.categ_id != self.env.ref('product.product_category_all'):
                s.categ_id =  s.categ_id
                return
            s.categ_id =  self.env.ref('product.product_category_all')
    
    def _search_categ_id(self, operator, value):
        query = self.with_context(active_test=False)._search([('categ_id', operator, value)])
        return [('id', 'in', query)]