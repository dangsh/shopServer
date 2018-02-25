from django.shortcuts import render

import re
from django.http import HttpResponse
import qrcode
import os
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
import json, urllib
from urllib.parse import urlencode

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

 
    # name = "liu";
    
    # cursor.execute('CREATE TABLE manager(username varchar(255),pwd varchar(255))')

    # cursor.execute('CREATE TABLE Persons2(Id_P int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255))')
    # cursor.execute('CREATE TABLE carts(cartsid varchar(255),number int, goodsid varchar(255),userid varchar(255))')
    print("uuuuuuuuuxxxxxxxxxxxx")
    is_login = request.session.get('IS_LOGIN')
    print(is_login)
    
    return render(request , "base.html");


def error(request):
    return HttpResponse("我是404");

def adsecondkill(request):
    return render(request , "adsecondkill.html");
def secondkillManage(request):
    return render(request , "secondkillManage.html");

def goodsManage(request):
    baseSelectName = ''
    try:
        baseSelectName = request.POST["baseSelectName"]
        
        print(baseSelectName)
    except:
        pass
    Dict = {'baseSelectName':baseSelectName}
    print(baseSelectName)
    if baseSelectName == "":
        return render(request , "goodsManage.html");
    else:
        return render(request , "goodsManage.html" , {'Dict':json.dumps(Dict)});
    


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
    xx=str.lower(xx);#大写字母转小写
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


#改变轮播图界面
def changePic(request):
    # a = request.POST["goodsid"];
    # print(a);
    return render(request,"changePic.html");

def drawManage(request):
    return render(request,"drawManage.html")


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

    
    statusDic = MyTool.resultOk("创建用户其他表成功");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");



# 登录界面
def login(request):
    request.session['IS_LOGIN'] = True
    return render(request , "login.html");


# 登录接口 (ok)
def loginApi(request):
    global xx; 
    userName = request.POST["username"]
    password = request.POST["password"]
    code=request.POST["code"]
    code=str.lower(code);
    print(userName)
    print(xx);
    if xx==code:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM manager WHERE username=\"%s\" AND pwd=\"%s\"'%(userName , password))
        a = cursor.fetchall()
        cursor.close()
        if a:
            
            successMSG = MyTool.resultOk("登陆成功");
            return HttpResponse(json.dumps(successMSG) , content_type="application/json")
        else:
            
            successMSG = MyTool.resultError("登录失败");
            return HttpResponse(json.dumps(errorMSG) , content_type="application/json")
    else:
        print("验证码错误请重新输入..............")
        errorMSG = MyTool.resultError("登录失败");
        return HttpResponse(json.dumps(errorMSG) , content_type="application/json")
# 用户添加接口
def userManageJsonAdd(request):
    if request.POST["username"]:
        username = request.POST["username"]
    if request.POST["password"]:
        pwd = request.POST["password"]

    
    userid = randomString()
    data = {"username":username , "password":pwd};
    imgName = randomString()+".jpg"
    img_file = r"./shopApp/static/myfile/" + imgName
    img = qrcode.make(data)
    img.save(img_file)

    cursor = connection.cursor();
    cursor.execute("SELECT * FROM user")
    datas=cursor.fetchall()
    cursor.close()
    print("**************88")
    print()
    for i in datas:
        if i[1] == username:
            
            statusDic=MyTool.resultError("用户已存在")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
            break;
    cursor = connection.cursor();
    result = cursor.execute("INSERT INTO user(userid , username , pwd , qrcode)VALUES('%s' , '%s' , '%s' , '%s')"%(userid , username , pwd , imgName))
    cursor.close()
    statusDic = "";
    print("&&&&&&&&&&&")
    if result == 1:
        
        statusDic = MyTool.resultOk("添加用户成功");
        redpackAddCurrency(userid, "注册", "3")
    else :
        
        statusDic = MyTool.resultError("添加用户失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");


# 用户查询接口  有待测试 尚德勋
def userManageJsonSelect(request):
    if request.POST and (request.POST['username'] !="" or request.POST['phone'] != ""):
        username = request.POST['username'].replace(" ","");
        phone = request.POST['phone'].replace(" ","");

        # if username =="" and phone == "":
        #     return HttpResponse(json.dumps({'data':allUsertables, 'status':'用户名和手机号为空'}), content_type="application/json");
        if username == "" and phone !="":
            sql = "SELECT * FROM user where phone like '%%%%%s%%%%'" % phone;
        elif phone == "" and username != "":
            sql = "SELECT * FROM user where username like '%%%%%s%%%%'" % username;
        else:
            sql = "SELECT * FROM user where username like '%%%%%s%%%%' or phone like '%%%%%s%%%%'" % (username, phone);
    else:
        sql = "SELECT * FROM user" ;

    cursor=connection.cursor()
    
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

    #删除头像图片
    cursor=connection.cursor();
    headimg = ""
    cursor.execute("SELECT * FROM user WHERE userid= %s "%(userid));
    datas = cursor.fetchall()
    for data in datas:
        headimg = data[2]  
    # print(headimg)
    aa = os.listdir("../shopServer/shopApp/static/myfile/")
    for item in aa:
        if item == headimg:
            os.remove("../shopServer/shopApp/static/myfile/"+headimg);
    cursor.close();

    #删除二维码图片
    cursor=connection.cursor();
    secondimg = ""
    cursor.execute("SELECT * FROM user WHERE userid= %s "%(userid));
    datas = cursor.fetchall()
    for data in datas:
        secondimg = data[18]  
    # print(headimg)
    aa = os.listdir("../shopServer/shopApp/static/myfile/")
    for item in aa:
        if item == secondimg:
            os.remove("../shopServer/shopApp/static/myfile/"+secondimg);
    cursor.close();

    cursor=connection.cursor();
    try:
        cursor.execute("DELETE  FROM user WHERE userid = %s"%(userid))
        connection.commit();
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
            
    except Exception as e:   
         # connection.rollback();
         return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

def userManageJsonUpdate(request):
    cursor = connection.cursor()
    datas = request.POST
    userid= request.POST["userid"]
    userid = str(userid)
    if request.FILES:
        #前台传过来的图片
        headImgs = request.FILES["headimg"];
        #随机字符串存取图片名字
        headImgsName = randomString() + ".jpg";
        print (headImgsName)
        #当上传头像的时候必然会传过来用户的Id,方法根据前台来决定
        
        cursor.execute("select headimg from user where userid='%s'" % userid)
        data = cursor.fetchall();
        if data[0][0]:
            print(data[0][0])
            tempimg = data[0][0];
            if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
            else:
                pass;
        filepath = "./shopApp/static/myfile/";
        #路径组合
        filepath = os.path.join(filepath,headImgsName)
        #在路径中创建图片名字
        fileobj = open(filepath , "wb");
        #并把前端传过来的数据写到文件中
        fileobj.write(headImgs.__dict__["file"].read());
        cursor.execute("update user set headimg='%s' where userid=%s"%(headImgsName , datas["userid"]))
    for key in datas:
        if key != 'userid' and datas[key] != "":
            cursor.execute("update user set %s='%s' where userid=%s"%(key , datas[key] , datas["userid"]))
    cursor.close();                   
    return HttpResponse(json.dumps(MyTool.resultOk("更新成功")) , content_type="application/json");



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
    statusDic = "";
    cursor = connection.cursor();
    sql = "select images from goods  where goodsid='%s'" % (request.POST["goodsid"]);
    cursor.execute(sql);
    data = cursor.fetchall()
    print(data)
    temimg = data[0][0];
    print("**********&&&&&&&&&&&&")
    print(temimg)
    if not request.FILES:
        statusDic = MyTool.resultError("请选择图片");
    elif  temimg == None:
        imgs = request.FILES["imgsFile"];
        imgsName = randomString() + ".jpg";
        filepath = "./shopApp/static/myfile/";
        filename = os.path.join(filepath,imgsName)
        filename = open(filename , "wb");
        filename.write(imgs.__dict__["file"].read());
        sqlfilename = filepath+imgsName
        result=cursor.execute("UPDATE goods SET images=concat('%s','---') where goodsid='%s'" % (imgsName , request.POST["goodsid"]));
        if result == 1:
            print("插入成功");
           
            statusDic = MyTool.resultOk("添加成功")
        else :
            
            statusDic = MyTool.resultError("数据库更新失败")
    elif temimg.count("---") < 6:
        imgs = request.FILES["imgsFile"];
        imgsName = randomString() + ".jpg";
        filepath = "./shopApp/static/myfile/";
        filename = os.path.join(filepath,imgsName)
        filename = open(filename , "wb");
        filename.write(imgs.__dict__["file"].read());
        sqlfilename = filepath+imgsName
        result=cursor.execute("UPDATE goods SET images=concat('%s','%s---') where goodsid='%s'" % (temimg , imgsName , request.POST["goodsid"]));
        if result == 1:
            print("插入成功");
            
            statusDic = MyTool.resultOk("添加成功")
        else :
           
            statusDic = MyTool.resultError("数据库更新失败");
            

    else:
        statusDic = MyTool.resultOk("轮播图最多添加6个图片");
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
    adId = randomString()
    imgsName = adId + ".jpg";  
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
        
        statusDic = MyTool.resultError("添加失败")
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
        mypage = (int(request.GET["page"]) - 1) * 8
        print(mypage)
        cursor = connection.cursor();
        #以八条数据为一页返回第mypage页,并且按时间排序
        cursor.execute("SELECT * FROM ad order by adtime desc LIMIT %d , 8"%mypage);
        #取出数据
        datas=cursor.fetchall();
        for data in datas:
            adid=data[0];s
            imgs=data[1];
            position=data[2];   
            adtime=data[3].strftime('%Y-%m-%d %H:%M:%S')
            tempDic = {"imgs":imgs , "adid":adid , "position":position,"adtime":str(adtime)}
            myData.append(tempDic)
        #查出总共有多少条数据
        cursor.execute("SELECT COUNT(*) FROM ad")
        adcounts  = cursor.fetchall();
        adcounts = adcounts[0][0];
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'adcounts':str(adcounts)}) , content_type="application/json");
    except Exception as e: 
        # raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'adcounts':'0'}), content_type="application/json");

