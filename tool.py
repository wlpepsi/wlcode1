#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyutil.common.procedure_helper import ProcedureBase, action


class Tool(ProcedureBase):
    default_db = "radarx"

    @action
    def create_radarx_f_credit51_comment(self):
        self.hive_execute("""
CREATE EXTERNAL TABLE `radarx.radarx_f_credit51_comment`(
    pid STRING COMMENT '帖子id',
    ct1 STRING COMMENT '一级分类',
    ct2 STRING COMMENT '二级分类',
    tit STRING COMMENT '帖子主题',
    tit_url STRING COMMENT '帖子超链接',
    pst_aut STRING COMMENT '帖子作者',
    aut_url STRING COMMENT '作者链接',
    rel_tim STRING COMMENT '帖子发布时间',
    new_com_aut STRING COMMENT '最新留言人',
    new_com_tim STRING COMMENT '最新留言时间',
    cid STRING COMMENT '评论id',
    com_aut STRING COMMENT '评论作者',
    com_aut_url STRING COMMENT '评论作者的id',
    aut_rel_tim STRING COMMENT '评论作者注册时间',
    com STRING COMMENT '评论的内容'
) COMMENT '51信用卡帖子'
PARTITIONED BY (`day` string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\\t'
LINES TERMINATED BY '\\n'
STORED AS TEXTFILE
LOCATION 's3a://%s/radarx_f_credit51_comment'
;

grant all on table radarx.radarx_f_credit51_comment to role radarx_all;
grant select on table radarx.radarx_f_credit51_comment to role radarx_select;
""" % self.proplus.get_value_by_name("aws.s3.bucketName.radarx"))

    @action
    def create_tables(self):
        self.create_radarx_f_credit51_comment()


if __name__ == "__main__":
    Tool().start()