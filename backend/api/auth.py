import os
import logging
from typing import Optional, Dict, Any
import jwt
from jwt.algorithms import RSAAlgorithm
import requests
from fastapi import HTTPException, status

logger = logging.getLogger("Auth")

# Try to get JWKS URL from env, or construct it from Issuer
CLERK_ISSUER = os.getenv("CLERK_ISSUER_URL") 
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

# Cache keys to avoid fetching on every request
_jwks_cache: Dict[str, Any] = {}

def get_jwks_url():
    if CLERK_JWKS_URL:
        return CLERK_JWKS_URL
    if CLERK_ISSUER:
        return f"{CLERK_ISSUER}/.well-known/jwks.json"
    raise ValueError("Missing CLERK_ISSUER_URL or CLERK_JWKS_URL in environment")

def get_public_key(kid: str):
    global _jwks_cache
    
    # Check cache first
    if kid in _jwks_cache:
        return _jwks_cache[kid]
    
    # Fetch from Clerk
    try:
        url = get_jwks_url()
        logger.info(f"Fetching JWKS from {url}")
        response = requests.get(url)
        response.raise_for_status()
        jwks = response.json()
        
        for key in jwks["keys"]:
            if key["kid"] == kid:
                public_key = RSAAlgorithm.from_jwk(key)
                _jwks_cache[kid] = public_key
                return public_key
                
    except Exception as e:
        logger.error(f"Failed to fetch JWKS: {e}")
        
    return None

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify Clerk JWT token and return payload.
    """
    try:
        # Get Header to find Key ID (kid)
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header",
            )
            
        public_key = get_public_key(kid)
        if not public_key:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key",
            )
        
        # Verify Token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            # Verify audience if needed, usually Clerk doesn't mandate it for basic usage unless configured
            options={"verify_aud": False} 
        )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
