# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .sql import Sql
from policy.items import PolicyItem

class PolicyPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, PolicyItem):
            name = item['name']
            ret = Sql.select(name)
            if ret[0] == 1:
                print('已经存在了')
                pass
            else:
                department = item['department']
                date = item['date']
                name = item['name']
                content = item['content']
                overview = item['overview']
                Sql.insert_policy(department, date, name, content, overview)
                print('开始存政策')

