if (window.innerWidth < 600) {
    
    $(".navbar").css("display", "none");

}
let togglebtn = document.querySelector('.toggle-btn')
        let navbar = document.querySelector('.navbar')

        togglebtn.addEventListener('click', ()=>{
            navbar.classList.toggle("show")
        } )