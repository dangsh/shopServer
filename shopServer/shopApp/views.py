from django.shortcuts import render


from django.http import HttpResponse

import os
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont


import datetime 
import time
from django import forms
from django.shortcuts import render_to_response
from django.core.files.uploadedfile import InMemoryUploadedFile
from shopApp.mytool import *
from django.db import connection

import json
xx="";
# Create your views here.

def home(request):
    # cursor = connection.cursor()

 
    name = "liu";
    
    
    # cursor.execute('CREATE TABLE manager(username varchar(255),pwd varchar(255))')

    # cursor.execute('CREATE TABLE Persons2(Id_P int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255))')
    # cursor.execute('CREATE TABLE carts(cartsid varchar(255),number int, goodsid varchar(255),userid varchar(255))')
    
    return render(request , "base.html");
def login(request):
    return render(request,"login.html")

def error(request):
    return HttpResponse("我是404");



def goodsManage(request):
    return render(request , "goodsManage.html");

def adPage(request):
    return render(request , "adPage.html");
# 生成随机验证码
def identificode(request):
    aaa = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    bg= (0 , 255 ,200)
    backcolor= (random.randint(32, 128), random.randint(32, 128), random.randint(32, 128))
    w = 60 * 4;
    h = 60
    # 创建一张图片，指定图片mode，长宽
    image = Image.new('RGB', (w, h), (255,182,193))
    # 设置字体类型及大小
    font = ImageFont.truetype(font='arial.ttf', size=36)
    # 创建Draw对象
    draw = ImageDraw.Draw(image)
    # 遍历给图片的每个像素点着色
    for x in range(w):
        for y in range(h):
            draw.point((x, y),fill=bg)
    # 将随机生成的chr，draw如image
    global xx;
    xx = "";
    for t in range(4):
        a=aaa[random.randint(0 , 61)];
        # temp = randomChar()
        draw.text((60 * t + 10, 10), a, font=font,fill=backcolor)
        xx=xx+a;
    # 设置图片模糊
    print(xx);
    image = image.filter(ImageFilter.BLUR)
    # 保存图片
    image.save('./shopApp/static/myfile/code.jpg', 'jpeg')
    imgDic = {"imgPath":"static/myfile/code.jpg"}
    return HttpResponse(json.dumps(imgDic) , content_type = "application/json")

def userManage(request):
    return render(request , "userManage.html");

def orderManage(request):
    print("*****************");
    return render(request , "orderManage.html");

def adManage(request):
    return render(request , "adManage.html");

def cartsManage(request):
    return render(request , "cartsManage.html");

def activeManage(request):

    return render(request , "activeManage.html");

def addGoods(request):
    return render(request, "goodsAdd.html")
def changeLunbo(request):
    return render(request,"addLunbo.html")

def changePic(request):
	return render(request, "changePic.html")

#改变轮播图界面
def changePic(request):
	return render(request,"changePic.html")


# 根据用户名创建属于他的表格
def personal(request):
    # name=request.get["name"];
    name=request.POST["name"]
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE %s_lookhistory(lookId varchar(255),userId varchar(255),looktime timestamp not null default current_timestamp)'%name)
        cursor.execute('CREATE TABLE %s_carts(cartsId varchar(255),number varchar(255),goodsId varchar(255),userId varchar(255))'%name)
        cursor.execute('CREATE TABLE %s_favorite(favoriteId varchar(255),goodsId varchar(255),userId varchar(255),favtime timestamp not null default current_timestamp)'%name)
        cursor.execute('CREATE TABLE %s_recharge(rechargeId varchar(255),money varchar(255),status varchar(255),rechargetime timestamp not null default current_timestamp)'%name)
        cursor.execute('CREATE TABLE %s_orderlist(orderlistId varchar(255),userId varchar(255),orderId varchar(255))'%name)
        cursor.execute('CREATE TABLE %s_ordertable(orderId varchar(255),userId varchar(255),ordertime timestamp not null default current_timestamp,isaudit tinyint(1),ispass tinyint(1),iscancel tinyint(1),ispay tinyint(1),issend tinyint(1),ispaydone tinyint(1),isclose tinyint(1))'%name)
        cursor.execute('CREATE TABLE %s_score(scoreId varchar(255),scoretime timestamp not null default current_timestamp,getpath nvarchar(255),scorecount varchar(255))'%name)
        cursor.execute('CREATE TABLE %s_rewardtable(rewardId varchar(255),userId varchar(255))'%name)
    except Exception as e:    
            return HttpResponse(json.dumps({'data':"创建该用户的其他表失败", 'status':'error'}), content_type="application/json");

    statusDic = {"status" : "ok" , "message" : "创建用户其他表成功"};
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");



# 登录界面
def login(request):
    
    return render(request , "login.html");


