document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("input[name='topic']").focus();

    if (performance.navigation.type === 1) {
        // Page was reloaded
        document.querySelector("input[name='topic']").value = '';
        document.querySelector("input[name='domain']").value = '';
        document.getElementById('explanation-output').innerHTML = '';
    }
});