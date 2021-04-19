var entities;
var segments;
var current_segment_start = -1;

var iframe = document.querySelector('iframe');
var player = new Vimeo.Player(iframe);
player.on('progress', function(data) {
    on_player_progress(data['seconds'])
});
player.getVideoTitle().then(function(title) {
    console.log('title:', title);
});

const typeselector = document.getElementById('type-selector');
typeselector.addEventListener('input', on_type_update);

const searchfield = document.getElementById('entity-search');
searchfield.addEventListener('input', on_search_update);

function on_type_update(e) {
    filter_entities();
}

function on_search_update(e) {
  filter_entities()
}

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
        entity.setAttribute("class", "entity-link");
        entity._data = entities[i];
        entity.innerHTML = entities[i].name;
        entity.addEventListener('click', function () {
          on_entity_select(this);
        }, true);
        entities_list.appendChild(entity);
        entities[i].node = entity;
    }
}

function filter_entities(haystring) {
    var haystring = searchfield.value;
    var selected_type = document.querySelector('input[name="entity_type"]:checked').id;
  console.log(haystring, selected_type);
  console.log(entities.length);
  for (var i = 0; i < entities.length; i++) { 
    var e = entities[i];
    if (e.name.toLowerCase().includes(haystring.toLowerCase()) && (e.type==selected_type || selected_type=="ALL")) {
      e.node.style = 'display: block;';
    } else {
      e.node.style = 'display: none;';
    }
  }
}

function on_entity_select(entity) {
    console.log("click " + entity._data.name);
    for (var i = 0; i < segments.length; i++) { 
        if (typeof segments[i].entities == "object") {
            for (var e in segments[i].entities) {
                if (segments[i].entities[e] == entity._data.name) {
                    player.setCurrentTime(segments[i].start);
                    player.play();
                    show_segment_infos(segments[i].start);
                    return
                }
            }
        }
    }
}

function add_info(target_list, info_object, info_name, info_type) {
    if (typeof info_object[info_name] == "string") {
        var li = document.createElement('li');
        if (info_type == "link") {
            li.innerHTML = '<a href="' + info_object[info_name] + '" target="_blank">' + info_name.replace("sapa", "SAPA").replace("wikidata", "Wikidata") + '</a>';
        } else if (info_type == "image") {
            img_path = info_object[info_name].replace("/max/", "/!200,200/");
            li.innerHTML = '<img src="' + img_path + '" width="200" height"200" />';
        } else {
            li.innerHTML = info_name + ": " + info_object[info_name];
        }
        target_list.appendChild(li)
    }
}

function show_segment_infos(start) {
    var segment_transscript = document.getElementById('transcript');
    segment_transscript.innerText = '';
    var segment_info = document.getElementById('entities_info');
    segment_info.innerText = '';
    var info_list = document.createElement('ul');
    segment_info.appendChild(info_list);
    for (var i = 0; i < segments.length; i++) { 
        if (segments[i].start == start) {
            segment_transscript.innerText = segments[i].text;
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
                                add_info(extras, entities[k], "image", "image");
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

function on_player_progress(seconds) {
    var l = 0;
    for (var i = 0; i < segments.length; i++) { 
        if (seconds < segments[i].start){
          break
        }
        l = segments[i].start;
    }
    if (l != current_segment_start) {
      current_segment_start = l;
      show_segment_infos(segments[i].start);
    }
}

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}