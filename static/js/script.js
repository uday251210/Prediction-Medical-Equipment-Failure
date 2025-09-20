document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll("input");

    // Add focus effect for all input fields
    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.style.borderColor = "#007bff";
            input.style.boxShadow = "0 0 5px rgba(0,123,255,0.5)";
        });
        input.addEventListener("blur", () => {
            input.style.borderColor = "#ccc";
            input.style.boxShadow = "none";
        });
    });

    // Form validation only if form exists on the page
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(e) {
            let empty = false;
            inputs.forEach(input => {
                if (input.hasAttribute("required") && !input.value.trim()) {
                    empty = true;
                }
            });
            if (empty) {
                e.preventDefault();
                alert("Please fill all required fields before submitting!");
            }
        });
    }
});
