(function($) {
    var body = $('body'),
        menu = $('#menu'),
        topbar = $('#topbar'),
        isTouch = function () {

            // return !!('ontouchstart' in window) // works on most browsers
            //     || !!('onmsgesturechange' in window); // works on ie10
            return true;
        },
        // using jQuery
        getCookie = function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        csrfSafeMethod = function (method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        sameOrigin = function (url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        },
        csrftoken = getCookie('csrftoken'),
        unreadField = $('ul#status form.unread input[name="read"]'),
        starredField = $('ul#status form.starred input[name="starred"]'),
        unreadButton = $('ul#status form.unread button'),
        starredButton = $('ul#status form.starred button'),
        nextArticle = $('form.goto'),
        nextLink = window.location.protocol + '//' + window.location.host + nextArticle.attr('action'),
        toggleUnread = function () {
            $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            $.ajax({
                type: 'POST',
                data: {
                    read: unreadField.val()
                },
                success: function (message) {

                    if(unreadField.val() == "true") {
                        unreadField.val("false");
                    } else {
                        unreadField.val("true");
                    }
                    // unreadField.val( !unreadField.val() );
                    console.log( unreadField.val() );

                    var disc = (unreadField.val()=="true")?'●':'○';
                    unreadButton.text(disc);

                }
            });
        },
        toggleStarred = function() {
            $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            $.ajax({
                type: 'POST',
                data: {
                    starred: starredField.val()
                },
                success: function (message) {

                    if(starredField.val() == "true") {
                        starredField.val("false");
                    } else {
                        starredField.val("true");
                    }
                    // starredField.val( !starredField.val() );
                    console.log( starredField.val() );

                    var star = (starredField.val()=="true")?'☆':'★';
                    starredButton.text(star);

                }
            });
        },
        gotoAndMarkUnread = function (target) {
            var target = target || null;
            nextArticle.submit();
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
                // console.log('this is called');
                gotoAndMarkUnread();
                // window.location.href = nextLink;
            }
        });
    }

    // keyboard shortcuts
    // FIXME should be ajaxified
    body.on('keypress', function (event) {
        if ( event.which == 104 ) {         // [h]
            $('a[rel=top]').get(0).click();
        }
        else if ( event.which == 109 ) {    // [m]
            // $('ul#status form.unread button').click();

            toggleUnread();
        }
        else if ( event.which == 115 ) {    // [s]
            // $('ul#status form.starred button').click();
            toggleStarred();
        }
        else if ( event.which == 110 ) {    // [n]
            // $('ul#status form.starred button').click();
            gotoAndMarkUnread();
        }

        else if ( event.which == 117 ) {     // [u]
            $('a[rel=parent]').get(0).click();
        }
        else if ( event.which == 65 ) {     // shift+[a]
            $('ul#status form.read-all button').click();
        }
        else if ( event.which == 85 ) {     // shift+[u]
            $('ul#status form.unread-all button').click();
        }
        else if ( event.which == 49 ) {     // [1]
            $('#stream-unread').get(0).click();
        }
        else if ( event.which == 50 ) {     // [2]
            $('#stream-starred').get(0).click();
        }
        else if ( event.which == 51 ) {     // [3]
            $('#stream-all').get(0).click();
        }
    });

    body.on('click', 'ul#status form.unread button', function (event) {
        event.preventDefault();
        toggleUnread();
    }).on('click', 'ul#status form.starred button', function (event) {
        event.preventDefault();
        toggleStarred();
    });
}(jQuery));
