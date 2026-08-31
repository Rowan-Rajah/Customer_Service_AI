/* =========================================================
   Customer Service AI
   Website Chat Widget
   JavaScript
   ========================================================= */


/* ---------------------------------------------------------
   API Configuration
   --------------------------------------------------------- */

// Local FastAPI server

const API_URL = "https://customer-service-ai-fastapi.onrender.com/chat";


/* ---------------------------------------------------------
   Create Session ID
   --------------------------------------------------------- */

// Each visitor gets their own session ID.

const sessionId = crypto.randomUUID();


/* ---------------------------------------------------------
   Get HTML Elements
   --------------------------------------------------------- */

const messageInput =
    document.getElementById("message-input");

const sendButton =
    document.getElementById("send-button");

const chatMessages =
    document.getElementById("chat-messages");

const closeButton =
    document.getElementById("close-chat");

const openButton =
    document.getElementById("open-chat");

const chatWidget =
    document.getElementById("chat-widget");


/* ---------------------------------------------------------
   Open Chat
   --------------------------------------------------------- */

openButton.addEventListener(
    "click",
    function() {

        chatWidget.style.display = "flex";

        openButton.style.display = "none";

    }
);


/* ---------------------------------------------------------
   Close Chat
   --------------------------------------------------------- */

closeButton.addEventListener(
    "click",
    function() {

        chatWidget.style.display = "none";

        openButton.style.display = "block";

    }
);



/* ---------------------------------------------------------
   Add Message to Chat
   --------------------------------------------------------- */

function addMessage(message, sender) {

    const messageElement =
        document.createElement("div");


    messageElement.classList.add(
        "message"
    );


    if (sender === "user") {

        messageElement.classList.add(
            "user-message"
        );

    }
    else {

        messageElement.classList.add(
            "assistant-message"
        );

    }


    /* -----------------------------------------------------
       Format AI Markdown
       ----------------------------------------------------- */

    // Escape HTML first so the AI cannot insert raw HTML
    // into the website.

    let formattedMessage =
        message
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");


    // Convert Markdown bold: **text** -> <strong>text</strong>

    formattedMessage =
        formattedMessage.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // Convert line breaks into HTML line breaks.

    formattedMessage =
        formattedMessage.replace(
            /\n/g,
            "<br>"
        );


    // Display the formatted message.

    messageElement.innerHTML =
        formattedMessage;


    chatMessages.appendChild(
        messageElement
    );


    // Automatically scroll to newest message.

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}



/* ---------------------------------------------------------
   Send Message
   --------------------------------------------------------- */

async function sendMessage() {

    const message =
        messageInput.value.trim();


    // Do nothing if input is empty.

    if (!message) {

        return;

    }


    /* -----------------------------------------------------
       Display Customer Message
       ----------------------------------------------------- */

    addMessage(
        message,
        "user"
    );


    // Clear input box.

    messageInput.value = "";


    /* -----------------------------------------------------
       Disable Button While Waiting
       ----------------------------------------------------- */

    sendButton.disabled = true;

    sendButton.textContent = "Sending...";


    try {

        /* -------------------------------------------------
           Send Request to FastAPI
           ------------------------------------------------- */

        const response =
            await fetch(
                API_URL,
                {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(
                        {
                            message: message,
                            session_id: sessionId
                        }
                    )

                }
            );


        /* -------------------------------------------------
           Check HTTP Response
           ------------------------------------------------- */

        if (!response.ok) {

            throw new Error(
                "API request failed."
            );

        }


        /* -------------------------------------------------
           Convert Response to JSON
           ------------------------------------------------- */

        const data =
            await response.json();


        /* -------------------------------------------------
           Display AI Response
           ------------------------------------------------- */

        addMessage(
            data.reply,
            "assistant"
        );


    }
    catch (error) {

        console.error(
            "Website widget error:",
            error
        );


        /* -----------------------------------------------
           Display Error Message
           ----------------------------------------------- */

        addMessage(
            "Sorry, I am unable to connect to the customer service system right now.",
            "assistant"
        );

    }


    /* -----------------------------------------------------
       Re-enable Button
       ----------------------------------------------------- */

    sendButton.disabled = false;

    sendButton.textContent = "Send";

}


/* ---------------------------------------------------------
   Send Button
   --------------------------------------------------------- */

sendButton.addEventListener(
    "click",
    sendMessage
);


/* ---------------------------------------------------------
   Press Enter to Send
   --------------------------------------------------------- */

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);