# 登录接口 (ok)
def loginApi(request):
    print("************************")
    global xx;
    
    userName = request.POST["username"]
    password = request.POST["password"]
    code=request.POST["code"]
    print(userName)
    print(xx);
    # userName = "admin"
    # global xx;
    # password = "123456"
    if xx==code:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM manager WHERE username=\"%s\" AND pwd=\"%s\"'%(userName , password))
        a = cursor.fetchall()
        cursor.close()
        if a:
            successMSG = {"status":"ok","message":"登陆成功"}
            return HttpResponse(json.dumps(successMSG) , content_type="application/json")
        else:
            errorMSG = {"status":"error","message":"登录失败"}
            return HttpResponse(json.dumps(errorMSG) , content_type="application/json")
    else:
        print("验证码错误请重新输入..............")
        errorMSG = {"status":"error","message":"登录失败"}
        return HttpResponse(json.dumps(errorMSG) , content_type="application/json")



# 用户添加接口
def userManageJsonAdd(request):
    # userid = request.POST["userid"]
    # username = request.POST["username"]
    # headimg = request.POST["headimg"]
    # phone = request.POST["phone"]
    # pwd = request.POST["pwd"]
    # wxid = request.POST["wxid"]
    # acountmoney = request.POST["acountmoney"]
    # rewardmoney = request.POST["rewardmoney"]
    # activecode = request.POST["activecode"]
    # redpack = request.POST["redpack"]
    # upperson = request.POST["upperson"]
    # downperson = request.POST["downperson"]
    # rebate = request.POST["rebate"]
    # integral = request.POST["integral"]
    # bankcard = request.POST["bankcard"]
    # power = request.POST["power"]
    # address = request.POST["address"]

    # userid = None;
    username = "";
    headimg = "";
    phone = "";
    pwd = "";
    wxid = "";
    acountmoney = "";
    rewardmoney = "";
    activecode = "";
    redpack = "";
    upperson = "";
    downperson = "";
    rebate = "";
    integral = "";
    bankcard = "";
    power = "";
    address = "";
    if request.POST["username"]:
        username = request.POST["username"]
    # if request.POST["pwd"]:
    #     username = request.POST["pwd"]
    # if request.POST["headimg"]:
    #     headimg = request.POST["headimg"]
    # if request.POST["phone"]:
    #     phone = request.POST["phone"]
    if request.POST["password"]:
        pwd = request.POST["password"]
    print(username);
    # if request.POST["wxid"]:
    #     wxid = request.POST["wxid"]
    # if request.POST["acountmoney"]:
    #     acountmoney = request.POST["acountmoney"]
    # if request.POST["rewardmoney"]:
    #     rewardmoney = request.POST["rewardmoney"]
    # if request.POST["activecode"]:
    #     activecode = request.POST["activecode"]
    # if request.POST["redpack"]:
    #     redpack = request.POST["redpack"]
    # if request.POST["upperson"]:
    #     upperson = request.POST["upperson"]
    # if request.POST["downperson"]:
    #     downperson = request.POST["downperson"]
    # if request.POST["rebate"]:
    #     rebate = request.POST["rebate"]
    # if request.POST["integral"]:
    #     integral = request.POST["integral"]
    # if request.POST["bankcard"]:
    #     bankcard = request.POST["bankcard"]
    # if request.POST["power"]:
    #     power = request.POST["power"]
    # if request.POST["address"]:
    #     address = request.POST["address"]


    cursor = connection.cursor();
    # cursor.execute("ALTER TABLE yyy.user MODIFY COLUMN username VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;");
    result = cursor.execute("INSERT INTO user(username , pwd)VALUES('%s' , '%s')"%(username , pwd))
    # result = cursor.execute("INSERT INTO user(userId , username , headimg , phone , pwd , wxid , acountmoney , rewardmoney , activecode , redpack , upperson , downperson , rebate , integral , bankcard , power , address) VALUES('%s' , '%s' , '%s' , '%s' ,'%s' , '%s' , '%s' , '%s' ,'%s' , '%s' , '%s' , '%s' ,'%s' , '%s' , '%s' , '%s' , '%s')"%(userid , username , headimg , phone , pwd , wxid , acountmoney , rewardmoney , activecode , redpack , upperson , downperson , rebate , integral , bankcard , power , address));
    cursor.close()
   
    print("9999999");
    statusDic = "";
    if result == 1:
        statusDic = {"status" : "ok" , "message" : "添加用户成功"};
    else :
        statusDic = {"status" : "error" , "message" : "添加用户失败"};
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

# 用户查询接口  有待测试 尚德勋
def userManageJsonSelect(request):

    cursor=connection.cursor()

    sql = 'SELECT * FROM user'
    allUsertables = []

    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            usertable = {
                'userid':row[0],
                'username':row[1],
                'headimg':row[2],
                'phone':row[3],
                'pwd':row[4],
                'wxid':row[5],
                'acountmoney':row[6],
                'rewardmoney':row[7],
                'activecode':row[8],
                'redpack':row[9],
                'upperson':row[10],
                'downperson':row[11],
                'rebate':row[12],
                'integral':row[13],
                'bankcard':row[14],
                'power':row[15],
                'address':row[16],
                'registetime':str(row[17]),
            }
            allUsertables.append(usertable)
            cursor.close();
        return HttpResponse(json.dumps({'data':allUsertables, 'status':'ok'}), content_type="application/json")
   
    except Exception as e:    
            return HttpResponse(json.dumps({'data':allUsertables, 'status':'error'}), content_type="application/json");

