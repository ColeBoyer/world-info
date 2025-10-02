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
    description: so.Mapped[str] = so.mapped_column(sa.String(280), default='')
    creation_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda : datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    owner: so.Mapped[User] = so.relationship(back_populates='worlds')
    projects: so.WriteOnlyMapped['Project'] = so.relationship(back_populates='world')

    def update_description(self, updated_description):
        world = db.session.execute(db.select(World).filter_by(id=self.id)).scalar_one()
        world.description = updated_description
        db.session.commit()

    def __repr__(self):
        return f"<World: {self.name} - {self.creation_date} - Description:{self.description}>"

class WorldUpdate(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    world_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(World.id), index=True)
    text: so.Mapped[str] = so.mapped_column(sa.Text())

    def __repr__(self):
        return f"<WorldUpdate - uid:{self.user_id} - wid:{self.world_id} - text:{self.text}>"

class WorldEvent(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    world_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(World.id), index=True)

class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[str] = so.mapped_column(sa.String(280))
    creation_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    world_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(World.id), index=True)

    world: so.Mapped[World] = so.relationship(back_populates='projects')

    def update_description(self, updated_description):
        project = db.session.execute(db.select(Project).filter_by(id=self.id)).scalar_one()
        project.description = updated_description
        db.session.commit()

    def __repr__(self):
        return f"<Project {self.name}, {self.description}>"

class ProjectUpdate(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    world_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(World.id), index=True)
    project_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Project.id), index=True)
    text: so.Mapped[str] = so.mapped_column(sa.Text())

    def __repr__(self):
        return f"<ProjectUpdate - uid:{self.user_id} - wid:{self.world_id} - text:{self.text}>"

'''
#Figure out how to handle events before creating.
#I.e., are we storing them as an enum, str, etc.
class ProjectEvent(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    world_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(World.id), index=True)
    project_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Project.id), index=True)
    event: so.Mapped[???]
'''

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))



'''
static/textures/
repeating-command-block-conditional
block/trial-spawner-top-ejecting-reward-ominous
'''