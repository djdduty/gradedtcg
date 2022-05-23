from fastapi import APIRouter, Depends

from app.api.dependencies.profiles import get_profile_by_username_from_path
from app.models.domain.profiles import Profile
from app.models.schemas.profiles import ProfileInResponse

router = APIRouter()


@router.get(
    "/{username}",
    response_model=ProfileInResponse,
    name="profiles:get-profile",
)
async def retrieve_profile_by_username(
    profile: Profile = Depends(get_profile_by_username_from_path),
) -> ProfileInResponse:
    return ProfileInResponse(profile=profile)
