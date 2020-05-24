$(document).ready(function(){
  const csrfToken = $('meta[name="csrf-token"]').prop('content')

  $('#title-save-modal').on('click', function(){
    alert($('#title-value-modal').val())
  })
})