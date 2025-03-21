import logging
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
import crud
from db.database import SessionLocal
from services.user_service import decode_access_token
from core.security import is_unauthorized_url

logging.basicConfig(level=logging.INFO)

class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if is_unauthorized_url(request):
            return await call_next(request)

        token = request.headers.get("Authorization", None)
        if token is None:
            return JSONResponse(
                content={"detail": "Authentication header missing"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        claim = decode_access_token(token)
        logging.info(f"Decoded Token: {claim}")  # 🛑 Token Debug Log

        if claim is None:
            return JSONResponse(
                content={"detail": "Invalid authentication token."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        user_id = claim.get("id", None)
        if user_id is None:
            return JSONResponse(
                content={"detail": "Invalid authentication token."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        db = SessionLocal()
        try:
            logging.info(f"Fetching user with ID: {user_id}")  # 🛑 User Fetch Debug Log
            user = crud.user.get_by_id(db, user_id)  

            if not user:
                return JSONResponse(
                    content={"detail": "User not found."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            request.state.current_user = user
        except Exception as e:
            logging.error(f"Internal Server Error: {str(e)}")  # 🛑 Log Actual Error
            return JSONResponse(
                content={"detail": f"Internal server error: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            db.close()

        return await call_next(request)