def userManageJsonDelete(request):
    for key in request.POST:
        userid = request.POST.getlist(key)[0]

    cursor=connection.cursor();
    # print(cursor)
    try:
        cursor.execute("DELETE  FROM user WHERE userid = %s"%(userid))
        # connection.commit();
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
            
    except Exception as e:   
         # connection.rollback();
         return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

def userManageJsonUpdate(request):
    datas = request.POST
    cursor = connection.cursor()
    for key in datas:
        if key != 'userid':
            # cursor.execute("ALTER TABLE yyy.user MODIFY COLUMN username VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;");
            cursor.execute("update user set %s='%s' where userid=%s"%(key , datas[key] , datas["userid"]))
    cursor.close();                   
    return HttpResponse(json.dumps({"message":"更新成功" , "status":"ok"}) , content_type="application/json");



# 按时间获取随机字符串
def randomString():
    for i in range (0,10):  
        nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S");  
        randomNum=random.randint(0,100);
        if randomNum<=10:  
            randomNum=str(0)+str(randomNum);  
        randomId=str(nowTime)+str(randomNum);
        return randomId
def addGoodsImage(request):
    print(request.FILES);
    imgs = request.FILES["imgsFile"];

    
    

    # print(imgs);
    # print(type(imgs));
        
    imgsName = randomString() + ".jpg";

    filepath = "./shopApp/static/myfile";
    filename = os.path.join(filepath,imgsName)
    filename = open(filename , "wb");
    filename.write(imgs.__dict__["file"].read());
    sqlfilename = filepath+imgsName

    # imgs = str(imgs)
    # adId = randomString();

    print("************   " , sqlfilename);
    # # 

    cursor = connection.cursor();
    result=cursor.execute("UPDATE goods SET images=concat('---%s',images) where goodsid='%s'" % (imgsName , request.POST["goodsid"]));
    statusDic = "";
    if result == 1:
        statusDic = {"status" : "ok" , "message" : "添加成功" , "imgName":imgsName};
    else :
        statusDic = {"status" : "error" , "message" : "添加失败"};
    
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    # image=request.POST['imgsFile']
    # # image = "kkkkkkk"
    # cursor=connection.cursor()
    # result=cursor.execute("UPDATE goods SET images='%s' where goodsid='1111'"% image)
    # stadic=""
    # if result==1:
    #     stadic={"status":"ok","message":"成功"}
    # else:
    #     stadic={"status":"error","message":"失败"}
    # imgsName=randomString()+".jpg";

    # return HttpResponse(json.dumps(stadic),content_type="application/json")

        
  

    

#添加广告接口
def adManageJsonAdd(request):
    
    imgs = request.FILES["images"];
    imgsName = randomString() + ".jpg";
    adId = request.POST["adId"]
    imagePath = imgsName;
    filepath = "./shopApp/static/myfile";
    filename = os.path.join(filepath,imgsName)
    filename = open(filename , "wb");
    filename.write(imgs.__dict__["file"].read());
    filename.close();
    sqlfilename = imgsName


    cursor = connection.cursor();
    result = cursor.execute("INSERT INTO ad(adid , imgs) VALUES ('%s' , '%s' )" % (adId , sqlfilename));

    statusDic = "";
    if result == 1:
        statusDic = {"status" : "ok" , "message" : "添加成功" , "imagePath":imgsName , "adId":adId};
    else :
        statusDic = {"status" : "error" , "message" : "添加失败"};
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

# 广告添加接口
def saveOneImageToServer(request):
    

    imgs = request.FILES["imgsFile"];
    imgsName = randomString() + ".jpg";
    filepath = "./shopApp/static/myfile";
    filename = os.path.join(filepath,imgsName)
    filename = open(filename , "wb");
    filename.write(imgs.__dict__["file"].read());
    filename.close();
    statusDic = {"status" : "ok" , "message" : "添加成功" , "imagePath":imgsName};
    
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

# 广告列表接口
def adManageJsonSelect(request):
    try:
        myData=[];
        mypage = 0
        mypage = (int(request.GET["page"]) - 1) * 8
        print(request.GET["page"]);
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM ad LIMIT %d , 8"%mypage);
        datas=cursor.fetchall();
        for data in datas:
            adid = data[0];#图片
            imgs = data[1];#广告id
            adtime = data[2];#时间
            tempDic = {"imgs":imgs , "adid":adid , "adtime":str(adtime) }
            myData.append(tempDic)
        cursor.execute("SELECT COUNT(*) FROM ad")
        adcounts  = cursor.fetchall();
        adcounts = adcounts[0][0];
        print (adcounts);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'adcounts':str(adcounts)}) , content_type="application/json");
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'adcounts':'0'}), content_type="application/json");




