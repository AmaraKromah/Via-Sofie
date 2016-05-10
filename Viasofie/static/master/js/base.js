$( document ).ready(function() {
    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        options.async = true; //make the login and register page load async
    });
    $('#login_link').on('click', function (event) {
        $('h4').html('Login');
		//$('#main-background').css('-webkit-filter', 'blur(5px)');
			$('#model-body-content').empty();
			$("#model-body-content").load( "/login/ .container-fluid", function() {
				$('#login-message').html("");
				$.getScript("/static/master/js/login.js")
				  .done(function( script, textStatus ) {
					console.log( textStatus );
				  })
				  .fail(function( jqxhr, settings, exception ) {
					console.log( "Triggered ajaxError handler." );
				});
			});
		$('#mainModal').modal();
        event.preventDefault();
    });

   /* $('.nav > .hvr-underline-reveal > a').on('click', function(event) {
        //event.preventDefault();
        $(".nav li a").each(function(idx, li) {
            console.log($(li));
            $(li).css('color', 'white');
            // and the rest of your code
        });
        $(this).css('color', 'red');
        console.log($(this).text());
    });*/

    console.log($(document).find("title").text());

    function findTextInNavBar(text) {
        $(".nav li a").each(function(idx, li) {
            if ($(li).text() == text) {
                $(li).css('text-decoration', 'underline');
            }
        });
    }
    if ($(document).find("title:contains('Viasofie')").text()) {
        findTextInNavBar('Home');
    } else if ($(document).find("title:contains('About')").text()) {
        findTextInNavBar('Over ons');
    } else if ($(document).find("title:contains('Contact')").text()) {
        findTextInNavBar('Contact');
    } else if ($(document).find("title:contains('Advice')").text()) {
        findTextInNavBar('Advies');
    } else if ($(document).find("title:contains('Partner')").text()) {
        findTextInNavBar('Partners');
    }

    /*Amara hippie code*/

	 $(document).on('click', '#min-prijs li', function() {
        $('#min-datebox').val($(this).html());
    });
    $(document).on('click', '#max-prijs li', function() {
        $('#max-datebox').val($(this).html());
    });

    $("#opties").on("hide.bs.collapse", function(){
        $(".btn-opties").html('<span class="glyphicon glyphicon glyphicon-chevron-down"></span> Meer opties');
    });
    $("#opties").on("show.bs.collapse", function(){
        $(".btn-opties").html('<span class="glyphicon glyphicon-chevron-up"></span> Minder opties');
    });

    console.log("Base.js loaded correctly.");
});