if(window.location.pathname == '/'){
    addQuestion = document.querySelector('.add-question');
    triggerArrow = document.querySelector('.addQuestion-container i.fa-angle-double-down');

    addQuestionForm = document.querySelector('.add-question-form');
    form = document.querySelector('.add-question-form form');
    
    triggerArrow.addEventListener('click',formApperance)
    addQuestion.addEventListener('click',formApperance)


    function formApperance(){
        if(addQuestionForm.dataset.status == 'collapsed'){
            addQuestionForm.dataset.status = 'expanded';
            addQuestionForm.style.height = addQuestionForm.scrollHeight + 'px';
            // addQuestionForm.style.transform = 'scaleY(1)';
            triggerArrow.classList.remove('animate-direction-down');
            triggerArrow.classList.add('animate-direction-up');
                // form.style.opacity = '1';
            
            }
            else{
                addQuestionForm.dataset.status = 'collapsed';
                addQuestionForm.style.height = '0px';
                // triggerArrow.style.transform = 'rotate(0deg)';
                triggerArrow.classList.remove('animate-direction-up');
                triggerArrow.classList.add('animate-direction-down');

            }
    }    
    
    function previewImage(){
        
        let files = document.querySelector("input[type='file']").files;
        let previewImageContainer = document.querySelector('.previewImageContainer');
        function readAndPreview(file){
    
            let reader = new FileReader();
    
            reader.addEventListener('load',function(){
                let image = new Image()
                image.src = this.result;
                previewImageContainer.appendChild(image);
            })
            reader.readAsDataURL(file);
        }
    
        // files.forEach(file,()=>{
        //     // readAndPreview(file);
        //     console.log(file)
        // });
        previewImageContainer.innerHTML = '';
    
        [].forEach.call(files,readAndPreview);
    
    }

    addQuestionForm.addEventListener('submit',() => {
        event.preventDefault();
        const tags = addQuestionForm.querySelector('input[name="tags"]');
        const tagsData= tags.value;
        tag = tagsData.split(' ').join('');
        console.log(tag);
        tagsValue = tag.split('#').join('#');
        tagsArray = tagsValue.split('');
        if(tagsArray[0] === '#'){
           tagsArray.shift();
        }
        tags.value = tagsArray.join('');
        console.log(tags.value)
        event.target.submit();

    })

}