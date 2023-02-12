var cellphoneRule =/0?(13|14|15|18|17|19)[0-9]{9}$/;//判断手机号
var chinesenameRule=/^[\u4E00-\u9FA5]{2,8}$/;//判断中文姓名
var mailboxRule =/^[A-z0-9]+@[A-z0-9]+\.[a-z]{1,3}$/;//判断邮箱
var hobbyRule=/^[\u4E00-\u9FA5]{1,32}$/;//判断兴趣
var stunumberRule=/^\d{13}$/;//判断学号
  function reg(eleID, rule){
      var inputValue = document.getElementById(eleID).value;
      var result = rule.test(inputValue.trim());
      if (result && inputValue != ""){
          document.getElementById(eleID+"Reg").innerHTML = "√";
          document.getElementById(eleID+"Reg").style.color = "green";
    
      }else {
          document.getElementById(eleID+"Reg").innerHTML = "×";
          document.getElementById(eleID+"Reg").style.color = "red";
  
      }
  }
    //改变but字体颜色
  function chengColor(color){
    document.getElementById("btn").style.color=color;
  }

const mysql = require('mysql');
const http = require('http');
const querystrinng=require('querystring');
var fs = require("fs");


const connection=mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'123456',
    port:3306,
    database:'dace01'
});
connection.connect();

const server=http.createServer((req,res)=>{
    if(req.method==='POST'){
        let postData='';
        req.on('data',chunk=>{
            postData+=chunk.toString();
            fs.writeFile('index.txt', chunk.toString(),  function(err) {
                if (err) {
                    return console.error(err);
                }
                console.log("数据写入成功");
             });
        })
        req.on('end',()=>{
            console.log('postData',postData);
            res.end('数据接收完毕');
        })
        console.log('post data content type',req.headers['content-type']);
    }
});

server.listen(5000,()=>{
    console.log('server running at port 5000');
})


  
    //判断用户名
    function regName(){
     reg("userName",chinesenameRule);
     return true;
    }
    function regstuNumber(){
        reg("stuNumber",stunumberRule);
        return true;
    }

      //判断邮箱格式   
    function regmail(){
     reg("userMail",mailboxRule);
     return true;
    }
    //判断手机号格式
    function regphone(){
     reg("userPhone",cellphoneRule );
     return true;
    }
    //判断学号

    //判断爱好
    function reghobby(){
     reg("userHobby",hobbyRule );
     return true;
    }
    String.prototype.format = function() {
        if(arguments.length == 0) return this;
        var param = arguments[0];
        var s = this;
        if(typeof(param) == 'object') {
         for(var key in param)
          s = s.replace(new RegExp("\\{" + key + "\\}", "g"), param[key]);
         return s;
        } else {
         for(var i = 0; i < arguments.length; i++)
          s = s.replace(new RegExp("\\{" + i + "\\}", "g"), arguments[i]);
         return s;
        }
       }


    //实现校验按钮
  function regbtn(){
   if(document.getElementById("userNameReg").innerHTML=="√"&&
    document.getElementById("stuNumberReg").innerHTML=="√"&&
    document.getElementById("userPhoneReg").innerHTML=="√"&&
    document.getElementById("userMailReg").innerHTML=="√"&&
    document.getElementById("userHobbyReg").innerHTML=="√"
   ){
    alert("提交成功！");


   }else{
    alert("注册失败");
   } 
  }
// const sql='select * from new_table01';
// connection.query(sql,(err,result)=>{
//     if(err){
//         console.error('error',err)
//         return;
//     }
//     console.log('result',result);
// });

//     var name=document.getElementById("userName").value;
// var number=document.getElementById("stuNumber").value;
// var phone=document.getElementById("userPhone").value;
// var mail=document.getElementById("userMail").value;
// var hobby=document.getElementById("userHobby").value;
 var sqladd='insert into new_table01(username,usernumber,userphone,usermail,userhobby) values ("哈哈哈","2019302130777","15333333333","qzy@qq.com","哈哈哈哈哈")';
console.log(sqladd);
    connection.query(sqladd,(err,result)=>{
    if(err){
        console.error('error',err)
        return;
    }
    console.log('result',result);
});
connection.end();