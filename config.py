import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///products.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Don’t track every object change internally — just save when I call commit()