function handleButtonClick(event) {
    window.location.href = event.target.id;
}
// Attach the click event listener to each button
document.querySelectorAll('.box').forEach(button => {
    button.addEventListener('click', handleButtonClick);
});