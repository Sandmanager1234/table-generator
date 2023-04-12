const button = document.getElementById('send')

document.getElementById('finp').addEventListener('change', function(){
    if( this.value ){
        button.disabled = false;
      } else { 
        button.disabled = true;
      }
})