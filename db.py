import databases
import sqlalchemy
from settings import settings

db = databases.Database(settings.DATABASE_URL)
mdt = sqlalchemy.MetaData()
users_db = sqlalchemy.Table("users", mdt,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("name", sqlalchemy.String(32)),
                            sqlalchemy.Column("surname", sqlalchemy.String(64)),
                            sqlalchemy.Column("password", sqlalchemy.String(64)),
                            sqlalchemy.Column("email", sqlalchemy.String(128)),
                            )

goods_db = sqlalchemy.Table("goods", mdt,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("name", sqlalchemy.String(32)),
                            sqlalchemy.Column("description", sqlalchemy.String(1000)),
                            sqlalchemy.Column("price", sqlalchemy.Integer),
                            )

offers_db = sqlalchemy.Table("offers", mdt,
                             sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                             sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                               nullable=False),
                             sqlalchemy.Column("good_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('goods.id'),
                                               nullable=False),
                             sqlalchemy.Column("status", sqlalchemy.Boolean),
                             sqlalchemy.Column("cur_time", sqlalchemy.DateTime),
                             )

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False})
mdt.create_all(engine)
