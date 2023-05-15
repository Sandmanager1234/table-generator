const button = document.getElementById('send')

document.getElementById('finp').addEventListener('change', function(){
    if( this.value ){
        button.disabled = false;
      } else { 
        button.disabled = true;
      }
})

button.addEventListener('click', function(){
  let load = document.querySelector('.load');
  load.style.visibility = 'visible';
})