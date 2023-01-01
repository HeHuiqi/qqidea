from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'always'
    priority = 1.0
    protocol = 'http'
    

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)
    
    def lastmod(self,obj:Post):
        return obj.created_time
    def location(self, obj: Post) -> str:
        return reverse('post-detail',args=[obj.pk])