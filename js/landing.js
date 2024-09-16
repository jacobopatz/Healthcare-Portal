function handleButtonClick(event) {
    window.location.href = event.target.id + '.html';
}
document.getElementById("index").addEventListener('click',handleButtonClick);
// Attach the click event listener to each button
document.querySelectorAll('.box').forEach(button => {
    button.addEventListener('click', handleButtonClick);
});