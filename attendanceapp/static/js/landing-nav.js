if (window.innerWidth < 600) {
    
    $(".navbar").css("display", "none");
    $(".nav-list").css("display", "none");


}
let togglebtn = document.querySelector('.toggle-btn')
        let navbar = document.querySelector('.navbar')
        let navlist = document.querySelector('.nav-list')

        togglebtn.addEventListener('click', ()=>{
            navbar.classList.toggle("show")
            navlist.classList.toggle("show")

        } )