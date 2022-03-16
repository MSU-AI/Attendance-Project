const img = document.getElementById("img")
const col1 = document.querySelector(".col-1")
const navBar = document.querySelector(".nav-list")
const circle1 = document.querySelector(".circle1")
const circle2 = document.querySelector(".circle2")
const circle3 = document.querySelector(".circle3")
const circle4 = document.querySelector(".circle4")
const triangle1 = document.querySelector(".triangle1")
const triangle2 = document.querySelector(".triangle2")
const circlewithoutborder = document.querySelector(".circlewithoutborder")

const tl = new TimelineMax()

tl.fromTo(img, 1.5, {transform: "translateX(-4rem)", opacity: "0"}, {transform: "translateX(0%)", opacity: '1'}).fromTo(col1, 1.5, {transform: "translateX(4rem)", opacity: "0"}, {transform: "translateX(0%)", opacity: '1'}, "-=1.5").fromTo(navBar, 1.5, {opacity: '0'}, {opacity: '1'}).fromTo(circle1,1.5,{opacity: '0'}, {opacity: '1'}).fromTo(circle2,1.5,{opacity: '0'}, {opacity: '1'},'-=1.5').fromTo(circle3,1.5,{opacity: '0'}, {opacity: '1'},'-=1.4').fromTo(circle4,1.5,{opacity: '0'}, {opacity: '1'},'-=2.3').fromTo(triangle1,1.5,{opacity: '0'}, {opacity: '1'},'-=1.6').fromTo(triangle2,1.5,{opacity: '0'}, {opacity: '1'},'-=1.0').fromTo(circlewithoutborder,1.5,{opacity: '0'}, {opacity: '1'},'-=1.2')

setTimeout(() => {$(document).ready(function(){
    animateDiv('.circle1');
    animateDiv('.circle2');
    animateDiv('.circle3');
    animateDiv('.circle4');
});

function makeNewPosition(){
    
    // Get viewport dimensions (remove the dimension of the div)
    var h = $(window).height() - 50;
    var w = $(window).width() - 50;
    
    var nh = Math.floor(Math.random() * h);
    var nw = Math.floor(Math.random() * w);
    
    return [nh,nw];    
    
}

function animateDiv(myclass){
    var newq = makeNewPosition();
    $(myclass).animate({ top: newq[0], left: newq[1] }, 4000,   function(){
      animateDiv(myclass);        
    });
    
};
}, 2000)