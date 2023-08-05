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
        $('#colorpicker_id_background_color').on('click' , function(){
            background_color = $('#id_background_color').val().replace('#', '');
            init(url_params());
        });
    }
    if(document.querySelector("#id_basic_color")){
        $('#colorpicker_id_basic_color').on('click' , function(){
            basic_color = $('#id_basic_color').val().replace('#', '');
            init(url_params());
        });
    }
    if(document.querySelector("#id_diff_color")){
        $('#colorpicker_id_diff_color').on('click' , function(){
            diff_color = $('#id_diff_color').val().replace('#', '');
            init(url_params());
        });
    }
    if(document.querySelector("#id_progress_color")){
        $('#colorpicker_id_progress_color').on('click' , function(){
            progress_color = $('#id_progress_color').val().replace('#', '');
            init(url_params());
        });
    }
});
