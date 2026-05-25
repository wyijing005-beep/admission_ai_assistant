from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User, UserProfile
from app.models.schemas import UserProfileRequest, UserProfileResponse
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/user/profile", response_model=UserProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile is None:
        return UserProfileResponse()
    return UserProfileResponse(
        province=profile.province,
        gaokao_score=profile.gaokao_score,
        gaokao_year=profile.gaokao_year,
        subject_type=profile.subject_type,
        interested_majors=profile.interested_majors,
    )


@router.put("/user/profile", response_model=UserProfileResponse)
def update_profile(
    request: UserProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile is None:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return UserProfileResponse(
        province=profile.province,
        gaokao_score=profile.gaokao_score,
        gaokao_year=profile.gaokao_year,
        subject_type=profile.subject_type,
        interested_majors=profile.interested_majors,
    )
