document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('explain-form');
    const spinner = document.getElementById('spinner');
    const explanationSection = document.getElementById('explanation-section');
    const explanationOutput = document.getElementById('explanation-output');
    const imageSection = document.getElementById('image-section');
    const generatedImage = document.getElementById('generated-image');

    document.querySelector("input[name='topic']").focus();

    if (performance.navigation.type === 1) {
        // Page was reloaded
        window.location.href = '/refresh';
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const topic = document.querySelector("input[name='topic']").value;
        const domain = document.querySelector("input[name='domain']").value;
        const level = document.querySelector("button[type='submit']:focus").value;

        spinner.style.visibility = 'visible';
        explanationSection.style.display = 'none';
        imageSection.style.display = 'none';

        // Generate explanation
        fetch('/generate_explanation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, domain: domain, level: level }),
        })
            .then(response => response.json())
            .then(data => {
                explanationOutput.innerHTML = data.explanation;
                explanationSection.style.display = 'block';
                spinner.style.visibility = 'hidden';
            })
            .catch((error) => {
                console.error('Error:', error);
                spinner.style.visibility = 'hidden';
            });

        // Generate image
        fetch('/generate_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic, domain: domain, level: level }),
        })
            .then(response => response.json())
            .then(data => {
                generatedImage.src = data.image_url;
                imageSection.style.display = 'block';
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});