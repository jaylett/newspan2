(function($) {
    var body = $('body'),
        offcanvas = $('#offcanvas');

    body.on('swiperight', function (event) {
        offcanvas.addClass('present');
    }).on('swipeleft', function (event) {
        offcanvas.removeClass('present');
    });

}(jQuery));
