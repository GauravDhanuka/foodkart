from django.shortcuts import render
from django.http import HttpRequest
from decimal import Decimal
from .models import Product, Order, OrderItem
from .constants import DEFAULT_CART_ITEMS

# Create your views here.
def cart_view(request: HttpRequest):
    """
    Handler for displaying cart items and processing submission
    """

    messages = []
    cart_items = []

    # Populate cart items with default quantities and fetch current stock
    for item in DEFAULT_CART_ITEMS:
        try:
            # Get the product from the database to show current stock
            product_in_db = Product.objects.get(name=item['name'])
            cart_items.append({
                'name': item['name'],
                'quantity': Decimal(item['quantity']),
                'price_per_kg': product_in_db.price_per_kg,
                'current_stock_in_kg': product_in_db.stock_in_kg
            })
        except Product.DoesNotExist:
            # If a product doesn't exist, add a message and skip it for order validation
            messages.append(f"Warning: Product '{item['name']}' not found in inventory. Please add it via admin.")
            cart_items.append({
                'name': item['name'],
                'quantity': Decimal(item['quantity']),
                'price_per_kg': Decimal(item['price_per_kg']),
                'current_stock_in_kg': Decimal(0) # Default to 0 stock
            })
    
    if request.method == 'POST':
        # Process the submitted order
        order_successful = True
        validation_errors = []
        updated_cart_quantities = {} # To store input quantities to repopulate form

        for item in DEFAULT_CART_ITEMS:
            product_name = item['name']
            # Get the submitted quantity for this product from the form
            try:
                submitted_qty_str = request.POST.get(f'{product_name.lower()}_qty')
                if not submitted_qty_str:
                    # If quantity not provided, default to 0 or original.
                    submitted_qty = Decimal(0)
                else:
                    submitted_qty = Decimal(submitted_qty_str)
                
                updated_cart_quantities[product_name] = submitted_qty

            except Exception:
                validation_errors.append(f'Invalid quantity submitted for {product_name}.')
                order_successful = False
                continue

            try:
                product_db = Product.objects.get(name=product_name)

                if submitted_qty <= 0:
                    # Skipping quantity validation if required quantity is 0
                    continue

                if product_db.stock_in_kg < submitted_qty:
                    # Insufficient stock
                    order_successful = False
                    if product_db.stock_in_kg == 0:
                        validation_errors.append(f'Sorry! we are out of stock for {product_name.lower()}.')
                    else:
                        validation_errors.append(f'Sorry! we only have {product_db.stock_in_kg} kg of {product_name.lower()} left.')
                
            except Product.DoesNotExist:
                # Product not found in database
                order_successful = False
                validation_errors.append(f"Product '{product_name}' not found in our inventory.")
            except Exception as e:
                # Other unexpected errors
                order_successful = False
                validation_errors.append(f'An error occurred checking stock for {product_name}: {e}')

        if order_successful and not validation_errors:
            # If all checks pass, order is successful
            messages.append('Order confirmed! Thank you for your purchase.')
            # Decrement stock and create order record
            order_total = Decimal(0)
            order_items = []
            for item in DEFAULT_CART_ITEMS:
                product_name = item['name']
                submitted_qty = updated_cart_quantities.get(product_name, Decimal(0))
                if submitted_qty > 0:
                    product_db = Product.objects.get(name=product_name)
                    # Deduct stock
                    product_db.stock_in_kg -= submitted_qty
                    product_db.save()
                    # Calculate line total
                    line_total = submitted_qty * product_db.price_per_kg
                    order_total += line_total
                    order_items.append((product_db, submitted_qty, product_db.price_per_kg))
            # Create order
            order = Order.objects.create(total=order_total)
            for product, qty, price_per_kg in order_items:
                OrderItem.objects.create(order=order, product=product, quantity=qty, price_per_kg=price_per_kg)
            
            # After successful purchase, we refresh the displayed stock
            for cart_item in cart_items:
                try:
                    product_in_db = Product.objects.get(name=cart_item['name'])
                    cart_item['current_stock_in_kg'] = product_in_db.stock_in_kg
                except Product.DoesNotExist:
                    cart_item['current_stock_in_kg'] = Decimal(0)
        else:
            # If there are any validation errors, add them to messages
            messages.extend(validation_errors)
            messages.append('Please adjust your quantities and try again.')
        
        # Update the cart_items list with submitted quantities for re-rendering the form
        for item in cart_items:
            if item['name'] in updated_cart_quantities:
                item['quantity'] = updated_cart_quantities[item['name']]

    # Render the cart page with context
    context = {
        'cart_items': cart_items,
        'messages': messages,
    }
    return render(request, 'cart/cart.html', context)