$(document).ready(function() {
    $('#collapseEntriesbtn').on('click', function(){
        $('#collapseEntries').toggle();
    });

    $('#collapseResultsbtn').on('click', function(){
        $('#collapseResults').toggle();
    });


    $(window).scroll(function () {
        var tempScrollTop = $(window).scrollTop();
        console.log("Scroll from Top: " + tempScrollTop.toString());
        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });
// scroll body to 0px on click
    $('#back-to-top').click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 400);
        return false;
    });


    $('.table').toggleClass('table-sm', $(window).width() < 768);
    $('.result-tbl').toggleClass('table-responsive', $(window).width() < 768);
    

});

