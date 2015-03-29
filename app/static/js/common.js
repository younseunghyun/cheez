var SWIPE_OFFSET;

$(document).ready(function() {
    initialize();


    $(document).on('mousedown', '.post', function(e){
        onDragStart(e, $(this));
    });
    $(document).on('mousemove', '.post', function(e){
        onDrag(e, $(this));
    });
    $(document).on('mouseup', '.post', function(e){
        onDragEnd(e, $(this));
    });

});


function initialize() {
    SWIPE_OFFSET = $(window).width() / 2;
    loadPosts();   
}

function loadPosts() {
    $.get('/posts', function(response) {
        $('body').prepend(response);
    });   
}


function onDragStart(event, $target) {
    $target.data('mouseDown', true);
    $target.data('initX', event.pageX);
}

function onDragEnd(event, $target) {
    $target.data('mouseDown', false);

    var dx = event.pageX - $target.data('initX');
    var moveDistance = Math.abs(dx);
    if (moveDistance < SWIPE_OFFSET) {
        $target.animate({left:0}, 'fast');
    } else {
        if (dx > 0) {
            $target.animate({left:'100%'}, 'fast', function() {
                $target.remove();
            });

            // do like


        } else {
            $target.animate({left:'-100%'}, 'fast', function() {
                $target.remove();
            });

            // do hate
        }


        if ($('.post').length < 5) {
            loadPosts();
        }

    }
}

function onDrag(event, $target) {
    if ($target.data('mouseDown')) {
        var dx = event.pageX - $target.data('initX');
        $target.css('left', dx);
    }
}

function like(postId) {

}

function hate(postId) {
    
}


