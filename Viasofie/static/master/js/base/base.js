/**
 * Created by Amara on 5/05/2016.
 */
$(document).ready(function(){

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

})