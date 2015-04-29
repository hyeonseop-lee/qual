$('.prob-btn.not-solved').mouseenter(function() {
  $(this).removeClass('btn-default').addClass('btn-primary');
});
$('.prob-btn.not-solved').mouseleave(function() {
  $(this).removeClass('btn-primary').addClass('btn-default');
});
$('.prob-btn.solved').mouseenter(function() {
  $(this).removeClass('btn-success').addClass('btn-primary');
});
$('.prob-btn.solved').mouseleave(function() {
  $(this).removeClass('btn-primary').addClass('btn-success');
});
