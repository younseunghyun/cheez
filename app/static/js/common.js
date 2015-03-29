var SWIPE_OFFSET;

$(document).ready(function() {
    initialize();


    $(document).on('touchstart', '.post', function(e){
        onDragStart(e, $(this));
    });
    $(document).on('touchmove', '.post', function(e){
        onDrag(e, $(this));
    });
    $(document).on('touchend', '.post', function(e){
        onDragEnd(e, $(this));
    });
    $(document).on('touchcancel', '.post', function(e){
        onDragEnd(e, $(this));
    });
    
    $(document).on('click', 'a.btn', function(){
        $(this).parents('.post').data('linkClicked', true);
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
    $target.data('initX', event.originalEvent.touches[0].screenX);
}

function onDragEnd(event, $target) {
    $target.data('mouseDown', false);

    var dx = parseInt($target.css('left')) - $target.data('initX');
    var moveDistance = Math.abs(dx);
    if (moveDistance < SWIPE_OFFSET) {
        $target.animate({left:0}, 'fast');
        $('.post:nth-child(2)').animate({opacity:0}, 'fast');
    } else {
        if (dx > 0) {
            $target.animate({left:'100%'}, 'fast', function() {
                $target.remove();
            });

            // do like
            like($target, true);

        } else {
            $target.animate({left:'-100%'}, 'fast', function() {
                $target.remove();
            });

            // do hate
            like($target, false);
        }
        $('.post:nth-child(2)').animate({opacity:1}, 'fast');


        if ($('.post').length < 5) {
            loadPosts();
        }

    }
}

function onDrag(event, $target) {
    if ($target.data('mouseDown')) {
        var dx = event.originalEvent.touches[0].screenX - $target.data('initX');
        $target.css('left', dx);
        $('.post:nth-child(2)').css('opacity',Math.abs(dx) / $(window).width());
    }
}

function like($target, isLiked) {
    var data = {
        'post_id': $target.data('postId'),
        'is_liked': isLiked,
        'link_clicked': $target.data('linkClicked')|false
    };

    for (var i in data) {
        if (data[i] === true) {
            data[i] = '1';
        } else if (data[i] === false) {
            data[i] = '0';
        }
    }

    $.post('/like', data);
}

