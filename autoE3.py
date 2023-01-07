import base64
import time
import ddddocr
import os
import requests
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

accountValue=str(sys.argv[1])
passwordValue=str(sys.argv[2])
nowMode=1 #本學期課程下載 預設為1:會下載本學期課程,0:不會
nowNumber=1 #本學期第N個課程 預設1:為本學期課程第1個課程
hisMode=1 #歷年課程下載 預設為1:會下載歷年課程,0:不會
PageValue=1 #頁數 預設為1:歷年課程第1頁
NumberValue=1    #那頁第N個課程 預設1:為歷年課程第x頁第1個課程
def custiomsetStart():
    global nowMode
    global nowNumber
    global hisMode
    global PageValue
    global NumberValue
    try:
        print(nowMode)
        nowMode=int(sys.argv[3]) #本學期課程下載
        nowNumber=int(sys.argv[4]) #本學期第N個課程
        hisMode=int(sys.argv[5]) #歷年課程下載
        PageValue=int(sys.argv[6]) #頁數
        NumberValue=int(sys.argv[7])    #那頁第N個課程
        print("使用自定義參數")
    except:
        nowMode=1 #本學期課程下載 預設為1:會下載本學期課程,0:不會
        nowNumber=1 #本學期第N個課程 預設1:為本學期課程第1個課程
        hisMode=1 #歷年課程下載 預設為1:會下載歷年課程,0:不會
        PageValue=1 #頁數 預設為1:歷年課程第1頁
        NumberValue=1    #那頁第N個課程 預設1:為歷年課程第x頁第1個課程
        print("使用預設下載參數")

custiomsetStart()
userPath="1"
#校正參數勿更改
NumberValue+=2
PageNow=PageValue
nowNumber+=1

userPath = "/home/"+os.popen('whoami').read()
userPath = userPath[0:len(userPath)-1]
userPath = userPath + "/workspace"
if not os.path.isdir(userPath): #建立Class資料夾
    os.system("mkdir "+userPath)
print("已建立目錄至 "+userPath, flush=True)
def isOK(road): #判斷元素是否存在
    flag=True
    try:
        OKOK = driver.find_element('id',road)
        return flag
    except :
        flag=False
        return flag

def checkNowDownload(classname,downloadhref,downloadHWK,nowNumber):
    homeworkName=downloadHWK.text
    try:
        response = requests.get(
            f''+downloadhref)
        if(os.path.isfile(userPath+'/Class/'+classname+'/'+homeworkName)): #假如該檔案重複
            ii="1"
            while(os.path.isfile(userPath+'/Class/'+classname+'/'+ii+'-'+homeworkName)):
                ii=str(int(ii)+1)
            homeworkName=ii+'-'+homeworkName
        time.sleep(0.3)
        with open(str(userPath+'/Class/'+classname+'/'+homeworkName), 'wb') as file:
            file.write(response.content)
        
        print('下載內容:'+homeworkName+' -ok', flush=True)
    except:
        print('本學期第'+str(nowNumber)+'個課程:'+classname+'-下載內容:'+homeworkName+' -ERROR', flush=True)


def checkdownload(dirPath,downloadhref,downloadHWK,i,j,Name):
    homeworkName=downloadHWK.text
    try:
        response = requests.get(
            f''+downloadhref)
        if (os.path.isfile(dirPath+'/'+homeworkName)): #假如該檔案重複
            ii="1"
            while(os.path.isfile(dirPath+'/'+ii+'-'+homeworkName)):
                ii=str(int(ii)+1)
            homeworkName=ii+'-'+homeworkName
        time.sleep(0.3)
        with open(str(dirPath+'/'+homeworkName), 'wb') as file:
            file.write(response.content)
        
        print('下載內容:'+homeworkName+' -ok', flush=True)
    except:
        print('第'+str(i)+'頁'+'第'+str(j-2)+'個:'+Name[6:len(Name)]+'-下載內容:'+homeworkName+' -ERROR', flush=True)

PATH="/snap/bin/chromium.chromedriver" #驅動路徑
#PATH="C:/CHs/chromedriver.exe" #驅動路徑
url="https://e3.nfu.edu.tw/EasyE3P/LMS2/login.aspx" #要自動登入的網址
#不自動關閉瀏覽器
option = webdriver.ChromeOptions() 
option.add_experimental_option( "detach" , True)
option.add_experimental_option( 'excludeSwitches' , [ 'enable-automation'])
option.add_experimental_option( 'useAutomationExtension' , False)
option.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH,chrome_options= option)

