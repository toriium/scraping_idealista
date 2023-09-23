import time

from data.db_orm.connection import get_writing_db_url
from alembic.config import Config
from alembic import command
from settings import BASE_DIR


def init_database():
    for _ in range(5):
        time.sleep(1)
        try:
            path = f"{BASE_DIR}/data/db_orm/alembic"
            alembic_cfg = Config()
            alembic_cfg.set_main_option("script_location", path)
            alembic_cfg.set_main_option("sqlalchemy.url", get_writing_db_url())
            command.upgrade(alembic_cfg, "head")
            break
        except:
            ...


if __name__ == '__main__':
    init_database()
