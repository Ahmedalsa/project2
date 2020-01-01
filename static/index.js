$(function(){

    // Initialize new Chat document ready
   var socket=io.connect(location.protocol+'//'+document.domain+':'+location.port);
   privateWindow=false;
   inRoom=false;
   socket.on('connect',()=>{
      $('#messageInput').on("keyup",function(key) {
          activeChannel=$("#channelList .active").attr('id');
          //broadcast to all
    // Initialize local storage
    if (key.keyCode==13 && $(this).val()!="" && !privateWindow && !inRoom) {
               const mymessage=$(this).val();
               const username=localStorage.getItem('username');
               const time=new Date().toLocaleString();
               $('#messageInput').val("")
               socket.emit('submit to all',{'mymessage':mymessage,'username':username,'time':time});
           }//send to room
           if (key.keyCode==13 && $(this).val()!="" && !privateWindow && inRoom) {
               const mymessage=$(this).val();
               const username=localStorage.getItem('username');
               const time=new Date().toLocaleString();
               $('#messageInput').val("")
               socket.emit('submit to room',{'channel':activeChannel,'mymessage':mymessage,'username':username,'time':time});
           //send private
      // Connect to websocket
    } else if (key.keyCode==13 && $(this).val()!="" && privateWindow && !inRoom) {
                const mymessage=$(this).val();
                const username=localStorage.getItem('username');
                const username2=localStorage.getItem('activeMessage');
                const time=new Date().toLocaleString();
                $('#messageInput').val("")
                socket.emit('private',{'mymessage':mymessage,'username':username,'time':time,'username2':username2});
            }
      // When connected, configure buttons
    });
           $('#channelList').on('click','li', function(){
               $('#messageInput').focus();
               if (!localStorage.getItem('activeChannel')) {
                   activeChannel="General";
               } else {
                   activeChannel=localStorage.getItem('activeChannel');
               }

               const username=localStorage.getItem('username');
                           const time=new Date().toLocaleString();
                           $(this).addClass('active');
                           $(this).siblings().removeClass('active');
                           $('#messages').html("");
                           if (activeChannel!="General" && !privateWindow) {
                               socket.emit('leave',{'channel':activeChannel,'mymessage':'has left the room','username':username,'time':time});
                           }
          // TODO Replace function below
          // Each button should emit a "submit vote" event
