var expand = function () {
    $("#filler").height(Math.max(50, $(window).height() - $("#letterboard").height() - $("#popcorn").height() - parseInt($("#splash").css("padding-top"))));
}

$(document).ready(function(){
    expand();
});

$(window).resize(function(){
    expand();
});