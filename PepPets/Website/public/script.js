function register() {
    var email = document.getElementById('email').value;
    var petID = document.getElementById('petID').value;
    var width = screen.width;

    if(email == "" || petID == "") {
        if (email == "") {
            document.getElementById("msg").innerHTML = "Please enter a valid email";
        }
        else {
            document.getElementById("msg").innerHTML = "Please enter a valid ID";
        }
    }
    else {
        if(width < 700 ) {
            console.log(width);
    
            document.body.style.backgroundImage = "url(images/mobile_meow2.png)";
            document.getElementById('msg').innerHTML = "Thank you for registering!";
        }
        else {
            document.body.style.backgroundImage = "url(images/meow2.png)";
            document.getElementById('msg').innerHTML = "Thank you for registering!";
        }
        // Fetch is a Javascript function that sends a request to a server
        let theURL = '/user/' + email + '/' + petID;
        fetch(theURL)
            .then(response => response.json()) // Convert response to JSON
            .then(function (response) {
                // Send URL with email and pet-ID
            });
    }
}

function createTask() {
    var petID = document.getElementById('petID').value;
    var task_description = document.getElementById('task').value;
    var width = screen.width;

    if(petID == "" || task_description == "") {
        if(petID == "") {
            document.getElementById("msg").innerHTML = "Please enter a valid ID";
        }
        else {
            document.getElementById("msg").innerHTML = "Please enter a valid task description";
        }
    }
    else {
        if(width < 700) {
            console.log(width);

            document.body.style.backgroundImage = "url(images/mobile_meow2.png)";
            document.getElementById('msg').innerHTML = "New Task Created!";
        }
        else {
            document.body.style.backgroundImage = "url(images/meow2.png)";
            document.getElementById('msg').innerHTML = "New Task Created!";
        }
        // Fetch is a Javascript function that sends a request to a server
        let theURL = '/task/' + petID + '/' + task_description;
        fetch(theURL)
            .then(response => response.json()) // Convert response to JSON
            .then(function (response) {
                // Send URL with email and pet-ID
            });
    }
}

function updateSheet() {
    var petID = document.getElementById('petID').value;
    var width = screen.width;

    if (petID == "") {
        document.getElementById("msg").innerHTML = "Please enter a valid ID";
    }
    else {
        if (width < 700) {
            console.log(width);

            document.body.style.backgroundImage = "url(images/mobile_meow2.png)";
            document.getElementById('msg').innerHTML = "Task Marked Finished!";
        }
        else {
            document.body.style.backgroundImage = "url(images/meow2.png)";
            document.getElementById('msg').innerHTML = "Task Marked Finished!";
        }
        // Fetch is a Javascript function that sends a request to a server
        let theURL = '/finishedtask/' + petID;
        fetch(theURL)
            .then(response => response.json()) // Convert response to JSON
            .then(function (response) {
                // Send URL with email and pet-ID
            });
    }
}