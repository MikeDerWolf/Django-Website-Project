from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import *
from app.forms import *
from datetime import date


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class RegisterBuyerView(CreateView):
    template_name = 'register_buyer.html'
    form_class = RegisterBuyerForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'],
                                        email=data['email'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])
        BuyerProfile.objects.create(user=user, address=data['address'])
        return redirect('login')


class RegisterSellerView(CreateView):
    template_name = 'register_seller.html'
    form_class = RegisterSellerForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'],
                                        email=data['email'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])
        SellerProfile.objects.create(user=user, telephone=data['telephone'], typeOfSeller=data['type_of_seller'])
        return redirect('login')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'autofocus': False, 'placeholder': 'Enter username'})
        form.fields['password'].widget.attrs.update({'autofocus': False, 'placeholder': 'Enter password'})
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            if hasattr(user, 'buyerProfile'):
                return redirect(reverse_lazy('product_list'))
            else:
                return redirect(reverse_lazy('my_product_list', kwargs={'pk': user.id}))
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login'))


class ProductListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        product_list = Product.objects.all()
        return render(request, 'products.html', {'product_list': product_list})


class MyProductListView(LoginRequiredMixin, ListView):
    template_name = 'my_products.html'
    context_object_name = 'my_product_list'

    def get_queryset(self):
        my_product_list = Product.objects.filter(user_id=self.kwargs['pk'])
        return my_product_list


class BuyerOrderListView(LoginRequiredMixin, ListView):
    template_name = 'buyer_orders.html'
    context_object_name = 'buyer_order_list'

    def get_queryset(self):
        buyer_order_list = Order.objects.filter(user_id=self.kwargs['pk'])
        return buyer_order_list


class SellerOrderListView(LoginRequiredMixin, ListView):
    template_name = 'seller_orders.html'
    context_object_name = 'seller_order_list'

    def get_queryset(self):
        my_product_list = Product.objects.filter(user_id=self.kwargs['pk'])
        seller_order_list = Order.objects.filter(product_id__in=list(map(lambda x: x.id, my_product_list)))
        return seller_order_list


class ProductAddView(LoginRequiredMixin, CreateView):
    template_name = 'add_product.html'
    form_class = AddProductForm
    model = Product

    def form_valid(self, form):
        data = form.cleaned_data
        post = Product.objects.create(name=data['name'],
                                      description=data['description'],
                                      price=data['price'],
                                      stock=data['stock'],
                                      user=self.request.user)

        return redirect(reverse_lazy("my_product_list", kwargs={"pk": self.request.user.id}))


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'edit_product.html'
    form_class = AddProductForm
    pk_url_kwarg = 'pk_product'

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs['pk_product'])
        product.name = form.cleaned_data['name']
        product.description = form.cleaned_data['description']
        product.price = form.cleaned_data['price']
        product.stock = form.cleaned_data['stock']

        product.save()
        return redirect(reverse_lazy("my_product_list", kwargs={"pk": self.kwargs['pk']}))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    pk_url_kwarg = 'pk_product'

    def get_success_url(self):
        return reverse_lazy("my_product_list", kwargs={"pk": self.kwargs['pk']})


class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        product = Product.objects.get(pk=self.kwargs['pk_product'])
        order = Order.objects.create(user=user.buyerProfile,
                                     product=product,
                                     noOfPcs=1,
                                     total=product.price,
                                     date=date.today(),
                                     shippingAddress=user.buyerProfile.address)

        product.stock -= 1
        product.save()
        return redirect(reverse_lazy("product_list"))


class OrderEditView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk_order'])
        order.status = "COMPLETE"

        order.save()
        return redirect(reverse_lazy("seller_order_list", kwargs={"pk": self.kwargs['pk']}))
