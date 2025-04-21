This is a simple API with flask that use jwt authentications 
to run you must have your .env file to run  ths API with the following con figuratio
SECRETE_KEY = 
DATABASE_URL = 
JWT_SECRETE_KEY = 
SQLALCHEMY_TRACK_MODIFICATION = False
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
