(function($){
    "use strict";
    $(document).ready(function(){
        $("#compose").click(function(){
            $("body").addClass("masked");
        });

        $("#close-overlay, #overlay").click(function(){
            $("body").removeClass("masked");
        });

        $("#overlay-content").click(function(e){
            e.stopPropagation();
        });

        // dropdown menu
        $("#tools > li").click(function(e){
            e.stopPropagation();
            $(".dropdown").addClass("hidden");
            $(this).find(".dropdown").toggleClass('hidden');
        });
        $("body").click(function(){
            $(".dropdown").addClass("hidden");
            $('.actions').hide();
        });

        // show options menu whe ellipses are clicked
        $('.ellipses').click(function(e){
            e.stopPropagation();
            $('.actions').hide();
            $(this).siblings('.actions').toggle();
        });
});
})(jQuery);
console.log('loaded...');
