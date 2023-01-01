from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        handler.addQuickElement('content:html',item['content_html'])
        return super().add_item_elements(handler, item)

from .models import Post

class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed
    title = 'QiQiIdea Blog'
    link = '/rss/'
    description = 'QiQiIdea is a blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]
    
    def item_title(self, item:Post):
        return item.title

    def item_description(self, item: Post) -> str:
        return item.description
    
    def item_link(self, item: Post) -> str:
        return reverse('post-detail',args=[item.pk])


    def item_extra_kwargs(self, item: Post):
        return {'content_html':self.item_content_html(item=item)}
        
    def item_content_html(self,item:Post):
        return item.content_html