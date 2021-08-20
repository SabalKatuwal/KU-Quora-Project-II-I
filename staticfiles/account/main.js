if(window.location.pathname == '/account/register/'){

    const form = document.querySelector('form');
    const password1 = form.querySelector('input[name = "password1"]');
    const password2 = form.querySelector('input[name = "password2"]');
    const username = form.querySelector('input[name = "username"]');
    const email = form.querySelector('input[name = "email"]');
    const submitBtn =form.querySelector('input[type="submit"]');
    
    form.addEventListener('submit',(e) => {
        e.preventDefault();
        checkInputs();
    }) 
    
     function checkInputs(){
        const usernameValue = username.value.trim();
        const emailValue = email.value.trim();
        const password1Value = password1.value.trim();
        const password2Value = password2.value.trim();

        if(usernameValue.length < 3){
            setErrorFor(username , 'Username is too short');
        }else{
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            let data = {
                'username' : username.value
            }
            fetch(username.parentElement.parentElement.getAttribute('data-url') , {
                method : 'post',
                body : JSON.stringify(data),
                headers : {
                    'Content-Type' : 'application/json',
                    'X-CSRFToken':csrfToken
                }
            }).then(res => res.json())
            .then(response => {
                if(response.taken){
                    setErrorFor(username , 'Username already used');
                }else{
                    setSuccess(username);
                }
                
                // Email validation 
                
                if(!isEmail(emailValue)){
                    setErrorFor(email , 'Email is invalid');
                }else{
                    
                    let data = {
                        'email' : email.value
                    }
                    fetch(email.parentElement.parentElement.getAttribute('data-url') , {
                        method : 'post',
                        body : JSON.stringify(data),
                        headers : {
                            'Content-Type' : 'application/json',
                            'X-CSRFToken':csrfToken
                        }
                    }).then(res => res.json())
                    .then(response => {
                        if(response.taken){
                            setErrorFor(email , 'Email already used');
                        }else{
                            setSuccess(email);
                        }
                        let strongPassword = new RegExp('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})')
                        let mediumPassword = new RegExp('((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))|((?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,}))')
                    
                        if(password1Value != password2Value){
                            setErrorFor(password2 , "password didn't match with previous");
                        }else{
                            setSuccess(password2);
                        }
                        if(!password1Value.match(strongPassword)){
                            setErrorFor(password1 , 'Password is not strong');
                        }else{
                            setSuccess(password1);
                        }

                    })
                }
            })

        }

        


        
        function setErrorFor(input , message){
            const field = input.parentElement.parentElement;
            field.querySelector('small').innerHTML = message;
            field.classList.remove('valid');
            field.classList.add('invalid');
        }
        function setSuccess(input){
            const field = input.parentElement.parentElement;
            field.classList.remove('invalid');
            field.classList.add('valid');
            let fields = form.querySelectorAll('.field');
            let valid = 0;
            fields.forEach(field => {
                if(field.classList.contains('valid')){
                    valid++;
                }
            })
            if(valid == 4){
                form.submit();
            }
        }
        function isEmail(email){
            return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
        }
        
    }
    
  



}

