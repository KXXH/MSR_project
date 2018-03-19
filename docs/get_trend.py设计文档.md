# get_trend.py设计文档

## Project类



project类是设计爬虫时顺带设计的产物，拥有同数据库的内容一样的信息。属性均为私有属性，包括：

- name（str，‘/owner/name’）
- language（str，同GitHub不同语言trend页面URL最后一部分相同）
- stars，forks，stars_today（int，从GitHub trend页面爬取）
- contributors（list，其中元素为str，为GitHub用户名，与用户个人主页URL最后一部分相同，来源是GitHub trend页面）
- topics（list，其中元素为str，由GitHub API v4提供）

project类还包括修改和查询属性的方法，具体都按照'change_'+属性名的格式命名，仅当输入参数与属性本身的类型相同时，才能够修改属性，否则（非空但类型不一致，将会抛出ValueError（可能不太严谨 要改））。函数不论参数是否为空，都返回最终属性的值。

## 数据库

数据库名为hot_project_info.db，基于sqlite3，存放了以下信息：

- name（text，同project类）
- language（text，同project类）
- stars（integer，同project类）
- forks（integer，同project类）
- stars_today（integer，同project类）
- contributors（text，由project.__contributors属性经由list2str()函数变换得到，具体实现是在list的每一个项后面加上'|'，然后把它们组合为一个大字符串）
- topics（text，由project.__topics属性经过list2str()函数变换得到