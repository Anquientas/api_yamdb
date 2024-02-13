from enum import Enum, unique


#  Enum: "user" "moderator" "admin"
@unique
class Role(Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'
