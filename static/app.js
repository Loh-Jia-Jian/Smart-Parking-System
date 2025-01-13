const toggleButton = document.getElementById('toggleButton');
const chatBody = document.getElementById("chatBody");
const chatInput = document.getElementById("chatInput");
const sidebar = document.getElementById('sidebar')
const chatbox = document.getElementById('chatbox');

function toggleSidebar() {
    sidebar.classList.toggle('close')
    toggleButton.classList.toggle('rotate')

    closeAllSubMenus()
}

function toggleSubMenu(button) {

    if (!button.nextElementSibling.classList.contains('show')) {
        closeAllSubMenus()
    }

    button.nextElementSibling.classList.toggle('show')
    button.classList.toggle('rotate')

    if (sidebar.classList.contains('close')) {
        sidebar.classList.toggle('close')
        toggleButton.classList.toggle('rotate')
    }
}

function closeAllSubMenus() {
    Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
        ul.classList.remove('show')
        ul.previousElementSibling.classList.remove('rotate')
    })
}

function appendMessage(text, sender) {
    const message = document.createElement("div");
    message.classList.add("message", sender);
    message.textContent = text;

    chatBody.appendChild(message);
    chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to the latest message
}

async function sendMessage() {
    const userInput = chatInput.value.trim();
    if (!userInput) return;

    // Display user's message
    appendMessage(userInput, "user");
    chatInput.value = "";

    // Display loading indicator
    const loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message", "assistant");
    loadingMessage.textContent = "Thinking...";
    loadingMessage.style.marginLeft = "10px";
    loadingMessage.style.marginRight = "auto";
    chatBody.appendChild(loadingMessage);
    chatBody.scrollTop = chatBody.scrollHeight;

    try {
        // Send message to backend
        const response = await axios.post("/ask", { question: userInput });
        chatBody.removeChild(loadingMessage); // Remove loading indicator

        // Display assistant's response
        appendMessage(response.data.answer, "assistant");
    } catch (error) {
        chatBody.removeChild(loadingMessage); // Remove loading indicator
        appendMessage(
            "Sorry, something went wrong. Please try again.",
            "assistant"
        );
    }
}