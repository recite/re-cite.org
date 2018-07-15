var $backdrop = $('.backdrop');
var $textarea = $('textarea');
var $citations = $('#citations')

function handleInput() {
  var text = $textarea.val();
  $citations.val(text)
}

function handleScroll() {
  var scrollTop = $textarea.scrollTop();
  $backdrop.scrollTop(scrollTop);

  var scrollLeft = $textarea.scrollLeft();
  $backdrop.scrollLeft(scrollLeft);
}

function bindEvents() {
  $textarea.on({
    'input': handleInput,
    'scroll': handleScroll
  });
}

bindEvents();