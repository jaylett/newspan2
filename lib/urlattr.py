from django.core.urlresolvers import reverse, NoReverseMatch

class UrlAttr(object):
    
    def __init__(self, **urls):
        self.urls = urls
    
    def __get__(self, instance, cls):
        if instance is not None:
            return self.UrlAttrInner(instance, self.urls)
        else:
            return self.UrlAttrInner(cls, self.urls)
    
    class UrlAttrInner(object):
        
        def __init__(self, instance, urls):
            self.instance = instance
            self.urls = urls
        
        def __getattr__(self, name):
            name = self.urls[name]
            # First, try to get the fragment if there is one
            try:
                name, fragment = name.split("#", 1)
            except ValueError:
                fragment = None
            # Then, split on the =, if there is one
            try:
                name, pkfunc = name.split("=", 1)
            except ValueError:
                pkfunc = None
            # Generate it
            if pkfunc is not None:
                if pkfunc:
                    getter = getattr(self.instance, pkfunc)
                    if callable(getter):
                        url = reverse(name, args=[getter()])
                    else:
                        try:
                            url = reverse(name, args=[getter])
                        except NoReverseMatch:
                            url = reverse(name, kwargs={pkfunc: getter})
                else:
                    url = reverse(name, args=[self.instance.id])
            else:
                url = reverse(name)
            # Possibly add fragment
            if fragment:
                url += "#" + getattr(self.instance, fragment)()
            return url
        
        def __repr__(self):
            return repr(self.default)
        
        def __str__(self):
            return self.default
        
        def __unicode__(self):
            return self.default


class UrlAttrMixin(object):
        
    def get_absolute_url(self):
        return self.url.default
