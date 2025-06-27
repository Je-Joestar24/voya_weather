export function showAppMessage(message, status) {
    const messageEl = document.getElementById('app__message');

    const classesToRemove = ['app__message', 'success', 'error', 'info'];

    classesToRemove.forEach(cls => {
        messageEl.classList.remove(cls);
    });

    messageEl.textContent = message;

    setTimeout(() => {
        messageEl.classList.add('app__message');
        if (status) {
            messageEl.classList.add(status);
        }
    }, 100); 
}
