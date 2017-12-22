"""shopServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from shopApp.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$' , home),
    url(r'^goodsManage/$' , goodsManage),
    url(r'^adPage/$' , adPage),
    url(r'^cartsManage/$' , cartsManage),#购物车界面
    url(r'^userManage/$' , userManage),
    url(r'^orderManage/$' , orderManage),
    url(r'^adManage/$' , adManage),
    url(r'^identificode/$',identificode),
    url(r'^changePic/$' , changePic),#改变轮播图界面
    url(r'^changeLunbo/$' , changeLunbo),# 添加轮播图界面
    url(r'^login/$' , login),#登录界面
    url(r'^loginApi/$' , loginApi),  # 登录接口 
    url(r'^register/$' , userManageJsonAdd), # 添加用户接口 
    # url(r'^uploadHeadImg/$' , uploadHeadImg), # 上传头像接口
    url(r'^drawManage/$',drawManage), #抽奖余额界面

    url(r'^saveOneImageToServer/$' , saveOneImageToServer),  # 添加一张图片到服务器 不和数据库产生联系

    url(r'^userManageJsonAdd/$' , userManageJsonAdd), # 添加用户接口
    url(r'^userManageJsonSelect/$' , userManageJsonSelect), # 查询用户接口
    url(r'^userManageJsonDelete/$' , userManageJsonDelete), #删除用户接口
    url(r'^userManageJsonUpdate/$' , userManageJsonUpdate), #更新用户接口
    url(r'^lookhistorytableManageJsonAdd/$' , lookhistorytableManageJsonAdd),#浏览记录添加接口
    url(r'^lookhistorytableManageJsonSelect/$' , lookhistorytableManageJsonSelect),#浏览记录查询接口
    url(r'^lookhistorytableManageJsonDelete/$' , lookhistorytableManageJsonDelete),#浏览记录删除接口
    url(r'^lookhistorytableManageJsonUpdata/$' , lookhistorytableManageJsonUpdata),#浏览记录更改接口
    url(r'^favoritetableManageJsonAdd/$' , favoritetableManageJsonAdd),#收藏功能添加接口
    url(r'^favoritetableManageJsonSelect/$' , favoritetableManageJsonSelect),#收藏功能查询接口
    url(r'^favoritetableManageJsonDelete/$' , favoritetableManageJsonDelete),#收藏功能删除接口
    url(r'^favoritetableManageJsonUpdata/$' , favoritetableManageJsonUpdata),#收藏功能更改接口
    # url(r'^lookhistorytableManage/$' , lookhistorytableManage),#浏览记录列表
    # url(r'^lookhistoryManage/$' , lookhistoryManage),#浏览记录列表接口
    url(r'^activeManage/$' , activeManage),
    
    url(r'^addGoodsImage/$' , addGoodsImage),
    
    url(r'^ordertabalelistJaon/$' , ordertabalelistJaon),
    

    url(r'^adManageJsonAdd/$' , adManageJsonAdd), # 广告添加的接口
    url(r'^adManageJsonSelect/$' , adManageJsonSelect), # 广告列表的接口  
    url(r'^adManageJsonDelete/$' , adManageJsonDelete), # 广告删除的接口

    url(r'^goodsManageJsonAdd/$' , goodsManageJsonAdd),  # 商品添加接口
    url(r'^goodsManageJsonSelect/$' , goodsManageJsonSelect),  # 商品查询接口   
    url(r'^addGoods/$' , addGoods),  # 添加商品接口


    url(r'^goodsManageJsonSelect/$' , goodsManageJsonSelect),  # 商品列表接口   
    url(r'^goodsManageJsonUpdata/$' , goodsManageJsonUpdata), # 商品列表修改接口
    url(r'^goodsManageJsonDelete/$' , goodsManageJsonDelete),  # 商品列表删除接口
    url(r'^goodsSelectByid/$' , goodsSelectByid), # 根据商品id查找商品
    url(r'^commodityQuery/$' , commodityQuery), # 商品模糊查询接口查找商品

    
    url(r'^activetableManageJsonAdd/$' , activetableManageJsonAdd),  # 活动添加接口
    url(r'^activeManageJsonSelect/$' , activeManageJsonSelect), # 活动列表接口
    url(r'^activetableManageJsonDelete/$' , activetableManageJsonDelete), # 活动删除接口接口
    url(r'^redpack/$',redpack),#红包页面
    url(r'^redpackApi/$',redpackApi),#红包查询
    url(r'^redpackAdd/$',redpackAdd),#红包添加
    url(r'^redpackDelete/$',redpackDelete),#红包删除
    

    url(r'^ordertableManageJsonAdd/$' , ordertableManageJsonAdd), # 订单添加接口
    url(r'^ordertableDelete/$' , ordertableDelete), # 订单删除接口
    url(r'^orderSpilit/$',orderSpilit), #订单分页接口

    url(r'cartstableManageJsonAdd/$' , cartstableManageJsonAdd), #购物车添加接口
    url(r'cartstableManageJsonDelete/$' , cartstableManageJsonDelete), #购物车删除接口
    url(r'cartstableManageJsonUpdate/$' , cartstableManageJsonUpdate), #购物车修改接口
    url(r'cartstableManageJsonSelect/$' , cartstableManageJsonSelect), #购物车查询接口



    url(r'^drawJsonAdd/$',drawJsonAdd),   #添加抽奖余额接口
    url(r'^drawJsonDel/$',drawJsonDel),   #删除抽奖余额接口
    url(r'^drawJsonUpdate/$',drawJsonUpdate),   #更新抽奖余额接口
    url(r'^drawJsonQuery/$',drawJsonQuery),   #查找抽奖余额接口
    
    url(r'cartstableManageJsonGain/$' , cartstableManageJsonGain),#购物车获取接口



    url(r'luckyManage/$' , luckyManage), #福袋管理界面
    url(r'luckyManageJsonQuery/$' , luckyManageJsonQuery), #福袋模糊查询接口(分页)
    url(r'luckyManageJsonDelete/$' , luckyManageJsonDelete), #福袋删除接口
    url(r'luckyManageJsonAdd/$' , luckyManageJsonAdd), #福袋添加接口
    url(r'luckyManageJsonUpdata/$' , luckyManageJsonUpdata), #福袋修改接口
    url(r'selectLuckyJsonByGoodsId/$' , selectLuckyJsonByGoodsId), #通过商品号查询福袋
    

    url(r'commentJsonQuery/$' , commentJsonQuery), #评论查询接口(分页)    
    url(r'commentJsonDelete/$' , commentJsonDelete), #评论删除接口
    url(r'commentJsonAdd/$' , commentJsonAdd), #评论添加接口


    url(r'^addAddress/$',addAddress),   #添加地址接口
    url(r'^delAddress/$',delAddress),   #删除地址接口
    url(r'^updateAddress/$',updateAddress),   #修改地址接口
    url(r'^findAddress/$',findAddress),   #查找地址接口

    url(r'^addMoney/$',addMoney),   #增加余额接口
    url(r'^delMoney/$',delMoney),   #删除余额接口
    url(r'^updateMoney/$',updateMoney),   #修改余额接口
    url(r'^findMoney/$',findMoney),   #查询余额接口
    url(r'^addShare/$',addShare),   #添加分享记录接口
    url(r'^delShare/$',delShare),   #删除分享记录接口
    url(r'^updateShare/$',updateShare),   #修改分享记录接口
    url(r'^findShare/$',findShare),   #查找分享记录接口

    url(r'^leaveMessage/$',leaveMessage), #查询用户留言接口
    url(r'^addLeaveMessage/$',addLeaveMessage), ##增加用户留言接口
    url(r'^deleLeaveMessage/$',deleLeaveMessage), ##删除用户留言接口

    url(r'^scoreAdd/$',scoreAdd), #积分添加接口
    url(r'^scoreDelete/$',scoreDelete), #积分删除接口 POST请求
    url(r'^scoreSelect/$',scoreSelect), #积分查询接口 POST请求

    url(r'^buyhistoryAdd/$',buyhistoryAdd), #购买历史添加接口
    url(r'^buyhistorySelect/$',buyhistorySelect), #购买历史删除接口 POST请求
    url(r'^buyhistoryDelete/$',buyhistoryDelete), #购买历史查询接口 POST请求
    url(r'^secondkillManageJsonAdd/$' , secondkillManageJsonAdd),#秒杀活动添加     
    url(r'^secondkillManageJsonSelect/$' , secondkillManageJsonSelect),#秒杀活动查询
    url(r'^secondkillManageJsonDelete/$' , secondkillManageJsonDelete),#秒杀活动删除
    url(r'^secondkillManageJsonUpdata/$' , secondkillManageJsonUpdata),#秒杀活动更新
    url(r'^secondkillManageJsonstock/$' , secondkillManageJsonstock),#查询库存
    url(r'^secondkillAddgoodsidintogoods/$' , secondkillAddgoodsidintogoods),
    url(r'^personal/$' , personal),      
    url(r'^guestbookSelect/$',guestbookSelect), #购买历史查询接口 POST请求
    url(r'^leavingMessage/$',leavingMessage), #留言查询接口 POST请求

    url(r'^getSession/$',getSession), #请求session数据的接口
    url(r'^setSession/$',setSession), #设置session数据的接口
    
    url(r'^$' , login),
    url(r'^.' , error),
]
