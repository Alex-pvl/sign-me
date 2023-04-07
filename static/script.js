const form = document.querySelector('form');
const response = document.querySelector('#response');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
        // Успешная авторизация, делаем запрос на /flag
        const flagResponse = await fetch('/flag', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const flagData = await flagResponse.json();
        const flagValue = flagData.flag;

        document.getElementById('flag-text').textContent = flagValue;
        document.getElementById('flag').style.display = 'block';
    } else {
        // Ошибка авторизации, выводим сообщение об ошибке
        alert('You are not admin.')
    }
});