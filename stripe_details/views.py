from django.shortcuts import render, redirect
# from gym.models import User,TrainerProfile
from .models import StripeDetail, Individual, Company, ExternalAccount
from .forms import IndividualForm, CompanyForm, ExternalAccountForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
import requests
from django.conf import settings

import json
import stripe

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY



# @login_required
# def stripe_register(request):
#     # get stripe id public and secret key
#     if (request.GET.get('stripe_register')):
#         user_id = request.user.id
#         import time
#         def createStripeAcct():
#             acct = stripe.Account.create(
#                 country="GB",
#                 type="custom"
#                 )
#             # print(acct.items)
#             # acct_id = acct.id
#             # print(acct.id)
#             # acct.legal_entity.dob.day = 8
#             # acct.legal_entity.dob.month = 7
#             # acct.legal_entity.dob.year = 1992
#             acct_keys = acct.items
#             # print(acct.items())
#             for x, y in acct_keys():
#                 print(x,y)
#             #     if x == 'keys':
#             #         pub = y['publishable']
#             #         sec = y['secret']
#             return
#
#     createStripeAcct()
#     # acct = stripe.Account.retrieve('acct_1DUJvLAO3xaCPEYY')
#     # print(acct)





@login_required
def stripe_register(request):
    # get stripe id public and secret key
    if (request.GET.get('stripe_register')):
        user_id = request.user.id

        def createStripeAcct():
            acct = stripe.Account.create(
                country="GB",
                type="custom"
                )
            acct_id = acct.id
            acct_keys = acct.items
            for x, y in acct_keys():
                if x == 'keys':
                    pub = y['publishable']
                    sec = y['secret']
            return acct_id, pub, sec


        stripe_deets = createStripeAcct()


        try:
            stripe_details = StripeDetail.objects.create(
                user = request.user,
                name = request.user.trainerprofile.name,
                stripe_id = stripe_deets[0],
                stripe_pub_key = stripe_deets[1],
                stripe_secret_key = stripe_deets[2],
            )
            stripe_details.save()
            return redirect('stripe:stripe_legal_type')

        except IOError as e:
                return e


    else:

        print('nothing to see here')
        pass


    return render(request, 'stripe_details/stripe_register.html')



@login_required
def stripe_legal_type(request):
    user_id = request.user.id
    stripe_detail = StripeDetail.objects.get(user=user_id)


    if (request.GET.get('individual')):
        stripe_detail.legal_entity_type = 'individual'
        stripe_detail.save()

        return redirect('stripe:stripe_individual')
    elif (request.GET.get('company')):
        stripe_detail.legal_entity_type = 'company'
        stripe_detail.save()
        return redirect('stripe:stripe_company')



    return render(request, 'stripe_details/stripe_legal_type.html')



@login_required
def stripe_individual(request):
    user_id = request.user.id

    # make this a global variable
    stripe_detail = StripeDetail.objects.get(user=user_id)

    # to get the users stripe account id
    stripe_account = stripe_detail.stripe_id

    # function to send verification data to stripe
    def send_to_stripe(stripe_detail):
        individual = Individual.objects.get(stripe_detail=stripe_detail)

        import time
        acct = stripe.Account.retrieve(stripe_account)

        acct.legal_entity.address.city = individual.legal_entity_address_city
        acct.legal_entity.address.line1 = individual.legal_entity_address_line1
        acct.legal_entity.address.postal_code = individual.legal_entity_address_postal_code
        acct.legal_entity.dob.day = individual.legal_entity_dob_day
        acct.legal_entity.dob.month = individual.legal_entity_dob_month
        acct.legal_entity.dob.year = individual.legal_entity_dob_year
        acct.legal_entity.first_name = individual.legal_entity_first_name
        acct.legal_entity.last_name = individual.legal_entity_last_name
        acct.legal_entity.type = 'individual'

        acct.tos_acceptance.date = int(time.time())
        acct.tos_acceptance.ip = '8.8.8.8' #TO BE REWORKED
        acct.save()
        print(acct)


    if request.method == 'POST':
        form = IndividualForm(request.POST)

        if form.is_valid():
            individual = form.save()
            individual.stripe_detail = stripe_detail
            individual.save()

            send_to_stripe(stripe_detail)

            return redirect('stripe:external_account')
    else:
        form = IndividualForm()

    context = {'form': form}
    return render(request,'stripe_details/stripe_individual.html', context)



