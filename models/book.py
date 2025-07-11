from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class BookDetails(models.Model):
    _name = 'book.details'
    _description = 'Book Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # For chatter integration

    title = fields.Char('book.title', required=True, tracking=True)
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        ondelete='cascade',
        domain="[('is_book', '=', True)]",
        help="Linked product for Sales"
    )
    stock_qty = fields.Integer(string="Stock Quantity", default=0)
    author_id = fields.Many2one(
        'res.partner', string='Author', domain="[('author', '=', True)]", tracking=True)
    publisher = fields.Char(required=True)
    published_date = fields.Date(required=True, tracking=True)
    book_age = fields.Integer(compute='_compute_book_age', store=True)
    isbn = fields.Char(string="ISBN", unique=True)
    is_archived = fields.Boolean(default=False)
    stock_qty = fields.Float()
    price = fields.Monetary()
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id.id)
    genre_ids = fields.Many2many('genre.details', string='Genres', tracking=True)

    cover_image = fields.Binary("Cover Image")

    can_archive = fields.Boolean(compute='_compute_archive_buttons')
    can_unarchive = fields.Boolean(compute='_compute_archive_buttons')

    # -------------------------------
    # OVERRIDES
    # -------------------------------

    @api.model
    def create(self, vals):
        book = super().create(vals)

        # If product is linked already, mark it as book
        if book.product_id:
            book.product_id.is_book = True
        else:
            # Create product and link
            product = self.env['product.product'].create({
                'name': book.title,
                'type': 'product',
                'sale_ok': True,
                'is_book': True,
            })
            book.product_id = product.id

        return book

    def write(self, vals):
        res = super().write(vals)
        for book in self:
            if book.product_id:
                book.product_id.is_book = True
        return res

    # -------------------------------
    # COMPUTE METHODS
    # -------------------------------

    @api.depends('published_date')
    def _compute_book_age(self):
        for record in self:
            if record.published_date:
                record.book_age = date.today().year - record.published_date.year
            else:
                record.book_age = 0

    @api.depends('is_archived')
    def _compute_archive_buttons(self):
        for record in self:
            record.can_archive = not record.is_archived
            record.can_unarchive = record.is_archived

    # CONSTRAINTS

    @api.constrains('stock_qty', 'price', 'published_date')
    def _check_validations(self):
        for record in self:
            if record.stock_qty < 0:
                raise ValidationError(_('Stock quantity cannot be negative.'))
            if record.price < 0:
                raise ValidationError(_('Price cannot be negative.'))
            if record.published_date and record.published_date > date.today():
                raise ValidationError(_('Published date cannot be in the future.'))
        
        

    
    def action_archive(self):
        for record in self:
            record.is_archived = True

    def action_unarchive(self):
        for record in self:
            record.is_archived = False
