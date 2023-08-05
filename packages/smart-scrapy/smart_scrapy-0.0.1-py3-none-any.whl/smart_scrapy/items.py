import scrapy


class SmartItem(scrapy.Item):

    def __init__(self, *args, **kwargs):
        """Force to add scrapy field when default value is set."""
        super().__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if 'default' in v:
                default_value = v.get('default')
                if default_value is NotImplemented:
                    raise NotImplementedError(f'"{k}" must be implemented!')
                else:
                    self[k] = kwargs.get(k) or v.get('default')
