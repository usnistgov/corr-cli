var client = new XMLHttpRequest();
var user = {
    url: "http://"+config.host+":"+config.port+"/cloud/v0.1",
    username:"",
    email: "",
    api: "",
    session: "",
    login: function() {
        var email = document.getElementById("login-email").value;
        var password = document.getElementById("login-password").value;
        console.log(email+" -- "+password)
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", this.url+"/public/user/login");
        var request = { 'email': email, 'password': password }
        xmlhttp.send(JSON.stringify(request));
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    var response = JSON.parse(xmlhttp.responseText);
                    this.session = response['session']
                    console.log(this.session);
                    
                    window.location.replace("./?session="+this.session);
                }
            } else {
                console.log(xmlhttp.responseText);
                Materialize.toast('<span>'+xmlhttp.responseText+'</span>', 3000);
            }
        }
    },
    register: function() {
        var username = document.getElementById("register-email").value;
        var email = document.getElementById("register-email").value;
        var password = document.getElementById("register-password").value;
        var password_again = document.getElementById("register-password-again").value;
        if(password == password_again){
            console.log(username+" -- "+email+" -- "+password);
            var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
            xmlhttp.open("POST", this.url+"/public/user/register");
            var request = { 'email': email, 'password': password, 'username':username };
            xmlhttp.send(JSON.stringify(request));
            xmlhttp.onreadystatechange=function()
            {
                if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                     if(xmlhttp.responseText == ""){
                        console.log("Cloud returned empty response!");
                    }else{
                        var response = JSON.parse(xmlhttp.responseText);
                        this.session = response['session'];
                        console.log(this.session);
                        window.location.replace("../?session="+this.session);
                    }
                } else {
                    var response = xmlhttp.responseText;
                    console.log(response);
                    console.log("Registration failed");
                    if(response == ""){
                        Materialize.toast('<span>Register failed: Unknown reason.</span>', 3000);
                    }else{
                        Materialize.toast('<span>Register failed: '+response+'</span>', 3000);
                    }
                }
            }
        }else{
            Materialize.toast('<span>Passwords mismatch.</span>', 3000);
        }  
    },
    logout: function(where) {
        var xmlhttp = new XMLHttpRequest();
        console.log(this.session);
        xmlhttp.open("GET", this.url+"/private/"+this.session+"/user/logout");
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                 if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    if(where != "dashboard"){
                        window.location.replace("./");
                    }else{
                        window.location.replace("../");
                    }
                }
            } else {
                console.log("Logout failed");
                Materialize.toast('<span>Logout failed</span>', 3000);
            }
        }   
    },
    update: function() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", this.url+"/private/"+this.session+"/user/update");
        var pwd = document.getElementById('edit-new-password').value;
        var pwd_2 = document.getElementById('edit-new-password-again').value;
        if(pwd != pwd_2){
            console.log("Passwords mismatch");
            Materialize.toast('<span>Passwords mismatch</span>', 3000);
        }else{
            var fname = document.getElementById('view-fname').value;
            var lname = document.getElementById('view-lname').value;
            var org = document.getElementById('view-org').value;
            var about = document.getElementById('view-about').value;
            if(fname == "None"){
                fname = ""
            }
            if(lname == "None"){
                lname = ""
            }
            if(org == "None"){
                org = ""
            }
            if(about == "None"){
                about = ""
            }
            console.log("Fname: "+fname);
            console.log("Lname: "+lname);
            var request = { 'pwd': pwd, 'fname': fname, 'lname': lname, 'org': org, 'about': about }
            xmlhttp.send(JSON.stringify(request));
            xmlhttp.onreadystatechange=function()
            {
                if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                    var response = xmlhttp.responseText;
                    console.log(response);

                    var file = document.getElementById("picture-input");
                    if (file.files.length > 0) {
                        user.upload_file(file, 'picture', 'none');
                    }else{
                        console.log("No picture to change");
                        window.location.replace("../?session="+user.session);
                    }
                    Materialize.toast('<span>Update succeeded</span>', 3000);
                } else {
                    console.log("Update failed");
                    Materialize.toast('<span>Update failed</span>', 3000);
                }
            }
        }
    },
    upload_file: function(file, group, item_id) {
        console.log("File: "+file.files[0].name);
        var formData = new FormData();
        formData.append("file", file.files[0], file.files[0].name);
        console.log(formData);
        $.ajax({
            url        : this.url+"/private/"+this.session+"/file/upload/"+group+"/"+item_id,
            type       : "POST",
            data       : formData, 
            async      : true,
            cache      : false,
            processData: false,
            contentType: false,
            success    : function(text){
                if(text == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    window.location.replace("../?session="+user.session);
                }
            }
         });
         event.preventDefault();
    },
    recover: function() {
        var email = document.getElementById("recover-email").value;
        console.log(email+" -- recover")
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", this.url+"/public/user/recover");
        var request = { 'email': email}
        xmlhttp.send(JSON.stringify(request));
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    console.log(xmlhttp.responseText);                
                    Materialize.toast('<span>'+xmlhttp.responseText+'</span>', 3000);
                }
            } else {
                console.log(xmlhttp.responseText);                
                Materialize.toast('<span>'+xmlhttp.responseText+'</span>', 3000);
            }
        }
    },
    trusted: function() {
        var xmlhttp = new XMLHttpRequest();
        console.log(this.session);
        xmlhttp.open("GET", this.url+"/private/"+this.session+"/user/trusted");
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                console.log(xmlhttp.responseText);
                if(xmlhttp.responseText != ""){
                    if(xmlhttp.responseText == ""){
                        console.log("Cloud returned empty response!");
                    }else{
                        var response = JSON.parse(xmlhttp.responseText);
                        var version = response["version"];
                        console.log("Version: "+version);
                        document.getElementById("footer-version").innerHTML = version;
                    }
                }
                Materialize.toast('<span>Access trusted!</span>', 3000);
                
            } else {
                window.location.replace("../error-404/");
            }
        } 
    },
    account: function() {
        var xmlhttp = new XMLHttpRequest();
        console.log(this.session);
        xmlhttp.open("GET", this.url+"/private/"+this.session+"/user/profile");
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    var response = JSON.parse(xmlhttp.responseText);
                    this.email = response['email'];
                    this.fname = response['fname']
                    this.lname = response['lname'];
                    this.organisation = response['organisation']
                    this.about = response['about']
                    this.api = response['api'];
                    $('#view-username-value').text(this.username);
                    document.getElementById('view-email').value = this.email;
                    document.getElementById('view-api').value = this.api;
                    document.getElementById('view-fname').value = this.fname;
                    document.getElementById('view-lname').value = this.lname;
                    document.getElementById('view-org').value = this.organisation;
                    document.getElementById('view-about').value = this.about;
                    console.log("Account Api: "+this.api);
                }
            } else {
                window.location.replace("../error-404/");
            }
        }
    },
    renew: function() {
        var xmlhttp = new XMLHttpRequest();
        console.log(this.session);
        xmlhttp.open("GET", this.url+"/private/"+this.session+"/user/renew");
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    var response = JSON.parse(xmlhttp.responseText);
                    this.api = response['api'];
                    if(this.api.length > 18){
                        $('#view-api-value').text(this.api.substring(0,15)+"...");
                    }else{
                        $('#view-api-value').text(this.api);
                    }
                    Materialize.toast('<span>API Token renewed!</span>', 3000);
                }
            } else {
                window.location.replace("../error-404/");
            }
        }
    },
    copy_api: function() {
        console.log("Api: "+this.api);
        console.log("Email: "+this.email);
        console.log("Username: "+this.username);
        console.log("Session: "+this.session);
    }
}

