const renderIcons = () => lucide.createIcons();

document.addEventListener('DOMContentLoaded', renderIcons);
document.addEventListener('htmx:afterSwap', renderIcons);
