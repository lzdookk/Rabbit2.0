# Rabbit2.0
**20220331**   
DATA表单信息调整，针对所在位置“合肥市区校外”增加了“所在城市片区”以及“具体位置”，修改DATA，然而第一次忘了加逗号，贻笑大方   

**20220318**   
DATA表单信息调整，增加了“居住地”，删去了“所在地”“所在校区”等，遂根据F12看到的cookie信息将SECRET中的DATA加以修改，txt文件也同步更新

**20220310**   
网页问题自动修复

**20220309**   
发现Run Failure了，待修复   
调试时发现系网页上不能选择所在地，导致即使手动登录网页也无法打卡，但clyston的原项目未受影响，很是奇怪

**20220120更新**     
原Rabbit项目的2022修正版，每天上午9:17打卡，借(zhao)鉴(chao)自clysto的打卡项目。  
  
1 由于上报内容增加了紧急联系人等三项数据，运行原项目必定失败。  
2 表单数据不再以data.json的文件形式存在，而是以DATA形式添加到Secrets中，并增加了紧急联系人的三行数据。  
**注意需符合json文件的格式，双引号引发的血案仍历历眼前**  
3 增加了登录时应对验证码的模块。  
4 20220120的json格式data数据已存入同名txt文件备查。    
5 删除了clysto项目中BARK_URL的部分。
