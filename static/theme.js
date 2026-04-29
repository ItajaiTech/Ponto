function loadTheme() {
    const cookies = document.cookie.split(';');
    let theme = 'green'; // padrão
    let encontrou = false;

    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'theme') {
            theme = value;
            encontrou = true;
            break;
        }
    }

    // Se não houver tema salvo, salva green como padrão
    if (!encontrou) {
        document.cookie = "theme=green; path=/; max-age=31536000";
    }

    document.documentElement.setAttribute('data-theme', theme);

    const btn = document.querySelector('.theme-btn.' + theme);
    if (btn) {
        btn.classList.add('active');
    }
}

loadTheme();
