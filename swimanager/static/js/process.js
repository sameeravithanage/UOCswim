$(document).ready(function() {
    $("#settingsdiv ").hide();

    $('[data-toggle="tooltip"]').tooltip();  

    $('#padlock').on('click', function(){
        $('#settingsdiv ').toggle();
    });

    $('#collapseEntriesbtn').on('click', function(){
        $('#collapseEntries').toggle();
    });

    $('#collapseResultsbtn').on('click', function(){
        $('#collapseResults').toggle();
    });

    // $('#del_meet').on('click',function() {
    //   confirm('Do you want to delete this meet and all its contents?')      
    // });

    $('#del_meet').confirm({
        title: 'Warning!',
        content: "Do you want to delete this meet?",
        backgroundDismiss: function(){
            return true; // modal wont close.
        },
        buttons: {
            Delete: {
                btnClass: 'btn-red',
                action: function(){
                    location.href = this.$target.attr('href');
                }
            }
            
        }
    });

    // results sync
    $('.evt').on('click', function() {
        $('.evt').attr("disabled", true);
        var event = $(this).attr('data-event');
        var id = $(this).attr('data-id');
        var gender = $(this).attr('data-gender');
        
        $("[id='result_" + event + gender + "']").html(
            '<h4> Fetching results.... </h4>'
        );


        $.ajax({
            type: 'POST',
            url: '/process',
            data: JSON.stringify({ "event" : event, "meetid":id, "gender":gender} ),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        })
        .done(function(data){
            var table = arrayToTable(data, {
                thead: true,
                attrs: {class: 'table table-bordered'}
            });
            $("[id='result_" + event + gender + "']").html(table);
            $("[id='header_" + event + gender + "']").addClass('text-success');
            $("[id='header_" + event + gender + "']").text('--Results Fetched!');
            $("[id='res_btn_" + event + gender + "']").show();
            $('.evt').attr("disabled", false);
        });
    });
    // results publish button
    $('.evtpub').on('click', function() {
        $('.evtpub').attr("disabled", true);
        var event = $(this).attr('data-event');
        var id = $(this).attr('data-id');
        var gender = $(this).attr('data-gender');
        
        // $("[id='header_" + event + "']").append("   --- Publishing Results...");
        


        $.ajax({
            type: 'POST',
            url: '/pub_res',
            data: JSON.stringify({ "event" : event, "meetid":id, "gender":gender} ),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        })
        .done(function(data){
            if(data == 'Published!'){
                $("[id='header_" + event + gender + "']").removeClass('text-info');
                $("[id='header_" + event + gender + "']").addClass('text-success');
                $("[id='header_" + event + gender + "']").text('--Results Published!');
                $("[id='icon_" + event + gender + "']").css('color','greenyellow');
            } else {
                $("[id='header_" + event + gender + "']").removeClass('text-success');
                $("[id='header_" + event + gender + "']").addClass('text-info');
                $("[id='header_" + event + gender + "']").text('--Results Unpublished!');
                $("[id='icon_" + event + gender + "']").css('color','grey');
            }
            $('.evtpub').attr("disabled", false);
        });
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

});