#广告查询接口
def adManageSelect(request):
    mypages=0
    position=request.POST["position"];
    print(position)
    alladtables=[];
    try:
        cursor=connection.cursor();
        if position!="":
            sql=("select * from ad where position='%s'"%(position));
        else:
            sql="select * from ad ";
        cursor.execute(sql);
        for row in cursor.fetchall():
            adtable={
                'adid':row[0],
                'imgs':row[1],
                'position':row[2],
                'adtime':row[3].strftime('%y-%m-%d %H:%M:%S'),
            }
            alladtables.append(adtable)
        cursor.close()
        return HttpResponse(json.dumps({'data':alladtables,'status':'ok'}),content_type="application/json");
    except Exception as e:
        return HttpResponse(json.dumps({'data':alladtables,'status':'ok'}),content_type="application/json");

#红包管理页面
def redpack(request):
    return render(request,"redpack.html")
#红包添加
def redpackAdd(request):
    userid=request.POST["userid"];
    redpackid=request.POST["redpackid"];
    getpath=request.POST["getpath"];
    money=request.POST["money"];
    print(redpackid,getpath,money);
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO redpack(userid,redpackid,getpath,money) VALUES (%s,%s,%s,%s)"% (userid,redpackid,getpath,money))
        
        statusDis=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        
        statusDis=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#红包添加的通用方法(非接口路由使用)
def redpackAddCurrency(userid, getpath, money):
    redpackid = randomString()
    print("********------------")
    print(redpackid,userid, getpath, money);
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO redpack(userid,redpackid,getpath,money) VALUES (%s,%s,%s,%s)"% (userid,redpackid,getpath,money))
        return True;
    except Exception as e :
        return False;

#红包删除
def redpackDelete(request):
    for key in request.POST:
        redpackid = request.POST.getlist(key)[0]
    cursor=connection.cursor();
    result = cursor.execute("DELETE FROM redpack WHERE redpackid='%s'" % redpackid)
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
    else:
        return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");

#红包查询
def redpackApi(request):
    print("666666666666666666666666666666666")
    commName=request.GET["commName"];
    mypage = 0
    mypage = (int(request.GET["thispage"]) - 1) * 10
    sql="SELECT * from redpack WHERE userid like '%%%%%s%%%%' LIMIT %d , 10"%(commName , mypage);   
    try:
        print(sql)
        allOrdertables = [];
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            ordertable = {
                'userid':row[0],
                'redpackid':row[1],
                'getpath':row[2],
                'money':row[3],
                'gettime':row[4].strftime('%Y-%m-%d %H:%M:%S'),
            }
            allOrdertables.append(ordertable)
        cursor.close()
        #获取数据总长度
        sql="SELECT COUNT(*) from redpack WHERE userid like '%%%%%s%%%%'"%(commName);
        cursor = connection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()[0][0]
        cursor.close()
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok' , 'myresult':myresult}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error'}), content_type="application/json")

        

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
    datas = request.POST
    print(datas)
    goodsid = randomString()
    print(goodsid)
    sql = "INSERT INTO goods ("
    for item in datas:
        sql = sql + item + ","
    sql = sql[0:-1]    
    sql = sql +',goodsid' ") values (";
    for key in datas:
        oneValue = datas[key]
        sql = sql + "'" + oneValue + "',"
    sql = sql[0:-1]
    sql = sql +','+"'"+goodsid+"'" ")"
    print(sql);
    try:
        cursor = connection.cursor()
        result = cursor.execute(sql)  
        cursor.close();  
        if result == 1:
            
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else :
            
            statusDic=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:
        raise e  
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
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d %H:%M:%S'),
                'proend':row[20].strftime('%Y-%m-%d %H:%M:%S'),
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
            cursor.execute("DELETE FROM lucky where goodsid = '%s'"%(goodsid))
            result += cursor.execute("DELETE FROM goods where goodsid = '%s'"%(goodsid))
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
    print(goodsid)
    sql = "SELECT * FROM goods WHERE goodsid = '%s'" % goodsid
    allGoodMes = []
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row[4]);
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
    timeUP = request.GET["timeUP"]
    sellcountBtnUp = request.GET["sellcountBtnUp"]
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    Status = ''
    if timeUP == '0' and sellcountBtnUp == '0':
        url = "SELECT * FROM goods where goodsname like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName, Status, mypage)
    elif timeUP == '1' and sellcountBtnUp == '':
        Status = "desc"
        url = "SELECT * FROM goods where goodsname like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName, Status, mypage)
    elif timeUP == '' and sellcountBtnUp == '0':
        url = "SELECT * FROM goods where goodsname like '%%%%%s%%%%' order by sellcount %s LIMIT %d , 10;"%(commName, Status, mypage)
    elif timeUP == '' and sellcountBtnUp == '1':
        Status = "desc"
        url = "SELECT * FROM goods where goodsname like '%%%%%s%%%%' order by sellcount %s LIMIT %d , 10;"%(commName, Status, mypage)
    elif timeUP == '' and sellcountBtnUp == '':
        url = "SELECT * FROM goods where goodsname like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName, Status, mypage)
    elif timeUP == '0' and sellcountBtnUp == '':
        url = "SELECT * FROM goods where goodsname like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName, Status, mypage)
    cursor.execute(url);
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
                'color':row[7],
                'size':row[8],
                'principal':row[9],
                'counts':row[10],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'price':row[5],
                'goodsname':row[16],
                'stock':row[11],
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
                'sellcount':row[22],
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


# 商品修改列表修改接口 有待测试 黄景召
def goodsManageJsonUpdata(request):

    datas = request.POST
    tempDict = {};
    for key in datas:
        value = datas[key]
        key = key.strip("#");
        tempDict[key] = value
        

    for key in list(tempDict):
        cursor = connection.cursor()

        cursor.execute("update goods set %s='%s' where goodsid='%s'"%(key , tempDict[key] , tempDict["goodsid"]));
    
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

