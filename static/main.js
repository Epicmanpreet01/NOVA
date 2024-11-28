$(document).ready(function () {
    // initialize textillate animation
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeIn",
        },
        out: {
            effect: "fadeOut",
        },
    });

    // initialize siri wave
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 640,
        height: 200,
        style: "ios9",
        speed: 0.02,
        amplitude: 2,
        autostart: true,
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeIn",
            sync: true,
            delay: 1000
        },
        out: {
            effect: "fadeOut",
            sync: true,
            delay: 1000
        },
        minDisplayTime: 2000,
        initialDisplay: 500
    });

    // starts the assistant audio recognition window with the siri wave
    function startAssistant() {
        $("#AI").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.playSound();
        eel.allCommands()();
    }

    // Mic button click handler
    $("#MicBtn").click(startAssistant);

    // Exposing the function triggerAssistant for wake word detection
    eel.expose(triggerAssistant);
    function triggerAssistant() {
        startAssistant();
    }

    // Keyboard shortcut handler
    function doc_keyUP(e) {
        if (e.key === 'j' && (e.metaKey || e.ctrlKey)) {
            startAssistant();
        }
    }
    document.addEventListener('keyup', doc_keyUP, false);

    // Chat functionality
    function chatAssistant(message) {
        if (message !== "") {
            $("#AI").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        }
    }

    // Send button visibility toggle
    function ShowSendBtn(message) {
        if (message.length === 0) {
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        } else {
            $("#MicBtn").attr("hidden", true);
            $("#SendBtn").attr("hidden", false);
        }
    }

    // Chat input handlers
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowSendBtn(message);
    });

    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        chatAssistant(message);
    });

    $("#chatbox").keypress(function (e) {
        let key = e.which;
        if (key === 13) {
            let message = $("#chatbox").val();
            chatAssistant(message);
        }
    });

    
});