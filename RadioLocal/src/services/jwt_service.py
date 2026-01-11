import jwt
from fastapi import HTTPException, Depends, Header
from config import settings

def get_user_from_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        #print(payload)
        return payload.get("user_id")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing JWT: "+str(e)) from e
		
def get_company_from_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        company_id = payload.get("company_id")
        #print(type(company_id))
        if company_id is not None:
            return company_id
        else:
            return "1"
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing JWT: "+str(e)) from e