document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("input[name='topic']").focus();

    // Social media button hover effect
    const fabContainer = document.querySelector('.fab-container');
    const fabOptions = document.querySelector('.fab-options');

    fabContainer.addEventListener('mouseover', function () {
        fabOptions.style.display = 'flex';
    });

    fabContainer.addEventListener('mouseout', function () {
        fabOptions.style.display = 'none';
    });

    fabOptions.addEventListener('mouseover', function () {
        fabOptions.style.display = 'flex';
    });

    fabOptions.addEventListener('mouseout', function () {
        fabOptions.style.display = 'none';
    });
});