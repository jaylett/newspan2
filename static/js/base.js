(function($) {
    var body = $('body'),
        menu = $('#menu'),
        topbar = $('#topbar');

    menu.addClass('hasJs');

    topbar.on('click', function (event) {
        event.preventDefault();
        menu.toggleClass('present');
    });




    body.on('swiperight', function (event) {
        menu.addClass('present');
    }).on('swipeleft', function (event) {
        menu.removeClass('present');
    });
}(jQuery));
