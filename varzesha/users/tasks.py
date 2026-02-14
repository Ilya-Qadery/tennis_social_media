"""
Celery tasks for user-related async operations.
"""
from celery import shared_task
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_sms_verification_code(self, phone: str, code: str):
    """
    Send SMS verification code via Kavenegar.
    
    Args:
        phone: Iranian phone number
        code: 6-digit verification code
    """
    try:
        from kavenegar import KavenegarAPI, APIException, HTTPException
        
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            "receptor": phone,
            "template": "verify",
            "token": code,
            "type": "sms",
        }
        response = api.verify_lookup(params)
        return response
        
    except APIException as e:
        # Log error, don't retry on API errors
        print(f"Kavenegar API error: {e}")
        return None
    except HTTPException as e:
        # Retry on HTTP errors
        print(f"Kavenegar HTTP error: {e}")
        self.retry(countdown=60)
    except Exception as e:
        print(f"SMS sending error: {e}")
        self.retry(countdown=60)
