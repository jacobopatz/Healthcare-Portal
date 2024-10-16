function handleButtonClick(event) {
    window.location.href = event.target.id + '.html';
}
document.getElementById('menu-toggle').addEventListener('click', function() {
    var menu = document.getElementById('menu');
    menu.classList.toggle('menu-open');
});
document.getElementById('menu-exit').addEventListener('click', function() {
    var menu = document.getElementById('menu');
    menu.classList.toggle('menu-open');
});
document.getElementById("index").addEventListener('click',handleButtonClick);
