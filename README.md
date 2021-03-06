# ErShouFang
抓取链家，我爱我家，房天下，中原地产房产中介二手房在售数据，做出数据可视化图片，并做简单的数据分析

简述    
想要了解北京二手房在售情况，房产中介的数据无疑是很有说服力的，本爬虫爬取四家中介网站的在售二手房共14万多条数据，覆盖了北京各个地区。以下会根据数据图片做简要的数据分析。
在技术方面，本爬虫使用scrapy框架，使用两个下载器中间件分别做了代理、cookie、请求头处理，创建extension自动维护代理池，数据写入mongo数据库，使用mongo聚合对数据进行分类、总和与平均值计算，使用pyecharts库对数据进行可视化，生成了柱状图与饼状图。
 
数据分析
![image](https://github.com/LemonBottom/ErShouFang/blob/master/ErShouFang/北京二手房平均价格.png?raw=true)
全北京在售二手房，西城区平均房价最高，达到了骇人听闻的十一万每平米，其次是东城区，直逼十万每平米，再然后是海淀和朝阳。以此数据与房天下网站公布的数据相比，总体价格趋势与房天下数据一致，不过海淀区的平均价格相差较大，本爬虫是九万，房天下数据是八万四，相差了六千。本人认为这与年末的学区房政策有着千丝万缕的联系，经微博网友雪球的爆料，根据其提供的上地实验中学的《关于北京市义务教育入学政策的通知》，其中提到《北京市海淀区教育委员会关于2018年义务教育阶段入学工作的实施意见》“自2019年1月1日起，在海淀区新登记并取得房屋不动产权证书的住房用于申请入学的，将不再对应一所学校，实施多校划片”。这或许是海淀区房价平均值不稳定的原因之一，一些房屋出售者会根据政策变化及时变更房屋价格。

![image](https://github.com/LemonBottom/ErShouFang/blob/master/ErShouFang/北京二手房在售数量.png?raw=true)
在北京哪里卖二手房子的最多？朝阳和海淀。不过通过数据可以看出，北京近郊的房产交易要比东西城火热。本人认为，随着地铁不断向外拓展，北京近郊的交通会越来越便利，房地产会越发火热，毕竟房价和中心城区差出了一个梯队，平均价格在五万左右。

![image](https://github.com/LemonBottom/ErShouFang/blob/master/ErShouFang/北京二手房平均面积.png?raw=true)
北京近郊的房子面积要比城区大。

![image](https://github.com/LemonBottom/ErShouFang/blob/master/ErShouFang/北京二手房数据分布.png?raw=true)
可以看出相比两大明码标价中介链家和我爱我家，房天下的数据最多，中原地产数据最少。

北京最贵的小区在哪？

西城区

小区名称 | 平均价格 
:------: | :------: 
丰融园 | 186127 |
中海凯旋 | 177202 |
丰侨公寓 | 176112 |
丰汇园 | 175823 |
北京尊府 | 172882 |

东城区

|小区名称|平均价格|
:------: | :------: 
|北下洼子胡同|165664|
|府学胡同|161980|
|八宝坑胡同|160336|
|普渡寺小区|151491|
|长安太和|140198|

朝阳区

|小区名称|平均价格|
:------: | :------: 
|泛海世家|178752|
|红玺台|151880|
北京壹号院|149892|
|翰林阁|149176|
|太阳公元|140682|

海淀区

|小区名称|平均价格|
:------: | :------: 
|万柳书院|192737|
|万城华府|182129|
|万城华府海园|179488|
|保利海德公园|166471|
|光大水墨风景|147323|


