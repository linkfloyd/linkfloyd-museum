var thumbnailSwitch = false;
function toggleThumbnail() {
    if (thumbnailSwitch === false) {
        if ($("img.thumbnail").length === 0) {
            $("div.thumbnail").show();
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
        return false;
    },
    "getPrev": function() {
        this.idx--;
        if (this.idx<=0) {
            this.idx = this.imgObjs.length - 1;
        }
        this.updateBg();
        return false;
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
                $('#id_url').addClass("busy");
                $('#id_url').prop('disabled', true);
                $('#id_submit').prop('disabled', true);
            },
            success: function(data) {
                $("#id_url").val(data.info.url);
                if ($(document).find("#id_title").val() === '') {
                    $("#id_title").val(data.info.title);
                };
                $("#id_description").html(data.info.description);
                $("#id_player").val(data.info.player);
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
    $('a#next').click(function (e) {
        // custom handling here
        thumbnailrepo.getNext();
    });
    $('a#prev').click(function (e) {
        // custom handling here
        thumbnailrepo.getPrev();
    });
});

