import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:blacklights3638@localhost:3306/weather_app_backend"
    SQLALCHEMY_TRACK_MODIFICATIONS = False