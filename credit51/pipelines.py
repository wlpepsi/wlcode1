# -*- coding: utf-8 -*-
# encoding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .assisted.get_filepath import get_filepath
import os

class Credit51Pipeline(object):

    def process_item(self, item, spider):

        filepath=get_filepath(item['cid'] + '.txt')

        if not os.path.exists(filepath):
            fp=open(filepath, 'a')
            key_list=['pid','ct1','ct2','tit','tit_url','pst_aut','aut_url','rel_tim','new_com_aut','new_com_tim','cid','com_aut','com_aut_url','aut_rel_tim','flr','com']

            for key in key_list:
                if item[key]:
                    fp.write(item[key].encode('utf-8').replace('\n', '').replace('\r', '') + '\t')
                else:
                    fp.write('NULL'+'\t')

            fp.close()
        return item


