 var	Newchess="8979695949392919097717866646260600102030405060708012720323436383";
			var Chess="8979695949392919097717866646260600102030405060708012720323436383";
			var Chesspiece=["红車","红马","相","仕","帅","仕","相","红马","红車","红炮","红炮","兵","兵","兵","兵","兵","黑車","黑马","象","士","将","士","象","黑马","黑車","砲","砲","卒","卒","卒","卒","卒"];
			var matrix=new Array(9);
			var round=0;
			var selected=null;
			var target=99;
			
			for(var i=0;i<9;i++)
			{
				matrix[i]=new Array(10);
				for(var j=0;j<10;j++){
					matrix[i][j]=-1;
				}
			}
			function start(){
				var flag=0;
				var img=0;
				while(flag!=64){
					var list=(Newchess.substring(flag,flag+1));
					var line=(Newchess.substring(flag+1,flag+2));
					//console.log(line+list);
					matrix[list][line]=img;
					//console.log(line+list);
					$("#"+list+line).append("<img class='img_chess' src='img/drawable-xhdpi/"+Chesspiece[img]+".png'>")
					//$("#"+line+list).css("background","url(img/drawable-xhdpi/"+Chesspiece[img]+".png)");
					img++;
					flag+=2;
				}
			
			}
			function BuildM(string){
				console.log('blackmove+'+string)
				$(".end").remove();
				$(".img_chess").remove();
				Chess=string
				var flag=0;
				var img=0;
				selected=null;
				target=99;
				while(flag!=64){
					var list=(string.substring(flag,flag+1));
					var line=(string.substring(flag+1,flag+2));
					//console.log(line+list);
					matrix[list][line]=img;
					//console.log(line+list);
					$("#"+list+line).append("<img class='img_chess' src='img/drawable-xhdpi/"+Chesspiece[img]+".png'>")
					//$("#"+line+list).css("background","url(img/drawable-xhdpi/"+Chesspiece[img]+".png)");
					img++;
					flag+=2;
				}
			}
			function Start(begin){
				var flag=0;
				var img=0;
				$("#"+begin).remove();
				while(flag!=64&&Chess.substring(flag,flag+2)!=99){
					var list=(Chess.substring(flag,flag+1));
					var line=(Chess.substring(flag+1,flag+2));
					//console.log(line+list);
					matrix[list][line]=img;
					//console.log(line+list);
					$("#"+list+line).append("<img class='img_chess' src='img/drawable-xhdpi/"+Chesspiece[img]+".png'>")
					//$("#"+line+list).css("background","url(img/drawable-xhdpi/"+Chesspiece[img]+".png)");
					img++;
					flag+=2;
				}
			
			}
			function restart(){
				$(".end").remove();
				$(".img_chess").remove();
				Chess=Newchess;
				round=0;
				selected=null;
				target=99;
				start();
			}
			function change(id){
				
				var list=document.getElementById(id);
				list.style.backgroundColor="red";
			}
			function Query(id,chesspiece){
				var move=selected+id;
				var tar=matrix[id.substring(0,1)][id.substring(1,2)];
				var f=false;
				var state=Chess.substring(0,chesspiece*2)+id+Chess.substring(chesspiece*2+2,64);
				if(tar!=-1)
					var state=state.substring(0,tar*2)+99+state.substring(tar*2+2,64);
				console.log("flag:"+f);
				$.ajax({
					type: "get",
					url: "http://127.0.0.1:5000/isLegal",
					data: {code:Chess,move:move}, 
					dataType: "json", //回调函数接收数据的数据格式
					async : false,				 
					success: function(msg){
					if(msg!=''){
						console.log(msg[0].flag) //将返回的json数据进行解析，并赋给data
					}
					console.log(msg); //控制台输出
					console.log(Chess);
					console.log(move);
					console.log(state);
					   // 对msg数据进行分析
					if(msg[0].flag == "true") {
					   console.log("ok")
					   f=true;
					} 
					else{
					   f=false;
					}
					   
					  },
					 
					  error:function(msg){
					  	console.log("failed")
					   return false;
					  }
					  });
					  console.log("flag:"+f)
					  Chess=state;
					  return f;
				/*$.getJSON('http://127.0.0.1:5000/Login?name=ll&pw=123&callback=?', function(data){
					console.log(data);
				  //处理data数据

				});*/
			}
			function Learn(state,move){
				 $.ajax({
					  type: "get",
					  url: "http://127.0.0.1:5000/learn",
					  data: {code:state,move:move}, 
					  dataType: "json", //回调函数接收数据的数据格式	
					  success: function(msg){
						console.log(msg)
					   
					  },
					 
					  error:function(msg){
					   console.log(msg);
					  }
					  });
			}
			function Ask_for_black(){
				var state=null;
				var move=null;
				 $.ajax({
					  type: "get",
					  url: "http://127.0.0.1:5000/getMove",
					  data: {code:Chess,color:1}, 
					  dataType: "json", //回调函数接收数据的数据格式	
						async : false,
					  success: function(msg){
					   if(msg!=''){
							state=msg[0].new_code;
							move=msg[0].move;
							console.log(state);
							console.log(move);
					   }
					  },
					  error:function(msg){
					   console.log(msg);
					  }
					  });
				if(state!=null&&move!=null){
					//console.log("black:"+state)
					Black_move(state)
				}
			}
			function Black_move(string){
				BuildM(string);
				round=0;
			}
			function Move(id){
				//console.log('我是？？新的，要到的位置的id?'+id);
			var img=matrix[selected.substring(0,1)][selected.substring(1,2)];
				if(Query(id,img)){
					// 调用learn函数需要用到的变量
					console.log("move")
					var move=selected+id;
					var state=Chess.substring(0,img*2)+id+Chess.substring(img*2+2,64);
					
					if(img!=-1){
						$("#"+id).empty()
					}
					matrix[id.substring(0,1)][id.substring(1,2)]=img
					$("#"+selected).empty()
					$("#"+selected).css({"opacity":"1","background":"","background-size":"100% 80%"})
					$("#"+id).append("<img class='img_chess' src='img/drawable-xhdpi/"+Chesspiece[img]+".png'>")
					matrix[selected.substring(0,1)][selected.substring(1,2)]=-1
					selected=null;
					//console.log("黑将"+state.substring(40,42))
					if(Chess.substring(8,10)==99){
						$("#Bigcontainer").append("<div class='end' style='width:100%;height:100%;position:absolute;left:0px;background:url(img/drawable-xhdpi/结束画面_黑.png);background-size:100% 100%' onclick='Start('begin')'><img style='width:170px;height:60px;margin-top:260px;margin-left:180px'src='img/drawable-xhdpi/再来一局.png' onclick='restart()'></div>")
					}
					else if(Chess.substring(40,42)==99){
						$("#Bigcontainer").append("<div class='end' style='width:100%;height:100%;position:absolute;left:0px;background:url(img/drawable-xhdpi/结束画面_红.png);background-size:100% 100%' onclick='Start('begin')'><img style='width:170px;height:60px;margin-top:260px;margin-left:180px'src='img/drawable-xhdpi/再来一局.png' onclick='restart()'></div>")
					}
						
					if(round==0)
						round=2;
					else if(round==2)
						round=0;
					
					console.log(Chess);
					console.log(move);
					// 调用learn函数
					Learn(Chess,move);
					// 成功移动后，更新棋局状态
					Chess = state;
					if(round==2)
						Ask_for_black();//红棋移动成功后黑棋移动
					console.log(Chess);
				}
			}
			function Select(id){
					//$("#"+id).css("opacity","0.8");
					//console.log(matrix[id.substring(0,1)][id.substring(1,2)]);
					console.log(id);
					var chesspiece=matrix[id.substring(0,1)][id.substring(1,2)]
					if(((round==0&&chesspiece<=15)||(round==2&&chesspiece>=16))&&chesspiece!=-1){
						if(matrix[id.substring(0,1)][id.substring(1,2)]!=-1){
							if(selected==null||selected==id){
								if($("#"+id).css("opacity")==1)
								{
									$("#"+id).css({"opacity":"0.8","background":"url(img/drawable-xhdpi/圆角矩形1.png) no-repeat","background-size":"100% 90%"})
									selected=id;
								}
								else
								{
									$("#"+id).css({"opacity":"1","background":"","background-size":"100% 80%"})
									selected=null;
								}
							}
							else{
								$("#"+selected).css({"opacity":"1","background":"","background-size":"100% 80%"})
								$("#"+id).css({"opacity":"0.8","background":"url(img/drawable-xhdpi/圆角矩形1.png) no-repeat","background-size":"100% 90%"})
								selected=id;
							}
						}								
					}
					else{
						
						if(selected!=null){
							console.log("选中"+selected)
							Move(id)
						}
					}
						
			}