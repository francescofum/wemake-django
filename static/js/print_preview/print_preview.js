var flag_printer_setup_page = 0



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

const csrftoken = getCookie('csrftoken');
string_mess = "Click Here";

$("document").ready(function () {
    console.log("Starting print preview js");

    wm_create_dropzone();
   
});

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
        parallelUploads: 1,
        uploadMultiple: false,
        success: wm_stl_uploaded_success_callback,       // Callback function for when a file has been uploaded successfully. This will create a new row in the table.   
        // complete: wm_stl_uploaded_complete_callback, // Callback function for when a file upload is complete, whether successfull or erronous.  
        sending: function wm_stl_upload_sending_callback() {
            $('.dz-preview').remove();
            document.getElementById("initial-upload-spinner").style.display = "initial"; 

        },
        createImageThumbnails: false,
        uploadprogress: function (file, progress, bytesSent) {
            if (file.previewElement) {
                var progressElement = file.previewElement.querySelector("[data-dz-uploadprogress]");
                progressElement.style.width = progress + "%";   
                $("#nav-prog-bar").attr('aria-valuenow', progress).css('width', progress + '%');
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
    $(`#stl_carousel_inner_${printer_id}`).append(`<div id="stl_cont_${printer_id}_${id}" class="w-100 h-100" ></div> `)

    stl_obj_list[id] = new StlViewer(document.getElementById(`stl_cont_${printer_id}_${id}`), {
        model_loaded_callback: model_loaded_callback,
        loading_progress_callback: stl_load_prog,
        models: [{ id: id, filename: stl_list[id]['url'] }],
    });
    stl_obj_list[id].set_grid(true, 50, 50);
}


/**
 * Callback function for when the stl has been uploaded successfully. 
 * The callback function should then render a new row in the table.
 * @param: file - object which represents the files.
 * @param: response - The response from the server. 
 */
function wm_stl_uploaded_success_callback(file, response) {
    document.getElementById("initial-upload-screen").style.display = "none"; 
    document.getElementById("stl_viewer-screen").style.display = "initial"; 
    try {
        //  Get the parameters
        id = response['id']
        material = 'Select';
        colour = 'Select';
        infill = 100;

        // Populate the array containing all the stls. The key is the ID.
        stl_list[id] = {};
        stl_list[id]['id'] = id;
        stl_list[id]['pretty_name'] = response['pretty_name']
        stl_list[id]['copies'] = 1;
        stl_list[id]['url'] = document.location.origin  + response["url"];
        stl_list[id]['filename'] = response['filename'];
        stl_list[id]['material'] = material;
        stl_list[id]['colour'] = colour;
        stl_list[id]['file_size'] = Number((file.size / 1000000).toFixed(3)); // Convert size from kb to mb and round to 3dp
        stl_list[id]['dims'] = { 'x': null, 'y': null, 'z': null } // Get from STL viewer x,y,z dimensions
        stl_list[id]['volume'] = null; //to be filled in the stl viewer callback
        stl_list[id]['scale'] = 1;
        stl_list[id]['infill'] = 100;
        stl_list[id]['price'] = null;
        stl_list[id]['printer'] = null;
        stl_list[id]['units'] = units;
        stl_list[id]['quantity'] = 1;
        stl_list[id]['time_to_print'] = null;
        stl_list[id]['length_of_filament'] = null;

        create_row_html(id,1);
    }
    catch (e) {
        console.log(e)
    }
}



function create_row_html(id,printer_id=1) {

    // If the name is to long, slice it
    // and add ...
    if(stl_list[id]['pretty_name'].length > 10){
        dotdotdot = "...";
    }
    else{
        dotdotdot = "";
    }
    create_new_div(id,printer_id);
    row_not_selected_flag = false;
    select_stl(id);
    // Render a new row. the stl dimensions will get added when the model is uploaded
    $(`#stl_div_${printer_id}`).append(
        `<div class="">
            <div class="progress" style="height: 2px;">
                <div id="render_progress_${id}" class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <div id=stl_row_${printer_id}_${id} class="stl_row row border selected_stl shadow-lg p-1 translucent" onclick="select_stl(${id});">
                <!-- 'Select'  -->

                <div id="stl_${id}_copies" class="col-sm-2 stl_copies" style=' display: inherit; '>
                    <div class="col-sm-3" onclick="delete_stl(${id});">
                    <button type="button" class="btn btn-link btn-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
      <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>
      <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>
    </svg>
                  </button>

                    </div></a>
                    <div class="col-sm-9">
                        <!-- 'Copies' -->
                            <input type="number" style="width:100%;" onchange="quantity_changed(${id});" class="form-control" name="number" id="stl_quantity_${id}" value="1" min=1>
                        <!-- end of 'Copies' -->
                    </div>                        
                </div>                        
                    <!-- end of 'Select' -->

                <!-- 'Filename' -->
                <div id="stl_${id}_filename" class="col-sm-2">
                    <small>
                        ${stl_list[id]['pretty_name'].slice(0,10)}${dotdotdot}
                    </small>
                </div>
                <!-- 'end of 'Filename' -->
                <!-- 'Size' -->
                <div id="stl_${id}_size_mb" class="col-sm-1">
                    <small>
                        ${stl_list[id]['file_size']}
                    </small>
                </div>
                <!-- end of 'Size' -->
                <!-- 'Materials' -->
                <div class="col-sm-2">
                    <small class="text-center"> 
                        <select style="width:100%" name="select" id="stl_${id}_material" onchange="material_selection_changed(${id},${printer_id});" class="btn-outline-secondary form-control">
                            <option hidden>Select</option>
                        </select>
                    </small>
                </div>
                <!-- end of 'Materials' -->
                <!-- 'Colours' -->
                <div class="col-sm-2">
                    <select name="select" id="stl_${id}_colour" onchange="colour_selection_changed(${id},${printer_id})" style="width:100%" class="btn-outline-secondary form-control">
                        <option hidden>Select</option>
                    </select>
                </div>
                <!-- end of 'Colours' --> 
                <!-- 'Size ' -->
                <div id="stl_${id}_dimensions_div" class="col-sm-2">
                    <div
                        data-html="true" 
                        data-toggle="popover-scale-${id}" 
                        data-trigger="hover"
                        data-content="

                            <div>
                                <label for='scale' style='display: block'>Scale: </label>
                                <input id='scale_stl_${id}' onchange='scale_change(${id});' class='col-xs-1' type='number'  name='quantity' min='0.1' max='10' step='0.1' value='1' style='display: block-inline'>
                            </div>
                        ">
                        <div id="stl_${id}_dimensions_val" >
                            <small>
                                Dimensions
                                <!-- populated by stlviewer -->
                            </small>
                        </div>
                    </div>
                </div>
                <!-- end of 'Size' -->
                <!-- 'Price' -->
                <div id="stl_${id}_price" class="col-sm-1 text-center stl_price">
                    <small id="stl_${id}_price_value" >
                        <div class="spinner-border text-primary" role="status"></div>
                    </small>
                </div>
                <!-- end of 'Price' -->
            </div>
        </div>
    </div>
        `
    )
    $(`#stl_div_${printer_id}`).height("40%");

    // Populate the material dropdown
    for (const [key, value] of Object.entries(material_colours)) {
        var name = material_colours[key]['name'];
        $(`#stl_${id}_material`).append(new Option(name, key))
    }
}


/**
 * Callback for when the user changes the material.
 * This will modify the corresponding entry in stl_list.
 * will also cause the colour dropdown to be updated with compatible materials.
 * @param id: The id of the stl who's material changes
 */
function material_selection_changed(id,printer_id) {

    row_not_selected_flag = true;
    var material = $(`#stl_${id}_material`).val();
    // Empty the colour dropdown
    var colour_dropdown = $(`#stl_${id}_colour`);
    colour_dropdown.empty();

    // if the material is 'any' simply display 'any' in the colour dropdown
    if (material == 'Select') $(`#stl_${id}_colour`).append(new Option('Select', 'Select'));
    else {
        // Add the 'any' option and select it.
        $(`#stl_${id}_colour`).append(new Option('Select', 'Select',true,true))       
        for (const [key, value] of Object.entries(material_colours[material]['colours'])){
                
                $(`#stl_${id}_colour`).append(new Option(value, value));
            
        };
        // Upate stl_list
        stl_list[id]['material'] = material_colours[material]['name'];
        // Get the colour key
        colour_key = Object.keys(material_colours[material]['colours'])[0]
        stl_list[id]['colour'] = material_colours[material]['colours'][colour_key];
        // Set the colour to the first available one
        $(`#stl_${id}_colour`).val(stl_list[id]['colour'])
        colour_selection_changed(id,printer_id);

    }
   
}


function quantity_changed(id){

    stl_list[id]['quantity'] = $(`#stl_quantity_${id}`).val()
    update_total_price()

}

/**
 * Callback for when the user changes the colour.
 * The stl colour changes as well. 
 * @param id: The id of the stl who's material changes
 */
function colour_selection_changed(id,printer_id) {

    // If this function was not called by model_loaded_callback
    // i.e was called by the user changing colour then set the flag.
    if (colour_selection_changed.caller != model_loaded_callback) {
        row_not_selected_flag = true;
    }
    //console.log(`----> In colour_changed :${row_not_selected_flag}`);
    var colour_lookup = {
        'Select': '#839192',
        'RED': '#F82C00',
        'PINK': '#F5B7B1',
        'ORANGE': '#E67E22',
        'YELLOW': '#F4D03F',
        'GREEN': '#27AE60',
        'BLUE': '#3498DB',
        'VIOLET': '#AF7AC5',
        'WHITE': '#FBFCFC',
        'GREY': '#839192',
        'BLACK': '#17202A',
    }
    colour = $(`#stl_${id}_colour`).val();
    stl_obj_list[id].set_color(id, colour_lookup[colour]);
    // Update stl_list with the new colour 
    stl_list[id]['colour'] = colour;
    get_available_printer(id);
    
}


function delete_stl(id,printer_id=1) {
    row_not_selected_flag = true;
    // Delete it from the stl_list object
    stl_obj_list[id].dispose()
    delete stl_list[id];

    // If the currently selected one was deleted, display the first one
    if ($(`#stl_row_${printer_id}_${id}`).hasClass("selected_stl") && Object.keys(stl_list).length > 0) {

        // Select the first stl in the list
        new_stl = Object.keys(stl_list)[0];
        //console.log(`Selecting new row: ${new_stl}`)
        // $(`#stl_row_${new_stl}`).addClass('shadow-lg selected_stl');
        // $(`#stl_row_${new_stl}`).css("background-color","rgb(229, 229, 229)");
        // Render the new stl 
        row_not_selected_flag = false;
        select_stl(new_stl)
        row_not_selected_flag = true;
    }
    // Delete the div
    $(`#stl_cont_${printer_id}_${id}`).remove();
    $(`#stl_row_${printer_id}_${id}`).remove();
    //console.log("Clearing session");
    // Notify backend so that it can be removed from the session. 
    response = $.ajax({
        url: 'remove_item_from_cart/',
        type: 'POST',
        data: {stl_id:id},
        success:function(response){
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });

    update_total_price();

}


function select_stl(id,printer_id=1) {

    if (!row_not_selected_flag) {
        // Clear the red border from the previous row that had it.
        // This is done by looping through all divs who have id's starting with 'stl_'
        var previously_selected_row;
        var list_of_rows = $(`div[id^="stl_row_${printer_id}_"]`);
        list_of_rows.each(function () {
            if ($(this).hasClass('selected_stl')) {
                // get the id 
                previously_selected_row = $(this).attr('id').match(/(\d+_)(\d+)/)[2];

            }
        });
        try {
            // Hide the previous stl 
            $(`#stl_cont_${printer_id}_${previously_selected_row}`).css('display', 'none'); //canvas 

            $(`#stl_row_${printer_id}_${previously_selected_row}`).removeClass('shadow-lg selected_stl');
            // $(`#stl_row_${previously_selected_row}`).addClass('shadow-sm')
            // $(`#stl_row_${previously_selected_row}`).css("background-color","rgb(255, 255, 255)");

        }
        catch (e) {
            // It will go into this catch block if previously_selected_row is undefined, which should happen only the first time round.
            alert("ERROR")
        }
        // Display the current stl 
        $(`#stl_cont_${printer_id}_${id}`).show(); //canvas
        // Make the border red to indicate it has been selected.
        $(`#stl_row_${printer_id}_${id}`).addClass('selected_stl shadow-lg');

        // Render the STL

        // render_stl(id)
    }
    else {
        row_not_selected_flag = false;
    }
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

// Function to display an stl ,
function render_stl(id,printer_id=1) {
    $(`#stl_cont_${printer_id}_${id}`).show()
}





/**
 * Callback for when model has finished loading.
 * Can be used to remove the loading spinner. 
 * Is also used to update stl_list with additional information such as the unit, dimensions etc.
 * */

function model_loaded_callback(id) {
    ////console.log(`Model info for model: ${id}`);
    $(`#render_progress_${id}`).parent().remove();

    model_info = stl_obj_list[id].get_model_info(id);

    // Populate stl_list[id] with the diension and units.
    stl_list[id]['dims']['x'] = parseInt(model_info['dims']['x'].toFixed(0));
    stl_list[id]['dims']['y'] = parseInt(model_info['dims']['y'].toFixed(0));
    stl_list[id]['dims']['z'] = parseInt(model_info['dims']['z'].toFixed(0));
    stl_list[id]['volume'] = parseInt(model_info['volume'].toFixed(0));
    stl_list[id]['units'] = units;

    // Display the units and dimensions
    ////console.log()
    $(`#stl_${id}_dimensions_val`).html(`<small> ${stl_list[id]['dims']['x']}x${stl_list[id]['dims']['y']}x${stl_list[id]['dims']['z']}</small>`)

    // Select the first material 
    // $(`#stl_${id}_material`).val(Object.entries(material_colours)[0]);

    var printer_id = this.parent_element.id.substring(
        this.parent_element.id.indexOf("_") + 6, 
        this.parent_element.id.lastIndexOf("_")
    );

    material_selection_changed(id,printer_id);
    colour_selection_changed(id,printer_id);
    
    if (flag_printer_setup_page == 1){
        try {
            update_price_summary(id, parseInt(printer_id));
        } catch (error) {
        }
    }



    //colour_selection_changed(id) // Set the model colour to whatever is in the dropdown.
    if (stl_list[id]['units'] == 'in') {
        scale_factor = 25.4;

        stl_list[id]['dims']['x'] = scale_factor * stl_list[id]['dims']['x'];
        stl_list[id]['dims']['y'] = scale_factor * stl_list[id]['dims']['y'];
        stl_list[id]['dims']['z'] = scale_factor * stl_list[id]['dims']['z'];

        stl_list[id]['volume'] = Math.pow(scale_factor, 3) * stl_list[id]['volume'];

    }
    else {
        // Nothing, as already in mm
    }
}

/********** Right side of the screen functions  ******************/

// Similar to get_avaialble_printers but for a single STL.
// This fixes the bug where the price isn't displayed when multiple
// STLs are present but not all have colours (not the most elegant way, we should change the backend isntead.)
function get_available_printer(id) {
    
    /* Display the spinner for this row*/
    $(`#stl_${id}_price_value`).html(`<div class="spinner-border text-primary" role="status"></div>`)
    /* Display TOTAL PRICE spiner  */
    $(`#total_price_value`).html(`<div class="spinner-border" role="status"></div>`)
    
    // display_price_spinner(id);
    if (stl_list[id]['material'] == "Select" || stl_list[id]['colour'] == "Select")
    {
        return;
    }
    // set the price to "null" to indicate that its being processed
    stl_list[id]['price'] == null;
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

}

function get_available_printer_success_callback(response) {

    console.log(response)
    if (response['stl_id'] == "KO"){
        alert("No available printers found with these settings.")
        return
    }
    
    id = response['stl_id']
    stl_list[id]['price'] = response['price']
    stl_list[id]['printer'] = response['printer_id']
    stl_list[id]['volume'] = response['cura_data']['fil_vol']
    stl_list[id]['length_of_filament'] = response['cura_data']['fil_len']
    stl_list[id]['time_to_print'] = response['cura_data']['print_s']
    /* Set the price */
    $(`#stl_${id}_price_value`).html(`<small>${stl_list[id]['price'] }</small>`)
    update_total_price();
}



function get_stl_price(id){
    var stl_to_send = {};
    stl_to_send[id] = stl_list[id];
    // POST to backend.
    response = $.ajax({
        url: ajax_object.ajax_url,
        type: 'POST',
        success: get_stl_price_success_callback,
        data: {
            action: 'calculate_stl_price',
            vendor_id: vendor_id,
            stl_list_string: stl_to_send
        }
    });
	// update_total_price();
}


function get_stl_price_success_callback(response) {

    console.log(response);
    response = JSON.parse(response);

    var total_price = 0
    for (var id of Object.keys(response)) {
        console.log(id + " -> " + response[id]['printer_id'])
        console.log(response);
        stl_list[id]['price'] = parseFloat(response[id]['price']);
        
    }

        remove_price_spinner(id);
        update_total_price();
    
        // sudo git add wp-content/plugins/wemake/static/js/BaseClasses/scene.js && sudo git commit -m "ffs"   && sudo git push origin WM-322 
        // git fetch -a && git checkout origin/WM-322 && rm wp-config.php && cp ../wp-config.php .
    
}



function slider_change(id) {

    var range = $(`#infill_slider_range_${id}`).val();
    var value = $(`#infill_range_value_${id}`).html(range);

    stl_list[id]['infill'] = range;

    range.on('input', function () {
        value.html(this.value);
    });

}

function update_total_price() {
    var total_price = 0;    
    var price_processing_flag = false;

    /* Compute the total price, and check if all have finished. */
    for (var id of Object.keys(stl_list)) {
        // Check if the price has changed, if yes update it. 
        
        stl_price = stl_list[id]['price'];
        stl_quantity = stl_list[id]['quantity'];
        console.log(`**** ${stl_price}`);
        if (stl_price != null){
            total_price += ( parseFloat(stl_price) * stl_quantity ); 
        }
        /** 
         * Else... set the price_processing_flag 
         * so that the total price spinner is stll showing
         **/ 
        else{
            price_processing_flag = true;
        }
    }

    /**
     * If price_processing_flag=False, all prices are computed,
     * dislay total price.
     */
    if(!price_processing_flag){
        total_price = parseFloat(total_price).toFixed(2);
        $('#total_price_value').html(`<h2> £${total_price}</h2>`);
    }

}

function display_CADSupport_modal(){
    $("#cad_support_modal").modal('toggle');
}

function display_contact_modal() {
    $("#contact_vendor_modal").modal('toggle');


}

function send_vendor_query() {
    var contactUs_email = $("#contactUs_email").val();
    var contactUs_topic = $("#contactUs_topic").val();
    var contactUs_details = $("#contactUs_details").val();

    response = $.ajax({
        url: 'send_vendor_query/',
        type: 'post',
        success: contact_vendor_success_callback,
        data: {
            email: contactUs_email,
            topic: contactUs_topic,
            description: contactUs_details
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    $("#contact_vendor_modal").modal('hide');
    $("#cad_support_modal").modal('hide');
    // $("#contactUs_details").val('')

}

function contact_vendor_success_callback(response) {
    console.log(response)
}

function send_vendor_cad_query() {
    var contactUs_email = $("#contactUsCad_email").val();
    var contactUs_topic = $("#contactUsCad_topic").val();
    var contactUs_details = $("#contactUsCad_details").val();
    
    response = $.ajax({
        url: 'send_vendor_query/',
        type: 'post',
        success: contact_vendor_success_callback,
        data: {
            email: contactUs_email,
            topic: contactUs_topic,
            description: contactUs_details
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    $("#contact_vendor_modal").modal('hide');
    $("#cad_support_modal").modal('hide');
    // $("#contactUs_details").val('')

}


function add_all_items_to_cart() {
    // Adds all items to the cart
    // by POSTing to backend. 
    request = jQuery.ajax({
        url: 'add_to_cart/',
        type: 'post',
        data:{'stl_list': JSON.stringify(stl_list)},
        success: function (response) {
            window.location.assign(response.url);
        },
        error: function (response) {
            console.log('error');
            console.log(response)
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });

}

function checkout() {

    var error = false;
    Object.keys(stl_list).forEach(function (id) {
        if (stl_list[id]['material'] == "Select") {
            alert(`Select Material for ${stl_list[id]['pretty_name']}`);
            error = true;
            return
        }
        if (stl_list[id]['colour'] == "Select") {
            alert(`Select Colour for ${stl_list[id]['pretty_name']}`);
            error = true;
            return
        }
        if(stl_list[id]['price'] == 0){
            error = true;
            return
        }
    })
    if(!error){
        // Add all items to cart
        add_all_items_to_cart();
        // Redirect to checkout page

    }
}

/**
 *  POPOVER AND OTHER RANDOM STUFF
 */

//**** */
// // Popover:


// Popover:

// function attach_infill_popover(id) {
//     $(`[data-toggle="popover-infill-${id}"]`).popover({
//         trigger: "manual",
//         html: true,
//         animation: false
//     })
//         .on("mouseenter", function () {
//             var _this = this;
//             $(this).popover("show");

//             var range = $(`#infill_slider_range_${id}`),
//                 value = $(`#infill_range_value_${id}`);

//             range.val(value[0].innerHTML); //value.html(this.value)


//             $(".popover").on("mouseleave", function () {
//                 $(_this).popover('hide');
//             });

//         }).on("mouseleave", function () {
//             var _this = this;
//             setTimeout(function () {
//                 if (!$(".popover:hover").length) {
//                     $(_this).popover("hide");
//                 }
//             }, 30);
//         });
// }

// function attach_scale_popover(id) {
//     $(`[data-toggle="popover-scale-${id}"]`).popover({
//         trigger: "manual",
//         html: true,
//         animation: false
//     })
//         .on("mouseenter", function () {
//             var _this = this;
//             $(this).popover("show");

//             $(`#scale_stl_${id}`).val(stl_list[id]['scale']);

//             $(".popover").on("mouseleave", function () {
//                 $(_this).popover('hide');
//             });
//         }).on("mouseleave", function () {
//             var _this = this;
//             setTimeout(function () {
//                 if (!$(".popover:hover").length) {
//                     $(_this).popover("hide");
//                 }
//             }, 30);
//         });
// }

// $('[data-toggle="popover"]').popover({
//     trigger: "manual",
//     html: true,
//     animation: false
// })
//     .on("mouseenter", function () {
//         var _this = this;
//         $(this).popover("show");
//         $(".popover").on("mouseleave", function () {
//             $(_this).popover('hide');
//         });
//     }).on("mouseleave", function () {
//         var _this = this;
//         setTimeout(function () {
//             if (!$(".popover:hover").length) {
//                 $(_this).popover("hide");
//             }
//         }, 30);
//     });


// $('#switch-toggle-all [data-toggle-all]').click(function () {
//     $('#switch-toggle-all input[type="checkbox"]').prop('checked', this.checked)
// });

// $(function () {
//     $('.example-popover').popover({
//         container: 'body'
//     })
// });


// // Button that changes the units between mm and inches
// $('#units-button').click(function () {
//     let _this = $(this)[0];
//     aa = _this.innerText;

//     if (aa == '(mm)') {
//         $(_this).text('(in)');
//         units = 'in';
//         // //console.log(units) ; 
//     }
//     else if (aa == '(in)') {
//         $(_this).text('(mm)');
//         units = 'mm';
//         // //console.log(units) ; 
//     }
//     else { };
//     // if stl_list is set, then loop for each item in the stl list (so apply correction the dim for the ORIGINAL stl, but keep the displayed dim the same)
//     unit_change();
// });






// // OnBoardign (button)
// var myFunc_show = function () {
//     $('#Onboarding_button').popover('show')
// }

// var myFunc_hide = function () {
//     $('#Onboarding_button').popover('hide')
// }

// window.onload = function () {
//     setTimeout(myFunc_show, 1000);
//     setTimeout(myFunc_hide, 3000);
// }


// // 	Onboarding (spotlight)	
// function Onboarding() {

//     ;


//     if (document.getElementById("large-image").classList.contains('hide')) {
//         id = Object.keys(stl_list)[0];

//         introJs().setOptions({
//             showProgress: true,
//             showBullets: false,
//             steps: [
//                 {
//                     element: document.querySelector('#dropzone-button'),
//                     intro: "Click here to add more files"
//                 },
//                 {
//                     element: document.querySelector(`#stl_${id}_material`),
//                     intro: "Edit Settings"
//                 },
//                 {
//                     element: document.querySelector('#checkout'),
//                     intro: "When finished, checkout",
//                     position: 'left'
//                 }
//             ]
//         }).start();
//     }
//     else {
//         id = Object.keys(stl_list)[0];

//         introJs().setOptions({
//             showProgress: true,
//             showBullets: false,
//             exitOnOverlayClick: true,
//             steps: [
//                 {
//                     element: document.querySelector('#dropzone-button'),
//                     intro: "Click here to add more files",
//                     position: 'right'
//                 }
//             ]
//         }).start();
//     }


// };

/**
 *  POPOVER AND OTHER RANDOM STUFF END
 */

/**
 * 
 *  FUTURE FUNCTIONS
 *  FOR ADVANCED OPTIONS ETC..
 * 
 */
//  function scale_change(id) {

//     var final_scale = parseFloat($(`#scale_stl_${id}`).val());
//     var current_scale = stl_list[id]['scale']
//     var scale_factor = final_scale / current_scale;

//     if (scale_factor >= 0.1 && scale_factor <= 10) {
//         // 1. Calculate the original dimension 
//         var orig_dimX = stl_list[id]['dims']['x'] / current_scale;
//         var orig_dimY = stl_list[id]['dims']['y'] / current_scale;
//         var orig_dimZ = stl_list[id]['dims']['z'] / current_scale;

//         var orig_vol = stl_list[id]['volume'] / (current_scale ^ 3);

//         // 2. Scale the original dimension 
//         stl_list[id]['dims']['y'] = orig_dimY * final_scale;
//         stl_list[id]['dims']['x'] = orig_dimX * final_scale;
//         stl_list[id]['dims']['z'] = orig_dimZ * final_scale;

//         stl_list[id]['volume'] = orig_vol * (final_scale ^ 3);

//         stl_list[id]['scale'] = final_scale;

//         $(`#stl_${id}_dimensions_val`).html(`<small> ${parseFloat(stl_list[id]['dims']['x'].toFixed(1))}x${parseFloat(stl_list[id]['dims']['y'].toFixed(1))}x${parseFloat(stl_list[id]['dims']['z'].toFixed(1))} </small>`)

//         get_available_printer(id);
//         // //update_price(scale_factor, id);      < previous version
//         // update_total_price()                 < previous version
//     }

//     else {
//         alert('Scale factor must be between 0.1 and 10!')
//     }
// };

// // Only apply to the 
// function unit_change() {

//     if (Object.keys(stl_list).length == 0) {
//         // no stl's, so don't matter (have set units for any future stl already)
//     }
//     else {
//         // Need to update all the old stl's that were done under the old units
//         // Loop over all the stl's in stl_list
//         for (const [id, value] of Object.entries(stl_list)) {
//             // ;

//             // //console.log(`${key}: ${value}`);
//             stl_list[id].units = units;  // Global 'units' has just been updated, so now update the Local 'units'
//             if (units == 'in') {
//                 // Were wrong about 100 = 100mm, actually 100 = factor*100mm  (100in = 2,540mm)
//                 scale_factor = 25.4;
//             }
//             else if (units == 'mm') {
//                 // Were wrong about 100 = factor*100mm, actually 100 = 100mm  (remove the factor)
//                 scale_factor = 1 / 25.4;
//             }
//             stl_list[id]['dims']['x'] = scale_factor * stl_list[id]['dims']['x'];
//             stl_list[id]['dims']['y'] = scale_factor * stl_list[id]['dims']['y'];
//             stl_list[id]['dims']['z'] = scale_factor * stl_list[id]['dims']['z'];

//             stl_list[id]['volume'] = Math.pow(scale_factor, 3) * stl_list[id]['volume'];

//             // //update_price(scale_factor, id);  < previous version
//             get_available_printer(id);
//         }
//         // update_total_price();                < previous version
//     }

// }