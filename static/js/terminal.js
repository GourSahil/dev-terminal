// -----------------------------
// ANSI setup
// -----------------------------

const ansi_up = new AnsiUp();

function normalizeAnsi(input) {
    return input.replace(/\\x1b/g, '\x1b');
}

function renderAnsi(text) {
    return ansi_up.ansi_to_html(text);
}

// -----------------------------
// DOM references
// -----------------------------

const input = document.getElementById("terminal-input");
const output = document.getElementById("terminal-output");
const terminal = document.getElementById("terminal-container");

// -----------------------------
// Input lock handling
// -----------------------------

function lockTerminalInput(duration = 3000) {
    input.disabled = true;
    input.placeholder = "⚠ Terminal cooling down…";

    setTimeout(() => {
        input.disabled = false;
        input.placeholder = "";
        input.focus();
    }, duration);
}

// -----------------------------
// Local (client-side) commands
// -----------------------------

function handleLocalCommand(raw) {
    const parts = raw.trim().split(/\s+/);
    const cmd = parts[0].toLowerCase();

    switch (cmd) {
        case "clear":
        case "cls":
            output.innerHTML = "";
            return true;

        default:
            return false;
    }
}

// -----------------------------
// Key handling
// -----------------------------

input.addEventListener("keydown", async (e) => {
    if (e.key !== "Enter") return;
    if (input.disabled) return;

    const raw = input.value;
    if (!raw.trim()) return;

    // ---- Echo command ----
    const cmdLine = document.createElement("p");
    cmdLine.classList.add("command");
    cmdLine.innerHTML = renderAnsi(`$ ${normalizeAnsi(raw)}`);
    output.appendChild(cmdLine);

    input.value = "";

    // ---- Local commands ----
    if (handleLocalCommand(raw)) {
        terminal.scrollTop = terminal.scrollHeight;
        return;
    }

    // ---- Backend commands ----
    try {
        const res = await fetch("/api/command", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: raw })
        });

        const data = await res.json();

        const resultLine = document.createElement("p");
        resultLine.classList.add("result");
        resultLine.innerHTML = renderAnsi(normalizeAnsi(data.output));
        output.appendChild(resultLine);

        // ---- Handle backend-enforced lock ----
        if (data.lock_input) {
            lockTerminalInput(3000);
        }

    } catch (err) {
        const errorLine = document.createElement("p");
        errorLine.classList.add("result");
        errorLine.innerHTML = renderAnsi(
            "\x1b[31mERROR\x1b[0m Backend unreachable"
        );
        output.appendChild(errorLine);
    }

    terminal.scrollTop = terminal.scrollHeight;
});

// -----------------------------
// Initial focus
// -----------------------------

input.focus();
