from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            for line in order.order_line:
                product = line.product_id
                book = self.env['book.details'].search([('product_id', '=', product.id)], limit=1)
                if book:
                    book.stock_qty += line.product_qty
        return res