@login_required
def stripe_company(request):
    user_id = request.user.id

    # make this a global variable
    stripe_detail = StripeDetail.objects.get(user=user_id)

    # to get the users stripe account id
    stripe_account = stripe_detail.stripe_id

    # function to send verification data to stripe
    def send_to_stripe(stripe_detail):
        company = Company.objects.get(stripe_detail=stripe_detail)

        import time
        acct = stripe.Account.retrieve(stripe_account)

        acct.legal_entity.dob.day = company.legal_entity_dob_day
        acct.legal_entity.dob.month = company.legal_entity_dob_month
        acct.legal_entity.dob.year = company.legal_entity_dob_year
        acct.legal_entity.first_name = company.legal_entity_first_name
        acct.legal_entity.last_name = company.legal_entity_last_name

        acct.legal_entity.address.city = company.legal_entity_address_city
        acct.legal_entity.address.line1 = company.legal_entity_address_line1
        acct.legal_entity.address.postal_code = company.legal_entity_address_postal_code
        acct.legal_entity.business_name = company.legal_entity_business_name
        acct.legal_entity.business_tax_id  = company.legal_entity_type_business_tax_id
        acct.legal_entity.personal_address.city = company.legal_entity_personal_address_city
        acct.legal_entity.personal_address.line1 = company.legal_entity_personal_address_line1
        acct.legal_entity.personal_address.postal_code = company.legal_entity_personal_address_postal_code

        acct.legal_entity.type = 'company'

        acct.tos_acceptance.date = int(time.time())
        acct.tos_acceptance.ip = '8.8.8.8' #TO BE REWORKED
        acct.save()
        print(acct)

    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save()
            company.stripe_detail = stripe_detail
            company.save()

            send_to_stripe(stripe_detail)

            return redirect('stripe:external_account')
    else:
        form = CompanyForm()

    context = {'form': form}
    return render(request,'stripe_details/stripe_company.html', context)


def external_account(request):
    user_id = request.user.id

    # make this a global variable
    stripe_detail = StripeDetail.objects.get(user=user_id)

    # to get the users stripe account id
    stripe_account = stripe_detail.stripe_id


    object = 'bank_account'
    country = 'GB'
    currency = 'gbp'
    # external_account.object = object
    # external_account.country = country
    # external_account.currency = currency
    # external_account.account_holder_type = stripe_detail.legal_entity_type


    def send_to_stripe(stripe_detail):
        external_account = ExternalAccount.objects.get(stripe_detail=stripe_detail)

        account_holder_name = external_account.account_holder_name
        account_holder_type = stripe_detail.legal_entity_type
        account_number = external_account.account_number
        routing_number = external_account.routing_number

        import time
        acct = stripe.Account.retrieve(stripe_account)
        acct.external_accounts.create(
            external_account = {
                'object': object,
                'country': country,
                'currency': currency,
                'account_holder_name':account_holder_name,
                'account_holder_type': account_holder_type,
                'account_number': account_number,
                'routing_number': routing_number

            }

        )


        acct.save()
        print(acct)



    if request.method == 'POST':
        form = ExternalAccountForm(request.POST)

        if form.is_valid():
            account = form.save()
            account.stripe_detail = stripe_detail
            account.object = object
            account.country = country
            account.currency = currency
            account.account_holder_type = stripe_detail.legal_entity_type
            account.save()

            send_to_stripe(stripe_detail)


            return redirect('/')
    else:
        form = ExternalAccountForm()




    context = {'form': form}
    return render(request,'stripe_details/stripe_external_account.html', context)




@require_POST
@csrf_exempt
def stripe_webhooks(request):

    # Retrieve the request's body and parse it as JSON:
    details = json.loads(request.body)
    # print(details)
    print(details['type'])


    # Do something with event_json

    return HttpResponse(status=200)








    #