# 订单查询列表接口
def ordertabalelistJaon(request):
    sql="";
    selectCount=0
    mypage = 0
    selectpage =0
    try:
        selectpage = request.POST["selectpage"]
    except:
        pass

    mypage = (int(selectpage) - 1) * 10
    print(request.POST)
    if request.POST and (request.POST["userid"]!="" or request.POST["orderid"]!="" or request.POST["status"]!="0"):
        # print(request.POST)
        userid = request.POST["userid"]
        orderid = request.POST["orderid"];
        status=request.POST["status"];
        print("xxxxxxxxxxxxxxxxxxxx",status)
        if userid=="" and orderid!="":
            sql="SELECT * from ordertable WHERE orderid='%s'"%(orderid);
            cursor2 = connection.cursor();
            cursor2.execute("SELECT COUNT(*) FROM ordertable WHERE orderid='%s'"%(orderid))
            selectCount  = cursor2.fetchall();
            cursor2.close()
            selectCount = selectCount[0][0]

        elif userid!="" and orderid=="":
            if status=="0":
                sql="SELECT * from ordertable WHERE userid='%s'"%(userid);
                cursor2 = connection.cursor();
                cursor2.execute("SELECT COUNT(*) FROM ordertable WHERE userid='%s'"%(userid))
                selectCount  = cursor2.fetchall();
                cursor2.close()
                selectCount = selectCount[0][0]
            else :
                sql="SELECT * from ordertable WHERE userid='%s' AND status='%s'"%(userid,status);
                print(sql)
                cursor2 = connection.cursor();
                cursor2.execute("SELECT COUNT(*) FROM ordertable WHERE userid='%s' AND status='%s'"%(userid,status))
                selectCount  = cursor2.fetchall();
                cursor2.close()
                selectCount = selectCount[0][0]

        elif userid=="" and orderid=="":
            sql="SELECT * from ordertable WHERE status='%s'"%(status);
            cursor2 = connection.cursor();
            cursor2.execute("SELECT COUNT(*) FROM ordertable WHERE status='%s'"%(status))
            selectCount  = cursor2.fetchall();
            cursor2.close()
            selectCount = selectCount[0][0]

        else:
            pass;
    else:
        print("xxxxxxxxxxx")
        sql = "SELECT * FROM ordertable";   
        cursor2 = connection.cursor();
        cursor2.execute("SELECT COUNT(*) FROM ordertable")
        selectCount  = cursor2.fetchall();
        cursor2.close()
        selectCount = selectCount[0][0]
    try:
        allOrdertables = [];
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            ordertable = {
                'orderid':row[1],
                'userid':row[0],
                'price':row[2],
                'ordertime':row[3].strftime('%Y-%m-%d %H:%M:%S'),
                'status':row[4],
            }
            allOrdertables.append(ordertable)
        cursor.close()
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok' , 'selectCount':str(selectCount)}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'error' , 'selectCount':str(selectCount)}), content_type="application/json")
# 订单删除接口 吕建威
def ordertableDelete(request):
    for key in request.POST:
        orderid = request.POST.getlist(key)[0]
    cursor=connection.cursor();
    result = cursor.execute("DELETE FROM ordertable WHERE orderid='%s'" % orderid)
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
    else:
        return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
# 活动查询接口  有待测试
def activeManageJsonSelect(request):
    myData=[]
    cursor=connection.cursor()

    cursor.execute("SELECT * FROM activetable ORDER BY activeid DESC")
    try:
        for data in cursor.fetchall():
            activeid=data[0]
            activedetail=data[1]
            starttime=data[2].strftime('%Y-%m-%d %H:%M:%S')
            imgs = data[3]
            stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S')
            activetitle = data[5]
            activeName = data[6]
            activePosition = data[7]
            tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
            myData.append(tempDic);
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");

# 活动添加接口 刘斌
def activetableManageJsonAdd(request):
    datas = request.POST
    imagesName = "None"
    #前台传过来的图片
    if request.FILES.get('imgs',False):
        print("gygygygygygygy")
        images = request.FILES["imgs"];
        #随机字符串存取图片名字
        imagesName = randomString() + ".jpg";
        #判断是否存在
        if os.path.exists("../shopServer/shopApp/static/myfile/"+imagesName)==True:
            os.remove("../shopServer/shopApp/static/myfile/"+imagesName);
        else:
            pass;
        filepath = "./shopApp/static/myfile/";
        #路径组合
        filepath = os.path.join(filepath,imagesName)
        #在路径中创建图片名字
        fileobj = open(filepath , "wb");
        #并把前端传过来的数据写到文件中
        fileobj.write(images.__dict__["file"].read());

        activeid = randomString()
        sql = "INSERT INTO activetable ("
        for item in datas:
            sql = sql + item + ","
        sql = sql[0:-1]    
        sql = sql +',activeid,imgs' ") values (";
        for key in datas:
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        sql = sql[0:-1]
        sql = sql +','+"'"+activeid+"','" + imagesName +"'" ")"

    else:
        activeid = randomString()
        sql = "INSERT INTO activetable ("
        for item in datas:
            sql = sql + item + ","
        sql = sql[0:-1]    
        sql = sql +',activeid' ") values (";
        for key in datas:
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        sql = sql[0:-1]
        sql = sql +','+"'"+activeid+"'" ")"
    print("************************")
    print(sql)
          
    cursor=connection.cursor()
    try:
        cursor.execute(sql)
        cursor.execute("SELECT * FROM activetable WHERE activeid='%s'" %activeid)
        data = cursor.fetchall()[0]
        activeid=data[0]
        activedetail=data[1]
        starttime=data[2].strftime('%Y-%m-%d %H:%M:%S')
        imgs = data[3]
        stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S')
        activetitle = data[5]
        activeName = data[6]
        activePosition = data[7]
        tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
        # cursor.execute("INSERT INTO order (activeid,activetime,activedetail) VALUES (%d,%s,%s)"% (activeid,str(activetime),activedetail))
        statusDis={"status":"ok","message":"添加成功","addactive":tempDic};
        
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        raise e
       
        statusDis=MyTool.resultError("添加失败")
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
    print(".........................................")
    active_id = request.GET["dataId"];
    print(active_id)
    try:
        cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % active_id)
        data = cursor.fetchall();
        if data[0][0]:
            print(data[0][0])
            tempimg = data[0][0];
            if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
            else:
                pass;
        cursor.execute("DELETE FROM activetable WHERE activeid='%s'"% (active_id))
        cursor.close()
        return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
    except expression as identifier:
        return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
def redpack(request):
    
    return render(request,"redpack.html")

