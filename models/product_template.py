from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean(string="Is a Book", default=False)
