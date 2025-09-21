"""
core.Project

A project is an element of WorldInfo.  It encapsulates all the information about a project in Minecraft.  A project has the following data:

- Meta
    This is just information about the project.  It includes a name, a description, status, etc.
- Tasks
    To complete a job, normally you have a series of tasks.  Tasks are created and completed as the project progresses.
- Updates
    Sometimes a player might want to write something down about a project.  An update is a place to do that.  It's simply some text associated with the project.
- Resources
    A project might contain a number of outside the game resources.  I'm imagining this will mainly be litematics, but allowing stuff like audio files might be nice.


"""
from enum import Enum
from datetime import datetime

class Status(Enum):
    PENDING = 1
    PLANNING = 2
    ACTIVE = 3
    ON_HOLD = 4
    CANCELLED = 5
    COMPLETED = 6
    ARCHIVED = 7

class Project():

    def __init__(self):
        print('Initialized Project')
        self.project_id = 0
        self.title = ''
        self.description = ''
        self.start_date = None
        self.end_date = None
        self.status = Status.PENDING
        pass