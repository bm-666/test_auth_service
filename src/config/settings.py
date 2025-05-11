from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


PRODUCTION = False
BASE_DIR = Path(__file__).parent.parent # Базовая дериктория
ENV_FILE = ".env.prod" if PRODUCTION else ".env.dev"
ENV_FILE_PATH = str(BASE_DIR.joinpath(ENV_FILE))
print(ENV_FILE_PATH)

class Settings(BaseSettings):
    PSQL_DB: str
    PSQL_USER: str
    PSQL_PASS: str
    PSQL_PORT: str
    PSQL_HOST: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH
    )

    def get_psql_async_connect_url(self) -> str:
        return f"postgresql+asyncpg://{self.PSQL_USER}:{self.PSQL_PASS}@{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_DB}"

settings = Settings()