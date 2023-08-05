
class CounterBase(object):
    title = None
    value = None
    style = None
    icon = None

    def get_title(self, request):
        return self.title
    
    def get_value(self, request):
        return self.value
    
    def get_style(self, request):
        return self.style if self.style else 'primary'
    
    def get_icon(self, request):
        return self.icon if self.icon else 'fa-user-circle'
