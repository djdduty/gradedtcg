from app.models.domain.tcgmodel import TCGModel


class TCGSchema(TCGModel):
    class Config(TCGModel.Config):
        orm_mode = True