# 广告删除接口 韩乐天
def adManageJsonDelete(request):
    adid = request.GET["Id"];
    
    adid = str(adid);
    cursor=connection.cursor();
    print (adid);
    try:
        print ("hahhaahahhh")
        cursor.execute("SELECT * FROM ad WHERE adid = '%s'" % adid);
        filename = cursor.fetchall()[0][1];
        #删除图片
        aa = os.listdir("../shopServer/shopApp/static/myfile/")
        for item in aa:
            print (item);
            if item == filename:
                os.remove("../shopServer/shopApp/static/myfile/"+filename);
        if cursor.execute("DELETE FROM ad where adid = '%s'" % adid):
            cursor.close();
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        
    except Exception as e:
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

# 商品添加接口
def goodsManageJsonAdd(request):
    goodsid =randomString()
    # rebate = "2222"
    lookhistoryid = "222"
    # standard = "2222"
    # images = "2222"
    details = "2222"
    # shopname = "222"
    # status = "333"
    # price = "333"
    # goodsname = "333"
    # stock = "333"         #库存
    # transportmoney="333"        #运费
    
    # if request.POST["goodsid"]:
    #     goodsid = request.POST["goodsid"]
    # if request.POST["rebate"]:
    #     rebate = request.POST["rebate"]
    # if request.POST["lookhistoryid"]:
    #     lookhistoryid = request.POST["lookhistoryid"]
    # if request.POST["standard"]:
    #     standard = request.POST["standard"]
    # if request.POST["images"]:
    #     images = request.POST["images"]
    # if request.POST["details"]:
    #     details = request.POST["details"]
    # if request.POST["shopname"]:
    #     shopname = request.POST["shopname"]
    # if request.POST["status"]:
    #     status = request.POST["status"]
    # if request.POST["price"]:
    #     price = request.POST["price"]
    # if request.POST["goodsname"]:
    #     goodsname = request.POST["goodsname"]
    # if request.POST["stock"]:
    #     stock = request.POST["stock"]
    # if request.POST["transportmoney"]:
    #     transportmoney=request.POST["transportmoney"]

    # goodsid = request.POST["goodsid"]

    rebate = request.POST["rebate"]

    # lookhistoryid = request.POST["lookhistoryid"]

    standard = request.POST["standard"]

    images = request.POST["images"]

    # details = request.POST["details"]

    shopname = request.POST["shopname"]

    status = request.POST["status"]

    price = request.POST["price"]

    goodsname = request.POST["goodsname"]

    stock = request.POST["stock"]

    transportmoney=request.POST["transportmoney"]

    cursor = connection.cursor()
    try:
        result = cursor.execute("INSERT INTO goods (goodsid , rebate , lookhistoryid , standard , images , details ,shopname , status , price , goodsname , stock, transportmoney) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (goodsid , rebate , lookhistoryid , standard , images , details ,shopname , status , price , goodsname , stock, transportmoney))

        if result == 1 :
            statusDic = {"status" : "ok" , "message" : "添加成功"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            statusDic = {"status" : "error" , "message" : "添加失败"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");

# 商品列表接口
def goodsManageJsonSelect(request):
    myData=[];
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor = connection.cursor();
    cursor.execute("SELECT * FROM goods LIMIT %d , 10"%mypage);
    datas=cursor.fetchall();
    try:
        for row in datas:
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'details':row[6],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'price':row[5],
                'goodsname':row[16],
                'stock':row[11],
            }
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM goods")
        goodscount  = cursor.fetchall();
        goodscount = goodscount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'goodscount':str(goodscount) }), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

# 商品列表接口
# def goodsManageJsonSelect(request):
#     myData=[];
#     cursor = connection.cursor();
#     cursor.execute("SELECT * FROM goods");
#     datas=cursor.fetchall();
#     try:
#         for row in datas:
#             goods = {
#                 'goodsid':row[0],
#                 'rebate':row[1],
#                 'lookhistoryid':row[2],
#                 'standard':row[3],
#                 'images':row[4],
#                 'details':row[5],
#                 'shopname':row[6],
#                 'status':row[7],
#                 'uptime':row[8].strftime('%Y-%m-%d %H:%M:%S'),
#                 'downtime':row[9].strftime('%Y-%m-%d %H:%M:%S'),
#                 'price':row[10],
#                 'goodsname':row[11],
#                 'stock':row[12],
#             }
#             myData.append(goods);
#         cursor.close();
#         return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    
#     except Exception as e: 
#         raise e   
#         return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");

