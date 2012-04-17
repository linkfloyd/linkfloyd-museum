var addthis_share =  { 
    templates: {
        twitter: '{' + '{title}' + '} {' + '{url}' + '}'
    }
};
var addthis_config = {
    "ui_click": true,
    "ui_header_color": "#333",
    "ui_header_background": "#fff",
    "ui_use_css": true,
    "ui_use_addressbook": true,
    "data_ga_property": "UA-6315603-13",
    "data_ga_social": true,
    "services_expanded": "friendfeed,reddit,twitter"
};
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
    $(".link").bind("switch_follow", function(event) {
        var link_el = $(this);
	    $.ajax({
            type: "POST",
	        url: "/api/links/subscription/switch/",
	        data: {
                'link_id': link_el.attr("id")
            },
            dataType: "json",
	        success : function(data, textStatus, jqXHR) {
                var switch_el = link_el.find(".switchFollowLink");
                switch_el.html(data["update_text"]);
                switch_el.attr("title", data["update_title"]);
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
    $('.getEditCommentForm').live('click', function(){
        var comment_el = $(this).parent().parent().parent();
        comment_el.addClass("busy");
        comment_el.load('/api/comments/get_form/?id=' + comment_el.attr("id"));
        return false;
    });

    $('.deleteLink').live('click', function(){
        var link_el = $(this).parent().parent().parent();
        var accepted = confirm("Are you sure to remove this link?");
        if (accepted) { link_el.trigger("delete"); }
        return false;
    });
    $('.switchFollowLink').live('click', function(){
        var link_el = $(this).parent().parent().parent();
        link_el.trigger("switch_follow");
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
