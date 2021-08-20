if(window.location.pathname.match(/PostEdit/)){

    const editPostForm = document.querySelector('#edit_post_form');
    const images = editPostForm.querySelectorAll('.images .image');
    const addImage = editPostForm.querySelector('.field input[type="file"]');

    images.forEach(image => {
        image.addEventListener('click',() => {
            const clickedItem = event.target;
            if(clickedItem.classList.contains('fa-times')){
                event.target.parentElement.classList.add('removed');
                const imageId = image.getAttribute('data-imageId');
                csrfToken = document.querySelectorAll('input[name="csrfmiddlewaretoken"]')[0].value;
                
                data = {
                    'imageId':imageId
                }
                fetch('/deletePostImage/',{
                    method : 'post',
                    body : JSON.stringify(data),
                    headers : {
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : csrfToken
                    }
                })
                .then(res =>  res.json())
                .then(data => {
                   console.log(data);
                })
            }            
        })
    })

    // addImage.addEventListener('click',() => {
        
    // })
    function previewImagePostEdit(){
        let files = editPostForm.querySelector("input[type='file']").files;
        let imagePreviewArea = editPostForm.querySelector('.images .recently-added-images');
        
        // images.forEach(image => {
        //     if(image.getAttribute('data-imageId')){
        //         console.log(image)
        //     }else{
        //         imagePreviewArea.removeChild(image);
        //     }
        // })
        imagePreviewArea.innerHTML = "";
        function readAndPreview(file){
    
            let reader = new FileReader();
    
            reader.addEventListener('load',function(){
                // let image = new Image()
                // image.src = this.result;
                // previewImageContainer.appendChild(image);
                div = document.createElement('div');
                div.classList.add('image');
                img = document.createElement('img');
                img.src = this.result;
                i = document.createElement('i');
                i.classList.add('fas','fa-times');
                div.append(img);
                div.append(i);
                imagePreviewArea.append(div);

                i.addEventListener('click',() => {
                    event.target.parentElement.classList.add('removed');
                })
            })
            reader.readAsDataURL(file);
        }
        
        
        [].forEach.call(files,readAndPreview);
    }

    editPostForm.addEventListener('submit',() => {
        event.preventDefault();
        const tags = editPostForm.querySelector('input[name="tags"]');
        const tagsData= tags.value;
        tag = tagsData.split(' ').join('');
        console.log(tag);
        // tagsValue = tag.split('#').join('#');
        // console.log(tagsValue)
        tagsArray = tag.split('');
        console.log(tagsArray);
        tagsArray.shift();
        tags.value = tagsArray.join('');
        console.log(tags.value)
        event.target.submit();
    })





}