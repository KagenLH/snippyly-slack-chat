document.addEventListener("DOMContentLoaded", () => {
    const webSocket = new WebSocket("ws://localhost:3000/websocket");
    const chatDisplay = document.getElementById("chat-display")
    const submitButton = document.getElementById("submit-button")
    const chatInput = document.getElementById("chat-input")

    const addMessageToChat = (message) => {
        const chatMessageElement = document.createElement("p");
        chatMessageElement.innerText = message;
        chatDisplay.appendChild(chatMessageElement);
    }

    submitButton.addEventListener("click", (event) => {
        addMessageToChat(`You: ${chatInput.value}`);
        webSocket.send(chatInput.value);
        chatInput.value = "";
    });

    webSocket.onmessage = (event) => {
        addMessageToChat(`Slack: ${event.data}`);
    }
});