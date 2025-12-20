import os
import json
import secrets
import string
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import stripe

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_key_here")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_your_webhook_secret_here")
LICENSE_STORE_PATH = Path(os.getenv("LICENSE_STORE_PATH", "licenses.json")).resolve()

stripe.api_key = STRIPE_SECRET_KEY

app = FastAPI(title="FileGenius License Backend")


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def _load_licenses() -> dict:
    if LICENSE_STORE_PATH.exists():
        try:
            return json.loads(LICENSE_STORE_PATH.read_text())
        except Exception:
            return {}
    return {}


def _save_licenses(data: dict) -> None:
    LICENSE_STORE_PATH.write_text(json.dumps(data, indent=2))


def _generate_license_key(length: int = 32) -> str:
    alphabet = string.ascii_uppercase + string.digits
    # Group into XXXX-XXXX-... blocks for readability
    raw = "".join(secrets.choice(alphabet) for _ in range(length))
    blocks = [raw[i : i + 4] for i in range(0, len(raw), 4)]
    return "-".join(blocks[:4])  # 4 blocks of 4 chars (16 visible chars)


# ----------------------------------------------------------------------------
# Public API used by FileGenius
# ----------------------------------------------------------------------------

@app.get("/validate")
async def validate_license(key: str):
    """Endpoint used by FileGenius to validate a license key.

    Returns JSON: {"valid": bool}
    """
    data = _load_licenses()
    record = data.get(key)
    if record and record.get("active", False):
        return {"valid": True}
    return {"valid": False}


# ----------------------------------------------------------------------------
# Stripe webhook: create & store license keys after successful checkout
# ----------------------------------------------------------------------------

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except Exception as exc:  # broad but fine for webhook
        raise HTTPException(status_code=400, detail=f"Webhook error: {exc}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = (session.get("customer_details") or {}).get("email")

        # Generate and store license key
        key = _generate_license_key()
        data = _load_licenses()
        data[key] = {
            "active": True,
            "stripe_session_id": session.get("id"),
            "customer_email": customer_email,
        }
        _save_licenses(data)

        # In a real deployment, you would also email the key to customer_email
        # or show it on a success page. For now, we just persist it server-side.

    return JSONResponse({"received": True})


# ----------------------------------------------------------------------------
# Simple admin/debug endpoint (optional)
# ----------------------------------------------------------------------------

@app.get("/licenses/{email}")
async def list_licenses_for_email(email: str):
    """Return all licenses associated with a given email (for support/debug)."""
    data = _load_licenses()
    matches = [k for k, v in data.items() if (v.get("customer_email") or "").lower() == email.lower()]
    return {"email": email, "licenses": matches}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("stripe_server:app", host="0.0.0.0", port=8000, reload=True)
