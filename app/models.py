from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    icon: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    worlds: so.WriteOnlyMapped['World'] = so.relationship(back_populates='owner')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f"<Post {self.body}>"

class World(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    creation_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda : datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    owner: so.Mapped[User] = so.relationship(back_populates='worlds')
    projects: so.WriteOnlyMapped['Project'] = so.relationship(back_populates='world')

    def __repr__(self):
        return f"<World: {self.name}, Creation Date: {self.creation_date}, User_ID: {self.user_id}>"

class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[str] = so.mapped_column(sa.String(280))
    creation_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    world_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(World.id), index=True)

    world: so.Mapped[World] = so.relationship(back_populates='projects')

    def __repr__(self):
        return f"<Project {self.name}, {self.description}>"

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))



'''
static/textures/
repeating-command-block-conditional
block/trial-spawner-top-ejecting-reward-ominous
'''