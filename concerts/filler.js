var expand = function () {
    $("#filler").height(Math.max(50, $(window).height() - 272 - 396 - 50 - 50));
    //$("#filler").height(Math.max(50, $(window).height() - $("#suspenders").height() - $("#bowtie").height() - parseInt($("#splash").css("padding-top"))));
}

$(document).ready(function(){
    expand();
});

$(window).resize(function(){
    expand();
});