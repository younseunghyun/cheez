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
        $.post('/link-click', {
            post_id: $(this).parents('.post').data('postId')

        });

        $(this).parents('.post').data('linkClicked', true);
    });

    toastr.options = {
          "closeButton": false,
          "debug": false,
          "newestOnTop": false,
          "progressBar": false,
          "positionClass": "toast-bottom-center",
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "200",
          "hideDuration": "200",
          "timeOut": "1000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
      }

});


function initialize() {
    SWIPE_OFFSET = $(window).width() / 3;
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
        'is_liked': isLiked
    };

    if (isLiked) {
        toastr.success('좋아요 :)');
    } else {
        toastr.error('싫어요 :(');
    }

    for (var i in data) {
        if (data[i] === true) {
            data[i] = '1';
        } else if (data[i] === false) {
            data[i] = '0';
        }
    }

    $.post('/like', data, function(){
        

  });
}


function SendSNS(sns, title, url, image)
{
    var o;
    var _url = encodeURIComponent(url);
    var _title = encodeURIComponent(title);
    var _br  = encodeURIComponent('\r\n');
 
    switch(sns)
    {
        case 'facebook':
            o = {
                method:'popup',
                height:600,
                width:600,
                url:'http://www.facebook.com/sharer/sharer.php?u=' + _url
            };
            break;
 
        case 'twitter':
            o = {
                method:'popup',
                height:600,
                width:600,
                url:'http://twitter.com/intent/tweet?text=' + _title + '&url=' + _url
            };
            break;
        
        case 'google':
            o = {
                method:'popup',
                height:600,
                width:600,
                url:'https://plus.google.com/share?url={' + _url + '}'
            };
            break;
                    
        case 'naverband':
            o = {
                method:'web2app',
                param:'create/post?text=' + _title + _br + _url,
                a_store:'itms-apps://itunes.apple.com/app/id542613198?mt=8',
                g_store:'market://details?id=com.nhn.android.band',
                a_proto:'bandapp://',
                g_proto:'scheme=bandapp;package=com.nhn.android.band'
            };
            break;
 
        default:
            return false;
    }
 
    switch(o.method)
    {
        case 'popup':
            if( o.height > 0 && o.width > 0 ){
                window.open(o.url,'', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height='+o.height+',width='+o.width);
            }
            else{
                 window.open(o.url);
            }
         
          break;            
        
        case 'web2app':
          if(navigator.userAgent.match(/android/i)){
              setTimeout(function(){ location.href = 'intent://' + o.param + '#Intent;' + o.g_proto + ';end'}, 100);
          }
          else if(navigator.userAgent.match(/(iphone)|(ipod)|(ipad)/i)){
              setTimeout(function(){ location.href = o.a_store; }, 200);          
              setTimeout(function(){ location.href = o.a_proto + o.param }, 100);
          }
          else{
              alert('Only mobile');
          }
          break;
    }
}

