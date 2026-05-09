async function sendMessage() {

    let input = document.getElementById("userInput");

    let message = input.value;

    if(message.trim() === ""){
        return;
    }

    let chatBox = document.getElementById("chatBox");

    // USER MESSAGE

    let userMessage = document.createElement("div");

    userMessage.classList.add("message", "user");

    userMessage.innerText = message;

    chatBox.appendChild(userMessage);

    // CLEAR INPUT

    input.value = "";

    // BOT LOADING MESSAGE

    let botMessage = document.createElement("div");

    botMessage.classList.add("message", "bot");

    botMessage.innerText = "Typing...";

    chatBox.appendChild(botMessage);

    // AUTO SCROLL

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        // API CALL

        const response = await fetch("http://127.0.0.1:8080/get", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        // SHOW RESPONSE

        botMessage.innerText = data.response;

    }

    catch(error){

        botMessage.innerText = "Error connecting to backend.";

        console.log(error);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}