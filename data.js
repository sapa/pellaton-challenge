var entities;
var segments;

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
                    console.log(segments[i].start);
                    break;
                }
            }
        }
    }
}