from django.shortcuts import render, redirect, get_object_or_404
from gym.models import Workout
from order.models import Order, OrderItem
from session.models import Session, AvailableSession
from gym.models import ClientProfile
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings

from django.template.loader import get_template
from django.core.mail import EmailMessage

platform_fee = 2 #aso remember to change in stripe application_fee if updated


def stripeFeeCalculator(total):
    percentage = (1.4/100) * total
    final = percentage + 0.2
    return final

def netCalculator(total, stripe_fee, platform_fee):
    net = total - stripe_fee - platform_fee
    return net


# tbd


# Create your views here.
@login_required
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart

@login_required
def add_cart(request, pk):
    workout = Workout.objects.get(pk=pk)
    trainer = workout.trainer.name # new addition
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(workout=workout,trainer=trainer,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(workout = workout,trainer=trainer,quantity = 1,cart = cart)
        cart_item.save()
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request, total=0, counter=0, cart_items = None):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.workout.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass



    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = total * 100
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    client_name = request.user.clientprofile.name #newnew
    client_id = request.user.id
    client_email = request.user.email
    stripe_customer_id = request.user.clientprofile.stripe_customer_id





    # to calculate the net pay
    stripe_fee = stripeFeeCalculator(total)
    service_fee = stripe_fee + platform_fee
    net_pay = netCalculator(total, stripe_fee, platform_fee)


    if request.method == 'POST':
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        trainer_stripe_id=cart_item.workout.trainer.user.stripedetail.stripe_id
        trainer_name = cart_item.workout.trainer.name
        workout_name = cart_item.workout.name
        trainer_email = cart_item.workout.trainer.user.email
        subscription = cart_item.workout.subscription
        workout_description = cart_item.workout.workout_description
        trainer_id = cart_item.workout.trainer.user.id
        sessions = cart_item.workout.sessions





        def product_name():
            product = stripe.Product.create(
            name=workout_name,
            type='service',
            # stripe_account=trainer_stripe_id,
                )
            product_name = product.name
            return product_name

        def plan_id(stripe_product_name):
            plan = stripe.Plan.create(
            product={'name': stripe_product_name},
            nickname=workout_name,
            interval='day',
            currency='gbp',
            amount=stripe_total,
            stripe_account=trainer_stripe_id,
            metadata={'client_name':client_name, 'trainer_name':trainer_name,
                        'token':token,'total':str(total), 'stripe_fee':str(stripe_fee),
                        'platform_fee':platform_fee, 'service_fee':service_fee,
                        'net_pay':str(net_pay), 'client_email':client_email, 'trainer_email':trainer_email,
                        'subscription':subscription, 'stripe_product_name':stripe_product_name, 'trainer_id':trainer_id,
                        'sessions':sessions
                        }


                )
            plan_id = plan.id
            return plan_id

        def customer_id(client_email, token):
            customer = stripe.Customer.create(
                email=client_email,
                source=token,
                stripe_account=trainer_stripe_id,
                    )
            customer_id = customer.id
            return customer_id


        if subscription == 0:
            stripe_product_name = 'None'
            stripe_plan_id = 'None'
            stripe_subscription_id = 'None'
            stripe_invoice_id = 'None'

            print('i am a normal charge')
            charge = stripe.Charge.create(
                        amount=stripe_total,
                        currency="gbp",
                        source=token,
                        # customer=stripe_customer_id,
                        destination={
                            "account": trainer_stripe_id,
                            }
                        # stripe_account=trainer_stripe_id,
                        )

        else:
            stripe_invoice_id = 'None'

            if stripe_customer_id == 'None':
            # create stripe customer id
                id = ClientProfile.objects.get(pk=client_id)
                stripe_customer_id = customer_id(client_email, token)
            # token_id = token_id(customer_id)
                id.stripe_customer_id = stripe_customer_id
            # id.stripe_token = token_id
                id.save()
            else:
                pass


            # create product and plan
            stripe_product_name = product_name()
            print(stripe_product_name)
            stripe_plan_id = plan_id(stripe_product_name)
            print(stripe_plan_id)

            print('i am in subscription mode')

            # stripe_customer_id = request.user.clientprofile.stripe_customer_id
            print(stripe_customer_id)

            def stripe_subscription(stripe_customer_id,stripe_plan_id,trainer_stripe_id):

                sub = stripe.Subscription.create(
                customer=stripe_customer_id,
                items=[
                    {
                    "plan": stripe_plan_id,
                    },
                ],
                application_fee_percent=1,
                stripe_account=trainer_stripe_id,
                )
                sub_id = sub.id
                return sub_id

            stripe_subscription_id = stripe_subscription(stripe_customer_id,stripe_plan_id,trainer_stripe_id)



    #     #Now Creating the Order
        try:
            order_details = Order.objects.create(
                    client_name = client_name,
                    trainer_name = trainer_name,
                    token = token,
                    total = total,
                    stripe_fee = stripe_fee,
                    platform_fee = platform_fee,
                    service_fee = service_fee,
                    net_pay = net_pay,
                    client_email = client_email,
                    trainer_email = trainer_email,
                    subscription = subscription,
                    stripe_subscription_id = stripe_subscription_id,
                    stripe_invoice_id = stripe_invoice_id,
                    stripe_product_name = stripe_product_name,
                    stripe_plan_id = stripe_plan_id,

            )
            order_details.save()

            for order_item in cart_items:
                oi = OrderItem.objects.create(
                        workout = workout_name,
                        sessions = sessions,
                        trainer_id = trainer_id,
                        client_id = client_id,
                        quantity = order_item.quantity,
                        price = order_item.workout.price,
                        order = order_details,
                        workout_description = workout_description,


                )
                oi.save()
                # the terminal will print confirmation
                print('order has been created')
            try:
                # Calling the sendEmail Function
                sendClientEmail(order_details.id)
                print('The order email has been sent')
                sendTrainerEmail(order_details.id)
            except IOError as e:
                return e

            # to get the sessions
            session_details = Session.objects.create(
                        client_id = client_id,
                        trainer_id = trainer_id,
                        order = order_details,
                        total_sessions = sessions,
                        workout_name = workout_name
            )
            session_details.save()

            for available_session in cart_items:
                a_s = AvailableSession.objects.create(
                        session = session_details,
                        available_sessions = available_session.workout.sessions,
                )
                a_s.save()




            return redirect('order:thanks', order_details.id)
        except ObjectDoesNotExist:
            pass
    #
    else:
        trainer_stripe_id = ''
        workout_name = ''


    context = {'data_key': data_key,'description':workout_name,'cart_items': cart_items, 'total': total,'stripe_total': stripe_total, 'counter': counter}
    return render(request,'cart/cart.html', context)



@login_required
def deleteItem(request,pk):
    cart_item = get_object_or_404(CartItem,pk=pk)
    cart_item.delete()
    return redirect('cart:cart_detail')

def sendClientEmail(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)
    try:
        # sending the order to customer
        subject = "Sweatsite - New Order #{}".format(transaction.id)
        to = ['{}'.format(transaction.client_email)]
        print(to)
        from_email = "orders@sweatsite.com"
        order_information = {
        'transaction': transaction,
        'order_items': order_items
        }
        message = get_template('email/client_email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e

def sendTrainerEmail(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)
    try:
        # sending the order to customer
        subject = "Sweatsite - New Order #{}".format(transaction.id)
        to = ['{}'.format(transaction.trainer_email)]
        print(to)
        from_email = "orders@sweatsite.com"
        order_information = {
        'transaction': transaction,
        'order_items': order_items
        }
        message = get_template('email/trainer_email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e
