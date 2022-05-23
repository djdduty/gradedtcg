from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal

from pypika import Query, Table


class TypedTable(Table):
    __table__ = ""

    def __init__(
        self,
        name: Optional[str] = None,
        schema: Optional[str] = None,
        alias: Optional[str] = None,
        query_cls: Optional[Query] = None,
    ) -> None:
        if name is None:
            if self.__table__:
                name = self.__table__
            else:
                name = self.__class__.__name__
        super().__init__(name, schema, alias, query_cls)


class Users(TypedTable):
    __table__ = "users"

    id: int
    username: str


class TCGs(TypedTable):
    __table__ = "tcgs"

    name_en: str


class Sets(TypedTable):
    __table__ = "sets"

    uuid: UUID
    tcg_id: int
    code: str
    name_en: str
    released_at: datetime


class Cards(TypedTable):
    __table__ = "cards"

    uuid: UUID
    tcg_id: int
    set_id: UUID
    collector_number: int
    name_en: str


class Collectibles(TypedTable):
    __table__ = "collectibles"

    id: int
    uuid: UUID
    owner_id: int

    is_card: bool  # False means this is likely a different kind of collectible
    is_graded: bool

    # Sealed product meta
    name: str
    description: str

    # Graded & Ungraded common meta
    card_id: UUID
    set_id: UUID

    # Ungraded meta
    quantity: int

    # Graded meta
    grade_overall: Decimal
    grade_centering: Decimal
    grade_corners: Decimal
    grade_edges: Decimal
    grade_surface: Decimal
    grade_signature: Decimal
    grade_org: str  # PSA or BGS
    grade_serial_no: str

    # Sharing meta
    is_shared: bool


users = Users()
tcgs = TCGs()
cards = Cards()
sets = Sets()