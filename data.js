var entities;
var segments;

var iframe = document.querySelector('iframe');
var player = new Vimeo.Player(iframe);
player.on('play', function() {
    console.log('played the video!');
});
player.getVideoTitle().then(function(title) {
    console.log('title:', title);
});

let request = new XMLHttpRequest();
request.open('GET', 'pellaton.json');
request.responseType = 'json';
request.send();
request.onload = function() {
    var content = request.response;
    entities = content['entities'];
    segments = content['segments'];
    show_entities();
}

function show_entities() {
    var entities_div = document.getElementById('entities');
    var entities_list = document.createElement('ul');
    entities_div.appendChild(entities_list);
    for (var i = 0; i < entities.length; i++) { 
        var entity = document.createElement('li');
        entity._data = entities[i];
        entity.innerHTML = entities[i].name;
        entity.addEventListener('click', function () {
            on_entity_select(this);
        }, true);
        entities_list.appendChild(entity);
    }
}

function on_entity_select(entity) {
    console.log("click " + entity._data.name);
    for (var i = 0; i < segments.length; i++) { 
        if (typeof segments[i].entities == "object") {
            for (var e in segments[i].entities) {
                if (segments[i].entities[e] == entity._data.name) {
                    var startTime = segments[i].start
                    var time_characters = startTime.length
                    var time_parts = startTime.split(":");
                    var seconds;
                    if (time_parts.length == 2){
                        seconds = parseInt(time_parts[0])*60 + parseInt(time_parts[1])
                    } else {
                        seconds = parseInt(time_parts[0])*3600 + parseInt(time_parts[1])*60 + parseInt(startTime[2])
                    }
                    player.setCurrentTime(seconds);
                    player.play();
                    show_segment_entities(startTime);
                    return
                }
            }
        }
    }
}

function add_info(target_list, info_object, info_name, info_type) {
    console.log(info_name, info_object[info_name], typeof info_object[info_name]);
    if (typeof info_object[info_name] == "string") {
        var li = document.createElement('li');
        if (info_type == "link") {
            li.innerHTML = '<a href="' + info_object[info_name] + '" target="_blank">' + info_name + '</a>';
        } else {
            li.innerHTML = info_name + ": " + info_object[info_name];
        }
        target_list.appendChild(li)
    }
}

function show_segment_entities(start) {
    var segment_info = document.getElementById('entities_info');
    segment_info.innerText = '';
    var info_list = document.createElement('ul');
    segment_info.appendChild(info_list);
    for (var i = 0; i < segments.length; i++) { 
        if (segments[i].start == start) {
            var found_entities = [];
            if (typeof segments[i].entities == "object") {
                for (var j = 0; j < segments[i].entities.length; j++) {
                    var e = segments[i].entities[j];
                    if (!found_entities.includes(e)) {
                        found_entities.push(e)
                        for (var k = 0; k < entities.length; k++) {
                            if (entities[k].name == e) {
                                var entity = document.createElement('li');
                                entity._data = entities[k];
                                entity.innerHTML = entities[k].name;
                                // entity.addEventListener('click', function () {
                                //     on_entity_select(this);
                                // }, true);
                                segment_info.appendChild(entity);
                                var extras = document.createElement('ul');
                                add_info(extras, entities[k], "wikidata", "link");
                                add_info(extras, entities[k], "sapa", "link");
                                add_info(extras, entities[k], "dob", "text");
                                add_info(extras, entities[k], "dod", "text");
                                entity.appendChild(extras);
                            }
                        }
                    }
                }
            }
        }
    }
}

