console.log("GetHired Loaded Successfully");

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("form[action*='/analyze']").forEach(function (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector("button[type='submit']");
            if (!button) return;

            button.disabled = true;
            button.textContent = "Running...";
        });
    });
});
