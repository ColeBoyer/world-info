"""
core.WorldInfo

Main WorldInfo class.  Contains the entire state of a WorldInfo project.  Will probably be broken down into constituent components as the project evolves.

Contains
- Meta Data: Stuff like world name, start date, etc.
- Projects: Start, end, status, description.
- Events: Same
"""

from core.project import Project

class WorldInfo():

    def __init__(self):
        proj = Project()
        print('Initialized WorldInfo')
        self.world_id = 0
        pass
