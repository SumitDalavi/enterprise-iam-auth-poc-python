"""TOTP-based MFA (RFC 6238). Compatible with Google Authenticator and Authy."""
from __future__ import annotations
import base64, hashlib, hmac, os, struct, time
from typing import Optional


def generate_totp_secret() -> str:
    """Generate a random 20-byte base32-encoded TOTP secret."""
    return base64.b32encode(os.urandom(20)).decode().rstrip("=")


def hotp(secret: str, counter: int, digits: int = 6) -> str:
    """HMAC-based OTP (HOTP) — base for TOTP."""
    key = base64.b32decode(secret.upper() + "=" * ((8 - len(secret) % 8) % 8))
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF
    return str(code % (10 ** digits)).zfill(digits)


def totp(secret: str, step: int = 30, digits: int = 6) -> str:
    """Current TOTP value for the given secret."""
    counter = int(time.time() // step)
    return hotp(secret, counter, digits)


def verify_totp(secret: str, code: str, step: int = 30, tolerance: int = 1) -> bool:
    """
    Verify a TOTP code with clock-drift tolerance.
    tolerance=1 allows codes from the previous and next time step.
    """
    counter = int(time.time() // step)
    for i in range(-tolerance, tolerance + 1):
        if hmac.compare_digest(hotp(secret, counter + i), code):
            return True
    return False


def totp_provisioning_uri(secret: str, email: str, issuer: str = "Enterprise IAM") -> str:
    """Generate an otpauth:// URI for QR code generation."""
    from urllib.parse import quote
    return f"otpauth://totp/{quote(issuer)}:{quote(email)}?secret={secret}&issuer={quote(issuer)}&algorithm=SHA1&digits=6&period=30"
