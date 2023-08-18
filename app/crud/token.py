from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt

from app.schemas import token as token_schemas

ACCESS_TOKEN_SECRET_KEY = 'eyJhbGciOiJIUzI1NiJ9' \
                          '.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI' \
                          '6MTY3MDgyODA2MywiaWF0IjoxNjcwODI4MDYzfQ.DJNvGj5c4rLRolPT1lIfKVsNqSdk3JAPp62ivufzxhI'

REFRESH_TOKEN_SECRET_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6Ikphdm' \
                           'FJblVzZSIsImV4cCI6MTY3MDgyODA2MywiaWF0IjoxNjcwODI4MDYzfQ.MA2SMrH_N2kKGwJmUQyNiHV88avtUlMsT' \
                           '2wG8M2Btcc'

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 3


def create_access_token(
        data: dict,
        access_token_expire_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token_expire_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
):  # -> token_schemas.Token
    access_encode = data.copy()
    refresh_encode = data.copy()

    if access_token_expire_delta:
        access_expire = datetime.utcnow() + access_token_expire_delta
    else:
        access_expire = datetime.utcnow() + timedelta(minutes=15)

    if refresh_token_expire_delta:
        refresh_expire = datetime.utcnow() + refresh_token_expire_delta
    else:
        refresh_expire = datetime.utcnow() + timedelta(days=1)

    access_encode.update({'exp': access_expire})

    access_encoded_jwt = jwt.encode(access_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

    refresh_encode.update({'exp': refresh_expire})
    refresh_encoded_jwt = jwt.encode(refresh_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

    return token_schemas.TokenQuery(access_token=access_encoded_jwt, refresh_token=refresh_encoded_jwt,
                                    user=data['user'])


def create_refresh_token(token: str, username: str):
    try:
        payload = jwt.decode(token=token, key=REFRESH_TOKEN_SECRET_KEY)

        if datetime.utcfromtimestamp(payload.get('exp')) > datetime.now() and username == \
                payload.get('user').get('username'):
            return create_access_token(data={'sub': username, 'user': payload.get('user')})

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired',
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired',
            headers={"WWW-Authenticate": "Bearer"},
        )
