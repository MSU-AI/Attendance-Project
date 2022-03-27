let togglebtn = document.querySelector('.toggle-btn')
        let navbar = document.querySelector('.navbar')

        togglebtn.addEventListener('click', ()=>{
            navbar.classList.toggle('mobile-nav')
        } )