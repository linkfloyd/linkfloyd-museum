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
    "services_expanded": "friendfeed, reddit, twitter"
};
$(document).ready( function() {
    $(".comment").bind("delete", function(event) {
        var comment_el = $(this);
        console.log(comment_el);
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
    $(".post").bind("delete", function(event) {
        var link_el = $(event.target).parent();
	    $.ajax({
            type: "GET",
	        url: "/api/links/delete/",
	        data: {
                'id': link_el.attr("data-id")
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
    $(".post").bind("switch_follow", function(event) {
        var link_el = $(event.target).parent();
	    $.ajax({
            type: "POST",
	        url: "/api/links/subscription/switch/",
	        data: {
                'link_id': link_el.attr("data-id")
            },
            dataType: "json",
	        success : function(data, textStatus, jqXHR) {
                var switch_el = link_el.find(".switchFollowLink");
                switch_el.html(data.update_text);
                switch_el.attr("title", data.update_title);
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
        var comment_el = $(this).parent().parent().parent().parent();
        var accepted = confirm("Are you sure to remove this comment?");
        if (accepted) { comment_el.trigger("delete"); }
        return false;
    });
    $('.getUpdateCommentForm').live('click', function(){
        var comment_el = $(this).parent().parent().parent().parent();
        comment_el.addClass("busy");
        comment_el.find("div.content").hide();
        $.get('/api/comments/get_form/?id=' + comment_el.attr("id"),
            function(data) {
              comment_el.append(data);
        });
        return false;
    });
    $('.cancelUpdateComment').live('click', function(){
        var comment_el = $(this).parent().parent();
        comment_el.find("div.content").show();
        comment_el.find("form.comment").remove();
        return false;
    });
    $('.switchFollowLink').live('click', function(){
        var link_el = $(this).parent().parent().parent();
        link_el.trigger("switch_follow");
        return false;
    });
    $("div.thumbnail i").click(function() {
        var attachment_el = $(this).parent().parent();
        var embed_player_el = attachment_el.find("div.embed_player");

        if (embed_player_el.length === 0) {
            embed_player_el = $("<div class='embed_player'></div>");
            embed_player_el.append($(this).attr("player"));
            attachment_el.find('p.title').after(embed_player_el);
            attachment_el.addClass("expanded");
        } else {
            embed_player_el.remove();
            attachment_el.removeClass("expanded");
        }
        return false;
    });
});
