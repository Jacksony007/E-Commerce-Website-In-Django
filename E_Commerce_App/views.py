
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category, Cart, Review
from django.contrib.auth import authenticate, login, logout


def home(request):

    categories = Category.objects.all()
    products = Product.objects.all()

    # Retrieve the user's name if authenticated
    user = request.user
    if user.is_authenticated:
        user_name = user.first_name  # Assuming you want the first name

    else:
        user_name = None

    context = {
        'user_name': user_name
    }

    return render(request, 'index.html', {'categories': categories, 'products': products, **context})


def fashion(request):
    # Retrieve the fashion category
    fashion_category = Category.objects.get(name='Fashion')

    # Retrieve all products related to the fashion category
    products = Product.objects.filter(category=fashion_category)

    # Retrieve the user's name if authenticated
    user = request.user
    if user.is_authenticated:
        user_name = user.first_name  # Assuming you want the first name
    else:
        user_name = None

    context = {
        'user_name': user_name
    }

    return render(request, 'fashion.html', {'products': products, **context})


def electronic(request):

    # Retrieve the fashion category
    electronic_category = Category.objects.get(name='Electronic')

    # Retrieve all products related to the fashion category
    products = Product.objects.filter(category=electronic_category)

    # Retrieve the user's name if authenticated
    user = request.user
    if user.is_authenticated:
        user_name = user.first_name  # Assuming you want the first name
    else:
        user_name = None

    context = {
        'user_name': user_name
    }

    return render(request, 'electronic.html', {'products': products, **context})


def jewellery(request):

    # Retrieve the fashion category
    jewellery_category = Category.objects.get(name='Jewellery')

    # Retrieve all products related to the fashion category
    products = Product.objects.filter(category=jewellery_category)

    # Retrieve the user's name if authenticated
    user = request.user
    if user.is_authenticated:
        user_name = user.first_name  # Assuming you want the first name
    else:
        user_name = None

    context = {
        'user_name': user_name
    }

    return render(request, 'jewellery.html', {'products': products, **context})


def help_desk(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Retrieve the user's name if authenticated
    user = request.user
    if user.is_authenticated:
        user_name = user.first_name  # Assuming you want the first name

    else:
        user_name = None

    context = {
        'user_name': user_name
    }

    return render(request, 'help_desk.html', {'categories': categories, 'products': products, **context})


def about_us(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Retrieve the user's name if authenticated
    user = request.user
    if user.is_authenticated:
        user_name = user.first_name  # Assuming you want the first name

    else:
        user_name = None

    context = {
        'user_name': user_name
    }

    return render(request, 'about_us.html', {'categories': categories, 'products': products, **context})


CustomUser = get_user_model()


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # Perform logic to add the product to the cart
        try:
            product = Product.objects.get(pk=product_id)
            # Assuming you have a logged-in user
            user = request.user
            # Assuming you have a cart instance associated with the user
            cart = Cart.objects.create(user=user, product=product, quantity=1)
            # Perform any additional logic or validations here
            response_data = {'success': True}
        except Product.DoesNotExist:
            response_data = {'success': False,
                             'error': 'Product does not exist'}
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    response_data = {'success': False, 'error': 'Invalid request method'}
    return JsonResponse(response_data)


@login_required
def cart_count(request):
    user = request.user
    cart_count = Cart.objects.filter(user=user).count()
    response_data = {'success': True, 'cart_count': cart_count}
    return JsonResponse(response_data)


def get_cart_item_count(request):
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'count': cart_item_count})
    else:
        return JsonResponse({'count': 0})


def cart_view(request):
    # Retrieve cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total price and other details
    subtotal = 0
    total_quantity = 0
    for index, item in enumerate(cart_items, start=1):
        subtotal += item.product.price * item.quantity
        total_quantity += item.quantity
        item.index = index  # Assign a number to each item

    # Apply discounts and delivery fee based on your logic
    # Update the total price and other details accordingly

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total_quantity': total_quantity,

        # Add other necessary context variables
    }

    return render(request, 'cart.html', context)


def remove_product_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return JsonResponse({'message': 'Product removed from the cart.'})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})
