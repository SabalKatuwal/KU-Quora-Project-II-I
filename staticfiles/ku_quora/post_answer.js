if(window.location.pathname.match(/post/)){
   
    const allAnswers = document.querySelector('.all-answers');
    const postAnswerForm = document.querySelector('.answersForm');
    const AnswerImages = postAnswerForm.querySelector('input[type="file"]');
    const answer = postAnswerForm.querySelector('textarea');
    const post_id = postAnswerForm.querySelector('input.post_id').value;
    let previewImageContainer = postAnswerForm.querySelector('.previewImageContainer');

    function previewImage(){    
        console.log('inside')
        let files = postAnswerForm.querySelector("input[type='file']").files;
        console.log(files)

        function readAndPreview(file){

            let reader = new FileReader();

            reader.addEventListener('load',function(){
                let image = new Image()
                image.src = this.result;
                previewImageContainer.appendChild(image);
            })
            
            reader.readAsDataURL(file);
        }

        previewImageContainer.innerHTML = '';

        [].forEach.call(files,readAndPreview);

      }

        const answers = document.querySelectorAll('.answer-container');
        answers.forEach(answer=>{
            // const expandBtn = answer.querySelector('.expand span');
            try{
                const options = answer.querySelector('.options');
                const optionsBtn = answer.querySelector('.options > div');
                
                const ul = options.querySelector('ul');
                optionsBtn.addEventListener('click',()=>{
                    if(ul.dataset.status == 'expanded'){
                        ul.dataset.status = 'collapsed';
                        ul.style.visibility = 'hidden';         
                    }else{
                        ul.dataset.status = 'expanded';
                    ul.style.visibility = 'visible';         
                    }
                })
            }catch(err) {
                console.log(err)
            }
            // like in answer
            const upVoteBtn = answer.querySelector('div.upVote');
            const upVoteIcon = upVoteBtn.querySelector('i');
            const answerId = upVoteBtn.getAttribute("data-answerId");
            const csrfToken = upVoteBtn.querySelector('input[name = "csrfmiddlewaretoken" ').value;
            const upVoteCount = upVoteBtn.querySelector('span.count');
            console.log('answerId = ',answerId);
            upVoteBtn.addEventListener('click',() => {
                let data = {
                    'answerId' : answerId
                }
                let endpoint = '/post/upVote';
                fetch(endpoint,{
                    method : "post",
                    body : JSON.stringify(data),
                    headers : {
                        'Content-Type' : 'application/json',
                        'X-CSRFToken' : csrfToken
                    }
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    let newUpVoteCount = data.upVoteCount;
                    upVoteCount.innerHTML = " ";
                    upVoteCount.innerHTML = newUpVoteCount;
                    if(data.upVoted){
                        // if(!upVoteIcon.classList.contains('upVoted')){
                            upVoteIcon.classList.add('upVoted')
                        // }
                    }else{
                        upVoteIcon.classList.remove('upVoted')
                    }
                } )


            })

        })
        





    postAnswerForm.addEventListener('submit',()=>{
        event.preventDefault();
        
        const endpoint = "/addAnswer/";
        const csrf = postAnswerForm.querySelector('input[name = "csrfmiddlewaretoken"').value;
    
        const formData = new FormData();
        let i = 0;
        for(const file of AnswerImages.files){
            formData.append(`image${++i}`,file);
        }
        formData.append('post_id',post_id);
        formData.append('answer',answer.value);
        
        fetch(endpoint , {
            method : 'post',
            body : formData,
            headers:{
                'X-CSRFToken':csrf
            }
        })
        .then(res => res.json())
        .then(data => {
            location.reload();
        })

     
    })

    const post_comment_form = allAnswers.querySelectorAll('#post_comment_form');


    post_comment_form.forEach(form => {
        const formTrigger = form.querySelector('input.trigger');
        const commentWritingArea = formTrigger.nextElementSibling;

        formTrigger.addEventListener('click',() => {
            event.target.style.display = "none";
            commentWritingArea.style.display = 'flex';
            commentWritingArea.children[0].focus();
        })

    })



}