function registered(){
    let width = screen.width;
    var email =  document.getElementById('email').value;
    var petid =  document.getElementById('petid').value;

    if(email == "" || petid ==""){
        document.getElementById("msg").innerHTML = "Please enter valid Email/ID";
        return;
    }
    else{
        if (width < 700 ){
            console.log(width);
    
            document.body.style.backgroundImage = "url(public/images/mobile_meow2.png)";
            document.getElementById('msg').innerHTML = "Thank you for registering!";
        }
        else{
            document.body.style.backgroundImage = "url(public/images/meow2.png)";
            document.getElementById('msg').innerHTML = "Thank you for registering!";
    
        }
    
        const xhttp =  new XMLHttpRequest();
        xhttp.onload = function(){
            // document.getElementById("msg").innerHTML = this.response;
        };
        var string = "email="+email+"&petid="+petid;
    
        xhttp.open("POST","Website/public/register.php");
        xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xhttp.send(string);

    }
}

function sent(){
    let width = screen.width;
    var task =  document.getElementById('task').value;
    var petid =  document.getElementById('petid').value;

    if(petid ==""){
        document.getElementById("msg").innerHTML = "Please enter valid ID";
    }
    else{
        if (width < 700 ){
            document.body.style.backgroundImage = "url(public/images/mobile_meow2.png)";
            document.getElementById('msg').innerHTML = "Sent!";
            }
            else{
            document.body.style.backgroundImage = "url(public/images/meow2.png)";
            document.getElementById('msg').innerHTML = "Sent!"
            }
            var string = "petid="+petid + "&task="+task;
            const xhttp =  new XMLHttpRequest();
            xhttp.onload = function(){
                // document.getElementById("msg").innerHTML = this.response;
            };
            xhttp.open("POST","Website/public/sendtask.php");
            xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xhttp.send(string);
    }
}
function updateDB(){
    var petid =  document.getElementById('petid').value;

    if(petid ==""){
        document.getElementById("msg").innerHTML = "Please enter valid ID";
    }
    else{
        const xhttp =  new XMLHttpRequest();
        xhttp.onload = function(){
            // document.getElementById("msg").innerHTML = this.response;
        };
        xhttp.open("POST","Website/public/update.php");
        xhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xhttp.send("petid="+petid);
        document.getElementById('msg').innerHTML = "Task marked complete!";
    }
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
  