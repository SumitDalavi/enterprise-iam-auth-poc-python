"""SCIM 2.0 user provisioning endpoints (RFC 7644)."""
from __future__ import annotations
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/scim/v2", tags=["SCIM"])

# In-memory user store (replace with DB in production)
_users: dict = {}


class ScimUser(BaseModel):
    userName: str
    displayName: Optional[str] = None
    emails: list = []
    active: bool = True
    externalId: Optional[str] = None


class ScimPatchOp(BaseModel):
    Operations: list  # [{op: "replace", path: "active", value: False}]


def _format_user(user_id: str, user: dict) -> dict:
    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": user_id,
        "userName": user["userName"],
        "displayName": user.get("displayName", user["userName"]),
        "emails": user.get("emails", []),
        "active": user.get("active", True),
        "meta": {"resourceType": "User", "location": f"/scim/v2/Users/{user_id}"},
    }


@router.get("/Users")
def list_users():
    resources = [_format_user(uid, u) for uid, u in _users.items()]
    return {"schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": len(resources), "Resources": resources}


@router.get("/Users/{user_id}")
def get_user(user_id: str):
    if user_id not in _users:
        raise HTTPException(404, "User not found")
    return _format_user(user_id, _users[user_id])


@router.post("/Users", status_code=201)
def create_user(user: ScimUser):
    user_id = str(uuid.uuid4())
    _users[user_id] = user.dict()
    return _format_user(user_id, _users[user_id])


@router.put("/Users/{user_id}")
def replace_user(user_id: str, user: ScimUser):
    if user_id not in _users:
        raise HTTPException(404, "User not found")
    _users[user_id] = user.dict()
    return _format_user(user_id, _users[user_id])


@router.patch("/Users/{user_id}")
def patch_user(user_id: str, patch: ScimPatchOp):
    if user_id not in _users:
        raise HTTPException(404, "User not found")
    for op in patch.Operations:
        if op.get("op") == "replace":
            path = op.get("path", "")
            value = op.get("value")
            if path in _users[user_id]:
                _users[user_id][path] = value
    return _format_user(user_id, _users[user_id])


@router.delete("/Users/{user_id}", status_code=204)
def delete_user(user_id: str):
    if user_id not in _users:
        raise HTTPException(404, "User not found")
    del _users[user_id]
