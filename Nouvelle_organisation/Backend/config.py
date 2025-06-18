class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://dev:1234@localhost/ifri_comotorage"

    JWT_SECRET_KEY = 'votre_clé_secrète_super_sécurisée'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORS_API_KEY = '5b3ce3597851110001cf624830dd089e936245beaae668bc47a6b315'
    SECRET_KEY = 'clé_très_secrète'