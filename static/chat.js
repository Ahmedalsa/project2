document.addEventListener('DOMContentLoaded', () => {

    // Display nickname if available
    var nickname = localStorage.getItem('nickname');

    document.querySelector('#nickname').innerHTML = nickname;

    //Display room if available
    if (!localStorage.getItem('room')) {
        var room = "default";
        localStorage.setItem('room', room);
    } else {
        document.querySelector('#room').innerHTML = room;
    }

    // By default, submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#message').onkeyup = () => {
        if (document.querySelector('#message').value.length > 0)
            document.querySelector('#submit').disabled = false;
        else
            document.querySelector('#submit').disabled = true;
    };
