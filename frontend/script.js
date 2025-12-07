const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const sessionId =
  (crypto.randomUUID && crypto.randomUUID()) || String(Date.now());

function appendMessage(text, sender, meta) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  wrapper.appendChild(bubble);

  if (meta && sender === "bot") {
    const metaDiv = document.createElement("div");
    metaDiv.className = "meta";
    metaDiv.textContent =
      `intent: ${meta.intent_tag}, model: ${meta.model_version}` +
      (meta.log_tx_hash ? `, log tx: ${meta.log_tx_hash.slice(0, 10)}...` : "");
    wrapper.appendChild(metaDiv);
  }

  chatWindow.appendChild(wrapper);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage(text, "user");
  userInput.value = "";

  try {
    const res = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });
    const data = await res.json();
    if (data.reply) {
      appendMessage(data.reply, "bot", data.meta);
    } else if (data.error) {
      appendMessage("Error: " + data.error, "bot");
    }
  } catch (e) {
    console.error(e);
    appendMessage("Error contacting server.", "bot");
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
