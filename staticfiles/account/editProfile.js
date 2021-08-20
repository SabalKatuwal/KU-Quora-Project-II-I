if(window.location.pathname.match('/editProfile/')){
    
    function previewProfileChange(){
        const form = document.querySelector('form#edit_profile_form');
        const profile_pic = form.querySelector('.profile_pic img');
        const profile_pic_input = form.querySelector('.profile_pic input');
        let files = profile_pic_input.files;
        
        let reader = new FileReader();

        reader.onload = function(){
            profile_pic.src = this.result;
        }

        reader.readAsDataURL(files[0]);

        
    }



}