from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip()) #漏写了compose,然后报错了 !!
    source_out = Compose(Join(), lambda s: s.strip())