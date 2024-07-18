document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('explain-form');
    const spinner = document.getElementById('spinner');

    document.querySelector("input[name='topic']").focus();

    if (performance.navigation.type === 1) {
        // Page was reloaded
        window.location.href = '/refresh';
    }

    form.addEventListener('submit', function (event) {
        spinner.style.visibility = 'visible';
    });

    // Hide spinner when page is fully loaded
    window.addEventListener('load', function () {
        spinner.style.visibility = 'hidden';
    });
});