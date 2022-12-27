from django.contrib.admin import AdminSite

# 自定义管理后台首页，可以定义多个
class CustomSite(AdminSite):
    site_header = 'QQidea管理后台'
    site_title = 'QQidea管理后台'
    index_title = '首页'

custom_site = CustomSite(name='custom_admin')