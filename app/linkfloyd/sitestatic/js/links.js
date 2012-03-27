$(document).ready( function() {
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
    $(".link").bind("delete", function(event) {
        var link_el = $(this);
	    $.ajax({
            type: "GET",
	        url: "/api/links/delete/",
	        data: {
                'id': link_el.attr("id")
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
        console.log(link_el);
        var embed_player = link_el.find("div.embed_player");
        if (embed_player.length) {
            console.log("player removed");
            embed_player.remove();
        } else {
            console.log("player appended");
            link_el.append(
                '<div class="embed_player">' + $(this).attr("play") + '</div>');
        }
        return false;
    });
});
