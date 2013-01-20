var attachment_el,
    thumbnailrepo,
    thumbnailRepo,
    bgImageSwitch   = false,
    origin          = {x: 0, y: 0},
    start           = {x: 0, y: 0},
    movecontinue    = false;

function toggleBgImage() {
    bgImageSwitch = !bgImageSwitch;
    if (bgImageSwitch) {
        $("#selectThumbnail").show();
        attachment_el.addClass("thumbnailed");
        thumbnailrepo.updateBg();
        $("input[name='thumbnail_url']").val(thumbnailrepo.imgObjs[thumbnailrepo.idx].src6);
    } else {
        $("#selectThumbnail").hide();
        attachment_el.css('background-image', 'None');
        attachment_el.removeClass("thumbnailed");
        $("input[name='thumbnail_url']").val('');
    }
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
                if (_this.imgObjs.length) {
                    $("#thumbnailControls").show();
                    _this.updateBg();
                    toggleBgImage()
                };
                if (_this.imgObjs.length > 0 && !bgImageSwitch) {
                    toggleBgImage();
                    $("#toggleBgImage").attr("checked", true);
                }
            }
        });
    };
};

thumbnailRepo.prototype = {
    "updateBg": function() {
        attachment_el.css('background-image', "url(" + this.imgObjs[this.idx].src + ")");
        $("#currentThumbnail").html(this.idx + 1);
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
   
function MoveAttachmentBg (e){
    var moveby = {
        // x: origin.x - e.clientX, 
        x: 0,
        y: origin.y - e.clientY
    };
    
    if (movecontinue === true) {
        start.x = start.x - moveby.x;
        start.y = start.y - moveby.y;        
        $(this).css('background-position', start.x + 'px ' + start.y + 'px');
        $("#id_thumbnail_offset").val(start.y);
    }
    
    origin.x = e.clientX;
    origin.y = e.clientY;
    
    e.stopPropagation();
    return false;
}

function handle (e){
    movecontinue = false;
    attachment_el.unbind('mousemove', MoveAttachmentBg);
    
    if (e.type == 'mousedown') {
        origin.x = e.clientX;
        origin.y = e.clientY;
        movecontinue = true;
        attachment_el.bind('mousemove', MoveAttachmentBg);
    } else {
        $(document.body).focus();
    }
    
    e.stopPropagation();
    return false;
}

function reset (){
    start = {x: 0, y: 0};
    $(this).css('backgroundPosition', '0 0');
}

$(document).ready(function() {
    $("#toggleBgImage").change(toggleBgImage);

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
                attachment_el.bind('mousedown mouseup mouseleave', handle);
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
 
