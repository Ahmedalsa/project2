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
                           activeChannel=$("#channelList .active").attr('id');
                                       localStorage.setItem('activeChannel',activeChannel)
                                       if (activeChannel=='General') {
                                           inRoom=false;
                                           privateWindow=false;
                                           return socket.emit('come back to general');
                                       } else {
                                           inRoom=true;
                                           privateWindow=false;
                                       }
                                       socket.emit('join',{'channel':activeChannel,'mymessage':'has entered the room','username':username,'time':time});
                                    });

                                   if (!localStorage.getItem('username')) {
                                       $("#myModal").modal({backdrop: 'static', keyboard: false});
                                       $('.modal-title').text("Please enter your username");
                                       $('#modalInput').val("");
                                   }
                               });
    socket.on('announce to all', data=> {
        if (!privateWindow){
            loadMessages(data);
        }

        $('.text-danger').on('click',function() {
            chooseUser($(this).text());
        });
    });

    socket.on('joined', data=> {
        loadMessages(data);
        $('#messageInput').focus();
        $('.text-danger').on('click',function() {
            chooseUser($(this).text());
        });
    });

    socket.on('left', data=> {
        loadMessages(data);
    });

    socket.on('announce to room', data=> {
        loadMessages(data);
        $('.text-danger').on('click',function() {
            chooseUser($(this).text());
        });
    });

    socket.on('load channels', data=> {
        $('#channelList li').remove();
        loadChannels(data);
        $('#'+localStorage.getItem('activeChannel')).click();
    });
