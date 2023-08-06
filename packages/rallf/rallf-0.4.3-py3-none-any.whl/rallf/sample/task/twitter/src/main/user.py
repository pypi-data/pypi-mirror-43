

class User:
    def __init__(self, username, is_follower, is_following, follow_button=None):
        self.isFollowing = is_following
        self.isFollower = is_follower
        self.username = username
        self.followButton = follow_button

    def to_json(self):
        return "{}"
