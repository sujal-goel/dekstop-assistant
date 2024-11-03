$(document).ready(function () {



    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message").text(message);
        $('.siri-message').textillate('start');

    }
    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }
    eel.expose(showRegister)
    function showRegister(){
        $("#Loader").attr("hidden", true);
        $("#login-form").attr("hidden",true)
        $("#register-form").attr("hidden",false)
    }
    const logtoregister = document.getElementById("logtoregister")
    logtoregister.addEventListener("click",showRegister,false)
    eel.expose(showLogin)
    
    function showLogin(){
        $("#Loader").attr("hidden", true);
        $("#register-form").attr("hidden",true)
        $("#login-form").attr("hidden",false)
    }
    const registertologin = document.getElementById("registertologin")
    registertologin.addEventListener("click",showLogin,false)
    
    // Hide Loader and display Face Auth animation
    eel.expose(hideLoader)
    function hideLoader(destination) {
        $('#Loader').attr("hidden", true);
        $(`#${destination}`).attr("hidden", false);

    }
    eel.expose(hideMessage)
    function hideMessage(){
        $('#message').attr("hidden",true)
    }
    // Hide Face auth and display Face Auth success animation
    eel.expose(hideFaceAuth)
    function hideFaceAuth() {

        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);

    }

    eel.expose(ask)
    function ask(message){
        let ans = prompt(message);
        if(ans!= null){
            return ans
        }
    }

    // Hide success and display 
    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {

        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);

    }

    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {

        $("#Start").attr("hidden", true);

        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");

        }, 1000)
        setTimeout(function () {
            $("#Oval").attr("hidden", false);
        }, 1000)
    }


});