# 活动批量删除接口 胡亚洲
def activesManageJsonDelete(request):
    activeidsDict =  request.POST
    activeids = activeidsDict.getlist("activeids")
    cursor=connection.cursor();
    result = 0
    try:
        for activeid in activeids:
            cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % activeid)
            data = cursor.fetchall();
            if data[0][0]:
                print(data[0][0])
                tempimg = data[0][0];
                if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                    os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
                else:
                    pass;
            result += cursor.execute("DELETE FROM activetable where activeid = '%s'"%(activeid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");



#浏览记录添加接口 有待测试  韩乐天(OK)
def  lookhistorytableManageJsonAdd(request):
    
    userid = request.GET["userid"];
    goodsid = request.GET["goodsid"];
    lookid = request.GET["lookid"]
    print(userid , goodsid , lookid) 
    cursor=connection.cursor()
    try:
        cursor.execute("INSERT INTO lookhistory(userid,goodsid,lookid) VALUES (%s,%s,%s)"% (userid,goodsid,lookid))
        
        statusDis=MyTool.resultOk("添加成功")
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
       
        statusDis=MyTool.resultError("添加失败")

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
#收藏功能添加接口  韩乐天  有待测试(ok)
def favoritetableManageJsonAdd(request):
    userid = request.POST["userid"];
    favoriteid = request.POST["favoriteid"];
    goodsid = request.POST["goodsid"];
    cursor=connection.cursor()
    try:
        # print(userid , favoriteid , goodsid)
        cursor.execute("INSERT INTO favorite (userid,favoriteid,goodsid) VALUES(%s,%s,%s)"% (userid,favoriteid,goodsid))
        
        statusDis=MyTool.resultOk("添加成功")
        # print("555555555555555555")
        cursor.close()
        return HttpResponse(json.dumps(statusDis), content_type = "application/json");
    except Exception as e :
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis), content_type = "application/json");
#收藏功能查询接口  韩乐天 有待测试(ok)
def favoritetableManageJsonSelect(request):
    myData=[]
    userid = request.POST["userid"];   
    cursor=connection.cursor()
    cursor.execute("SELECT userid,favoriteid,goodsid,favtime FROM favorite where userid='%s'"%userid)
    print(userid)
    try:
        print("55")
        for data in cursor.fetchall():
            print(data)
            userid=data[0];
            favoriteid=data[1];
            goodsid =data[2]
            favtime=data[3].strftime('%Y-%m-%d %H:%M:%S');
            tempDic={"userid":userid,"favoriteid":favoriteid,"goodsid":goodsid,"favtime":favtime}
            myData.append(tempDic);
            print(userid , favoriteid , goodsid , favtime)
        cursor.close()
        print(myData)
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}),  content_type = "application/json");      
    except Exception as e:   
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type = "application/json");
#收藏功能删除接口 有待测试 韩乐天(ok)
def favoritetableManageJsonDelete(request):
    userid = request.POST["userid"];
    cursor=connection.cursor()
    try:
        cursor.execute("DELETE FROM favorite where userId = '%s'"%userid);
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}),  content_type = "application/json");
    except Exception as e:   
        # connection.rollback();
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) ,  content_type = "application/json");
#收藏功能修改接口  有待测试 韩乐天
def favoritetableManageJsonUpdata(request):
    datas = request.POST
    for key in list(datas):
        cursor = connection.cursor()
        cursor.execute("update favorite set %s='%s' where userid='%s'"%(key , datas[key] , datas["userid"]))
    data = {'data':'success', 'status':'ok'}
    return HttpResponse(json.dumps(data) ,  content_type = "application/json");
# 问题接口:  商品修改列表修改接口(黄景召)    存在参数给的不对的问题,自己代码思路问题
#           活动添加接口(刘斌)      不清楚时间是什么时间, 结束时间？开始时间？ 存在不明确的问,
#                                 修改了数据库中活动表的时间字段,数据类型由DataTime修改为timestamp,加入默认值为记录创建时间

 # 购物车添加接口 
def cartstableManageJsonAdd(request):   
    # cartsid = request.carts["cartsid"]
    # number = request.POST["number"]
    # goodsid = request.POST["goodsid"]
    # userid = request.POST["userid"]  
    cursor = connection.cursor()
    name = "liu";   
    cartsid = "22"
    number = "22"
    goodsid = "22"
    userid = "22"
    result = cursor.execute("INSERT INTO %s_carts(cartsid , number , goodsid , userid) VALUES ('%s' , '%s' , '%s' , '%s' )" % (name,cartsid , number , goodsid , userid))   
    if result == 1:
        statusDis=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    else:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#购物车删除接口
def cartstableManageJsonDelete(request):
    for key in request.POST:
        cartsid = request.POST.getlist(key)[0]
    cursor=connection.cursor()
    name = "liu";
    # cartsid = request.GET["id"];
    try:
        result = cursor.execute("DELETE FROM %s_carts WHERE cartsid='%s'" % (name , cartsid))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")
#购物车修改接口   
def cartstableManageJsonUpdate(request):
    cursor = connection.cursor();
    cartsid = request.GET["id"];   
    datas = request.POST
    Num = datas["num"];
    print(cartsid);
    print(Num);  
    result = cursor.execute("update liu_carts set number='%s' where cartsid='%s'"%(Num , cartsid))
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({"message":"修改成功","status":"ok"}),content_type="application/json")
    else:
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
#添加抽奖余额接口
def drawJsonAdd(request):  
    cursor = connection.cursor() 
    userid = request.POST["userid"];
    drawmoney = request.POST["drawmoney"];
    drawdetail = request.POST["drawdetail"];
    username = "11111"
    drawid = randomString();
    try:
        cursor.execute("INSERT INTO draw (userid , drawmoney , username , drawdetail , drawid) VALUES ('%s' , '%s' , '%s' , '%s' , '%s')" % (userid , drawmoney , username , drawdetail , drawid))
        statusDis=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#删除抽奖余额接口
def drawJsonDel(request):
    cursor = connection.cursor()
    userid = request.POST["userid"];
    drawid = request.POST["drawid"];   
    try:
        cursor.execute("DELETE FROM draw WHERE drawid=\"%s\""%drawid)
        statusDis=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#更新抽奖接口
def drawJsonUpdate(request):
    cursor = connection.cursor()
    datas = request.POST
    try:
        for key in list(datas):
            cursor.execute("update draw set %s='%s' where userid='%s'"%(key , datas[key] , datas["userid"]))
            statusDis=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
# 查询抽奖余额接口
def drawJsonQuery(request):
    cursor = connection.cursor()
    userid = request.POST["userid"]
    myData = []
    try:
        cursor.execute('SELECT * FROM draw WHERE userid=\"%s\"' % userid)
        datas = cursor.fetchall()
        print(datas)
        for data in datas:
            userid = data[0];
            drawmoney = data[1];
            drawtime = data[2].strftime('%Y-%m-%d %H:%M:%S');
            username = data[3];
            drawid = data[4];
            drawdetail = data[5];
            tempDic = {"userid":userid , "drawmoney":drawmoney , "drawtime":drawtime ,"username":username , "drawid":drawid , "drawdetail":drawdetail}
            myData.append(tempDic)

        return HttpResponse(json.dumps(myData) , content_type="application/json");
    except:
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    pass
# 福袋管理页面 胡亚洲
def luckyManage(request):
    return render(request , "luckyManage.html");
# 福袋模糊查询(分页) 胡亚洲
def luckyManageJsonQuery(request):
    myData = []
    timeUP = "0"
    cursor = connection.cursor()
    commName = request.GET["commName"]
    timeUP = request.GET["timeUp"]
    timeStatus = "desc"
    if timeUP == '1':
        timeStatus = ""
    mypage = 0
    luckycount = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor.execute("SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid and goods.goodsname like '%%%%%s%%%%' order by lucky.uptime %s LIMIT %d , 10;"%(commName, timeStatus, mypage));
    datas = cursor.fetchall()
    try:
        for row in datas:
            try:
                uptime = row[5].strftime('%Y-%m-%d %H:%M:%S')
            except:
                uptime = "未知"
            lucky = {
                'luckyid':row[0],
                'goodsid':row[1],
                'goodsname':row[2],
                'counts':row[3],
                'price':row[4],
                'uptime':uptime,
            }
            myData.append(lucky);
        cursor.execute("SELECT COUNT(*) FROM goods,lucky where lucky.goodsid=goods.goodsid and goods.goodsname like '%%%%%s%%%%'" % (commName))
        luckycount = cursor.fetchall()[0][0]
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'luckycount':str(luckycount) }), content_type="application/json")
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");
# 福袋列表删除接口 胡亚洲
def luckyManageJsonDelete(request):
    luckyidsDict =  request.POST
    luckyids = luckyidsDict.getlist("luckyids")
    cursor=connection.cursor();
    result = 0
    try:
        for luckyid in luckyids:
            result += cursor.execute("DELETE FROM lucky where luckyid = '%s'"%(luckyid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
# 福袋修改列表修改接口 胡亚洲
def luckyManageJsonUpdata(request):
    print(request.POST)
    num=request.POST["num"];
    luckyid=request.POST["luckyid"]
    try:
        cursor = connection.cursor()
        cursor.execute("update lucky set counts='%s' where luckyid='%s'"%(num , luckyid))
        data = {'data':'success', 'status':'ok'}
        return HttpResponse(json.dumps(data) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'修改失败' , "status":"error"}) , content_type="application/json");
