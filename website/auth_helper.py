
from flask import Blueprint
from flask import current_app
from datetime import datetime, timedelta
import requests
from website.models.Admin_models import Admin
from website import db


auth_helper = Blueprint('auth_helper', __name__)

# Inside website/utils/oauth_helpers.py


def refresh_access_token(admin):
    """Refresh OAuth2 access token using the stored refresh token."""
    if not admin.oauth_refresh_token:
        return None

    refresh_data = {
        "client_id": current_app.config["OAUTH2_CLIENT_ID"],
        "client_secret": current_app.config["OAUTH2_CLIENT_SECRET"],
        "refresh_token": admin.oauth_refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(current_app.config["MICROSOFT_TOKEN_URL"], data=refresh_data)
    new_token_data = response.json()

    if "access_token" not in new_token_data:
        return None

    # Update user record with new tokens
    admin.oauth_token = new_token_data["access_token"]
    admin.oauth_refresh_token = new_token_data.get("refresh_token", admin.oauth_refresh_token)
    admin.oauth_token_expiry = datetime.now() + timedelta(seconds=new_token_data.get("expires_in", 3600))
    db.session.commit()

    return admin.oauth_token



