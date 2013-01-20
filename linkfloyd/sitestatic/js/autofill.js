var thumbnailSwitch = false;

function toggleThumbnail() {
    if (thumbnailSwitch === false) {
        console.log("switch false");
        if ($("img.thumbnail").length === 0) {
            console.log("creating img");
            $(".attachment").prepend("<div class='thumbnail'><img src='' /></div>");
        } else {
            $("div.thumbnail").show();
        }
    } else {
        $("div.thumbnail").hide();
    }
    thumbnailSwitch = !thumbnailSwitch;
}

thumbnailRepo = function(imgUrls) {
    this.idx = 0;
    this.imgBuffer = [];
    this.imgObjs = [];
    var _this = this;
    for (var i=0; i<imgUrls.length; i++) {
        this.imgBuffer[i] = new Image();
        this.imgBuffer[i].src = imgUrls[i];
        this.imgBuffer[i].addEventListener("load", function(ev) {
            if (this.width > 310 && this.height > 120) {
                _this.imgObjs.push(this);
                $("#totalThumbnails").html(_this.imgObjs.length);
                if (_this.imgObjs.length > 0) {
                    $("#thumbnailControls").show();
                };
                if (_this.imgObjs.length > 0 && !thumbnailSwitch) {
                    toggleThumbnail();
                    _this.updateBg();
                }
            }
        });
    };
};

thumbnailRepo.prototype = {
    "updateBg": function() {
        $("#currentThumbnail").html(this.idx + 1);
        $("div.thumbnail img").attr("src", thumbnailrepo.imgObjs[thumbnailrepo.idx].src)
        $("input[name='thumbnail_url']").val(thumbnailrepo.imgObjs[thumbnailrepo.idx].src);
    },
    "getNext": function() {
        this.idx++;
        if (this.idx>=this.imgObjs.length) {
            this.idx = 0;
        }
        this.updateBg();
    },
    "getPrev": function() {
        this.idx--;
        if (this.idx<=0) {
            this.idx = this.imgObjs.length - 1;
        }
        this.updateBg();
    }
};


$(document).ready(function() {
    $("#toggleBgImage").change(toggleThumbnail);

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
                $("input[name='player']").val(data.info.player);
                $("#remove_link").show();
                $("#url").hide();
                thumbnailrepo = new thumbnailRepo(data.info.images);
                attachment_el = $(".attachment");
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
 
