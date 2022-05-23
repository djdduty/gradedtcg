from typing import Optional

from app.models.domain.tcgmodel import TCGModel


class Profile(TCGModel):
    username: str
    bio: str = ""
    image: Optional[str] = None
