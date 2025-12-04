"""Payment and subscription endpoints for Genius AI"""
import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import stripe

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_YOUR_KEY_HERE")

router = APIRouter(prefix="/api/payments", tags=["payments"])


class SubscriptionRequest(BaseModel):
    plan: str  # 'pro' or 'enterprise'
    payment_method_id: str
    email: str


class SubscriptionResponse(BaseModel):
    subscription_id: str
    client_secret: str
    status: str


@router.post("/create-subscription", response_model=SubscriptionResponse)
async def create_subscription(request: SubscriptionRequest):
    """Create a new Stripe subscription"""
    try:
        # Price IDs (you'll need to create these in Stripe Dashboard)
        price_ids = {
            "pro": os.getenv("STRIPE_PRICE_ID_PRO", "price_pro_monthly"),
            "enterprise": os.getenv("STRIPE_PRICE_ID_ENTERPRISE", "price_enterprise_monthly")
        }

        if request.plan not in price_ids:
            raise HTTPException(status_code=400, detail="Invalid plan")

        # Create or retrieve customer
        customer = stripe.Customer.create(
            payment_method=request.payment_method_id,
            email=request.email,
            invoice_settings={
                "default_payment_method": request.payment_method_id,
            },
        )

        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price_ids[request.plan]}],
            expand=["latest_invoice.payment_intent"],
        )

        return SubscriptionResponse(
            subscription_id=subscription.id,
            client_secret=subscription.latest_invoice.payment_intent.client_secret,
            status=subscription.status,
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel-subscription")
async def cancel_subscription(subscription_id: str):
    """Cancel an existing subscription"""
    try:
        subscription = stripe.Subscription.delete(subscription_id)
        return {
            "success": True,
            "subscription_id": subscription.id,
            "status": subscription.status
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/subscription/{subscription_id}")
async def get_subscription(subscription_id: str):
    """Get subscription details"""
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "current_period_end": subscription.current_period_end,
            "cancel_at_period_end": subscription.cancel_at_period_end,
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=404, detail="Subscription not found")


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle events
    if event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        # TODO: Update database with new subscription

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        # TODO: Update subscription status in database

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # TODO: Mark subscription as cancelled in database

    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        # TODO: Handle failed payment

    return {"success": True}


@router.get("/config")
async def get_stripe_config():
    """Get Stripe publishable key for frontend"""
    return {
        "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_YOUR_KEY_HERE")
    }
