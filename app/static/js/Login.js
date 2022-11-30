const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".container1");

signInBtn.addEventListener("click", () => {
	container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
	container.classList.add("right-panel-active");
});

$('.alert').fadeOut(5000);

const con=document.querySelector('.container1');
  let isIn=true;
  let isOut=false;
  
  
  var span;
  con.addEventListener('mouseenter',(e)=>{
    if(isIn){
    let inX=e.clientX-e.target.offsetLeft;
    let inY=e.clientY-e.target.offsetTop;
    let el=document.createElement('span');
    el.style.left=inX+'px';
    el.style.top=inY+'px';
    con.appendChild(el);
  
    $('.container1 span').removeClass('out');
    $('.container1 span').addClass('in');
    span=document.querySelector(".container1 span");
    isIn=false;
    isOut=true;
  
    }
  })
  con.addEventListener('mouseleave',(e)=>{
    if(isOut){
    let outX=e.clientX-e.target.offsetLeft;
    let outY=e.clientY-e.target.offsetTop;
    $('.container1 span').removeClass('in');
    $('.container1 span').addClass('out');
    $('.out').css("left",outX+'px');
    $('.out').css('left',outY+'px');
    isOut=false;
    setTimeout(()=>{
      con.removeChild(span);
      isIn=true;
    },500);
  }
  
  })
