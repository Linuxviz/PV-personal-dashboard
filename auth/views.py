from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.business.jwt_handler import sign_jwt
from auth.models import AdminSignIn, User, AdminData

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

async def add_admin(user: User) -> User:
    new_user = await user.create()
    return new_user


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn):
    user_exists = await User.find_one(User.email == admin_credentials.email)
    if user_exists:
        password = hash_helper.verify(
            admin_credentials.password, user_exists.password
        )
        if password:
            return sign_jwt(str(user_exists.id))

        raise HTTPException(
            status_code=403,
            detail="Incorrect email or password"
        )
    raise HTTPException(
        status_code=403,
        detail="Incorrect email or password"
    )


@router.post("/new", response_model=AdminData)
async def admin_signup(user: User = Body(...)):
    user_exists = await User.find_one(User.email == user.email)

    if user_exists:
        raise HTTPException(
            status_code=409,
            detail="Admin with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    new_user = await add_admin(user)
    return new_user
