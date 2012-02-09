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
function show_login() {
    alert("Please Login");
};
$(document).ready(function() {
    $(".vote_buttons").bind("vote", function(event, value) {
        var vote_el = $(this);
 	    $.ajax({
            type:'POST',
	        url: "/api/votes/vote/",
	        data: {
                'model': vote_el.attr("x:model"),
                'id': vote_el.attr("x:id"),
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
                    vote_el.find("a.downVote").addClass("voted");
                }
                if (value == 0) {
                    vote_el.find("a.upVote, a.downVote").removeClass("voted");
                }
	        },
            statusCode: {
                401:  function(){
                    show_login();
                }
            }
        });
    });
    $('.upVote, .downVote').live('click', function(){
        $(this).parent().trigger("vote", $(this).attr("x:value"));
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
	        },
            statusCode: {
                401:  function(){
                    show_login();
                }
            }
        });
    });
    $(".comment").bind("delete", function(event) {
        var comment_el = $(this);
	    $.ajax({
            type: "GET",
	        url: "/api/comments/delete/",
	        data: {
                'id': comment_el.attr("id")
            },
	        success : function(data, textStatus, jqXHR) {	
                comment_el.slideUp();
	        },
            statusCode: {
                401:  function(){
                    show_login();
                }
            }
        });
    });
    $('.deleteLink').live('click', function(){
        var link_el = $(this).parent().parent().parent();
        var accepted = confirm("Are you sure to remove this link?");
        if (accepted) { link_el.trigger("delete"); }
        return false;
    });
    $('.deleteComment').live('click', function(){
        var comment_el = $(this).parent().parent().parent();
        var accepted = confirm("Are you sure to remove this comment?");
        if (accepted) { comment_el.trigger("delete"); }
        return false;
    });
    $("a.playble").click(function() {
        var link_el = $(this).parent();
        var embed_player = link_el.find("div.embed_player");
        if (embed_player.length) {
            embed_player.remove();

        } else {
            link_el.append(
                '<div class="embed_player">' + $(this).attr("play") + '</div>');
        }
        return false;
    });
    $('.reportLink').live('click', function() {
        if (window.loginDialog) {
            window.loginDialog.show();
        } else {
            var link_el = $(this).parent().parent().parent();
            window.submitReportDialog = new Boxy(
                $.tmpl($("#submitReportFormTemplate"), {
                    link_id: link_el.attr("id")
                }), {
                    title: "Report link",
                    modal: true,
                    fixed: true,
                    hideAndUnload: true
                });
        }
    });
});
