// static/js/hide_messages.js
setTimeout(function() {
    var messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        message.style.display = 'none';
    });
}, 3000);