# 福袋添加接口 胡亚洲
def luckyManageJsonAdd(request):
    luckyid = randomString()
    try:
        goodsName = request.POST["goodsName"]
        counts = request.POST["counts"]
        print(luckyid, goodsName, counts)
        cursor2 = connection.cursor()
        sql2 = "SELECT goodsid from goods where goodsname='%s'"%goodsName
        cursor2.execute(sql2)
        goodsid = cursor2.fetchall()[0][0]
        cursor2.close()
        cursor = connection.cursor()
        sql = "INSERT INTO lucky (luckyid , goodsname , counts , goodsid) VALUES('%s','%s','%s','%s')" % (luckyid, goodsName, counts , goodsid)
        result = cursor.execute(sql)
        if result == 1 :
            statusDic = {"status" : "ok" , "message" : "添加成功"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            statusDic = {"status" : "error" , "message" : "添加失败"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");

#通过商品号查询福袋数
def selectLuckyJsonByGoodsId(request):
    myData = []
    goodsidsDict =  request.POST
    goodsids = goodsidsDict.getlist("goodsids")
    print("qqqqqq", goodsids)
    try:
        for goodsid in goodsids:
            oneData = []
            cursor = connection.cursor();
            luckycount = cursor.execute("SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid and goods.goodsid = '%s'" % (goodsid))
            datas = cursor.fetchall();
            for row in datas:
                try:
                    uptime = row[5].strftime('%Y-%m-%d %H:%M:%S')
                except:
                    uptime = "未知"
                lucky = {
                    'luckyid':row[0],
                    'goodsid':row[1],
                    'goodsname':row[2],
                    'counts':row[3],
                    'price':row[4],
                    'uptime':uptime,
                }
                oneData = {
                    'luckyData':lucky,
                    'luckyCount':luckycount,
                }
            cursor.close();
            if luckycount > 0:
                myData.append(oneData)
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'luckycount':str(len(myData)) }), content_type="application/json")
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");
# 评论查询(通过商品id) 胡亚洲
def commentJsonQuery(request):
    myData = []
    cursor = connection.cursor()
    goodsid = request.GET["goodsid"]
    mypage = 0
    luckycount = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    luckycount = cursor.execute("SELECT commentid , goodsid , userid , comment_text FROM comment where goodsid='%s' LIMIT %d , 10;"%(goodsid, mypage));
    datas = cursor.fetchall()
    try:
        for row in datas:
            try:
                uptime = row[4].strftime('%Y-%m-%d %H:%M:%S')
            except:
                uptime = "未知"
            comment = {
                'commentid':row[0],
                'goodsid':row[1],
                'userid':row[2],
                'comment_text':row[3],
                'uptime':uptime,
            }
            myData.append(comment);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'luckycount':str(luckycount) }), content_type="application/json")
    
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

# 评论查询(通过用户id和商品id) 胡亚洲
def commentJsonQuery(request):
    myData = []
    cursor = connection.cursor()
    userid = request.GET["userid"]
    goodsid = request.GET["goodsid"]
    mypage = 0
    luckycount = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    luckycount = cursor.execute("SELECT commentid , goodsid , userid , comment_text FROM comment where userid='%s' and goodsid='%s' LIMIT %d , 10;"%(userid, goodsid, mypage));
    datas = cursor.fetchall()
    try:
        for row in datas:
            try:
                uptime = row[4].strftime('%Y-%m-%d %H:%M:%S')
            except:
                uptime = "未知"
            comment = {
                'commentid':row[0],
                'goodsid':row[1],
                'userid':row[2],
                'comment_text':row[3],
                'uptime':uptime,
            }
            myData.append(comment);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'luckycount':str(luckycount) }), content_type="application/json")
    
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

