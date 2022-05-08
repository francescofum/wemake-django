var flag_printer_setup_page = 0



$("document").ready(function () {
    console.log("Starting print preview js");
    // Create the dropzone.


    wm_create_dropzone();
   
    // if (cart != null) {
    //     if (cart.cart.length > 0) {
    //         // wm_stl_upload_sending_callback();
    //     }
    //     reload_cart();
    // }



});


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
        url: ajax_object.ajax_url,
        type: 'POST',
        success: contact_vendor_success_callback,
        data: {
            action: 'contact_vendor',
            vendor_id: vendor_id['vendor_id'],
            email: contactUs_email,
            topic: contactUs_topic,
            description: contactUs_details
        }
    });
    $("#contact_vendor_modal").modal('hide');
    $("#cad_support_modal").modal('hide');
    // $("#contactUs_details").val('')

}

function contact_vendor_success_callback(response) {
    console.log(response)

}



function add_all_items_to_cart() {
    // Adds all items to the cart
    // by POSTing to backend. 
    request = jQuery.ajax({
        url: 'add_to_cart/',
        type: 'post',
        data:{'stl_list': JSON.stringify(stl_list)},
        success: function (response) {
            console.log('here');
            var url = `${window.location.origin}/checkout`;
            console.log(url)
            // window.location.assign(url);

        },
        error: function (response) {
            console.log('error');
            console.log(url)
        }
        headers: {
            'X-CSRFToken': csrftoken
        }
    });

}

function checkout() {
    // display_checkout_spinner();
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
