$(document).ready(function() {
	$('#id_url').change(function() {
		$.ajax({
			url: "/api/fetch_info",
            method: "GET",
            dataType: "json",
            data: {"url": $('#id_url').val()},
            beforeSend: function(xhr) {
                $("#id_title, #id_description").attr(
                    {"disabled":"disabled"});

                $("#id_title, #id_description").css(
                    {"background": "url(http://friendlybracelets.com/loader.gif no-repeat center center"});
            },
			success : function(data) {
                $("#id_title").val(data['title']);
                $("#id_description").val(data['description']);
                $("#id_title, #id_description").removeAttr("disabled");
                $("#id_title, #id_description").css(
                    {"background": "white"});
                $("#id_thumbnail_url").val(data['image']);
			},
			error : function(data) {
                $("#id_title, #id_description").removeAttr("disabled");
			}
		});
	});
});