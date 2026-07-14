from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings (BaseSettings):

     # Database
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
 
     # Authentication
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file= ".env",
        case_sensitive= True
    )
settings = Settings()