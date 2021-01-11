function deletePatient(id) {
    event.preventDefault();
    fetch(`/eliminar/${id}/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
    })
    .then(response => () => {
        if (!response.ok) {
            throw Error(response.statusText + ' - ' + response.url);
        }
        return response.json();
    })
    .finally(() => {
        window.location.replace('/');
    })
    .catch((err) => {
        alert(`Error\n${err}`);
    });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
