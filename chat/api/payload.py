from datetime import datetime
from graphql_jwt.settings import jwt_settings


def jwt_payload(user, context=None):
    jwt_datetime = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    jwt_expires = int(jwt_datetime.timestamp())
    payload = {
        'username': user.username,
        'pk': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'exp': jwt_expires,

        # 'https://hasura.io/jwt/claims': {}
    }
    # payload['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] = [user.profile.role]
    # payload['https://hasura.io/jwt/claims']['x-hasura-default-role'] = user.profile.role
    # payload['https://hasura.io/jwt/claims']['x-hasura-user-id'] = str(user.id)
    return payload

