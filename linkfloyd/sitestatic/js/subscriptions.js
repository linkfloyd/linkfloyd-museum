$(document).ready(function(){
    $("a.subscription_status").bind("click", function() {
        var channel_slug = $(this).attr("data-slug");
        var button_el = $(this);
        var request = function(extra_data) {
            $.ajax({
                type:'POST',
	            url: '/api/channels/subscription/switch/',
                dataType: 'json',
                data: $.extend({'channel_slug': channel_slug}, extra_data),
                success : function(data, textStatus, jqXHR) {
                    if (data.status === "subscribed") {
                        button_el.addClass("subscribed");
                        button_el.html(data.update_text);
                    } else if (data.status === "unsubscribed") {
                        button_el.removeClass("subscribed");
                        button_el.html(data.update_text);
                    } else if (data.status === "confirmation_needed") {
                        var confirmed = confirm(data.confirmation_text);
                        if (confirmed) {
                            request({"sure": true});
                        }
                    }
                },
                statusCode: {
	                401:  function(data) {
                        window.location = "/accounts/login/";
                    }
	            }
	        });
        };
        request();
        return false;
    }); 
});
