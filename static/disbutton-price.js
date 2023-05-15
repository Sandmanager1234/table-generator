const button = document.getElementById('send')

var file = false
var txt = false

document.getElementById('finp').addEventListener('change', function(){
    if( this.value){
        check(true, txt);
        file = true;
      } else { 
        check(false, txt);
        file = false;
      }
})

document.getElementById('currency').addEventListener('change', function(){
  if( this.value) {
      check(file, true);
      txt = true;
    } else { 
      check(file, false);
      txt = false;
    }
})

function check(file, txt) {
  if (file && txt) {
    button.disabled = false;
  } else {
    button.disabled = true;
  }
}