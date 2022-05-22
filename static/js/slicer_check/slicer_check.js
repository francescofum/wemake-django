
/**
 * Global variables
 * stl_list : An array containing the details of stl files the user has submitted
 *            This includes: 
 *              - id
 *              - STL url 
 *              - STL name
 *              - material 
 *              - colour
 *              - infill
 *              - unit
 *  
 * dropzone obj   : The dropzone object 
 *  
 * stl viewer obj : The stl viewer object 
 */

// TODO: Actually get an id (add to db, return id etc)

units = {};
stl_list = {};
stl_obj_list = {};
row_not_selected_flag = false;
// Keeps track of how many prices are still being calculated
var price_counter=0;
const csrftoken = getCookie('csrftoken');
string_mess = "Click Here";

function wm_create_dropzone() {
    
    Dropzone.autoDiscover = false;
    var dropzoneOptions = { // Make the whole body a dropzone
        dictDefaultMessage: "Drop files here to upload",
        url: `upload/`,
        maxfilesize: 5000,
        parallelUploads: 10,
        clickable: '#user_dropzone',
        acceptedFiles: ".stl",
        timeout: 1200000,                             // Set a timeout for uploading files.
        success: wm_stl_uploaded_success_callback,       // Callback function for when a file has been uploaded successfully. This will create a new row in the table.   
        sending: wm_stl_upload_sending_callback,  // Callback function for when dropzone starts to send. All the callback does is remove the thumbnail (I havent found another way of doing it).
        createImageThumbnails: false,

        uploadprogress: function (file, progress, bytesSent) {
            if (file.previewElement) {
                var progressElement = file.previewElement.querySelector("[data-dz-uploadprogress]");
                progressElement.style.width = progress + "%";
        
                $("#nav-prog-bar").attr('aria-valuenow', progress).css('width', progress + '%');
                //console.log('data-dz-uploadprogress:')
                //console.log(progress);
            }
        },
        totaluploadprogress(progress) {
            total_loading_progress(progress, -1);
        },
        headers: {
            'X-CSRFToken': csrftoken
        }

    };
    // Create the dropzone.
    var user_dropzone = new Dropzone(document.body, dropzoneOptions);

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function create_new_div(id,printer_id=1) {

    // $("#stl_carousel_inner").next();
    $(`#stl_carousel_inner_${printer_id}`).append(`<div id="stl_cont_${printer_id}_${id}" class="w-100 h-100" ></div> `)

    stl_obj_list[id] = new StlViewer(document.getElementById(`stl_cont_${printer_id}_${id}`), {
        model_loaded_callback: model_loaded_callback,
        loading_progress_callback: stl_load_prog,
        models: [{ id: id, filename: stl_list[id]['url'] }],
        // canvas_height: "100%"

    });
    //console.log(stl_obj_list)
    stl_obj_list[id].set_grid(true, 50, 50);
    //console.log(stl_obj_list[id]);
}


function wm_stl_upload_sending_callback() {
    $('.dz-preview').remove();
}


/**
 * Callback function for when the stl has been uploaded successfully. 
 * The callback function should then render a new row in the table.
 * @param: file - object which represents the files.
 * @param: response - The response from the server. 
 */
function wm_stl_uploaded_success_callback(file, response) {

    try {

        //  Get the parameters
        id = response['id']
        // url      = response["url"]; // Get the url from the response. From it we'll get
        // ////console.log(url);
        // filename = 
        material = 'Select';
        colour = 'Select';
        infill = 100;

        // Populate the array containing all the stls. The key is the ID.
        stl_list[id] = {};
        stl_list[id]['id'] = id;
        stl_list[id]['pretty_name'] = response['pretty_name']
        stl_list[id]['copies'] = 1;
        stl_list[id]['url'] = response["url"];
        stl_list[id]['filename'] = response['filename'];
        stl_list[id]['material'] = material;
        stl_list[id]['colour'] = colour;
        stl_list[id]['file_size'] = Number((file.size / 1000000).toFixed(3)); // Convert size from kb to mb and round to 3dp
        stl_list[id]['dims'] = { 'x': null, 'y': null, 'z': null } // Get from STL viewer x,y,z dimensions
        stl_list[id]['volume'] = null; //to be filled in the stl viewer callback
        stl_list[id]['scale'] = 1;
        stl_list[id]['infill'] = 100;
        stl_list[id]['price'] = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
        stl_list[id]['printer'] = $("#dropzone-button").attr('printer') ; 
        stl_list[id]['units'] = units;
        stl_list[id]['quantity'] = 1;
        stl_list[id]['time_to_print'] = "";
        stl_list[id]['length_of_filament'] = "";

        get_available_printer(id);

    }
    catch (e) {
        console.log(e)
    }
}



function create_row_html(id,printer_id=1) {
    $('.dz-preview').remove();

    // Render a new row. the stl dimensions will get added when the model is uploaded
    $(`#stl_div`).append(
        `<div class="">
            <div class="progress" style="height: 2px;">
                <div id="render_progress_${id}" class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <div id=stl_row_${id} class="stl_row row border selected_stl shadow-lg p-1 translucent" >
                <!-- 'Select'  --> 
                <div id="stl_${id}_copies" class="col-sm-1 stl_copies" style=' display: inherit; '>
                    <div class="col-sm-3" onclick="delete_stl(${id});">
                        X
                    </div>                   
                </div>                        
                <!-- end of 'Select' -->

                <!-- 'Filename' -->
                <div id="stl_${id}_filename" class="col-sm-2">
                    <small>
                        ${stl_list[id]['pretty_name']}
                    </small>
                </div>
                <!-- 'end of 'Filename' -->
                <!-- 'Size' -->
                <div id="stl_${id}_size_mb" class="col-sm-1">
                    <small>
                        ${stl_list[id]['file_size']}MB
                    </small>
                </div>
                <!-- end of 'Size' -->
                <!-- 'Time to print' -->
                <div id="stl_${id}_time_to_print" class="col-sm-2">
                    <small>
                        ${stl_list[id]['time_to_print']}sec
                    </small>
                </div>
                <!-- end of 'Time to print' -->
                <!-- 'Filament Length' -->
                <div id="stl_${id}_length_of_filament" class="col-sm-2">
                    <small>
                        ${stl_list[id]['length_of_filament']}m
                    </small>
                </div>
                <!-- end of 'Filament Length' --> 
            </div>
        </div>
        `
    )
    $(`#stl_div_${printer_id}`).height("40%");


}





function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}