# 商品列表删除接口
def goodsManageJsonDelete(request):
  # goodsid = '1'
    goodsidsDict =  request.POST
    goodsids = goodsidsDict.getlist("goodsids")

    # cursor = connection.cursor();
    # cursor.execute("SELECT details FROM goods WHERE goodsid = '%s'"%goodsids);
    # detailsDatas=cursor.fetchall();
    # print(detailsDatas)

    # path.exists(r'') == False
    # os.remove(r'')

    # goodsids = goodsidsStr[2:-2].split("\",\"")
    # print(goodsids)
    # print(type(goodsids['goodsids']), goodsids['goodsids'])

    cursor=connection.cursor();
    result = 0
    result = 0
    try:
        for goodsid in goodsids:
            cursor.execute("DELETE FROM goods where goodsid = '%s'"%(goodsid))
            result += 1
        # result = cursor.execute("DELETE FROM goods where goodsid = '%s'"%(goodsid))
        # connection.commit();
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

#商品详情列表展示 有待测试 吕健威
def goodsSelectByid(request):
    cursor = connection.cursor()
    # goodsid = "123456789"
    goodsid = request.POST["goodsid"]
    sql = "SELECT * FROM goods WHERE goodsid = '%s'" % goodsid
    allGoodMes = []
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'details':row[6],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'price':row[5],
                'goodsname':row[16],
                'stock':row[11],
            }
            allGoodMes.append(goods)
            
        # 关闭连接
        cursor.close()
        return HttpResponse(json.dumps({'data':allGoodMes, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':allGoodMes, 'status':'error'}), content_type="application/json")

# 商品模糊查询接口 黄景召 胡亚洲改


def commodityQuery(request):
    print("******************************************")
    myData = []
    cursor = connection.cursor()
    # commName = "xiaomi"
    commName = request.GET["commName"]
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor.execute("SELECT * FROM goods where goodsname like '%%%%%s%%%%' LIMIT %d , 10;"%(commName, mypage));
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'details':row[6],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'price':row[5],
                'goodsname':row[16],
                'stock':row[11],
            }
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM goods where goodsname like '%%%%%s%%%%'" % (commName))
        goodscount  = cursor.fetchall();
        goodscount = goodscount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'goodscount':str(goodscount) }), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

#订单分页
def orderSpilit(request):
    print("******************************************")
    myData = []
    cursor = connection.cursor()
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor.execute("SELECT * FROM ordertable LIMIT %d , 10;" % mypage);
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = {
                'userid':row[0],
                'orderid':row[1],
                'price':row[2],
                'ordertime':row[3].strftime('%Y-%m-%d %H:%M:%S'),
                'isaudit':row[4],
                'ispass':row[5],
                'iscancel':row[6],
                'ispay':row[7],
                'issend':row[8],
                'ispaydone':row[9],
                'isclose':row[10],
            }
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM ordertable")
        ordercount  = cursor.fetchall();
        ordercount = ordercount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'ordercount':str(ordercount)}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error' , 'ordercount':str(ordercount)}), content_type="application/json");

# 商品修改列表修改接口 有待测试 黄景召
def goodsManageJsonUpdata(request):
    
    datas = request.POST
    print("((((((((((((((((((((((");
    print(datas)
    for key in list(datas):
        cursor = connection.cursor()
        cursor.execute("update goods set %s='%s' where goodsid='%s'"%(key , datas[key] , datas["goodsid"]))
    data = {'data':'success', 'status':'ok'}
    return HttpResponse(json.dumps(data) , content_type="application/json");


# 订单添加接口 有待测试 胡亚洲
def ordertableManageJsonAdd(request):
    ordertableid = request.POST["ordertableid"]
    userid = request.POST["userid"]
    goodsid = request.POST["goodsid"]
    isaudit = request.POST["isaudit"]
    ispass = request.POST["ispass"]
    iscancel = request.POST["iscancel"]
    ispay = request.POST["ispay"]
    issend = request.POST["issend"]
    ispaydone = request.POST["ispaydone"]
    isclose = request.POST["isclose"]
    # 获取游标
    cursor = connection.cursor()
    sql = "INSERT  INTO xxx (ordertableid,userid,goodsid,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    param=(ordertableid,userid,goodsid,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose)
    cursor.execute(sql, param)
    # 关闭连接
    cursor.close()
    try:
        status = json.dumps({
        'status':'ok',
        })
        return HttpResponse(status, content_type="application/json")
    except Exception as e:
        status = json.dumps({
        'status':'error',
        })
        return HttpResponse(status, content_type="application/json")

# 订单列表接口  有待测试 韩乐天
def ordertabalelistJaon(request):
    userid = request.POST["userid"]
    orderid = request.POST["orderid"];
    print(userid,orderid)
    print("000000000000000000000000000")
    cursor = connection.cursor()
    sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose,price FROM ordertable";
    allOrdertables = [];
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            ordertable = {
                'orderid':row[0],
                'userid':row[1],
                'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                'isaudit':row[3],
                'ispass':row[4],
                'iscancel':row[5],
                'ispay':row[6],
                'issend':row[7],
                'ispaydone':row[8],
                'isclose':row[9],
                'price':row[10],
            }
            allOrdertables.append(ordertable)
        cursor.close()
        # print(allOrdertables)
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
    # print(userid)
