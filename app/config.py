from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    reset_token_expire_minutes:int

    mail_server:str
    mail_port:int
    mail_username:str
    mail_password:str
    mail_from:str
    mail_use_tls:bool
    front_end_url:str



    class Config:
        env_file = ".env"


settings = Settings()