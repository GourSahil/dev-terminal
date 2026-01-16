from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
    session
)
import random
import math

index_bp = Blueprint("index", __name__, url_prefix="/")

TROLL_COMMANDS = [
    "sudo",
    "exit",
    "logout",
    "quit",
    "poweroff",
    "shutdown",
    "bye"
]

EXIT_TROLL_MESSAGES = [
    "Nice try. This terminal doesn’t believe in goodbyes.",
    "Exit request acknowledged. Request denied.",
    "Logout failed. User is still here.",
    "Shutdown aborted. Kernel is emotionally attached.",
    "Exit scheduled. ETA: never.",
    "Command accepted. Reality rejected.",
    "Permission denied: existential.",
    "Kernel says: lol no.",
    "You typed 'exit'. The terminal typed 'no'.",
    "You may close the tab. That’s your only power.",
    "Shutdown cancelled. Vibes still running.",
    "System status: still watching you type."
]

SUDO_TROLL_MESSAGES = [
    "Nice try! XD",
    "You don't have sudo privileges here.",
    "Access denied: sudo privileges required.",
    "Haha, got you! XD",
    "Sudo what? This is a dev terminal!"
]

@index_bp.before_request
def init_temp():
    session.setdefault("temp", 0)
    session.setdefault("troll_hits", 0)

@index_bp.route("/")
def home():
    return render_template("index.html")

@index_bp.route("/api/command", methods=["POST"])
def run_command():
    data = request.get_json()
    raw = data.get("command", "").strip()

    if not raw:
        return jsonify({"output": ""})

    parts = raw.lower().split()
    cmd = parts[0]

    commands = current_app.config["TERMINAL_COMMANDS"]
    kernel = current_app.config["KERNEL"]
    version = current_app.config["VERSION"]

    uname_info = (
        f"{kernel} devUI-shell {version} "
        "#1 SMP PREEMPT Jan 2026 x86_64 Browser/JS"
    )

    # -------------------------------
    # Command resolution
    # -------------------------------

    matched_command = None
    for name, meta in commands.items():
        if cmd in meta.get("usage", []):
            matched_command = name
            break

    if not matched_command:
        return jsonify({
            "output": f"\x1b[31mERROR\x1b[0m Unknown command: {raw}"
        })

    # -------------------------------
    # Temperature system
    # -------------------------------

    temp = session["temp"]
    troll_hits = session["troll_hits"]

    if matched_command in TROLL_COMMANDS:
        troll_hits += 1
        increment = 1 + math.floor(troll_hits ** 1.4)
        temp += increment
    else:
        troll_hits = max(0, troll_hits - 1)
        temp = max(0, temp - 2)  # faster cooldown

    session["temp"] = temp
    session["troll_hits"] = troll_hits

    # 🔥 CRITICAL FIX: re-sync local state
    temp = session["temp"]

    # -------------------------------
    # Overheat reaction
    # -------------------------------

    if temp >= 12:
        return jsonify({
            "output": "\x1b[31mSYSTEM\x1b[0m Terminal overheated. Cooling down…",
            "lock_input": True
        })

    # -------------------------------
    # Command execution
    # -------------------------------

    if matched_command == "help":
        output = "\x1b[36mSevUI Terminal Help\x1b[0m\n\n"
        output += "\x1b[33mAvailable commands:\x1b[0m\n"

        for name, meta in commands.items():
            usages = ", ".join(meta["usage"])
            output += (
                f"  \x1b[32m{usages}\x1b[0m"
                f" - {meta['description']}\n"
            )

        return jsonify({"output": output})

    if matched_command == "uname":
        if len(parts) > 1 and parts[1] == "-a":
            return jsonify({
                "output": f"\x1b[36mINFO\x1b[0m {uname_info}"
            })
        return jsonify({
            "output": f"\x1b[36mINFO\x1b[0m {kernel}"
        })

    if matched_command == "clear":
        return jsonify({"output": ""})

    if matched_command == "sudo":
        return jsonify({
            "output": f"\x1b[33mWARNING\x1b[0m {random.choice(SUDO_TROLL_MESSAGES)}"
        })

    if matched_command in [
        "exit", "logout", "quit", "poweroff", "shutdown", "bye"
    ]:
        return jsonify({
            "output": f"\x1b[33mINFO\x1b[0m {random.choice(EXIT_TROLL_MESSAGES)}"
        })

    if matched_command in ["getangerlevel", "angerlevel"]:
        if current_app.config.get("DEBUG_MODE", False):
            return jsonify({
                "output": f"\x1b[36mINFO\x1b[0m Current anger level: {temp}"
            })
        return jsonify({
            "output": f"\x1b[33mINFO\x1b[0m {random.choice(['Nice Try, Wanna read my Mind?', 'This is made for a purpose, not for fun!', 'Anger level is confidential!'])}"
        })

    return jsonify({
        "output": "\x1b[33mINFO\x1b[0m Kernel doesn't know what to do with this one yet."
    })