# 评论删除接口 胡亚洲
def commentJsonDelete(request):
    commentidsDict =  request.POST
    commentids = luckyidsDict.getlist("commentids")
    cursor=connection.cursor();
    result = 0
    try:
        for commentid in commentids:
            result += cursor.execute("DELETE FROM comment where commentid = '%s'"%(commentid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

# 评论添加接口 胡亚洲
def commentJsonAdd(request):
    try:
        commentid = randomString()
        goodsid = request.POST["goodsid"]
        userid = request.POST["userid"]
        comment_text = request.POST["comment_text"]
        cursor = connection.cursor()
        sql = "INSERT INTO comment (commentid , goodsid , userid , comment_text) VALUES('%s','%s','%s','%s')" % (commentid, goodsid, userid, comment_text)
        result = cursor.execute(sql)
        if result == 1 :
            statusDis=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            statusDic=MyTool.resultError("添加失败");
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");

#购物车获取数据接口
def cartstableManageJsonGain(request):
    cursor = connection.cursor()
    name = "liu";
    myData = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s_carts" % (name));
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
        statusDis=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#删除地址接口
def delAddress(request):
    cursor = connection.cursor()
    # addid = request.POST["addid"]
    addid = "123"
    
    try:
        cursor.execute("DELETE FROM address WHERE addid=\"%s\""%addid)
        statusDis=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#更新地址接口
def updateAddress(request):
    cursor = connection.cursor()
    datas = request.POST

    try:
        for key in list(datas):
            cursor.execute("update address set %s='%s' where addid='%s'"%(key , datas[key] , datas["addid"]))
            statusDis=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")


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
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    pass


#删除余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def delMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        sql = "delete from remainmoney where userId='%s'" % userid;
        cursor = connection.cursor();
        result = cursor.execute(sql);
        if result:
            statusDis=MyTool.resultOk("删除成功")
        else:
            statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

#添加余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def addMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        money = request.GET["money"];
        sql = "insert into remainmoney (userId , money) values('%s','%s')" % (userid , money);
        cursor = connection.cursor();
        result = cursor.execute(sql);
        if result:
            statusDis=MyTool.resultOk("添加成功")
        else:
            statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
#更新余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def updateMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        money = request.GET["money"];
        sql = "update remainmoney set money='%s' where userId='%s'" % (money ,userid);
        cursor = connection.cursor();
        result = cursor.execute(sql);
        if result:
            statusDis=MyTool.resultOk("修改成功")
        else:
            statusDic=MyTool.resultError("修改失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
#查询余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def findMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        print (userid);
        sql = "select * from remainmoney where userId='%s'" % userid;
        print(sql);
        cursor = connection.cursor();
        datas = cursor.execute(sql);
        myData = [];
        datas = cursor.fetchall()
        print (datas);
        if datas:
            for data in datas:
                userid = data[0];
                money = data[1];
                tempDic = {"userId":userid , "money":money}
                myData.append(tempDic)
            statusDic = {"data" : myData,"status" : "ok", "message" : "查找成功"};
        else:
            statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
         
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

#添加分享接口
#查询用户留言接口
def leaveMessage(request):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM message')
    a = cursor.fetchall()
    print(a)
    cursor.close()
    imgDic = []
    for i in a:
        aaa = {"goodsid":i[0] , "userid":i[1] , "leavemessage":i[2]}
        imgDic.append(aaa)
    return HttpResponse(json.dumps(imgDic) , content_type = "application/json")

#增加用户留言接口
def addLeaveMessage(request):
    data = request.POST
    goodsid = data["goodsid"]
    userid = data["userid"]
    leavemessage = data["leavemessage"]
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # goodsid = "2017121519245103"
    # userid = "2017121519245103"
    # leavemessage = "啥的感觉爱仕达将刷机大师"
    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO message(goodsid , userid , leavemessage)VALUES('%s' , '%s' , '%s')"%(goodsid , userid , leavemessage))
    cursor.close()
    if result == 1:
         statusDis=MyTool.resultOk("留言添加成功")
    else :
        statusDic=MyTool.resultError("留言添加失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")

#删除用户留言接口
def deleLeaveMessage(request):
    data = request.POST
    goodsid = data["goodsid"]
    userid = data["userid"]
    # goodsid = "2017121115433480"
    # userid = "2017121517150701"
    # print("***********************8")
    cursor = connection.cursor()
    sql = " delete from message where goodsid = '"+goodsid+"' and userid = '" + userid +"'"
    result = cursor.execute(sql)
    cursor.close() 
    if result == 0:
        statusDis=MyTool.resultOk("留言删除成功")
    else :
        statusDic=MyTool.resultError("留言删除失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")

#添加分享接口
def addShare(request):

    # shareid = request.POST["shareid"]
    # goodsid = request.POST["goodsid"]
    # userid = request.POST["userid"]
    # friendid = request.POST["friendid"]

    cursor = connection.cursor()
    shareid = "1111"
    goodsid = "2221"
    userid = "3331"
    friendid = "4441"
    try:
        cursor.execute("INSERT INTO share (shareid , goodsid , userid , friendid) VALUES ('%s' , '%s' , '%s' , '%s')" % (shareid , goodsid , userid , friendid))
        statusDis=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#删除分享接口
def delShare(request):
    cursor = connection.cursor()
    # shareid = request.POST["shareid"]
    shareid = "001"
    
    try:
        cursor.execute("DELETE FROM share WHERE shareid=\"%s\""%shareid)
        statusDis=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#更新分享接口
def updateShare(request):
    
    cursor = connection.cursor()
    datas = request.POST

    try:
        for key in list(datas):
            cursor.execute("update share set %s='%s' where shareid='%s'"%(key , datas[key] , datas["shareid"]))
            statusDis=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json");
#查找分享接口
def findShare(request):
    cursor = connection.cursor()
    # shareid = request.POST["shareid"]
    shareid = "111"
    myData = []
    try:
        cursor.execute('SELECT * FROM share WHERE shareid=\"%s\"' % shareid)
        datas = cursor.fetchall()
        for data in datas:
            shareid = data[0]
            goodsid = data[1]
            userid = data[2]
            friendid = data[3]
            tempDic = {"shareid":shareid , "goodsid":goodsid , "userid":userid , "friendid":friendid}
            myData.append(tempDic)

        return HttpResponse(json.dumps(myData) , content_type="application/json");

    except:
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");


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
                'status':row[4]
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

#积分添加接口
def scoreAdd(request):
    userid = "1111"
    scoreid = "2221"
    scoretime = "3331"
    scorecount = "4441"
    getpath = "5551"
    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO score(userid , scoreid , scoretime , scorecount , getpath) VALUES ('%s' , '%s' , '%s' ,'%s' ,'%s')" % (userid , scoreid , scoretime , scorecount , getpath))
    try:
        if result == 1:
            statusDis=MyTool.resultOk("添加成功");
            cursor.close()
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#积分删除接口
def scoreDelete(request):
    scoreid = request.POST["scoreid"]
    try:
        cursor.execute("DELETE * FROM score WHERE %s" %(scoreid))
        statusDis=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#积分查询接口
def scoreSelect(request):
    userid = request.POST["userid"]
    cursor=connection.cursor()
    myData=[]
    cursor.execute("SELECT (userid , scoreid , scoretime , scorecount ,getpath) FROM score WHERE userid = %s" %userid)
    try:
        for data in cursor.fetchall():
            userid=data[0]
            scoreid=data[1]
            scoretime=data[2]
            scorecount = data[3]
            getpath = data[4]
            tempDic={"userid":userid,"scoreid":scoreid,"scoretime":scoretime,"scorecount":scorecount,"getpath":getpath}
            myData.append(tempDic)
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");

# 购买历史添加接口
def buyhistoryAdd(request):

    userid=goodsid=goodsname=buytime=price=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO buyhistory(userid , goodsid , goodsname , buytime , price) VALUES ('%s' , '%s' , '%s' ,'%s' ,'%s')" % (userid , goodsid , goodsname , buytime , price))
    try:
        if result == 1:
            statusDis=MyTool.resultOk("添加成功");
            cursor.close()
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#购买记录删除接口
def buyhistoryDelete(request):
    goodsid = request.POST["goodsid"]
    try:
        cursor.execute("DELETE * FROM buyhistory WHERE %s" %(goodsid))
        statusDis=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

# #积分查询按钮 吕建威
# def scoreSelect(request):

# #积分查询按钮 吕建威
# def scoreSelect(request):
#购买记录查询接口
def buyhistorySelect(request):
    userid = request.POST["userid"]
    cursor=connection.cursor()
    myData=[]
    cursor.execute("SELECT * FROM buyhistory WHERE userid = %s" %userid)
    try:
        for data in cursor.fetchall():
            userid=data[0]
            goodsid=data[1]
            goodsname=data[2]
            buytime = data[3]
            price = data[4]
            tempDic={"userid":userid,"goodsid":goodsid,"goodsname":goodsname,"buytime":buytime,"price":price}
            myData.append(tempDic)
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");

#好友列表查询功能
def friendslistManageJsonSelect(request):
    # friendslistid = request.friendsList["friendslistid"]
    friendslistid = "11"
   
    myData = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM friendsList WHERE friendslistid='%s'" % (friendslistid))
    for data in cursor.fetchall():
        friendslistid = data[0];
        userid = data[1];
        friendid = data[2];
        setuptime = data[3].strftime('%Y-%m-%d %H:%M:%S');
    
        tempDic = {"friendslistid":friendslistid , "userid":userid , "friendid":friendid , "setuptime":setuptime}
        myData.append(tempDic)
    cursor.close()
    return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
def settings(request):
    return render(request,"setting.html")
def settingsApi(request):
    sql="";
    if request.POST and (request.POST["settingid"]!=""):
        print("666666666666666666666666666666666")
        settingid=request.POST["settingid"];     
        sql="update settingtable redmoney='%s',rebatepercent='%s',rebatevalue='%s' WHERE settingid='%s'"%(redmoney,rebatepercent,rebatevalue,settingid);
     
    else:
        sql = "SELECT * FROM settingtable";   
    # try:
    print(sql)
    allOrdertables = [];
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        ordertable = {
            'settingid':row[0],
            'redmoney':row[1],
            'rebatepercent':row[2],
            'rebatevalue':row[3],
        }
        allOrdertables.append(ordertable)
    cursor.close()
    return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")

def settingsAdd(request):
    settingid=request.POST["settingid"];
    redmoney=request.POST["redmoney"];
    rebatepercent=request.POST["rebatepercent"];
    rebatevalue=request.POST["rebatevalue"];
    print(settingid,redmoney,rebatevalue);
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO settingtable(settingid,redmoney,rebatepercent,rebatevalue) VALUES (%s,%s,%s,%s)"% (settingid,redmoney,rebatepercent,rebatevalue))
        statusDis=MyTool.resultOk("添加成功");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
def settingsUpdate(request):   
    cursor = connection.cursor()
    
    datas = request.POST
    settingid= request.POST["settingid"]
    settingid = str(settingid)
    for key in datas:
        if key != 'settingid' and datas[key] != "":
            cursor.execute("update settingtable set %s='%s' where settingid=%s"%(key , datas[key] , datas["settingid"]))
    cursor.close();                   
    return HttpResponse(json.dumps({"message":"更新成功" , "status":"ok"}) , content_type="application/json");

#base页面消息接口
def guestbookSelect(request):  
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM guestbook")
    data = cursor.fetchall()
    dataArr = []
    for i in data:
        userid = i[1]
        cursor.execute("SELECT * FROM user WHERE userid= %s "%(userid))
        userA = cursor.fetchall()
        userName = userA[0][1]
        userHeading = userA[0][2]
        ss = {"guestbookid":i[0] , "userid":i[1] , "leavemessage":i[2] , "leavtime":str(i[3]) , "status":i[4] , "username":userName , "userHeading":userHeading}
        dataArr.append(ss)
    cursor.close();
                     
    return HttpResponse(json.dumps({"data":dataArr , "status":"ok"}) , content_type="application/json");


def leavingMessage(request):
    return render(request , "leavingMessage.html");

#获取session接口
def getSession(request):
    is_login = request.session.get('IS_LOGIN',False)
    # print(is_login)
    return HttpResponse(json.dumps({"data":is_login , "status":"ok"}) , content_type="application/json");
#设置session接口
def setSession(request):
    request.session['IS_LOGIN'] = False
    is_login = request.session.get('IS_LOGIN')
    print(is_login)
    return HttpResponse(json.dumps({"status":"ok"}) , content_type="application/json");
#获取当前时间
def getdatatime(request):
    secondkill = "";
    string = '2014-01-08 11:59:58'
    time1 = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
    starttime = request.POST["starttime"];
    stoptime = request.POST["stoptime"]
    a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    starttime= datetime.datetime.strptime(starttime,"%Y-%m-%d %H:%M:%S")  
    stoptime = datetime.datetime.strptime(stoptime,"%Y-%m-%d %H:%M:%S")  
    nowtime= datetime.datetime.strptime(a,"%Y-%m-%d %H:%M:%S")

    nowtime = int((nowtime - time1).seconds);
    starttime = int((starttime-time1).seconds);
    stoptime = int((stoptime - time1).seconds);
    startleng = nowtime - starttime;
    stopleng = nowtime - stoptime;
    if startleng < 0:
        secondkillstatus = 0;#未开始
    if startleng >=0 and stopleng <0:
        secondkillstatus = 1;#正进行
    if stopleng >=0:
        secondkillstatus = 2;#以结束


    return HttpResponse(json.dumps({"status":"ok" , "datatime":secondkillstatus}) , content_type="application/json");



#秒杀
def secondkillManageJsonAdd(request):
    cursor = connection.cursor();
    killid = randomString();
    goodsid = request.POST["goodsid"];
    goodsname = request.POST["goodsname"];
    # goodstatus = request.POST["goodstatus"];
    goodstatus = '0'
    starttime = request.POST["starttime"];
    
    stoptime = request.POST["stoptime"]
    result = cursor.execute("INSERT INTO secondkill(killid , goodsid , goodstatus,starttime, stoptime,goodsname) VALUES ('%s' , '%s' ,'%s' , '%s' , '%s','%s')" % (killid , goodsid , goodstatus, starttime ,stoptime,goodsname))
    try:
        if result == 1:
            statusDis=MyTool.resultOk("添加成功");
            cursor.close()
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e:
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
def secondkillManageJsonSelect(request):
    cursor=connection.cursor()
    myData=[]
    cursor.execute("SELECT killid , goodsid , goodstatus ,starttime ,  stoptime FROM secondkill")
    try:
        print("*********")
        for data in cursor.fetchall():
            killid=data[0]
            goodsid=data[1]
            goodstatus=data[2]
            starttime = data[3].strftime('%Y-%m-%d %H:%M:%S') 
            stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S');
            tempDic={"killid":killid,"goodsid":goodsid,"goodstatus":goodstatus,"starttime":starttime, "stoptime":stoptime}
            myData.append(tempDic)
        cursor.close()
        print(tempDic)
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");
def secondkillManageJsonDelete(request):
    killid = request.GET["killid"];
    cursor=connection.cursor()
    print(killid)
    try:
        cursor.execute("DELETE FROM secondkill where killid = %s" %killid)
        print("***************")
        statusDis=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        
        statusDic=MyTool.resultError("删除失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#秒杀分页 韩乐天
def secondkillcommodityQuery(request):
    print("-------------------")
    try:
        myData=[];
        mypage = (int(request.POST["page"]) - 1) * 8
        print(mypage)
        cursor = connection.cursor();
        #以八条数据为一页返回第mypage页,并且按时间排序
        cursor.execute("SELECT * FROM secondkill  LIMIT %d , 8"%mypage);
        #取出数据
        datas=cursor.fetchall();
        for data in datas:
            killid = data[0];
            goodsid = data[1];
            goodstatus = data[2];
            starttime = data[3].strftime('%Y-%m-%d %H:%M:%S');
            stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S');
            goodsname = data[5];
            tempDic = {"killid":killid, "goodsid":goodsid , "goodstatus":goodstatus , "starttime":starttime , "stoptime":stoptime ,"goodsname":goodsname}
            myData.append(tempDic)
        #查出总共有多少条数据
        cursor.execute("SELECT COUNT(*) FROM secondkill")
        adcounts  = cursor.fetchall();
        adcounts = adcounts[0][0];
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'adcounts':str(adcounts)}) , content_type="application/json");
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'adcounts':'0'}), content_type="application/json");
def secondkillManageJsonUpdata(request):
    cursor = connection.cursor()
    datas = request.POST

    try:
        for key in list(datas):
            cursor.execute("update secondkill set %s='%s' where killid='%s'"%(key , datas[key] , datas["killid"]))
            statusDis=MyTool.resultOk("修改成功");
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
def secondkillManageJsonstock(request):
    killid = request.POST["killid"];
    cursor = connection.cursor();
    
    print(killid)
    try:
        cursor.execute("select stock from goods where goodsid = (select goodsid from secondkill where killid = '%s')"%killid);
        data = cursor.fetchall();
        stock = data[0][0];
        print(stock)
        cursor.close();
        return HttpResponse(json.dumps({'data':stock, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"message":"没有该商品", 'status':'error'} , content_type="application/json"))
