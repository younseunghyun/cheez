$(document).ready(function() {
    initialize();
});


function initialize() {
    var $contentWrap = $('.content-wrap');
    var contentHeight = $contentWrap.height();
    $contentWrap.css('margin-top', -contentHeight/2);

    $(document).on('swipe', function(){
        location.reload();
    });
}