from decouple import config


class ProductionConfig:
    FLASK_ENV = "prod"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )
