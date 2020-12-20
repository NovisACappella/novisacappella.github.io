var centralize = function () {
    $("#splashcontainer").height($("#centerpiece").height() - $("nav").height() - 2*parseInt($("nav").css("padding-top")));
}

$(document).ready(function(){
    centralize();
});

$(window).resize(function(){
    centralize();
});