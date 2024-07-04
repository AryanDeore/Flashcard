document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("input[name='topic']").focus();

    // Social media button hover effect
    const fabContainer = document.querySelector('.fab-container');
    const fabOptions = document.querySelector('.fab-options');

    // Show options on mouseover and keep them visible for a while
    fabContainer.addEventListener('mouseover', function () {
        fabOptions.style.display = 'flex';
    });

    // Hide options after a delay on mouseout
    fabContainer.addEventListener('mouseout', function () {
        setTimeout(function () {
            fabOptions.style.display = 'none';
        }, 500); // Adjust delay as needed
    });

    // Ensure options stay visible when hovering over them
    fabOptions.addEventListener('mouseover', function () {
        fabOptions.style.display = 'flex';
    });

    // Hide options after a delay when mouse leaves the options
    fabOptions.addEventListener('mouseout', function () {
        setTimeout(function () {
            fabOptions.style.display = 'none';
        }, 100000); // Adjust delay as needed
    });
});