

var $table = $('#table')

$(function () {
  $table.bootstrapTable()
})

var passwordCheck = (val)=>{
  let psc = val;
  let ps = document.getElementById('password').value;
  let lb = document.getElementById('password_confirm');
  if(psc !== ps){
    lb.innerHTML = 'Password Mismatch!';
    lb.className = 'btn btn-danger btn-block'
  }else{
    lb.innerHTML = '';
    lb.className = ''
  }
}

$(document).ready(function () {
  $("#sidebar").mCustomScrollbar({
    theme: "minimal"
  });

  $('#dismiss, .overlay').on('click', function () {
    // hide sidebar
    $('#sidebar').removeClass('active');
    // hide overlay
    $('.overlay').removeClass('active');
  });

  $('#sidebarCollapse').on('click', function () {
    // open sidebar
    $('#sidebar').addClass('active');
    // fade in the overlay
    $('.overlay').addClass('active');
    $('.collapse.in').toggleClass('in');
    $('a[aria-expanded=true]').attr('aria-expanded', 'false');
  });
  
});

//.toast('show');

$('#file').change(function(event){
  let path = URL.createObjectURL(event.target.files[0]);
  $('#file-img').attr('src', path);
  $('#img_path').attr('value', path);
})