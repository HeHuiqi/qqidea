
from .base import * #NOQA
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qqidea_db',
        'USER':'root',
        'PASSWORD':'h12345678',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        # 最大链接时长
        'CONN_MAX_AGE': 5*60,
        'OPTIONS':{
            # 支持emoji字符
            'charset':'utf8mb4'
        }
    }
}