def secondkillAddgoodsidintogoods(request):
    goodsid = request.POST['goodsid'];
    cursor = connection.cursor();
    killid = randomString();
    print(goodsid)
    try:
        sql = "INSERT INTO secondkill(killid,goodsid) VALUES ('%s','%s')" %  (killid,goodsid) ;
        cursor.execute(sql);
        cursor.close();
        return HttpResponse(json.dumps({'message':'添加成功', 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"message":"添加失败", 'status':'error'}) , content_type="application/json")
# 快递查询接口  测试版   （陈云飞）
def express(request):

    # print(datas)
    # return HttpResponse("datas")
    NO = request.POST["NO"];
    company = request.POST["company"];
    appkey = '6a5e822ae9dacf265266ea02bd27b5ba';
    url = "http://v.juhe.cn/exp/index"
    print(type(company))
    params = {
        "com" : company, #需要查询的快递公司编号
        "no" : NO, #需要查询的订单号
        "key" : appkey, #应用APPKEY(应用详细页查询)
        "dtype" : "json", #返回数据的格式,xml或json，默认json
    
    }
    params = urlencode(params)
    print(params)    
    f = urllib.request.urlopen("%s?%s" % (url, params))
    content = f.read()
    res = json.loads(content)
    print(res)
    error_code = res["error_code"]    
    if error_code == 0:
        #成功请求
        resultDic = (res['result'])
        print(resultDic)
        return HttpResponse(json.dumps(resultDic) , content_type="application/json");
    else:
        return HttpResponse(json.dumps({"error_code":res["error_code"] , "reason":res["reason"]}) , content_type="application/json");

#查询快递公司编号接口  测试用 （陈云飞）
def expressCompany(request):
    appkey = '6a5e822ae9dacf265266ea02bd27b5ba';
    url = "http://v.juhe.cn/exp/com";
    params = {
        "key":appkey
    }
    params = urlencode(params)
    f = urllib.request.urlopen("%s?%s" % (url, params))

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            return HttpResponse(res["result"])
        else:
            return HttpResponse("%s:%s" % (res["error_code"],res["reason"]))
    else:
        return HttpResponse("request api error")

#发送短信接口  测试用  （陈云飞）
def shortMsgFromName(request):
    username = request.POST["username"];
    cursor = connection.cursor();
    cursor.execute('SELECT * FROM manager WHERE username = "%s"' % username)
    datas = cursor.fetchall();
    for i in datas:
        phone = i[2];
        p=re.compile('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$')
        match = p.match(phone)
        if match:  

            sendurl = 'http://v.juhe.cn/sms/send' #短信发送的URL,无需修改 
            appkey = '0f2f46d95cfe854988012bf5a1da65cf';
            mobile = phone;
            tpl_id = "56951";
            code = str(random.randint(0,999999));
            tpl_value = '#code#='+code;
            params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
                    (appkey, mobile, tpl_id, urllib.request.quote(tpl_value)) #组合参数
        
            wp =urllib.request.urlopen(sendurl+"?"+params)
            content = wp.read() #获取接口返回内容
        
            result = json.loads(content)
            error_code = result['error_code']
            if error_code == 0:
                #发送成功
                smsid = result['result']['sid']
                statusDic = {"status":"ok" , "smsid":smsid}
                return HttpResponse(json.dumps(statusDic) , content_type="application/json");
            else: 
                #发送失败
                statusDic = {"status":"error" , "reason":result['reason']}
                return HttpResponse(json.dumps(statusDic) , content_type="application/json");
        else:
            
            statusDic=MyTool.resultError("手机号码格式出错")
            return HttpResponse(json.dumps(statusDic) , content_type="application/json")


    

