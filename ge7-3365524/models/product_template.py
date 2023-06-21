from odoo import api, fields, models, exceptions
from datetime import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'


    # overriding name field
    name = fields.Char('Name', index='trigram', required=True, translate=True, compute="_compute_product_name")

    
    @api.depends('year', 'make', 'model', 'detailed_type')
    def _compute_product_name(self):
        """
            Compute product name based on year, make and model of product.
            Only applies to motorcycles.
        """
        for record in self:

            # sanity checks
            # check if product is a motorcycle

            # TODO: need to add handling for cases where make, model and year are empty
            if not record.year:
                record.year = int(datetime.now().year)
            if not record.make:
                record.make = "<placeholder>"
            if not record.model:
                record.model = "<placeholder>"

            if record.detailed_type == 'motorcycle':
                record.name = f'{record.year}-{record.make}-{record.model}'
            else:
                record.name = record.name

