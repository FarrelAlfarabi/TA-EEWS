var socket = new WebSocket('ws://localhost:8000/get_gmji/20090118_064750/')

socket.onmessage = function(e){
    var data = JSON.parse(e.data);
    console.log(data);

    document.querySelector('#api').innerText = data;
}

socket.onclose = console.log('connection closed') 
