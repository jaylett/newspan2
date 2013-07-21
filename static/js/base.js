(function($) {
    var body = $('body'),
        menu = $('#menu'),
        topbar = $('#topbar'),
        isTouch = function () {
          return !!('ontouchstart' in window) // works on most browsers
              || !!('onmsgesturechange' in window); // works on ie10
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
            menu.removeClass('present');
        });
    }
}(jQuery));
