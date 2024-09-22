from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Product

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found.")

    context = {'product': product}
    size = request.GET.get('size')

    if size:
        try:
            # Attempt to get the price based on the selected size
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
        except Exception as e:
            # Handle any error during price retrieval
            print(e)
            context['error'] = "Could not retrieve price for the selected size."

    # Ensure we always return an HttpResponse
    return render(request, 'product/product.html', context=context)


