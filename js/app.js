const button = document.getElementById('myb');
// Add a click event listener to the button
button.addEventListener('click', function() {
    // Perform an action when the button is clicked
    const username = document.getElementById('usr').value;
    const pwd = document.getElementById('pwd').value;
    alert(username + pwd);

});