driver.get(url)
time.sleep(3)



# --------------- 自動登入頁面操作 --------------- #
driver.implicitly_wait(15) #等待頁面載入完畢
account = WebDriverWait(driver, 1).until( #抓取帳號輸入格
    EC.presence_of_element_located(('id', 'txtLoginId')),
    "no catch password-input[id:txtLoginId]"
)
password = WebDriverWait(driver, 1).until( #抓取密碼輸入格
    EC.presence_of_element_located(("id", "txtLoginPwd")),
    "no catch password-input[id:txtLoginPwd]"
)
verify = WebDriverWait(driver, 1).until( #抓取驗證碼輸入格
    EC.presence_of_element_located(("id", "txtCheck")),
    "no catch verify-input[id:txtCheck]"
)

#account = driver.find_element(('id', 'txtLoginId'))
#下載驗證碼圖片
img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, driver.find_element('xpath','//*[@id="imgCheck"]'))
with open(userPath+"/VerPicture.png", 'wb') as image:
    image.write(base64.b64decode(img_base64))

#辨識驗證碼圖片
ocr = ddddocr.DdddOcr()
with open(userPath+'/VerPicture.png', 'rb') as f:
    img_bytes = f.read()
VerPictureRes = ocr.classification(img_bytes)
#送出帳號、密碼、驗證碼、登入
account.send_keys(accountValue)
password.send_keys(passwordValue)
verify.send_keys(VerPictureRes)
send = driver.find_element("id","btnLogin")
send.send_keys(Keys.RETURN)
# ----------------------------------------------- #
# --------------- 自動化點擊操作 ---------------- #
# 下載本學期課程作業
if not os.path.isdir(userPath+"/Class"): #建立Class資料夾
    os.system("mkdir "+userPath+"/Class")

driver.implicitly_wait(15) #等待頁面載入完畢
if(nowMode==1):
    while(1):
        #time.sleep (5)
        driver.implicitly_wait(15) #等待頁面載入完畢
        nowNumber_str=str(nowNumber) #取nowNumber字串類型改為2位數
        if(len(nowNumber_str)==1):
            nowNumber_str="0"+nowNumber_str
            
        driver.implicitly_wait(2) #等待頁面載入完畢
        if(isOK("ctl00_ContentPlaceHolder1_gvCourse_ctl"+nowNumber_str+"_lnkCourseName")==True): #本課程存在
            now_className=driver.find_element("id","ctl00_ContentPlaceHolder1_gvCourse_ctl"+nowNumber_str+"_lnkCourseName").text #抓課程名稱
            if(now_className[len(now_className)-1]==" "):
                now_className=now_className[1:len(now_className)-1]
            if(now_className[len(now_className)-1]==")"):
                endleft=len(now_className)-1
                while(now_className[endleft]!="("):
                    endleft-=1
                now_className=now_className[0:endleft]
            print('\n目前科目:'+now_className, flush=True)
            if not os.path.isdir(userPath+"/Class/"+now_className): #建立課程名稱的資料夾
                os.system("mkdir "+userPath+"/Class/"+"\""+now_className+"\"")
                #os.makedirs("Class/"+now_className, mode=0o777) ERROR
            now_intoclass=driver.find_element("id","ctl00_ContentPlaceHolder1_gvCourse_ctl"+nowNumber_str+"_lnkCourseName")
            now_intoclass.click()
            
            if(EC.alert_is_present()(driver)!=False): #解決切換課程談窗
                driver.switch_to.alert.accept()
            if(isOK("ctl00_lnkHwkDoc")==True): #課程裡面有開作業列表
                intoHomework = driver.find_element('id','ctl00_lnkHwkDoc') #進入作業列表
                intoHomework.click()
                headi = "02"
                if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl00_lnkFile')==True): #下載檔案存在
                    while(1): #頭i
                        tailj="00"
                        if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl00_lnkFile')==False):
                            break
                        while(1): #尾j
                            if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl'+tailj+'_lnkFile')==False):
                                break
                            downloadHWK = WebDriverWait(driver, 2).until( 
                                EC.presence_of_element_located(('id','ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl'+tailj+'_lnkFile'))
                            )
                            downloadhref=downloadHWK.get_attribute('href') #下載檔案
                            checkNowDownload(now_className,downloadhref,downloadHWK,nowNumber)
                            tailj=str(int(tailj)+1)
                            if(len(tailj)==1):
                                tailj="0"+tailj
                        headi=str(int(headi)+1) 
                        if(len(headi)==1):
                            headi="0"+headi
                        time.sleep(0.5)
                nowNumber+=1        
                backtoHome = WebDriverWait(driver, 2).until( 
                    EC.presence_of_element_located(('xpath','//*[@id="ctl00_btnHome"]')),
                    "no catch backtoHome "
                )
                backtoHome.click()
        else:
            break
        time.sleep(1)

