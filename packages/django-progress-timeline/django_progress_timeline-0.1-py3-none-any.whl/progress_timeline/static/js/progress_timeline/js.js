function move(elem) {
    var elem = document.getElementById(elem);   
    var ratio = parseFloat(elem.getAttribute('data-progress'));
    var width = 1;
    var time = 200 / ratio;
    var step = 0.1;
    var id = setInterval(frame, time);
    function frame() {
        if (width >= ratio) {
            clearInterval(id);
        } else {
            width += step; 
                elem.style.width = width + '%'; 
        }
    }
}

function load(url){
    fetch(url)
        .then(function(response) {
            return response.text();
        })
        .then(function(body) {
            elem.innerHTML = body;
            move("myBar-" + attr);
            move("myBar2-" + attr);
        });
}

function init(params=""){
    elem = document.querySelectorAll("#get_progress_timeline")[0];
    if (elem){
        attr = elem.getAttribute("data-timeline");
        url = '/progress-timeline/' + attr + params;
        load(url)
    }
}

init();


document.addEventListener("DOMContentLoaded", function() {
    var background_color = "";
    var basic_color = "";
    var diff_color = "";
    var progress_color = "";

    function url_params(){
        return "?background_color=" + background_color + "&basic_color=" + basic_color + "&diff_color=" + diff_color + "&progress_color=" + progress_color;
    }
    if(document.querySelector("#id_background_color")){
        document.querySelector("#id_background_color").onchange = function (e) {
            background_color = this.value;
            init(url_params());
        }
    }
    if(document.querySelector("#id_basic_color")){
        document.querySelector("#id_basic_color").onchange = function (e) {
            basic_color = this.value;
            init(url_params());
        }
    }
    if(document.querySelector("#id_diff_color")){
        document.querySelector("#id_diff_color").onchange = function (e) {
            diff_color = this.value;
            init(url_params());
        }
    }
    if(document.querySelector("#id_progress_color")){
        document.querySelector("#id_progress_color").onchange = function (e) {
            progress_color = this.value;
            init(url_params());
        }
    }
});
