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
            $.post(url, data, function(data){
                addBucketCallback(data, '/buckets/'+bucketId);
            });
        }

        function addBucketCallback(data, url){
            var data = JSON.parse(data);
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
            year = parseInt(date[0]);
            self.text(day);
            var months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            var month = months[mon-1];
            self.siblings('.mon-year').text(month +', '+ year);
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
            // $('#bucket-'+data.bucket_id).text(data.name);
            window.location = window.location
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
        var updateItemStatusBtn = $('.js-toggle-item-status');
        var deleteItemBtn = $('.js-delete-item');
        var saveItemBtn = $('.js-save-item');
        var cancelSaveItemBtn = $('.js-cancel-edit-item')

        //// make marking items as complete or incomplete work
        updateItemStatusBtn.click(function(){
            var self = $(this);
            var url = self.data('action-url');
            $.post(url, null, function(data){
                data = JSON.parse(data);
                $('#item-'+data.item_id).toggleClass('complete');
                // toggleEditItemBtn(self);
                window.location = location
            });
        });

        function toggleEditItemBtn(btn){
            var url = btn.data('action-url');
            if(url.match("/complete")){
                url = url.replace("/complete", "/incomplete");
                btn.attr('data-action-url', url);
                btn.text("Mark as incomplete");
            } else{
                url = url.replace("/incomplete", "/complete");
                btn.attr('data-action-url', url);
                btn.text("Mark as complete");
            }
        }

        //// make deleting items work
        deleteItemBtn.click(function(){
            var self = $(this);
            var url = self.data('action-url');
            var url = self.data('action-url');
            $.post(url, null, function(data){
                data = JSON.parse(data);
                // $('#item-'+data.item_id).remove();
                window.location = location
            });
        });
        

        //// make editing items work
        editItemBtn.click(function(){
            var self = $(this);
            var postUrl = self.data('action-url');
            var parent = self.parents('.bucket-item');
            initializeEditMode(parent);
        });

        saveItemBtn.click(function(){
            var self = $(this);
            var parent = self.parents('.bucket-item');
            
            editItem(parent);
        });

        cancelSaveItemBtn.click(function(){
            var self = $(this);
            var parent = self.parents('.bucket-item');
            exitEditMode(parent);
        });

        function initializeEditMode(item){
            item.addClass('edit-mode');
        }

        function exitEditMode(item){
            item.removeClass('edit-mode');
        }

        function editItem(item){
            var $title = item.find('.js-item-title');
            var $desc = item.find('.js-item-description');
            var $date = item.find('.js-item-date');
            var url = item.find('.js-edit-item').data('action-url');
            var data = {
                title: $title.val(),
                description: $desc.val(),
                date: $date.val()
            }
            $.post(url, data, editComplete);
        }

        function editComplete(data){
            data = JSON.parse(data);
            window.location = window.location
        }

        
});
})(jQuery);
