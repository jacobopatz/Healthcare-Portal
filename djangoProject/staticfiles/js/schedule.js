document.addEventListener("DOMContentLoaded", () => {
    let startTime = null;

    const buttons = document.querySelectorAll(".appointment-time.available");
    const dateInput = document.getElementById("date");
    const endDateInput = document.getElementById("enddate");
    const form = document.getElementById("apt-form");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const dateValue = button.getAttribute("data-time");

            if (!startTime) {
                // First click: Set the start time
                startTime = dateValue;
                button.classList.add("selected");
            } else {
                // Second click: Set the end time and submit the form
                const endTime = dateValue;
                button.classList.add("selected");

                dateInput.value = startTime;
                endDateInput.value = endTime;

                form.submit();
            }
        });
    });
    
});

function openDiv(slotTime) {
    const SelectedDiv = document.getElementById(slotTime);
    SelectedDiv.style.display = "block";
}
function closeDiv(slotTime) {
    const SelectedDiv = document.getElementById(slotTime);
    SelectedDiv.style.display = "none";
}