(function($) {
    var body = $('body'),
        menu = $('#menu'),
        topbar = $('#topbar'),
        isTouch = function () {

            // return !!('ontouchstart' in window) // works on most browsers
            //     || !!('onmsgesturechange' in window); // works on ie10
            return true;
        };

    menu.addClass('hasJs');

    topbar.on('click', function (event) {
        event.preventDefault();
        menu.toggleClass('present');
    });

    if(isTouch()) {
        body.on('swiperight', function (event) {
            menu.addClass('present');

        }).on('swipeleft', function (event) {
            if(menu.hasClass('present')) {
                menu.removeClass('present');
            } else {
                window.location.href = 'http://localhost:8000/';
            }
        });
    }

    // keyboard shortcuts
    // FIXME should be ajaxified
    body.on('keypress', function (event) {
        if ( event.which == 109 ) {         // [m]
            $('ul#status form.unread button').click();
        }
        else if ( event.which == 115 ) {    // [s]
            $('ul#status form.starred button').click();
        }
        else {
            console.log('key code: ' + event.which);
        }
    });
}(jQuery));