# 下載歷年課程作業
driver.implicitly_wait(15) #等待頁面載入完畢
if(hisMode==1):
    click1 = driver.find_element('id','ctl00_lnkHistory') #歷年課程
    click1.click()
    driver.implicitly_wait(15) #等待頁面載入完畢

    PageAllnum=driver.find_element('id','ctl00_ContentPlaceHolder1_DataNavigator1_ctl02').text
    PageAllnum=PageAllnum[9:9+len(PageAllnum)-11]
    Skipitem=0
    driver.implicitly_wait(3) #等待頁面載入完畢
    time.sleep(0.5)
    for i in range(PageValue,int(PageAllnum)+1): #第N頁
        if((Skipitem==0)and(i==PageValue)): #
            Skipitem=1
            for j in range(NumberValue,13): 
                #轉移目前頁面
                for k in range(1,PageNow):
                    NextPage = WebDriverWait(driver, 1).until( 
                        EC.presence_of_element_located(('id','ctl00_ContentPlaceHolder1_DataNavigator1_ctl03')),
                        "no catch NextPage"
                    )
                    NextPage.click()
                    time.sleep(0.5)
                time.sleep(0.5)

                driver.implicitly_wait(2) #等待頁面載入完畢
                time.sleep(0.2)
                jnum=str(j)
                if(len(jnum)==1):
                    jnum="0"+jnum
                findnameroad='ctl00_ContentPlaceHolder1_dg_ctl'+jnum+'_lbCourseName' #抓取課程名稱id
                intoClassroad='ctl00_ContentPlaceHolder1_dg_ctl'+jnum+'_lnbEnter' #進入課程的id
                if(isOK(findnameroad)==False): #判斷此元素(id)是否存在
                    break
                classState = driver.find_element('id',findnameroad).text #抓取課程狀態 有使用/沒使用
                classState = classState[len(classState)-4:len(classState)-1] 
                className = driver.find_element('id',findnameroad).text #抓取課程名稱
                className =  className[0:len(className)-5]

                if(classState=="有使用"): #假如課程狀態是 有使用
                    dirPath=userPath+"/Class/"+className
                    if(dirPath[len(dirPath)-1]==' '): #catch space
                        dirPath=dirPath[0:len(dirPath)-1]

                    if not os.path.isdir(dirPath): #建立課程名稱的資料夾
                        os.system("mkdir "+"\""+dirPath+"\"")
                        #os.makedirs(dirPath, mode=0o777)
                    print('\n目前科目:'+dirPath, flush=True)
                    intoClass = driver.find_element('id',intoClassroad) #進入課程
                    intoClass.click()
                    time.sleep(0.5)
                    if(EC.alert_is_present()(driver)!=False): #解決切換課程談窗
                        driver.switch_to.alert.accept()

                    time.sleep(0.5)
                    if(isOK("ctl00_lnkHwkDoc")==True): #課程裡面有開作業列表
                        intoHomework = driver.find_element('id','ctl00_lnkHwkDoc') #進入作業列表
                        intoHomework.click()
                        headi = "02"
                        while(1): #頭i
                            tailj="00"
                            if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl00_lnkFile')==False):
                                    break
                            while(1): #尾j
                                if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl'+tailj+'_lnkFile')==False):
                                    break
                                downloadHWK = WebDriverWait(driver, 2).until( 
                                    EC.presence_of_element_located(('id','ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl'+tailj+'_lnkFile'))
                                )
                                downloadhref=downloadHWK.get_attribute('href') #下載檔案
                                checkdownload(dirPath,downloadhref,downloadHWK,i,j,dirPath)
                                tailj=str(int(tailj)+1)
                                if(len(tailj)==1):
                                    tailj="0"+tailj
                            headi=str(int(headi)+1) 
                            if(len(headi)==1):
                                headi="0"+headi
                        time.sleep(0.5)
                #返回剛才地方
                backtoHome = WebDriverWait(driver, 2).until( 
                    EC.presence_of_element_located(('xpath','//*[@id="ctl00_btnHome"]')),
                    "no catch backtoHome "
                )
                backtoHome.click()
                backtoHistory = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(('xpath','//*[@id="ctl00_lnkHistory"]')),
                    "no catch backtoHistory "
                )
                backtoHistory.click()

        else:
            for j in range(3,13):
                #轉移目前頁面
                for k in range(1,PageNow):
                    NextPage = WebDriverWait(driver, 1).until( 
                        EC.presence_of_element_located(('id','ctl00_ContentPlaceHolder1_DataNavigator1_ctl03')),
                        "no catch NextPage"
                    )
                    NextPage.click()
                    time.sleep(0.5)
                time.sleep(0.5)

                driver.implicitly_wait(2) #等待頁面載入完畢
                time.sleep(0.2)
                jnum=str(j)
                if(len(jnum)==1):
                    jnum="0"+jnum
                findnameroad='ctl00_ContentPlaceHolder1_dg_ctl'+jnum+'_lbCourseName' #抓取課程名稱id
                intoClassroad='ctl00_ContentPlaceHolder1_dg_ctl'+jnum+'_lnbEnter' #進入課程的id
                if(isOK(findnameroad)==False): #判斷此元素(id)是否存在
                    break
                classState = driver.find_element('id',findnameroad).text #抓取課程狀態 有使用/沒使用
                classState = classState[len(classState)-4:len(classState)-1] 
                className = driver.find_element('id',findnameroad).text #抓取課程名稱
                className =  className[0:len(className)-5]

                if(classState=="有使用"): #假如課程狀態是 有使用
                    dirPath=userPath+"/Class/"+className
                    if(dirPath[len(dirPath)-1]==' '): #catch space
                        dirPath=dirPath[0:len(dirPath)-1]

                    if not os.path.isdir(dirPath): #建立課程名稱的資料夾
                        os.system("mkdir "+"\""+dirPath+"\"")
                        #os.makedirs(dirPath, mode=0o777)
                    print('\n目前科目:'+dirPath, flush=True)
                    intoClass = driver.find_element('id',intoClassroad) #進入課程
                    intoClass.click()
                    time.sleep(0.5)
                    if(EC.alert_is_present()(driver)!=False): #解決切換課程談窗
                        driver.switch_to.alert.accept()

                    time.sleep(0.5)
                    if(isOK("ctl00_lnkHwkDoc")==True): #課程裡面有開作業列表
                        intoHomework = driver.find_element('id','ctl00_lnkHwkDoc') #進入作業列表
                        intoHomework.click()
                        headi = "02"
                        while(1): #頭i
                            tailj="00"
                            if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl00_lnkFile')==False):
                                    break
                            while(1): #尾j
                                if(isOK('ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl'+tailj+'_lnkFile')==False):
                                    break
                                downloadHWK = WebDriverWait(driver, 2).until( 
                                    EC.presence_of_element_located(('id','ctl00_ContentPlaceHolder1_dgAlready_ctl'+headi+'_fileAttachManageLite_rpFileList_ctl'+tailj+'_lnkFile'))
                                )
                                downloadhref=downloadHWK.get_attribute('href') #下載檔案
                                checkdownload(dirPath,downloadhref,downloadHWK,i,j,dirPath)
                                tailj=str(int(tailj)+1)
                                if(len(tailj)==1):
                                    tailj="0"+tailj
                            headi=str(int(headi)+1) 
                            if(len(headi)==1):
                                headi="0"+headi
                        time.sleep(0.5)
                #返回剛才地方
                backtoHome = WebDriverWait(driver, 2).until( 
                    EC.presence_of_element_located(('xpath','//*[@id="ctl00_btnHome"]')),
                    "no catch backtoHome "
                )
                backtoHome.click()
                backtoHistory = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(('xpath','//*[@id="ctl00_lnkHistory"]')),
                    "no catch backtoHistory "
                )
                backtoHistory.click()
        PageNow+=1
        if(i!=PageValue):
            if(i<int(PageAllnum)): #點擊下一頁
                NextPage = WebDriverWait(driver, 1).until( 
                    EC.presence_of_element_located(('id','ctl00_ContentPlaceHolder1_DataNavigator1_ctl03')),
                    "no catch NextPage"
                )
                NextPage.click()

time.sleep(0.5)
