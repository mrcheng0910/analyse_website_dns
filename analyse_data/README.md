## 对所获取的域名解析信息进行统计分析
1. 为统计分析系统提供展示数据
2. 为写论文提供参考图片

### 文件功能介绍

* #### 目录ip_location

实现IP定位功能，开源代码，在githup上

* #### 目录graph
保存生成的图表等内容

* #### domain_collection.py

数据库操作文件，数据库操作功能都在该文件中进行实现

* #### extract_domain_pkt.py

整理站点的多次探测数据，进行粗过滤后，存入数据库中

* #### domain_relation.py

展示站点各个域名的关联信息，不同簇使用不同颜色进行标记

* #### show_domain_type.py

展示站点中嵌入式域名/cname/IP的关联关系

* #### analyse_content.py

分析网站的详细内容，包括嵌入的域名/cname/ip，簇，集合等信息

* #### dir_graph_analyse.py

分析有向图的信息