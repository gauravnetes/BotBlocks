from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from db.database import get_db
from db import models, schemas
from . import auth

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency verify token and return current user from DB.
    Creates user if they don't exist (JIT provisioning).
    """
    token = credentials.credentials
    payload = auth.verify_token(token)
    
    clerk_id = payload.get("sub")
    if not clerk_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user ID",
        )
            
    # ... (previous dependency code)
    
    # Check if user exists in DB
    user = db.query(models.User).filter(models.User.clerk_id == clerk_id).first()
    
    # Extract details from token first (fastest)
    email = payload.get("email")
    username = payload.get("username")
    
    # If not in top-level, check standard Clerk locations
    if not email and "email_addresses" in payload:
        emails = payload["email_addresses"]
        if isinstance(emails, list) and emails:
            email = emails[0].get("email_address")
            
    # FETCH FROM CLERK API if missing (Robust fallback)
    # We need CLERK_SECRET_KEY in backend .env for this to work
    import os
    import requests
    CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
    
    if (not email or not username) and CLERK_SECRET_KEY:
        try:
             # Fetch user from Clerk API
             headers = {"Authorization": f"Bearer {CLERK_SECRET_KEY}"}
             resp = requests.get(f"https://api.clerk.com/v1/users/{clerk_id}", headers=headers)
             if resp.status_code == 200:
                 clerk_user = resp.json()
                 
                 # Extract Email
                 if not email and clerk_user.get("email_addresses"):
                     # prioritized finding primary
                     primary_id = clerk_user.get("primary_email_address_id")
                     for e in clerk_user["email_addresses"]:
                         if e["id"] == primary_id:
                             email = e["email_address"]
                             break
                     if not email: # fallback to first
                         email = clerk_user["email_addresses"][0]["email_address"]
                         
                 # Extract Username
                 if not username:
                     username = clerk_user.get("username")
                     
        except Exception as e:
            print(f"Failed to fetch user from Clerk API: {e}")

    # Fallback if still missing
    if not email:
         email = f"{clerk_id}@clerk.user"
         
    if not user:
        # Create new user
        user = models.User(
            clerk_id=clerk_id,
            email=email,
            username=username
        )
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            # Handle race condition
            user = db.query(models.User).filter(models.User.clerk_id == clerk_id).first()
            if not user:
                raise HTTPException(status_code=500, detail="Failed to create user account")
    else:
        # Update existing user if info changed (Sync)
        changed = False
        if email and user.email != email and "@clerk.user" not in email:
            user.email = email
            changed = True
        if username and user.username != username:
            user.username = username
            changed = True
            
        if changed:
            try:
                db.commit()
                db.refresh(user)
            except:
                db.rollback()

    return user
