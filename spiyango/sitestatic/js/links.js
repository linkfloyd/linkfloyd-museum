$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
$(document).ready(function() {
    $(".vote_buttons").bind("vote", function(event, value) {
        var vote_el = $(this);
	    $.ajax({
            type:'POST',
	        url: "/api/votes/vote/",
	        data: {
                'model': vote_el.attr("x:model"),
                'object_id': vote_el.attr("x:object_id"),
                'value': value
            },
	        success : function(data, textStatus, jqXHR) {	
	            vote_el.find(".score").html(data['score']);
                if (value == 1) {
                    vote_el.find("a.downVote").removeClass("voted");
                    vote_el.find("a.upVote").addClass("voted");
                }
                if (value == -1) {
                    vote_el.find("a.upVote").removeClass("voted");
                    vote_el..find("a.downVote").addClass("voted");
                }
                if (value == 0) {
                    vote_el.find("a.upVote, a.downVote").removeClass("voted");
                }
	        },
        });
    });
    $('.upVote, .downVote').live('click', function(){
        if (window.loginDialog) {
            window.loginDialog.show();
        } else {
            $(this).parent().trigger("vote", $(this).attr("x:value"));
        }
    });
    $(".link").bind("delete", function(event) {
        var link_el = $(this);
	    $.ajax({
            type: "GET",
	        url: "/api/links/delete/",
	        data: {
                'object_id': link_el.attr("id")
            },
	        success : function(data, textStatus, jqXHR) {	
                link_el.slideUp();
	        }
        });

    });

    $('.deleteLink').live('click', function(){
        var link_el = $(this).parent().parent().parent();
        Boxy.confirm("Are you sure to remove this link?", function(){
            link_el.trigger("delete");
        });
    });
});

$("a.showReportForm").click(function(){
    if (user_id) {
        $.tmpl($("#submitReportTemplate"), {
            user_id: user_id,
            link_id: $(this).parent().parent().parent().attr("id")
        }).appendTo("div#content");
    } else {
        alert("Login before");
    };
});
$('#submitReportButton').live('click', function() {
    var form = $(this).parent().parent();
    if (form.find("#id_reason option:selected").val()) {
     	$.ajax({
            type:'POST',
         	url: "/api/reports/post/",
         	data: form.serialize(),
        	success : function(data, textStatus, jqXHR) {
                alert("oldu lan");
        	}
        });
        console.log(form.serialize());
    } else {
        form.find("label[for=id_reason] > ul.errorlist").show();
    }
});
