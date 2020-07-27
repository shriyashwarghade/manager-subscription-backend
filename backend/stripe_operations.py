import stripe

stripe.api_key = "sk_test_51H7kMmLGNTiPStWhmOEZp93xr2dlng1pPHU8KAqMJtlNtiN7Nb5nuwtnQVASxECTjnpxTeOQnNxg8XVQ6WiImkJ300UYlQHopv"


def get_plans_list():
    """
    :return: Fetch all the products from stripe and return array of products
    """
    try:
        return stripe.Price.list().get('data'), True
    except stripe.error.AuthenticationError as e:
        return str(e), False
    except stripe.error.RateLimitError as e:
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        return str(e), False
    except stripe.error.APIConnectionError as e:
        return str(e), False
    except stripe.error.StripeError as e:
        return e, False
    except Exception as e:
        return e, False


def get_card_by_id(user_id, card_id):
    """
    card_id: String
    :return: Return Card Details
    """
    try:
        return stripe.Customer.retrieve_source(user_id, card_id), True
    except stripe.error.AuthenticationError as e:
        return str(e), False
    except stripe.error.RateLimitError as e:
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        return str(e), False
    except stripe.error.APIConnectionError as e:
        return str(e), False
    except stripe.error.StripeError as e:
        return e, False
    except Exception as e:
        return e, False


def create_user_in_stripe(email_id):
    """
        email_id: String
        :return: Return Card Details
        """
    try:
        user = stripe.Customer.create(email=email_id)
        return user.stripe_id, True
    except stripe.error.AuthenticationError as e:
        return str(e), False
    except stripe.error.RateLimitError as e:
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        return str(e), False
    except stripe.error.APIConnectionError as e:
        return str(e), False
    except stripe.error.StripeError as e:
        return e, False
    except Exception as e:
        return e, False


def create_card_in_stripe(cust_id, card_number, exp_month, exp_year, cvv, ):
    """
    email_id: String
    :return: Return Card Details
    """
    try:
        card = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": int(exp_month),
                "exp_year": int(exp_year),
                "cvc": str(cvv),
            },
        )
        attach = stripe.PaymentMethod.attach(
            card.id,
            customer=cust_id,
        )
        # stripe.PaymentMethod.attach(card.id, customer=stripe_id)
        return card.id, True
    except stripe.error.AuthenticationError as e:
        return str(e), False
    except stripe.error.RateLimitError as e:
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        return str(e), False
    except stripe.error.APIConnectionError as e:
        return str(e), False
    except stripe.error.StripeError as e:
        return e, False
    except Exception as e:
        return e, False


def create_subscription_in_stripe(cust_id, payment_id, product_id):
    try:
        subscription = stripe.Subscription.create(
            customer=cust_id,
            default_payment_method=payment_id,
            items=[
                {"price": product_id},
            ],
        )
        return subscription.id, True
    except stripe.error.AuthenticationError as e:
        return str(e), False
    except stripe.error.RateLimitError as e:
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        return str(e), False
    except stripe.error.APIConnectionError as e:
        return str(e), False
    except stripe.error.StripeError as e:
        return e, False
    except Exception as e:
        return e, False


def delete_subscription_in_stripe(subscription_id):
    try:
        stripe.Subscription.delete(subscription_id)
        return '', True
    except stripe.error.AuthenticationError as e:
        return str(e), False
    except stripe.error.RateLimitError as e:
        return str(e), False
    except stripe.error.InvalidRequestError as e:
        return str(e), False
    except stripe.error.APIConnectionError as e:
        return str(e), False
    except stripe.error.StripeError as e:
        return e, False
    except Exception as e:
        return e, False