function delete_stl(id,printer_id=1) {

    $(`#stl_row_${id}`).remove();


}




function stl_load_prog(load_status, load_session) {
    var loaded = 0;
    var total = 0;

    //go over all models that are/were loaded
    Object.keys(load_status).forEach(function (id) {
        if (load_status[id].load_session == load_session) //need to make sure we're on the last loading session (not counting previous loaded models)
        {
            loaded += load_status[id].loaded;
            total += load_status[id].total;

            newprogress = (load_status[id].loaded / load_status[id].total) * 100

            // Render the Progress on each row of the table
            //console.log(`For Model ${id} loaded: ${load_status[id].loaded} total: ${load_status[id].total} %: ${newprogress}`)
            $(`#render_progress_${id}`).attr('aria-valuenow', newprogress).css('width', newprogress + '%');

            // //console.log(load_status[id].loaded/load_status[id].total)
            //set the relevant model's progress bar
            // document.getElementById("pb"+id).value=load_status[id].loaded/load_status[id].total;
        }
    });

    total_loading_progress(-1, 100 * (loaded / total));

}

function total_loading_progress(dz_progress, stl_viewer_progress) {

    stl_total_progress = 0;
    // Uploading into the database first
    if (stl_viewer_progress == -1) {
        stl_viewer_progress = 0;
    }
    // Then loading into the stl_viewer
    if (dz_progress == -1) {
        dz_progress = 100;


        count = 0;
        Object.keys(stl_obj_list).forEach(function (id) {
            if (stl_obj_list[id].load_session == 0) { count += 1 };
        });

        files_uploaded = (Object.keys(stl_obj_list).length - count) + 1;
        fractional_progress = 100 * (files_uploaded / Object.keys(stl_obj_list).length);
        current_progress = stl_viewer_progress / Object.keys(stl_obj_list).length;
        stl_total_progress = fractional_progress + current_progress;
    }

    total_progress = 0.5 * (dz_progress + stl_total_progress);
    $('#nav-progressbar').css({ 'width': total_progress + '%' });

    if (total_progress >= 100) {
        $('#nav-progressbar').css({ 'display': 'none' });
        $('#nav-progressbar').css({ 'width': 0 + '%' });
        $('#nav-progressbar').css({ 'display': 'block' });
    }
}



/********** Right side of the screen functions  ******************/

// Similar to get_avaialble_printers but for a single STL.
// This fixes the bug where the price isn't displayed when multiple
// STLs are present but not all have colours (not the most elegant way, we should change the backend isntead.)
function get_available_printer(id) {
    

    var stl_to_send = {};
    stl_to_send[id] = stl_list[id];

    json_data = JSON.stringify(stl_list[id]); 
    // POST to backend.
    response = $.ajax({
        url: "get_available_printers/",
        type: 'POST',
        success: get_available_printer_success_callback,
        data: {
            stl_data:json_data
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    // dummmy
    

}

function get_available_printer_success_callback(response) {

    console.log(response)

    id = response['stl_id']
    
    stl_list[id]['price'] = response['price']

    stl_list[id]['printer']             = response['printer_id']
    stl_list[id]['volume']              = response['cura_data']['fil_volume']
    stl_list[id]['length_of_filament']  = response['cura_data']['fil_len']
    stl_list[id]['time_to_print']       = response['cura_data']['print_s']
    
    create_row_html(id,1);


}









// ************************* Cura function *********************************


function analyse_stl(id){

    request = jQuery.ajax({
        url: 'https://www.zlizer.xyz/analyse_stl',
        type: 'POST',
        crossDomain: true,
        data: stl_list[id],
        success: function (data) {
            console.log(data);
            stl_list[id]['time_to_print'] = data['print_s'][0];
            stl_list[id]['length_of_filament'] = data['fil_len'][0];
        }
    })
}