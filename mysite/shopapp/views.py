from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order


class ShopIindexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphon', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'
    # queryset = Product.objects.filter(archived=False)


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    url = reverse('shopapp:orders_list')
    return render(request, 'shopapp/create-order.html', context=context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_address', 'promocode', 'created_at', 'user', 'products'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    # fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)


class OrdersListView(ListView):
    template_name = 'shopapp/order-list.html'
    model = Order
    context_object_name = 'orders'
    # queryset = Product.objects.filter(archived=False)


# class OrdersListView(ListView):
#     queryset = (
#         Order.objects
#         .select_related('user')
#         .prefetch_related('products')
#     )


# class ProductListView(ListView):
#     template_name = 'shopapp/products-list.html'
#     context_object_name = 'products'
#     queryset = Product.objects.filter(archived=False)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class OrderDetailView(DetailView):
    template_name = 'shopapp/order-details.html'
    model = Order
    context_object_name = 'object'


# class OrderDetailView(DetailView):
#     queryset = (
#         Order.objects
#         .select_related('user')
#         .prefetch_related('products')
#     )
# class GroupsListView(View):
# # def groups_list(request: HttpRequest):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         context = {
#             'form': GroupForm(),
#             'groups': Group.objects.prefetch_related('permissions').all(),
#         }
#         return render(request, 'shopapp/groups-list.html', context=context)
#
#     def post(self, request: HttpRequest) -> HttpResponse:
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#         return redirect(request.path)
#
#
# class ProductDetailsView(DetailView):
#     template_name = 'shopapp/products-details.html'
#     model = Product
#     context_object_name = 'product'
#     # def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#     #     # product = Product.objects.get(pk=pk)
#     #     product = get_object_or_404(Product, pk=pk)
#     #     context = {
#     #         'product': product,
#     #     }
#     #     return render(request, 'shopapp/products-details.html', context=context)
#
#
# class ProductListView(ListView):
#     template_name = 'shopapp/products-list.html'
#     model = Product
#     context_object_name = 'products'
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['products'] = Product.objects.all()
#     #     return context
#
#
# # def products_list(request: HttpRequest):
# #     context = {
# #         'products': Product.objects.all(),
# #     }
# #     return render(request, 'shopapp/products-list.html', context=context)
#
#
# # def create_product(request: HttpRequest) -> HttpResponse:
# #     if request.method == 'POST':
# #         form = ProductForm(request.POST)
# #         if form.is_valid():
# #             # name = form.cleaned_data['name']
# #             # Product.objects.create(**form.cleaned_data)
# #             form.save()
# #             url = reverse('shopapp:products_list')
# #             return redirect(url)
# #     else:
# #         form = ProductForm()
# #     context = {
# #         'form': form,
# #     }
# #     url = reverse('shopapp:products_list')
# #     return render(request, 'shopapp/create-product.html', context=context)
#
# class ProductCreateView(CreateView):
#     model = Product
#     fields = 'name', 'price', 'description', 'discount'
#     success_url = reverse_lazy('shopapp:products_list')
#
#
# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data['name']
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse('shopapp:orders_list')
#             return redirect(url)
#     else:
#         form = OrderForm()
#     context = {
#         'form': form,
#     }
#     url = reverse('shopapp:orders_list')
#     return render(request, 'shopapp/create-order.html', context=context)
#
#
# class OrdersListView(ListView):
#     queryset = (
#         Order.objects
#         .select_related('user')
#         .prefetch_related('products')
#     )
# #     template_name = 'shopapp/products-list.html'
# #     model = Product
# #     context_object_name = 'products'
# #
#
#
# class OrderDetailView(DetailView):
#     queryset = (
#         Order.objects
#         .select_related('user')
#         .prefetch_related('products')
#     )


# def orders_list(request: HttpRequest):
#     context = {
#         'orders': Order.objects.select_related('user').prefetch_related('products').all(),
#     }
#     return render(request, 'shopapp/order_list.html', context=context)

    # print(request.path)
    # print(request.method)
    # print(request.headers)
    # return HttpResponse('Hello World')
