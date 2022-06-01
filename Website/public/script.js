function registered(){
    let width = screen.width;
    if (width < 700 ){
        console.log(width);

        document.body.style.backgroundImage = "url(public/images/mobile_meow2.png)";
        document.getElementById('msg').innerHTML = "Thank you for registering!";
    }
    else{
        document.body.style.backgroundImage = "url(public/images/meow2.png)";
        document.getElementById('msg').innerHTML = "Thank you for registering!";

    }

    var email =  document.getElementById('email').value;
    var petid =  document.getElementById('petid').value;
    const xhttp =  new XMLHttpRequest();
    xhttp.onload = function(){
        // document.getElementById("msg").innerHTML = this.response;
    };
    var string = "email="+email+"&petid="+petid;

    xhttp.open("POST","register.php");
    xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhttp.send(string);

}

function sent(){
    let width = screen.width;
    if (width < 700 ){

    document.body.style.backgroundImage = "url(public/images/mobile_meow2.png)";
    document.getElementById('msg').innerHTML = "Sent!";
    }
    else{
    document.body.style.backgroundImage = "url(public/images/meow2.png)";
    document.getElementById('msg').innerHTML = "Sent!"
    }

    // TODO will write code that communicates with server to push task to database

}

function welcome(){
    let width = screen.width;
    if (width < 700 ){
        //console.log(width);

        document.body.style.backgroundImage = "url(public/images/mobile_meow2.png)";
        document.getElementById('msg').innerHTML = "Welcome Back!";
    }
    else{
        document.body.style.backgroundImage = "url(public/images/meow2.png)";
        document.getElementById('msg').innerHTML = "Welcome Back!";

    }
}
window.addEventListener('load', function () {
    if (this.screen.width < 700 ){
        var element  = this.document.getElementById("body");
        element.style.fontSize("x-large");
    }
  })
  