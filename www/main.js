$(document).ready(function () {

    eel.init()()

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
      });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // mic button click event

    $("#MicBtn").click(function () { 
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });


    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
    

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

    async function login(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = String(document.getElementById('login-password').value);
        const result = await eel.login(username, password)();
         if (result) {
            alert('Login successful');
            await eel.speak("Login successful");
            $("#login-form").attr("hidden",true);
            $("#Loader").attr("hidden",false);
            await eel.init();
        } else {
            alert('Login failed');
        }
    }
    const loginSubmit = document.getElementById("login-submit")
    loginSubmit.addEventListener("click",login,false)

    async function register(event) {
        event.preventDefault();
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const phone = document.getElementById('register-phone').value;
        const password = document.getElementById('register-password').value;
        const save = document.getElementById('register-save-info').value;
        const result = await eel.createAuthenticateUser(username, email,phone, password,save)();
        if (result) {
            alert('Registration successful');
             await eel.speak("Registration Successful");
             $("#register-form").attr("hidden",true);
             $("#Loader").attr("hidden",false);
             await eel.init();
        } else {
            alert('Registration failed');
        }
    }
    const registerSubmit = document.getElementById("register-submit");
    registerSubmit.addEventListener("click",register,false);

    const settingsBtn = document.getElementById('SettingsBtn');
    const toggleMenu = document.getElementById('toggle-menu');
    
    settingsBtn.addEventListener('click', function () {
            if (toggleMenu.hidden) {
                toggleMenu.hidden = false;
            } else {
                toggleMenu.hidden = true;
            }
        });
    
        // Close the menu if clicked outside
    document.addEventListener('click', function (event) {
            if (!settingsBtn.contains(event.target) && !toggleMenu.contains(event.target)) {
                toggleMenu.hidden = true;
            }
        });

     const logout = document.getElementById("logout-btn");
     logout.addEventListener('click',function (event){
        event.preventDefault();
        var confiramtion = confirm("Are you sure logging out yourself");
        if (confiramtion){
            $('#Oval').attr("hidden",true);
            $('#HelloGreet').attr("hidden",true);
            $("#Start").attr("hidden",false);
            $("#Loader").attr("hidden",false);
            eel.logout();
        }
     })   

     const profile = document.getElementById("profile-btn");
     profile.addEventListener('click',(event)=>{
        event.preventDefault();
        $('#Oval').attr("hidden",true);
        $('#profile').attr("hidden",false);
     })

     function setUserDetails(userDetails) {
        document.getElementById('username').value = userDetails.username;
        document.getElementById('email').value = userDetails.email;
        document.getElementById('phone').value = userDetails.phone;
        document.getElementById('password').value = userDetails.password;
        document.getElementById('confirm-password').value = userDetails.password; // Assuming confirm password is same as password initially
    }

    // Fetch user details from eel and set them into the form
    eel.getUserDetails()(function(userDetails) {
        setUserDetails(userDetails);
    });
	document.getElementById('profile-update-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get current form values
        const updatedUserDetails = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            password: document.getElementById('password').value,
        };

        // Check if there are any changes
        const hasChanges = Object.keys(updatedUserDetails).some(key => updatedUserDetails[key] !== initialUserDetails[key]);

        if (hasChanges) {
            // Update user details through eel
            eel.updateUser(updatedUserDetails)(function(response) {
                if (response.success) {
                    alert('Profile updated successfully!');
					$('#profile').attr("hidden",true);
					$('#Oval').attr("hidden",false);
                } else {
                    alert('Failed to update profile. Please try again.');
                }
            });
        } else {
            alert('No changes detected.');
			$('#profile').attr("hidden",true);
			$('#Oval').attr("hidden",false);
        }
    });
    //  const contact = document.getElementById("contact-btn");
    //  contact.addEventListener('click',(event)=>{
    //     event.preventDefault();
    //  })
});
