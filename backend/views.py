import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse


def products(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            from backend.stripe_operations import get_plans_list
            data = get_plans_list()
            if data[1]:
                return HttpResponse(json.dumps({'msg': data[0]}), status=200)
            else:
                return HttpResponse(json.dumps({'msg': data[0]}), status=412)
        else:
            return HttpResponse(json.dumps({'msg': "You Are Not Login To Portal."}), status=403)


def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        from backend.models import Manager
        db_data = Manager.objects.filter(email=data.get("email_id"))
        if db_data.count() > 0:
            return HttpResponse(json.dumps({"msg": "User Already Registered."}), status=406)
        else:
            from backend.stripe_operations import create_user_in_stripe
            user = create_user_in_stripe(data.get("email_id"))
            if not user[1]: return HttpResponse(json.dumps({"msg": "Error:{}".format(user[0])}), status=412)
            Manager(
                Manager.objects.all().count() + 1,
                data.get("email_id"),
                data.get("first_name"),
                data.get("last_name"),
                data.get("address"),
                data.get("dob"),
                data.get("company"),
                "",
                user[0]
            ).save()
            User.objects.create_superuser(username=data.get("email_id"), email=data.get("email_id"),
                                          password=data.get("password")).save()
            return HttpResponse(json.dumps({"msg": "Account Created Successfully"}), status=200)


def login_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data.get("email_id"), password=data.get("password"))
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({'msg': "Login Success.", "session_id": request.session.session_key}),
                                status=200)
        else:
            return HttpResponse(json.dumps({'msg': "User Id Or Password Incorrect."}), status=403)


def logout_request(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse(json.dumps({'msg': "User Logged Out."}), status=200)
        else:
            return HttpResponse(json.dumps({'msg': "User Already Logged Out."}), status=200)


def user_info(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            from backend.models import Manager
            user = list(Manager.objects.filter(email=request.user.email))[0]

            return HttpResponse(json.dumps({'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'dob': str(user.dob),
                'company': user.company,
                'product_id': user.product_id,
                'sub_id': user.sub_id,

            }}), status=200)
        else:
            return HttpResponse(json.dumps({'msg': "You Are Not Login To Portal."}), status=403)


def subscription(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            from backend.models import Manager, Subscription
            user = list(Manager.objects.filter(email=request.user.email))[0]
            subscription = list(Subscription.objects.filter(user_id=user.id))
            data_to_send = []
            for data in subscription:
                data_to_send.append({
                    "subscription_name": data.subscription_name,
                    "subscription_id": data.subscription_id,
                    "subscription_purchase_on": data.subscription_purchase_on,
                    "subscription_status": data.subscription_status,
                    "subscription_ended_on": data.subscription_ended_on
                })
            return HttpResponse(json.dumps({'subscription': data_to_send}), status=200)
        else:
            return HttpResponse(json.dumps({'msg': "You Are Not Login To Portal."}), status=403)
    elif request.method == 'POST':
        body = json.loads(request.body)
        if request.user.is_authenticated:
            from backend.models import Manager
            user = list(Manager.objects.filter(email=request.user.email))[0]
            from backend.stripe_operations import create_card_in_stripe
            card = create_card_in_stripe(user.stripe_user_id, body.get('card_number'), body.get('exp_month'),
                                         body.get('exp_year'), body.get('cvv'))
            if not card[1]: return HttpResponse(json.dumps({"msg": "Error:{}".format(card[0])}), status=412)
            user.card_number = str(body.get('card_number'))[12:]
            from backend.stripe_operations import create_subscription_in_stripe
            subscription = create_subscription_in_stripe(user.stripe_user_id, card[0], body.get("product_id"))
            if not subscription[1]: return HttpResponse(json.dumps({"msg": "Error:{}".format(subscription[0])}),
                                                        status=412)

            from backend.models import Subscription
            sub_id = Subscription.objects.all().count() + 1
            Subscription(
                sub_id,
                user.id,
                body.get("product_name"),
                subscription[0],
                str(datetime.now())[:19],
                "Active",
                "", ).save()
            user.sub_id = str(sub_id)
            user.product_id = body.get("product_id")
            user.save()
            return HttpResponse(json.dumps({'msg': "Subscription Successfully Completed."}), status=200)
        else:
            return HttpResponse(json.dumps({'msg': "You Are Not Login To Portal."}), status=403)
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            from backend.models import Manager,Subscription
            user = list(Manager.objects.filter(email=request.user.email))[0]
            subscription = list(Subscription.objects.filter(id=user.sub_id))[0]
            from backend.stripe_operations import delete_subscription_in_stripe
            delted_subscription = delete_subscription_in_stripe(subscription.subscription_id)
            if not delted_subscription[1]: return HttpResponse(json.dumps({"msg": "Error:{}".format(delted_subscription[0])}),
                                                        status=412)
            user.sub_id = ''
            user.product_id = ''
            user.save()
            subscription.subscription_status = "Deleted"
            subscription.subscription_ended_on = str(datetime.now())[:19]
            subscription.save()
            return HttpResponse(json.dumps({'msg': "Subscription Deleted Successfully."}), status=200)
        else:
            return HttpResponse(json.dumps({'msg': "You Are Not Login To Portal."}), status=403)
