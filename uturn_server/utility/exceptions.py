class ProjectDoesntExistError(Exception):
    """
        Project provided to Project class doesn't exist. Thus, either the path in config.json
        is wrong or the name.
    """
    pass

class InvalidHashError(Exception):
    """
        Hash provided to the gitutility isn't that of a valid commit for the project.
    """
    pass