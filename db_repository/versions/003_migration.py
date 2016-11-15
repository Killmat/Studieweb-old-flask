from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
projects = Table('projects', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('filename', String(length=128)),
    Column('random_id', String(length=6)),
    Column('title', String(length=256)),
    Column('short_title', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['projects'].columns['short_title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['projects'].columns['short_title'].drop()
