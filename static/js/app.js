function toggleDebug(show) {
    document.querySelectorAll('.debug_text').forEach(el => {
        if (show) {
            el.classList.remove('hidden');
        } else {
            el.classList.add('hidden');
        }
    });
}

function setTerminalBg(hex) {
    document.documentElement.style.setProperty('--terminal-bg', hex);
}

