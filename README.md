# Django Cart - FoodKart Shopping Cart

A Django-based shopping cart application for managing grocery items with real-time stock validation and dynamic pricing calculations.

## 🛒 Features

- **Interactive Shopping Cart**: Real-time quantity updates with automatic price calculations
- **Stock Validation**: Checks available inventory before allowing purchases
- **Responsive Design**: Mobile-friendly interface with modern UI
- **Admin Interface**: Easy product management through Django admin
- **Default Cart Items**: Pre-populated with common grocery items (Potatoes, Carrots, Onions)
- **Real-time Updates**: JavaScript-powered cart total calculations
- **Form Validation**: Server-side validation for quantities and stock availability

## 🏗️ Project Structure

```
django-cart/
├── foodkart/                 # Main Django project
│   ├── cart/                # Cart application
│   │   ├── migrations/      # Database migrations
│   │   ├── static/cart/     # Static files (CSS, JS)
│   │   ├── templates/cart/  # HTML templates
│   │   ├── templatetags/    # Custom template tags
│   │   ├── admin.py         # Admin configuration
│   │   ├── models.py        # Product model
│   │   ├── views.py         # Cart view logic
│   │   ├── forms.py         # Cart form handling
│   │   ├── constants.py     # Default cart items
│   │   └── urls.py          # URL routing
│   ├── foodkart/            # Project settings
│   │   ├── settings.py      # Django settings
│   │   ├── urls.py          # Main URL configuration
│   │   └── wsgi.py          # WSGI configuration
│   ├── templates/           # Project templates
│   └── manage.py            # Django management script
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd django-cart
   ```

2. **Create and activate virtual environment**

   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Django**

   ```bash
   pip install django
   ```

4. **Navigate to the Django project**

   ```bash
   cd foodkart
   ```

5. **Create and Apply Migrations (including initial data)**

   This step will set up your database schema and populate it with the initial product data. The migration files (`0001_initial.py` for schema and `0002_populate_initial_products.py` for data) are already included in the repository.

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Shopping Cart: http://127.0.0.1:8000/cart/
   - Admin Interface: http://127.0.0.1:8000/admin/

## 📦 Default Products

The application comes with pre-configured default products:

| Product  | Default Quantity | Price per kg (AED) |
| -------- | ---------------- | ------------------ |
| Potatoes | 2 kg             | 5.00               |
| Carrots  | 1 kg             | 4.00               |
| Onions   | 1 kg             | 2.00               |

## 🛠️ Adding Products via Admin

1. Access the admin interface at http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Navigate to "Products" under the "Cart" section
4. Click "Add Product" to create new products
5. Fill in:
   - **Name**: Product name (e.g., "Tomatoes")
   - **Price per kg**: Price in AED
   - **Stock in kg**: Available quantity

## 🎨 Customization

### Styling

- CSS styles are located in `foodkart/cart/static/cart/css/style.css`
- The design is responsive and mobile-friendly
- Uses Inter font family for modern typography

### JavaScript Functionality

- Cart calculations are handled in `foodkart/cart/static/cart/js/cart.js`
- Real-time updates when quantities change
- Automatic total calculation

### Template Tags

- Custom template tag `mul` for multiplication in templates
- Located in `foodkart/cart/templatetags/cart_extras.py`

## 🔧 Configuration

### Settings

Main Django settings are in `foodkart/foodkart/settings.py`:

- Database: SQLite (default)
- Static files: Configured for development
- Debug mode: Enabled for development

### Environment Variables

For production deployment, consider setting:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False
- `ALLOWED_HOSTS`: Configure allowed hosts

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 📱 Features in Detail

### Shopping Cart Interface

- Clean, modern design with responsive layout
- Real-time price calculations
- Stock availability display
- Form validation with error messages
- Mobile-optimized interface

### Stock Management

- Real-time stock checking
- Prevents over-ordering
- Clear error messages for out-of-stock items
- Admin interface for stock updates

### User Experience

- Instant feedback on quantity changes
- Clear pricing display
- Responsive design for all devices
- Intuitive navigation

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**

   ```bash
   python manage.py runserver 8001
   ```

2. **Database errors**

   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Static files not loading**

   ```bash
   python manage.py collectstatic
   ```

4. **Import errors**
   - Ensure virtual environment is activated
   - Check Django installation: `pip list | grep Django`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue in the repository or contact the development team.

## 📝 Data Migration File

### cart/migrations/0002_populate_initial_products.py

After creating the empty migration file, edit it with the following content:

```python
from django.db import migrations

def populate_initial_products(apps, schema_editor):
    Product = apps.get_model('cart', 'Product')

    products_data = [
        {"name": "Potatoes", "price_per_kg": 5.00, "stock_in_kg": 100.0},
        {"name": "Carrots", "price_per_kg": 4.00, "stock_in_kg": 50.0},
        {"name": "Onions", "price_per_kg": 2.00, "stock_in_kg": 75.0},
    ]

    for data in products_data:
        Product.objects.get_or_create(
            name=data["name"],
            defaults={
                "price_per_kg": data["price_per_kg"],
                "stock_in_kg": data["stock_in_kg"]
            }
        )

def reverse_populate_initial_products(apps, schema_editor):
    Product = apps.get_model('cart', 'Product')
    Product.objects.filter(
        name__in=["Potatoes", "Carrots", "Onions"]
    ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            populate_initial_products,
            reverse_populate_initial_products
        ),
    ]
```

This migration will automatically populate your database with the default products when you run `python manage.py migrate`.

---

**Happy Shopping! 🛒**
