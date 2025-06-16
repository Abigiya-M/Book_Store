# 📚 **Odoo Bookstore Management Module** 
A custom Odoo 17 module to manage a digital bookstore — built for learning and production use. This module includes books, genres, authors, and a wizard to assign authors easily.

## 🚀 Features

- 📘 Book Management: Add, edit, delete books with fields like name, ISBN, publish date, genre, and more.
- 🏷️ Genre Management: Create and manage book genres.
- ✍️ Author Management: Assign authors to books using a user-friendly wizard.
- 🧠 Book Age Calculation: Automatically computes the age of a book from its publish date.
- 📦 Archiving: Archive old books using a batch operation.
- 🧪 Unit Tests: Core features are tested to ensure reliability.
- 🧩 Wizard: Assign authors to multiple books via a simple wizard interface.
- 🎨 Custom Icon: Custom icon support for the module in the Odoo backend.

## 🛠️ Installation

1. Clone this repository or copy the module into your Odoo addons path:
   ```bash
   git clone https://github.com/yourusername/odoo_bookstore.git

## 🧪 Testing

Run the tests using the Odoo testing framework:

```bash
odoo-bin --test-enable --stop-after-init -i bookstore
