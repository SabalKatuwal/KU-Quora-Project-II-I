if(window.location.pathname.match(/notification/)){
    console.log('hello')
    const notificationDivs = document.querySelectorAll('.notification');
    notificationDivs.forEach( notification => {
        notification.addEventListener('click',() => {
            // console.log('clicked')
            const data = {
                'notification_id' : notification.dataset.notification_id
            };
            const csrfToken = notification.querySelector('input[name="csrfmiddlewaretoken"]').value;
            const endpoint = notification.dataset.url;
            console.log(endpoint);

            fetch('/notification/notification_seen_status',{
                method : 'post',
                body : JSON.stringify(data),
                headers : {
                    "Content-Type":'application/json',
                    "X-CSRFToken":csrfToken
                }
            })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                window.location = endpoint;
            })
        })
    } )



}