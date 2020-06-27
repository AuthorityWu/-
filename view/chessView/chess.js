 var	Newchess="8979695949392919097717866646260600102030405060708012720323436383";
			var Chess="8979695949392919097717866646260600102030405060708012720323436383";
			var Chesspiece=["红車","红马","相","仕","帅","仕","相","红马","红車","红炮","红炮","兵","兵","兵","兵","兵","黑車","黑马","象","士","将","士","象","黑马","黑車","砲","砲","卒","卒","卒","卒","卒"];
			var matrix=new Array(9);
			var round=0;
			var selected=null;
			var target=99;
			var train=0;
			for(var i=0;i<9;i++)
			{
				matrix[i]=new Array(10);
				for(var j=0;j<10;j++){
					matrix[i][j]=-1;
				}
			}
			function Train(){
				train=1;
				Start("begin");
			}
			function choose_black(){
				Start("begin");
				Ask_for_black("-1");
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
				for(var i=0;i<9;i++)
			{
				matrix[i]=new Array(10);
				for(var j=0;j<10;j++){
					matrix[i][j]=-1;
				}
			}
				while(flag!=64){
					if(Chess.substring(flag,flag+2)!=99){
						var list=(string.substring(flag,flag+1));
						var line=(string.substring(flag+1,flag+2));
						//console.log(line+list);
						matrix[list][line]=img;
						//console.log(line+list);
						$("#"+list+line).append("<img class='img_chess' src='img/drawable-xhdpi/"+Chesspiece[img]+".png'>")
						//$("#"+line+list).css("background","url(img/drawable-xhdpi/"+Chesspiece[img]+".png)");
											
					}
					img++;
					flag+=2;
					
				}
				console.log(matrix)
			}
			function Start(begin){
				var flag=0;
				var img=0;
				$("#"+begin).remove();
				while(flag!=64){
					if(Chess.substring(flag,flag+2)!=99){
						var list=(Chess.substring(flag,flag+1));
						var line=(Chess.substring(flag+1,flag+2));
						//console.log(line+list);
						matrix[list][line]=img;
						//console.log(line+list);
						$("#"+list+line).append("<img class='img_chess' src='img/drawable-xhdpi/"+Chesspiece[img]+".png'>")
						//$("#"+line+list).css("background","url(img/drawable-xhdpi/"+Chesspiece[img]+".png)");
					}
					img++;
					flag+=2;
				}
				
			
			}
			function restart(){
				window.location.reload()
				Chess=Newchess;
				round=0;
				selected=null;
				target=99;
				//start();
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
					url: "http://120.79.195.191:80/isLegal",
					data: {code:Chess,move:move}, 
					dataType: "json", //回调函数接收数据的数据格式
					async : false,				 
					success: function(msg){
					//console.log("link")
					if(msg!=''){
						console.log(msg) //将返回的json数据进行解析，并赋给data
					}
					//console.log(msg); //控制台输出
					//console.log(Chess);
					//console.log(move);
					//console.log(state);
					   // 对msg数据进行分析
					if(msg.flag == true) {
					   console.log("ok")
					   Chess=state;
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
					  
					  return f;
				/*$.getJSON('http://127.0.0.1:5000/Login?name=ll&pw=123&callback=?', function(data){
					console.log(data);
				  //处理data数据

				});*/
			}
			function Learn(state,move){
				 $.ajax({
					  type: "get",
					  url: "http://120.79.195.191:80/learn",
					  data: {code:state,move:move}, 
					  dataType: "json", //回调函数接收数据的数据格式	
					  success: function(msg){
						console.log("learn ok")
					   
					  },
					 
					  error:function(msg){
					   console.log(msg);
					  }
					  });
			}
			function Ask_for_black(color){
				var state=null;
				var move=null;
				//console.log("black1")
				 $.ajax({
					  type: "get",
					  url: "http://120.79.195.191:80/getMove",
					  data: {code:Chess,color:color}, 
					  dataType: "json", //回调函数接收数据的数据格式	
						async : false,
					  success: function(msg){
						//console.log("black")
					   if(msg!=''){
							state=msg.new_code;
							move=msg.move;
							console.log(msg)
							//console.log("新+"+state);
							//console.log("新+"+move);
					   }
					  },
					  error:function(msg){
					   console.log("blackfaled");
					  }
					  });
				if(state!=null&&move!=null){
					//console.log("black:"+state)
					if(round==2)
						Black_move(state);
					else if(round==0)
						Red_move(state);
				}
			}
			function end(){
				if(Chess.substring(8,10)==99){
						$("#Bigcontainer").append("<div class='end' style='width:100%;height:100%;position:absolute;left:0px;background:url(img/drawable-xhdpi/结束画面_黑.png);background-size:100% 100%' onclick='Start('begin')'><img style='width:170px;height:60px;margin-top:260px;margin-left:180px'src='img/drawable-xhdpi/再来一局.png' onclick='restart()'></div>")
						return false;
					}
				else if(Chess.substring(40,42)==99){
						$("#Bigcontainer").append("<div class='end' style='width:100%;height:100%;position:absolute;left:0px;background:url(img/drawable-xhdpi/结束画面_红.png);background-size:100% 100%' onclick='Start('begin')'><img style='width:170px;height:60px;margin-top:260px;margin-left:180px'src='img/drawable-xhdpi/再来一局.png' onclick='restart()'></div>")
						return false;
					}
				else return true;
				
			}
			function Red_move(string){
				BuildM(string);
				end()
				round=2;
			}
			function Black_move(string){
				BuildM(string);
				end();
				round=0;
			}
			
			function Move(id){
				//console.log('我是？？新的，要到的位置的id?'+id);
			var img=matrix[selected.substring(0,1)][selected.substring(1,2)];
			var temp=Chess;
				if(Query(id,img)){
					// 调用learn函数需要用到的变量
					//console.log("move")
					var move=selected+id;
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
					if(end()){
						if(round==0)
							round=2;
						else if(round==2)
							round=0;
						//console.log("红棋移动前"+temp);
						//console.log(move);
						Learn(temp,move);
						//console.log("红棋移动后"+Chess)
						if(train==0){
							if(round==2)
								Ask_for_black("1");//红棋移动成功后黑棋移动
							else if(round==0)
								Ask_for_black("-1");
						
						}
					}
					
					//console.log(Chess);
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