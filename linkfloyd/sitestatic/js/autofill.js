function attach() {
}
$(document).ready(function() {
    $("#id_url").change(function() {
        $.ajax({
            url: "/api/fetch_info/",
            type: "get",
            dataType: "json",
            data: {
                url: $('#id_url').val(),
            },
            beforeSend: function() {
                $('#id_url').prop('disabled', true);
                $('#id_url').addClass("busy");
                $('#id_submit').prop('disabled', true);
            },
            success: function(data) {
                $("#attachment_preview").html(data.html);
                $("input[name='url']").val(data.info.url);
                $("input[name='title']").val(data.info.title);
                $("input[name='description']").val(data.info.description);
                $("input[name='thumbnail_url']").val(data.info.image);
                $("input[name='player']").val(data.info.player);
                $("#remove_link").show();
                $("#link_input").hide();
            },
            statusCode: {
                404: function() {
                    $("#add_link ul.errorlist").show();
               }
            },
            complete: function(data) {
                $("#id_url").removeClass("busy");
                $("#id_url").prop('disabled', false);
                $("#id_submit").prop('disabled', false);
            }
        });
    });
    $("#remove_link a").click(function() {
        $("input[name='url']").val("");
        $("input[name='title']").val("");
        $("input[name='description']").val("");
        $("input[name='thumbnail_url']").val("");
        $("input[name='player']").val("");
        $("#attachment_preview").empty();
        $("#remove_link").hide();
        $("#id_url").prop('disabled', false);
        $("#link_input").show();
    });
    if ($("#id_url").val()) {
        $("#id_url").trigger("change");
    }
});
