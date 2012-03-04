$(document).ready(function(){
    $("a.subscription_status").bind("click", function() {
        var channel_el = $(this).parent();
        var button_el = $(this);
        if (button_el.hasClass("subscribed")) {
	 	    $.ajax({
	            type:'GET',
		        url: '/api/channels/unsubscribe/',
		        data: {
	                'channel_slug': channel_el.attr("id")
	            },
		        success : function(data, textStatus, jqXHR) {
                    button_el.html("Subscribe");
                    button_el.removeClass("subscribed");
		        },
	            statusCode: {
	                401:  function() {
	                    show_not_authenticated_error();
	                }
	            }
	        });
        } else {
	 	    $.ajax({
	            type:'GET',
		        url: '/api/channels/subscribe/',
		        data: {
	                'channel_slug': channel_el.attr("id")
	            },
		        success : function(data, textStatus, jqXHR) {
                    button_el.html("Unsubscribe");
                    button_el.addClass("subscribed");
		        },
	            statusCode: {
	                401:  function() {
	                    show_not_authenticated_error();
	                }
	            }
	        });
        }
    });
});