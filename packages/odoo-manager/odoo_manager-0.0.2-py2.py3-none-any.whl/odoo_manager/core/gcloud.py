class ComputeInstance:
    """
    Helper class for connecting to GCloud compute instances. This will primarily
    be helpful when deploying applications to either staging or production
    servers.
    """

    def __init__(self, username, passfile):
        self.username = username
        self.passfile = passfile