def ordertableManageJsonSelete(request):
    userid = request.POST["userid"]
    orderid = request.POST["orderid"];
    print("000000000000000000000000000")
    cursor = connection.cursor()
    sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE orderid = '%s'" % orderid;
    allOrdertables = [];
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            ordertable = {
                'orderid':row[0],
                'userid':row[1],
                'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                'isaudit':row[3],
                'ispass':row[4],
                'iscancel':row[5],
                'ispay':row[6],
                'issend':row[7],
                'ispaydone':row[8],
                'isclose':row[9],
            }
            allOrdertables.append(ordertable)
        cursor.close()
        print(allOrdertables)
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
    # print(userid)
    # 获取游标
    if request.GET["userid"]:      
        userid = request.GET["userid"]
        if request.GET["status"] == "1":
            isaudit = request.GET["status"]
            cursor = connection.cursor()
            sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND isaudit = '%s'" % (userid,isaudit);
            allOrdertables = [];
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ordertable = {
                            'orderid':row[0],
                            'userid':row[1],
                            'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                            'isaudit':row[3],
                            'ispass':row[4],
                            'iscancel':row[5],
                            'ispay':row[6],
                            'issend':row[7],
                            'ispaydone':row[8],
                            'isclose':row[9],
                    }
                    allOrdertables.append(ordertable)
                cursor.close()
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
        if request.GET["status"] == "2":
            ispass = request.POST["status"]
            cursor = connection.cursor()
            sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND ispass = '%s'" % (userid,ispass);
            allOrdertables = [];
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ordertable = {
                            'orderid':row[0],
                            'userid':row[1],
                            'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                            'isaudit':row[3],
                            'ispass':row[4],
                            'iscancel':row[5],
                            'ispay':row[6],
                            'issend':row[7],
                            'ispaydone':row[8],
                            'isclose':row[9],
                    }
                    allOrdertables.append(ordertable)
                cursor.close()
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
        if request.GET["status"] == "7":
                iscancel = request.GET["status"];
                cursor = connection.cursor()
                sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND iscancel = '%s'" % (userid,iscancel);
                allOrdertables = [];
                try:
                    cursor.execute(sql)
                    for row in cursor.fetchall():
                        ordertable = {
                                'orderid':row[0],
                                'userid':row[1],
                                'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                                'isaudit':row[3],
                                'ispass':row[4],
                                'iscancel':row[5],
                                'ispay':row[6],
                                'issend':row[7],
                                'ispaydone':row[8],
                                'isclose':row[9],
                        }
                        allOrdertables.append(ordertable)
                    cursor.close()
                    return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
                except Exception as e:
                    return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
        if request.GET["status"] == "3":
            ispay = request.GET["status"];
            cursor = connection.cursor()
            sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND ispay = '%s'" % (userid,ispay);
            allOrdertables = [];
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ordertable = {
                            'orderid':row[0],
                            'userid':row[1],
                            'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                            'isaudit':row[3],
                            'ispass':row[4],
                            'iscancel':row[5],
                            'ispay':row[6],
                            'issend':row[7],
                            'ispaydone':row[8],
                            'isclose':row[9],
                    }
                    allOrdertables.append(ordertable)
                cursor.close()
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
        if request.GET["status"] =="6":
            issend = request.GET["status"];
            cursor = connection.cursor()
            sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND issend = '%s'" % (userid,issend);
            allOrdertables = [];
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ordertable = {
                            'orderid':row[0],
                            'userid':row[1],
                            'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                            'isaudit':row[3],
                            'ispass':row[4],
                            'iscancel':row[5],
                            'ispay':row[6],
                            'issend':row[7],
                            'ispaydone':row[8],
                            'isclose':row[9],
                    }
                    allOrdertables.append(ordertable)
                cursor.close()
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
        if request.GET["status"] == "4":
            ispaydone = request.GET["status"];
            cursor = connection.cursor()
            sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND ispaydone = '%s'" % (userid,ispaydone);
            allOrdertables = [];
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ordertable = {
                            'orderid':row[0],
                            'userid':row[1],
                            'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                            'isaudit':row[3],
                            'ispass':row[4],
                            'iscancel':row[5],
                            'ispay':row[6],
                            'issend':row[7],
                            'ispaydone':row[8],
                            'isclose':row[9],
                    }
                    allOrdertables.append(ordertable)
                cursor.close()
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
        if request.GET["status"]=="8":
            isclose = request.GET["status"];
            cursor = connection.cursor()
            sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE userid = '%s'AND isclose = '%s'" % (userid,isclose);
            allOrdertables = [];
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    ordertable = {
                            'orderid':row[0],
                            'userid':row[1],
                            'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                            'isaudit':row[3],
                            'ispass':row[4],
                            'iscancel':row[5],
                            'ispay':row[6],
                            'issend':row[7],
                            'ispaydone':row[8],
                            'isclose':row[9],
                    }
                    allOrdertables.append(ordertable)
                cursor.close()
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
    else:
        orderid = request.POST["orderid"];
        print("000000000000000000000000000")
        cursor = connection.cursor()
        sql = "SELECT orderid,userid,ordertime,isaudit,ispass,iscancel,ispay,issend,ispaydone,isclose FROM ordertable WHERE orderid = '%s'" % orderid;
        allOrdertables = [];
        try:
            cursor.execute(sql)
            for row in cursor.fetchall():
                ordertable = {
                    'orderid':row[0],
                    'userid':row[1],
                    'ordertime':row[2].strftime('%Y-%m-%d %H:%M:%S'),
                    'isaudit':row[3],
                    'ispass':row[4],
                    'iscancel':row[5],
                    'ispay':row[6],
                    'issend':row[7],
                    'ispaydone':row[8],
                    'isclose':row[9],
                }
                allOrdertables.append(ordertable)
            cursor.close()
            print(allOrdertables)
            return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")