#发送短信接口  测试用  （陈云飞）
def shortMsgFromPhone(request):
    phone = request.POST["phone"]
    p=re.compile('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$')
    match = p.match(phone)
    if match:
        sendurl = 'http://v.juhe.cn/sms/send' #短信发送的URL,无需修改 
        appkey = '0f2f46d95cfe854988012bf5a1da65cf';
        mobile = phone;
        tpl_id = "56951";
        code = str(random.randint(0,999999));
        tpl_value = '#code#='+code;
        params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
        (appkey, mobile, tpl_id, urllib.request.quote(tpl_value)) #组合参数
            
        wp =urllib.request.urlopen(sendurl+"?"+params)
        content = wp.read() #获取接口返回内容
            
        result = json.loads(content)
        error_code = result['error_code']
        if error_code == 0:
            #发送成功
            smsid = result['result']['sid']
            statusDic = {"status":"ok" , "smsid":smsid}
            return HttpResponse(json.dumps(statusDic) , content_type="application/json");
        else: 
            #发送失败
            statusDic = {"status":"error" , "reason":result['reason']}
            return HttpResponse(json.dumps(statusDic) , content_type="application/json");
    else:
        
        statusDic=MyTool.resultError("手机号码格式出错")
        return HttpResponse(json.dumps(statusDic) , content_type="application/json")

#活动修改接口
# def activetableManageJsonchange(request):     
#     imgs = request.FILES["sb"];
#     activeid = request.POST["activeid"]
#     activeidw = randomString()
#     imgsName = activeidw + ".jpg";
#     imagePath = imgsName;
#     filepath = "./shopApp/static/myfile";
#     filename = os.path.join(filepath,imgsName)
#     filename = open(filename , "wb");
#     filename.write(imgs.__dict__["file"].read());
#     filename.close();
#     sqlfilename = imgsName
#     print(sqlfilename)
#     cursor = connection.cursor();
#     result = cursor.execute("UPDATE activetable SET imgs='%s' WHERE activeid='%s'" % (sqlfilename , activeid));
#     statusDic = "";
#     if result == 1:
#         statusDic = {"status" : "ok" , "message" : "编辑成功" };
#     else :
#         statusDic = {"status" : "error" , "message" : "添加失败"};
#     return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

#活动修改接口
def activetableManageJsonchange(request):
    try:
        print("activetableManageJsonchange ******** ")
        datas = request.POST
        # print(datas)
        cursor=connection.cursor();
        if request.FILES:
            #前台传过来的图片
            Imgs = request.FILES["imgs"];
            print("*-*-*-*-*-*-*-*", Imgs)
            #随机字符串存取图片名字
            ImgsName = randomString() + ".jpg";
            print (ImgsName)
            #当上传头像的时候必然会传过来用户的Id,方法根据前台来决定
            
            cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % datas["activeid"])
            data = cursor.fetchall();
            if data[0][0]:
                print(data[0][0])
                tempimg = data[0][0];
                if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                    os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
                else:
                    pass;
            filepath = "./shopApp/static/myfile/";
            #路径组合
            filepath = os.path.join(filepath,ImgsName)
            #在路径中创建图片名字
            fileobj = open(filepath , "wb");
            #并把前端传过来的数据写到文件中
            fileobj.write(Imgs.__dict__["file"].read());
            cursor.execute("update activetable set imgs='%s' where activeid=%s"%(ImgsName , datas["activeid"]))
        for key in list(datas):
            if key != "imgs":
                cursor.execute("update activetable set %s='%s' where activeid='%s'"%(key , datas[key] , datas["activeid"]))
        cursor.execute("SELECT * FROM activetable WHERE activeid='%s'" % datas["activeid"])
        data = cursor.fetchall()[0]
        activeid=data[0]
        activedetail=data[1]
        starttime=data[2].strftime('%Y-%m-%d %H:%M:%S')
        imgs = data[3]
        stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S')
        activetitle = data[5]
        activeName = data[6]
        activePosition = data[7]
        tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
        data = {'data':'success', 'status':'ok','addactive':tempDic}
        cursor.close();
        return HttpResponse(json.dumps(data) , content_type="application/json");
    except Exception as e :
        cursor.close();
        raise e
        statusDis={'data':'error', 'status':'error'};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");


def audioToStr(request):
     return render(request , "audiotostr.html");


def audioToStrApi(request):

    
    print (request.POST["audio"]);
    a = request.POST["audio"]
    print (type(a));


    dic = {"statu":"ok"};
    return HttpResponse(json.dumps(dic) , content_type = "application/json");


#留言删除接口
def leavingMessDelete(request):
    cursor=connection.cursor();
    data = request.POST
    data = data.getlist("data[]")
    for key in data:
        result = cursor.execute("UPDATE guestbook SET status='read' WHERE guestbookid='%s'" % (key))
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({'message': '操作成功','status':'ok'}), content_type="application/json");
    else:
        return HttpResponse(json.dumps({'message': '操作失败','status':'error'}), content_type="application/json");



#根据商品名模糊查询
def goodsNameSelect(request):
    myData = []
    cursor = connection.cursor()
    goodsName = request.POST["goodsName"]
    cursor.execute("SELECT * FROM goods where goodsname like '%%%%%s%%%%'"%(goodsName));
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
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
            }
            myData.append(goods);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");

#根据商品名准确查询
def goodsNameOneSelect(request):
    myData = []
    cursor = connection.cursor()
    goodsName = request.POST["goodsName"]
    cursor.execute("SELECT * FROM goods where goodsname='%s'"%(goodsName));
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
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
            }
            myData.append(goods);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");


#留言接口
def leavingMessAdd(request):
    data = request.POST
    #测试数据
    # userid = "2017121610132964" 
    # leavemessage = "啊实打实大所大是打算打算啊实打实大所大所大所大所大所，"
    userid = data["userid"];
    leavemessage = data["leavemessage"]
    #根据时间随机生成guestbookid
    guestbookid = randomString()
    cursor=connection.cursor();
    result = cursor.execute("INSERT INTO guestbook(guestbookid , userid , leavemessage)VALUES('%s' , '%s' , '%s')"%(guestbookid , userid , leavemessage))
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({'message': '留言成功','status':'ok'}), content_type="application/json");
    else:
        return HttpResponse(json.dumps({'message': '留言失败','status':'error'}), content_type="application/json");

#留言页面留言查询接口
def leavingMessageSelectAll(request):
    if request.POST:
        print("-------------0-000000000-------------------");
        data = request.POST
        userName = data.getlist("userid")[0]
        status = data.getlist("status")[0]
        print(userName , status)
        cursor = connection.cursor();
        if userName == "" and status == "0":
            cursor.close();
            return HttpResponse(json.dumps({'message': '请输入内容','status':'error'}), content_type="application/json");
            
        else:
            print("((((((((((((((((((((")
            if status == "0":
                selectCount = 1
                if userName != "":
                    cursor.execute("SELECT * from guestbook WHERE username='%s'"%(userName))
                    selectCount  = cursor.fetchall();
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '用户名不存在','status':'error'}), content_type="application/json");
                    else:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                        
            elif status == "1":
                if userName == "":
                    cursor.execute("SELECT * from guestbook WHERE status='read'")
                    selectCount  = cursor.fetchall();
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '没有已读留言','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                        
                    else:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                        
                if userName != "":
                    cursor.execute("SELECT * from guestbook WHERE username='%s' and status='read'"%(userName))
                    selectCount  = cursor.fetchall()
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '用户不存在或没有已读留言','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                        
                    else:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                        
            elif status == "2":
                if userName == "":
                    cursor.execute("SELECT * from guestbook WHERE status='unread'")
                    selectCount  = cursor.fetchall();
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '没有未读留言','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                        
                    else:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                    
                if userName != "":
                    cursor.execute("SELECT * from guestbook WHERE username='%s' and status='unread'"%(userName))
                    selectCount  = cursor.fetchall()
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '用户不存在或没有未读留言','status':'ok' , "data":str(selectCount)}), content_type="application/json");
                    
                    else:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":str(selectCount)}), content_type="application/json");

#新消息提醒接口
def newMessage(request):
    pass
