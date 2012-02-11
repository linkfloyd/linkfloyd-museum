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

                $("#id_title, #id_description").addClass("busy");
            },
			success : function(data) {
                $("#id_title").val(data['title']);
                $("#id_description").val(data['description']);
                $("#id_title, #id_description").removeAttr("disabled");
                $("#id_title, #id_description").removeClass("busy");
                if (data['image']) {
                    $("div#thumbnail_preview").slideDown();
                    $("div#thumbnail_preview img").attr("src", data['image']);
                }
                $("#id_thumbnail_url").val(data['image']);
                $("#id_player").val(data['player']);
			},
			error : function(data) {
                $("#id_title, #id_description").removeAttr("disabled");
			}
		});
	});
    $("div#thumbnail_preview label span a").click(function(){
        $(this).parent().parent().parent().slideUp();
        $("#id_thumbnail_url").val("");
    });
});