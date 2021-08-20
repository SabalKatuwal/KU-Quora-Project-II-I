if(window.location.pathname.match('/account/followings/')){
    const container = document.querySelector('.Follow-container');
    const filter = document.querySelector('.filter');
    const followingBtn = container.querySelector('.followings_count');
    const followerBtn = container.querySelector('.followers_count');
    const followingList = filter.querySelector('.following');
    const followerList = filter.querySelector('.follower');
    const usersList = filter.querySelectorAll('div.user');

    const body = document.querySelector('body');
    body.style.backgroundColor = "white";

    usersList.forEach(user => {
        user.addEventListener('click',()=>{
            console.log(user.getAttribute('data-url'));
            window.location = user.getAttribute('data-url');
        })
    })







    followingBtn.addEventListener('click',() => {
        followingBtn.classList.add('active');
        followerBtn.classList.remove('active');
        followingList.classList.add('active');
        followerList.classList.remove('active');
    })
    followerBtn.addEventListener('click',() => {
        followingBtn.classList.remove('active');
        followerBtn.classList.add('active');
        followingList.classList.remove('active');
        followerList.classList.add('active');
    })

}