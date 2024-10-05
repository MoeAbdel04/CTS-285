function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
}

document.addEventListener('DOMContentLoaded', (event) => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    const themeSelect = document.getElementById('theme');
    if (themeSelect) {
        themeSelect.value = savedTheme;
        themeSelect.onchange = (event) => {
            const selectedTheme = event.target.value;
            setTheme(selectedTheme);
            localStorage.setItem('theme', selectedTheme);
        };
    }
});