from __future__ import annotations

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from nacl.signing import VerifyKey
from loguru import logger as log

__all__ = ("VerificationMiddleware",)


class VerificationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, client_public_key: str) -> None:
        super().__init__(app)
        self.client_public_key = client_public_key
        self.verification_key = VerifyKey(bytes.fromhex(self.client_public_key))

    def verify_request(self, passed_signature: str, passed_timestamp: str, body: bytes):
        signature = passed_signature
        timestamp = passed_timestamp
        message = timestamp.encode() + body

        try:
            self.verification_key.verify(message, bytes.fromhex(signature))
        except Exception as e:
            log.error(e)
            return False, 401

        else:
            return True, 200

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        log.debug("Intercepting request.")
        if request.url.path == "/ping":
            log.info("Ping forwarding.")
            return await call_next(request)

        try:
            signature = request.headers["X-Signature-Ed25519"]
            timestamp = request.headers["X-Signature-Timestamp"]
            body = await request.body()
        except Exception as e:
            log.error("Incorrect request")
            return JSONResponse(
                status_code=400, content={"error_message": "Incorrect request."}
            )

        else:
            status_bool, status_code = self.verify_request(signature, timestamp, body)
            if status_bool:
                log.success("Approved request.")
                return await call_next(request)
            return JSONResponse(
                status_code=status_code, content="Something went wrong."
            )
