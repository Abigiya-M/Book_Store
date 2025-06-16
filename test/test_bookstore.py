from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestBookstore(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Book = self.env['book.details']
        self.Author = self.env['res.partner']
        self.Wizard = self.env['archive.author.wizard']

    def test_book_age_computation(self):
        book = self.Book.create({
            'title': 'Test Book',
            'publisher': 'Test Pub',
            'published_date': date(2000, 1, 1),
            'isbn': '1234567890123',
            'stock_qty': 10,
            'price': 20.0,
            'currency_id': self.env.ref('base.USD').id,
        })
        book._compute_book_age()
        self.assertGreaterEqual(book.book_age, 20)

    def test_archiving_old_books(self):
        old_date = date.today() - timedelta(days=10*365)
        book = self.Book.create({
            'title': 'Old Book',
            'published_date': old_date,
            'isbn': '1111111111111',
            'stock_qty': 1,
            'price': 5.0,
            'currency_id': self.env.ref('base.USD').id,
        })
        self.Book.archive_old_books()
        self.assertTrue(book.active is False)

    def test_author_archive_wizard(self):
        author = self.Author.create({'name': 'Archivable Author', 'is_author': True})
        book = self.Book.create({
            'title': 'A Book',
            'author_id': author.id,
            'isbn': '0000000000001',
            'published_date': date(2010, 5, 15),
            'stock_qty': 3,
            'price': 10.0,
            'currency_id': self.env.ref('base.USD').id,
        })

        wizard = self.Wizard.create({'author_id': author.id})
        wizard.archive_author_books()
        book.refresh()
        self.assertFalse(book.active)
