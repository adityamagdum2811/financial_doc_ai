from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.deps import get_current_user, require_role

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/create")
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))
):
    existing = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = models.Role(name=role.name, permissions=role.permissions)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {"message": "Role created", "role_id": new_role.id}


@router.post("/assign-role")
def assign_role(
    payload: schemas.AssignRole,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))
):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    role = db.query(models.Role).filter(models.Role.id == payload.role_id).first()

    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")

    if role not in user.roles:
        user.roles.append(role)
        db.commit()

    return {"message": f"Role '{role.name}' assigned to user '{user.username}'"}


@router.get("/users/{user_id}/roles")
def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user": user.username, "roles": [role.name for role in user.roles]}


@router.get("/users/{user_id}/permissions")
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": user.username,
        "permissions": {role.name: role.permissions for role in user.roles}
    }