var Space = function (session){
    var url = "http://"+config.host+":"+config.port+"/cloud/v0.1";
    this.session = session;
    this.dash_content = "";
    this.dashboard = function() {
        var xmlhttp = new XMLHttpRequest();
        console.log(this.session);
        xmlhttp.open("GET", url+"/private/"+this.session+"/dashboard/projects");
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText != ""){
                    var response = JSON.parse(xmlhttp.responseText);
                    this.dash_content = response;
                    document.getElementById("projects-list").innerHTML = "";
                    var version = response["version"];
                    console.log("Version: "+version);
                    for(var i = 0; i < response["projects"].length; i++){
                        project = response["projects"][i];
                        console.log(project);
                        var disable_view = "";
                        if(project["project"]["records"] == 0){
                            disable_view = "disabled";
                        }
                        var content = "<div class='col s12 m6 l4'>";
                        content += "<div id='profile-card' class='card'>";
                        content += "<div class='card-image waves-effect waves-block waves-light'><img class='activator' src='../images/user-bg.jpg' alt='user background'></div>";
                        content += "<div class='card-content'>";
                        content += "<img src='../images/project.png' alt='' class='circle responsive-img activator card-profile-image'>";
                        content += "<a href='./?session="+session+"&view=records&project="+project["project"]["id"]+"' class='btn-floating activator btn-move-up waves-effect waves-light darken-2 right "+disable_view+"'><i class='mdi-action-visibility'></i></a>";
                        content += "<a href='' class='btn-floating activator btn-move-up waves-effect waves-light darken-2 right ><i class='mdi-action-delete'></i></a>";
                        content += "<a href='' class='btn-floating activator btn-move-up waves-effect waves-light darken-2 right ><i class='mdi-editor-mode-edit'></i></a>";
                        content += "<a href='' class='btn-floating activator btn-move-up waves-effect waves-light darken-2 right ><i class='mdi-editor-mode-edit'></i></a>";
                        content += "<span class='card-title activator white-text text-darken-4'> "+project["project"]["name"]+"</span>";
                        content += "<p class='grey-text ultra-small'><i class='mdi-device-access-time cyan-text text-darken-2'></i> "+project["project"]["created"]+"</p>";
                        content += "<p><i class='mdi-device-access-alarm cyan-text text-darken-2'></i> "+project["project"]["duration"]+"</p>";
                        content += "<p><i class='mdi-action-description cyan-text text-darken-2'></i> "+project["project"]["description"]+"</p>";
                        content += "<p><i class='mdi-action-subject cyan-text text-darken-2'></i> "+project["project"]["goals"]+"</p>";
                        content += "<div class='card-action center-align'>";
                        content += "<a href='#' class='valign'><i class='mdi-file-cloud-done cyan-text text-darken-2'></i> <span class='records badge'>"+project["project"]["records"]+"</span></a>";
                        content += "<a href='#' class='valign'><i class='mdi-image-compare cyan-text text-darken-2'></i> <span class='diffs badge'>"+project["project"]["diffs"]+"</span></a>";
                        content += "<a href='#' class='valign'><i class='mdi-editor-insert-chart cyan-text text-darken-2'></i> <span class='containers badge'>"+project["project"]["environments"]+"</span></a>";
                        content += "</div>";
                        content += "</div>";
                        content += "</div>";
                        content += "</div>";
                        document.getElementById("projects-list").innerHTML += content;
                    }
                    if(document.getElementById("temporal-slider") && response["projects"].length >0){
                        document.getElementById("temporal-slider").innerHTML = "<div class='slider-date'><div class='lower'></div><div class='upper'></div></div><span id='event-start' class='temporal-val'>Thursday, 30th December 2010</span><span id='event-end' class='temporal-val date-right'>Thursday, 1st January 2015</span>";
                        if(response["projects"].length >0){
                            function timestamp(str){
                                return new Date(str).getTime();   
                            }
                            function nth (d) {
                              if(d>3 && d<21) return 'th';
                              switch (d % 10) {
                                case 1:  return "st";
                                case 2:  return "nd";
                                case 3:  return "rd";
                                default: return "th";
                                }
                            }
                            function formatDate ( date ) {
                                var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
                                var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                                return weekdays[date.getDay()] + ", " + date.getDate() + nth(date.getDate()) + " " + months[date.getMonth()] + " " + date.getFullYear();
                            }
                            function setDate( value ){
                                $(this).html(formatDate(new Date(+value)));   
                            }
                            $('.slider-date').noUiSlider({
                                animate: true,
                                connect: true,
                                start: [ timestamp(response["projects"][0]["project"]["created"]), timestamp(response["projects"][response["projects"].length - 1]["project"]["created"]) ],
                                step: 1 * 24 * 60 * 60 * 1000,
                                format: wNumb({
                                    decimals: 0
                                    }),
                                range: {
                                    min: timestamp(response["projects"][0]["project"]["created"]),
                                    max: timestamp(response["projects"][response["projects"].length - 1]["project"]["created"])
                                }
                            });
                            $(".slider-date").Link('lower').to($("#event-start"), setDate);
                            $(".slider-date").Link('upper').to($("#event-end"), setDate);
                        }
                    }else{
                        if(response["projects"].length == 0){
                            document.getElementById("temporal-slider").innerHTML = "<div><span class='chart-title cyan-text'>No project found.</span><div>";
                        }
                    }
                    document.getElementById("footer-version").innerHTML = version;
                }else{
                    console.log("Cloud returned empty response!");
                }
            } else {
                console.log("Dashboard failed");
            }
        }
    },
    this.records = function(project_id) {
        document.getElementById("records-list").innerHTML = "<div class='progress'><div class='indeterminate'></div></div>";
        document.getElementById("temporal-slider").innerHTML = "";
        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
        console.log("Project id: "+project_id);
        if(project_id == "all"){
            xmlhttp.open("GET", url+"/private/"+this.session+"/dashboard/records/all");
        }else{
            xmlhttp.open("GET", url+"/private/"+this.session+"/dashboard/records/"+project_id);
        }
        console.log(this.session);
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    var response = JSON.parse(xmlhttp.responseText);
                    document.getElementById("records-list").innerHTML = "";
                    this.dash_content = response;
                    
                    for(var i = 0; i < response["records"].length; i++){
                        record = response["records"][i];
                        console.log(record);
                        var content = "<div class='col s12 m6 l4' id='record-"+record["head"]["id"]+"'> ";
                        content += "<div id='profile-card' class='card'>";
                        content += "<div class='card-image waves-effect waves-block waves-light'><img class='activator' src='../images/user-bg.jpg' alt='user background'></div>";
                        content += "<div class='card-content'>";
                        var disable_download = "";
                        if(record["container"] == false){
                            disable_download = "disabled";
                        }
                        content += "<img src='../images/record.png' alt='' class='circle responsive-img activator card-profile-image'><a onclick=\"space.pull('"+record["head"]["project"]+"','"+record["head"]["id"]+"')\" class='btn-floating activator btn-move-up waves-effect waves-light darken-2 right "+disable_download+"'><i class='mdi-file-cloud-download tooltipped' data-position='top' data-delay='50' data-tooltip='download'></i></a><span class='card-title activator grey-text text-darken-4'> "+record["head"]["label"]+"</span>";
                        content += "<p class='grey-text ultra-small'><i class='mdi-device-access-time cyan-text text-darken-2'></i> "+record["head"]["created"]+"</p>";
                        content += "<p><i class='mdi-device-access-alarm cyan-text text-darken-2'></i> "+record["head"]["updated"]+"</p>";
                        content += "<p><i class='mdi-notification-event-note cyan-text text-darken-2'></i> "+record["head"]["id"]+"</p>";
                        content += "<p><i class='mdi-notification-sync cyan-text text-darken-2'></i> "+record["head"]["status"]+"</p>";
                        content += "<div class='card-action center-align'>";
                        content += "<a href='#' class='valign'><i class='mdi-action-input cyan-text text-darken-2'></i> <span class='inputs badge'>"+record["head"]["inputs"]+"</span></a>";
                        content += "<a href='#' class='valign'><i class='mdi-action-launch cyan-text text-darken-2'></i> <span class='outputs badge'>"+record["head"]["outputs"]+"</span></a>";
                        content += "<a href='#' class='valign'><i class='mdi-editor-insert-link cyan-text text-darken-2'></i> <span class='dependencies badge'>"+record["head"]["dependencies"]+"</span></a>";
                        content += "</div>";
                        content += "</div>";                
                        content += "</div>";
                        content += "</div>";
                        document.getElementById("records-list").innerHTML += content;
                    }
                    if(document.getElementById("temporal-slider") && response["records"].length >0){
                        document.getElementById("temporal-slider").innerHTML = "<div class='slider-date'><div class='lower'></div><div class='upper'></div></div><span id='event-start' class='temporal-val'>Thursday, 30th December 2010</span><span id='event-end' class='temporal-val date-right'>Thursday, 1st January 2015</span>";
                        if(response["records"].length >0){
                            function timestamp(str){
                                return new Date(str).getTime();   
                            }
                            function nth (d) {
                              if(d>3 && d<21) return 'th';
                              switch (d % 10) {
                                case 1:  return "st";
                                case 2:  return "nd";
                                case 3:  return "rd";
                                default: return "th";
                                }
                            }
                            function formatDate ( date ) {
                                var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
                                var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                                return weekdays[date.getDay()] + ", " + date.getDate() + nth(date.getDate()) + " " + months[date.getMonth()] + " " + date.getFullYear();
                            }
                            function setDate( value ){
                                $(this).html(formatDate(new Date(+value)));   
                            }
                            console.log(response["records"][0]["head"]["created"]);
                            $('.slider-date').noUiSlider({
                                animate: true,
                                connect: true,
                                start: [ timestamp(response["records"][0]["head"]["created"]), timestamp(response["records"][response["records"].length-1]["head"]["created"]) ],
                                step: 1 * 24 * 60 * 60 * 1000,
                                format: wNumb({
                                    decimals: 0
                                    }),
                                range: {
                                    min: timestamp(response["records"][0]["head"]["created"]),
                                    max: timestamp(response["records"][response["records"].length-1]["head"]["created"])
                                }
                            });
                            $(".slider-date").Link('lower').to($("#event-start"), setDate);
                            $(".slider-date").Link('upper').to($("#event-end"), setDate);
                        }
                    }else{
                        if(response["records"].length == 0){
                            document.getElementById("temporal-slider").innerHTML = "<div><span class='chart-title cyan-text'>No records found.</span><div>";
                        }
                    }
                }
            } else {
                console.log("Dashboard failed");
            }
        }
    },
    this.exportToJson = function () {
        var xmlhttp = new XMLHttpRequest();
        console.log(this.session);
        xmlhttp.open("GET", url+"/private/"+this.session+"/dashboard/projects");
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
        {
            if ((xmlhttp.status >= 200 && xmlhttp.status <= 300) || xmlhttp.status == 304) {
                if(xmlhttp.responseText == ""){
                    console.log("Cloud returned empty response!");
                }else{
                    var pom = document.createElement('a');
                    pom.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(JSON.parse(xmlhttp.responseText), null, 2)));
                    pom.setAttribute('download', 'dashboard.json');

                    if (document.createEvent) {
                        var event = document.createEvent('MouseEvents');
                        event.initEvent('click', true, true);
                        pom.dispatchEvent(event);
                    }
                    else {
                        pom.click();
                    }
                }
            } else {
                console.log("Dashboard download failed");
            }
        }
    },
    this.pull = function(project_name, record_id) {
        console.log("Before...");
        window.location.replace(url+"/private/"+this.session+"/record/pull"+"/"+record_id);
        console.log("...After");
    }
};