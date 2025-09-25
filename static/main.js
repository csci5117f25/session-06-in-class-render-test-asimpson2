const messages = {}

function Submit() {
    messages[document.getElementById("user").value] = document.getElementById("message").value;
}