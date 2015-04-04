var SWIPE_OFFSET;
var BASE_URL = "http://cheez.co";

$(document).ready(function() {
    initialize();


    $(document).on('touchstart', 'body', function(e){

        onDragStart(e, $('.post:first-child'));
    });
    $(document).on('touchmove', 'body', function(e){
        onDrag(e, $('.post:first-child'));
    });
    $(document).on('touchend', 'body', function(e){
        onDragEnd(e, $('.post:first-child'));
    });
    $(document).on('touchcancel', 'body', function(e){
        onDragEnd(e, $('.post:first-child'));
    });
    
    $(document).on('click', 'a.btn', function(){
        var postId = $(this).parents('.post').data('postId');
        
        document.cookie = 'clicked='+postId;
        document.cookie = 'original='+location.href.split('/').splice(-1)[0];


        $.post('/link-click', {
            post_id: postId
        });
    });
    $(document).on('click','#btn-share-kakao',function(){
        var data = {
            'post_id': $('.post:first-child').data('postId'),
            'sns': 'kakao',
        };


        $.post('/sns_log', data, function(){

        });

    });

    toastr.options = {
      "closeButton": false,
      "debug": false,
      "newestOnTop": true,
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
    Kakao.init('eb29042a172000d9a50826b3d1fe7dca');
    $.nonbounce();
    document.cookie = 'clicked=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    document.cookie = 'original=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function loadPosts() {
    $.get('/posts', function(response) {
        $('#contents').append(response);
        setKakaoShareButton();
    });   
}


function onDragStart(event, $target) {
    $target.data('mouseDown', true);
    $target.data('initX', event.originalEvent.touches[0].screenX);
}

function onDragEnd(event, $target) {
    $target.data('mouseDown', false);

    var dx = parseInt($target.css('left'));
    var moveDistance = Math.abs(dx);
    if (moveDistance < SWIPE_OFFSET) {
        $target.animate({left:0}, 'fast');
        $('.post:nth-child(2)').animate({opacity:0}, 'fast');
    } else {
        if (dx > 0) {
            $target.animate({left:'100%'}, 'fast', function() {
                $target.remove();
                setKakaoShareButton();
            });

            // do like
            like($target, true);

        } else if (dx < 0) {
            $target.animate({left:'-100%'}, 'fast', function() {
                $target.remove();
                setKakaoShareButton();
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


function SendSNS(sns)
{
    var url = BASE_URL + '/' + $('.post:first-child').data('postId')
    var title = $('.contents:first').text().trim();
    title = title.substring(0, title.length - 4);
    var o;
    var _url = encodeURIComponent(url);
    var _title = encodeURIComponent(title);
    var _br  = encodeURIComponent('\r\n');

    console.log(_url);
    var data = {
        'post_id': $('.post:first-child').data('postId'),
        'sns': sns,
    };

    
    $.post('/sns_log', data, function(){

    });

    


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

function setKakaoShareButton() {
    $('#share-kakao').html('<img id="btn-share-kakao" src="/static/res/img/kakaotalk.png" width="30" height="30" alt="">');
    var title = $('.contents:first').text().trim();
    title = title.substring(0, title.length - 4);
    Kakao.Link.createTalkLinkButton({
      container: '#btn-share-kakao',
      label: title,
      image: {
        src: $('.post:first-child').css('background-image').replace('url(','').replace(')',''),
        width: 100,
        height: 100
    },
    webButton: {
        text: 'Cheez에서 보기',
        url: BASE_URL + '/' + $('.post:first-child').data('postId')
    }
});

}


$(function() {

    function updateLog(x, y) {
        var data = {
            'post_id': $('.post:first').data('postId'),
            'x': x,
            'y': y
        };


        $.post('/touch_log', data, function(){

        });

    }

    document.addEventListener('touchstart', function(e) {
        updateLog(e.changedTouches[0].pageX, e.changedTouches[0].pageY);
    }, false);

    document.addEventListener('touchmove', function(e) {
        e.preventDefault();
        updateLog(e.targetTouches[0].pageX, e.targetTouches[0].pageY);
    }, false);
});