# 订单删除接口 吕建威
def ordertableDelete(request):
    cursor = connection.cursor()
    # ordertableid = "123456789"
    ordertableid = request.POST["ordertableid"]
    try:
        result = cursor.execute("DELETE FROM xxx WHERE ordertableid=%s" % ordertableid)
        if result == 1 :
            statusDic = {"status" : "ok" , "message" : "删除订单成功"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            statusDic = {"status" : "error" , "message" : "删除订单失败"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e: 
        # raise e   
        return HttpResponse(json.dumps({'message':"删除订单失败", 'status':'error'}), content_type="application/json");

# 活动查询接口  有待测试
def activeManageJsonSelect(request):
    myData=[]
    cursor=connection.cursor()

    cursor.execute("SELECT activeid,activedetail,activetime FROM activetable")
    try:
        for data in cursor.fetchall():
            activeid=data[0]
            activedetail=data[1]
            activetime=data[2].strftime('%Y-%m-%d %H:%M:%S')
        
            tempDic={"activeid":activeid,"activedetail":activedetail,"activetime":activetime}
            myData.append(tempDic);
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");

# 活动添加接口 刘斌
def activetableManageJsonAdd(request):
        # activeid="123";
        # activetime="465";
        # activedetail="798";
        activeid = request.POST["activeid"]
        activedetail = request.POST["activedetail"]
        cursor=connection.cursor()
        try:
            cursor.execute("INSERT INTO order (activeid,activetime,activedetail) VALUES (%d,%s,%s)"% (activeid,str(activetime),activedetail))
            statusDis={"status":"ok","message":"添加成功"};
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
        except Exception as e :
            statusDis={"status":"error","message":"添加失败"};
            return HttpResponse(json.dumps(statusDis),content_type="application/json");

#图片上传并返回拼接地址   韩乐天
def imgUpload(request):
    uf = UserForm(request.POST,request.FILES)
    test = imagesupload();
    imgpath = test.upload(request)
    return render_to_response('test.html',{'uf':uf})


# 活动删除接口 有待测试 刘斌
def activetableManageJsonDelete(request):
    cursor=connection.cursor()
    active_id = request.POST["activeid"];
    try:
        cursor.execute("DELETE FROM activetable WHERE activeid='%s'"% (active_id))
        cursor.close()
        return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
    except expression as identifier:
        return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
def redpack(request):
    return render(request,"redpack.html")

#浏览记录添加接口 有待测试  韩乐天(OK)
def  lookhistorytableManageJsonAdd(request):
    
    userid = request.GET["userid"];
 
    goodsid = request.GET["goodsid"];
 
    lookid = request.GET["lookid"]
    print(userid , goodsid , lookid)
  
    cursor=connection.cursor()
    try:
        cursor.execute("INSERT INTO lookhistory(userid,goodsid,lookid) VALUES (%s,%s,%s)"% (userid,goodsid,lookid))
        statusDis={"status":"ok","message":"添加成功"};
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        statusDis={"status":"error","message":"添加失败"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#浏览记录查询接口  有待测试  韩乐天(OK)
def lookhistorytableManageJsonSelect(request):
    myData=[]
    userid = request.GET["userid"];
    cursor=connection.cursor()
    cursor.execute("SELECT userid,lookid,goodsid,looktime FROM lookhistory where userid = '%s'"%userid)
    try:
        for data in cursor.fetchall():
            userid=data[0];
            lookid=data[1];
            goodsid =data[2]
            looktime=data[3].strftime('%Y-%m-%d %H:%M:%S');
        
            tempDic={"userid":userid,"lookid":lookid,"goodsid":goodsid,"looktime":looktime}
            myData.append(tempDic);
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");
#浏览记录删除接口 有待测试 韩乐天(OK)
def lookhistorytableManageJsonDelete(request):
    userid = request.GET["userid"];
    cursor=connection.cursor()
    try:
        cursor.execute("DELETE FROM lookhistory where userid = '%s'"%userid);
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
    except Exception as e:   
        # connection.rollback();
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
#浏览记录修改接口  有待测试 韩乐天
def lookhistorytableManageJsonUpdata(request):
    datas = request.POST
    for key in list(datas):
        cursor = connection.cursor()
        cursor.execute("update lookhistory set %s='%s' where userid='%s'"%(key , datas[key] , datas["userid"]))
    data = {'data':'success', 'status':'ok'}
    return HttpResponse(json.dumps(data) , content_type="application/json");

# 问题接口:  商品修改列表修改接口(黄景召)    存在参数给的不对的问题,自己代码思路问题
#           活动添加接口(刘斌)      不清楚时间是什么时间, 结束时间？开始时间？ 存在不明确的问,
#                                 修改了数据库中活动表的时间字段,数据类型由DataTime修改为timestamp,加入默认值为记录创建时间


# # 购物车添加接口 
def cartstableManageJsonAdd(request):
    
    # cartsid = request.carts["cartsid"]
    # number = request.POST["number"]
    # goodsid = request.POST["goodsid"]
    # userid = request.POST["userid"]
    # cursor=connection.cursor()
    
    cursor = connection.cursor()

    name = "liu";
    
    cartsid = "22"
    number = "22"
    goodsid = "22"
    userid = "22"
    result = cursor.execute("INSERT INTO %s_carts(cartsid , number , goodsid , userid) VALUES ('%s' , '%s' , '%s' , '%s' )" % (name,cartsid , number , goodsid , userid))
    
    if result == 1:
        statusDis={"status":"ok","message":"添加成功"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    else:
        statusDis={"status":"error","message":"添加失败"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#购物车删除接口
def cartstableManageJsonDelete(request):
    cursor=connection.cursor()
    # cartsid = request.POST["cartsid"];

    name = "liu";
    cartsid = "222";
    try:
        cursor.execute("DELETE FROM %s_carts WHERE cartsid='%s'" % (name , cartsid))
        cursor.close()
        return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")

#购物车修改接口   
def cartstableManageJsonUpdate(request):
    
    cartsid = "111";
    datas = request.POST
    print(datas)
    try:
        for key in list(datas):
            cursor = connection.cursor()
            cursor.execute("update %s_carts set %s='%s' where cartsid='%s'"%(name , key , datas[key] , datas["cartsid"]))
        statusDis = {'data':'修改成功', 'status':'ok'}
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")

#购物车查询接口
def cartstableManageJsonSelect(request):
   
    cursor = connection.cursor()
    name = "liu";
    cartsid = "111";
    myData = []
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM %s_carts WHERE cartsid=\"%s\"'%(name , cartsid))
    datas = cursor.fetchall()
    for data in datas:
        cartsid = data[0];
        number = data[1];
        goodsid = data[2];
        userid = data[3];
        tempDic = {"cartsid":cartsid , "number":number , "goodsid":goodsid , "userid":userid }
        myData.append(tempDic)

    return HttpResponse(json.dumps(myData) , content_type="application/json");

#添加地址接口
def addAddress(request):

    # addid= request.POST["addid"]
    # userid= request.POST["userid"]
    # username= request.POST["username"]
    # tel= request.POST["tel"]
    # address= request.POST["address"]
    # mailcode= request.POST["mailcode"]
    # flag= request.POST["flag"]

    cursor = connection.cursor()
    addid = "003"
    userid = "0111"
    username = "王五"
    tel = "18538749356"
    address = "软件学院"
    mailcode = "450007"
    flag = "1"
    try:
        cursor.execute("INSERT INTO address (addid , userid , username , tel , address , mailcode , flag) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' )" % (addid , userid , username , tel , address , mailcode , flag))
        statusDis={"status":"ok","message":"添加成功"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDis={"status":"error","message":"添加失败"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#删除地址接口
def delAddress(request):
    cursor = connection.cursor()
    # addid = request.POST["addid"]
    addid = "123"
    
    try:
        cursor.execute("DELETE FROM address WHERE addid=\"%s\""%addid)
        statusDis={"status":"ok","message":"删除成功"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDis={"status":"error","message":"删除失败"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#更新地址接口
def updateAddress(request):
    cursor = connection.cursor()
    datas = request.GET

    try:
        for key in list(datas):
            cursor.execute("update address set %s='%s' where addid='%s'"%(key , datas[key] , datas["addid"]))
            statusDis = {'data':'修改成功', 'status':'ok'}
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")

    # cursor = connection.cursor()
    # cursor.execute("update address set tel='444444' where addid=003")
    # return HttpResponse("a")

#查找地址接口
def findAddress(request):
    cursor = connection.cursor()
    # addid = request.POST["addid"]
    addid = "003"
    myData = []
    try:
        cursor.execute('SELECT * FROM address WHERE addid=\"%s\"' % addid)
        datas = cursor.fetchall()
        for data in datas:
            addid = data[0]
            userid = data[1]
            username = data[2]
            tel = data[3]
            address = data[4]
            mailcode = data[5]
            tempDic = {"addid":addid , "userid":userid , "username":username , "tel":tel , "address":address , "mailcode":mailcode}
            myData.append(tempDic)

        return HttpResponse(json.dumps(myData) , content_type="application/json");

    except:
        statusDis={"status":"error","message":"查找失败"};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    pass

