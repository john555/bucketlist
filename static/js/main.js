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

        // make adding bucket work
        var bucketForm = $('#bucket-form'),
            cancelBtn = $('#bkt-cancel'),
            createBtn = $('#bkt-create'),
            nameInput = $('#js-bucket-name');
        $("#js-add-bucket-btn").click(function(){
            bucketForm.toggle();
        });

        cancelBtn.click(function(){
            bucketForm.hide();
            nameInput.val('')
        });

        createBtn.click(createBucket);
        nameInput.on('keydown', function(e){
            if(e.keyCode == 13){
                createBucket();
            }
        })

        // make adding Items to buckets possible
        $('#js-add-bucket-item').click(addBucketItem);

        function addBucketItem(e){
            e.preventDefault();
            var form = $('#goal-form');
            var title = $('#goal-title').val(),
                bucketId = $('#goal-bucket').val(),
                date = $('#target-date').val(),
                description = $('#description').val();
            
            var data = {title:title, date:date, description:description};
            var url = form.attr('action');
            url = url.replace(':id', bucketId);
            console.log(url, data);
            $.post(url, data, function(data){
                addBucketCallback(data, '/buckets/'+bucketId);
            });
        }

        function addBucketCallback(data, url){
            var data = JSON.parse(data);
            console.log(data);
            $('body').removeClass('masked');
            window.location = url
        }

        function createBucket(){
            var val = nameInput.val().trim();
            if (val === ""){
                // add danger
                // nameInput.addClass('btn-invalid')
                return false;
            }
            
            $.post("/buckets/create", {name:val}, function(data){
                nameInput.val('')
                data = JSON.parse(data);
                displayBucket(data);
                showNotification("Added a new bucket.");
                $('#goal-bucket').append("<option value='"+data.bucket_id+"'>"+data.name+"</option>");
                bucketForm.hide();
            });
            
        }
        var buckets = $('#js-buckets');

        function displayBucket(data){
            var templ = '<div class="bucket">';
            templ += '<a href="/buckets/'+data.bucket_id+'" class="js-bucket-name">'
            templ += data.name +'</a></div>';
            templ = $(templ);
            buckets.append(templ);
        }

        var notif = $('#popup')
        function showNotification(message){
            notif.text(message);
            notif.addClass('visible');
            var id = setTimeout(function(){
                notif.removeClass('visible');
            }, 3500);
        }

        // display date on bucket items
        var days = $('.day');
        days.each(function(){
            var self = $(this);
            var dateStr = self.text();
            var date = dateStr.split("-"),
            day = date[2],
            mon = parseInt(date[1]),
            year = parseInt([0]);
            self.text(day);
            var months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            var month = months[mon-1];
            self.siblings('.mon-year').text(month);
        });

        // make editing buckets work
        var editBucketBtn = $('#js-edit-bucket');
        var editTarget = $('#js-edit-bucket-target');
        var saveBtn = $('#save-edit');
        var cancelBtn = $('#cancel-edit');
        var parent = $('#editable-bucket');

        editBucketBtn.click(function(){
            var self = $(this);
            var currentValue = editTarget.text();
            
            parent.addClass('edit-mode');
            $('#bucket-name').val(currentValue);
        });

        cancelBtn.click(function(){
            parent.removeClass('edit-mode');
        });

        saveBtn.click(function(){
            var newValue = $('#bucket-name').val();
            parent.removeClass('edit-mode');
            editTarget.text(newValue);
            var url = editBucketBtn.data('action-url');
            var data = {name:newValue}
            $.post(url, data, onEditBucketComplete)
        });

        function onEditBucketComplete(data){
            var data = JSON.parse(data);
            $('#bucket-'+data.bucket_id).text(data.name);
        }
        
        // make deleting work
        var deleteBucketBtn = $('#js-delete-bucket');

        deleteBucketBtn.click(function(){
            deleteBucket();
        })
        function deleteBucket(){
            var url = deleteBucketBtn.data('action-url');
            $.post(url, null, onDeleteBucketComplete)
        }

        function onDeleteBucketComplete(data){
            var data = JSON.parse(data);
            window.location = "/u/";
            
        }

        // work on bucket list items

        var editItemBtn = $('.js-edit-item');
        var completeItemBtn = $('.js-complete-item');
        var deleteItemBtn = $('.js-delete-item');

        //// make marking items as complete or incomplete work
        completeItemBtn.click(function(){
            var self = $(this);
            
        });
});
})(jQuery);
