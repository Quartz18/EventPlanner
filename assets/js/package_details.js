$(document).ready(function(){
  $(".candid_photo").hide();
  $(".event_photo").hide();
  $(".videography").hide();
  $(".non_veg").hide();
  $("#edit_name_form").hide();
  $("#edit_photographer_form").hide();
  $("#edit_decor_form").hide();
  $("#edit_food_form").hide();
  $("#edit_party_form").hide();
  $("#delete_image_form").hide();
  $("#outside_travel_price").hide();
  $("#edit_policy_form").hide();
  $("#outside_alcohol").hide();
  $(".room_info").hide();
  $("#late_music").hide();
  $("#more_content").hide();
  $("#dots").show();
  $("#edit_contact_form").hide();
  $("#edit_address_form").hide();
  $("#edit_time_form").hide();
  $("#edit_image_form").hide();
  $("#videography").click(function(){
    $(".videography").toggle(this.checked);
});
  $("#event_photo").click(function(){
    $(".event_photo").toggle(this.checked);
});
  $("#candid_photo").click(function(){
    $(".candid_photo").toggle(this.checked);
});
  $("#edit_photographer_button").click(function(){
    $("#edit_photographer_form").toggle();
});
  $("#edit_name_button").click(function(){
      $("#edit_name_form").toggle();
  });
  $("#edit_decor_button").click(function(){
      $("#edit_party_form").hide();
      $("#edit_food_form").hide();
      $("#edit_decor_form").toggle();
  });
  $("#non_veg_food").click(function(){
      $(".non_veg").toggle(this.checked);
  });
  $("#edit_food_button").click(function(){
      $("#edit_party_form").hide();
      $("#edit_decor_form").hide();
      $("#edit_food_form").toggle();
  });
  $("#edit_party_button").click(function(){
      $("#edit_food_form").hide();
      $("#edit_decor_form").hide();
      $("#edit_party_form").toggle();
  });
  $("#travel_allowance").click(function(){
      $("#outside_travel_price").toggle(this.checked);
  });
  $("#edit_policy_button").click(function(){
      $("#edit_policy_form").toggle();
  });
  $("#alcohol_allowance").click(function(){
      $("#outside_alcohol").toggle(this.checked);
  })
  $("#venue_room_available").click(function(){
      $(".room_info").toggle(this.checked);
  })
  $("#music_allowance").click(function(){
      $("#late_music").toggle(this.checked);
  })
  $("#edit_time_button").click(function(){
    $("#edit_time_form").toggle();
  });
  $("#edit_image_button").click(function(){
      $("#edit_image_form").toggle();
  });
  $("#edit_address_button").click(function(){
      $("#edit_address_form").toggle();
  });
    $("#edit_contact_button").click(function(){
      $("#edit_contact_form").toggle();
  });
  $("#delete_image_button").click(function(){
      $("#delete_image_form").toggle();
  }); 
});

readMoreFunc()

function readMoreFunc() {
  var dots = document.getElementById("dots");
  var moreText = document.getElementById("more_content");
  var btnText = document.getElementById("read_more_btn");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more"; 
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less"; 
    moreText.style.display = "inline";
  }
}
function logging_out_confirm(){
          
  var r = confirm("Are you sure you want to logout?");
  if (r == true){
      window.location.replace("{% url 'logout_page' %}");
  }
}
function food_package_show(package) {
    var package_id = package.getAttribute("data-package");
    var modal = document.getElementById("package_model");
    var modal_body = document.getElementById("package_model_check");
    modal.style.display = "block";
    const xhttp = new XMLHttpRequest();
    const method = 'GET'
    const url ='/Vendor/foodDetail/'+package_id+'/'
    const responseType = "json"
    xhttp.responseType = responseType
    xhttp.open(method, url)
    xhttp.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest")                
    xhttp.onload = function(){
    console.log(xhttp.response)
    const serverResponse = xhttp.response
    var listedItems = serverResponse.vendor_list
    console.log(listedItems)
    modal_body.innerHTML = `
        <div class="card m-1">
          <div class="card-header">
          ${listedItems.package_name}
          </div>
          <div class="card-body">
              <table class="table table-hover">
                <thead>
                  <tr>
                      <th>Dishes</th>
                      <th>Types</th>
                  </tr>
                </thead>
                <tbody>
                <tr>
                <td>Salads</td>
                <td>${listedItems.salads}</td>
                </tr>
                <tr>
                <td>Veg Starter</td>
                <td>${listedItems.veg_starter}</td>
                </tr>
                <tr>
                <td>Veg Main Course</td>
                <td>${listedItems.veg_main_course}</td>
                </tr>
                <tr>
                <td>Raita</td>
                <td>${listedItems.raita}</td>
                </tr>
                <tr>
                <td>Dessets</td>
                <td>${listedItems.dessert}</td>
                </tr>
                <tr>
                <td>Assorted rotis/breads</td>
                <td>${listedItems.rotis_bread}</td>
                </tr>
                <tr>
                <td>Rice/Biryani</td>
                <td>${listedItems.rice_biryani}</td>
                </tr>
                <tr>
                <td>dal</td>
                <td>${listedItems.dal}</td>
                </tr>
                <tr>
                <td>welcome_drinks</td>
                <td>${listedItems.welcome_drinks}</td>
                </tr>
                <tr>
                <td>Soup</td>
                <td>${listedItems.soup}</td>
                </tr>
                </tbody>
              </table>
          </div>
        </div>
        `
    var span = document.getElementsByClassName("close")[0];
    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }
  }
  xhttp.send()
  }

function decor_package_show(package) {
  var package_id = package.getAttribute("data-package");
  var modal = document.getElementById("package_model");
  var modal_body = document.getElementById("package_model_check");
  modal.style.display = "block";
  const xhttp = new XMLHttpRequest();
  const method = 'GET'
  const url ='/Vendor/decorDetail/'+package_id+'/'
  const responseType = "json"
  xhttp.responseType = responseType
  xhttp.open(method, url)
  xhttp.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest")                
  xhttp.onload = function(){
  console.log(xhttp.response)
  const serverResponse = xhttp.response
  var listedItems = serverResponse.vendor_list
  console.log(listedItems)
  modal_body.innerHTML = `
      <div class="card m-1">
        <div class="card-header">
        ${listedItems.package_name}
        </div>
        <div class="card-body">
            <table class="table table-hover">
              <thead>
                <tr>
                    <th>Equipment</th>
                    <th>Available</th>
                </tr>
              </thead>
              <tbody>
              <tr>
              <td>Stage</td>
              <td>${listedItems.stage}</td>
              </tr>
              <tr>
              <td>Veg Lights</td>
              <td>${listedItems.lights}</td>
              </tr>
              <tr>
              <td>Flowers</td>
              <td>${listedItems.flowers}</td>
              </tr>
              <tr>
              <td>Tables/Chairs</td>
              <td>${listedItems.furniture}</td>
              </tr>
              <tr>
              <td>Entrance</td>
              <td>${listedItems.entrance}</td>
              </tr>
              <tr>
              <td>Lounge</td>
              <td>${listedItems.lounge}</td>
              </tr>
              </tbody>
            </table>
        </div>
      </div>
      `
  var span = document.getElementsByClassName("close")[0];
  span.onclick = function() {
      modal.style.display = "none";
  }
  window.onclick = function(event) {
  if (event.target == modal) {
      modal.style.display = "none";
  }
  }
}
xhttp.send()
}

function photographer_package_show(package) {
  var package_id = package.getAttribute("data-package");
  var modal = document.getElementById("package_model");
  var modal_body = document.getElementById("package_model_check");
  modal.style.display = "block";
  const xhttp = new XMLHttpRequest();
  const method = 'GET'
  const url ='/Vendor/photographerDetail/'+package_id+'/'
  const responseType = "json"
  xhttp.responseType = responseType
  xhttp.open(method, url)
  xhttp.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest")                
  xhttp.onload = function(){
  console.log(xhttp.response)
  const serverResponse = xhttp.response
  var listedItems = serverResponse.vendor_list
  console.log(listedItems)
  modal_body.innerHTML = `
      <div class="card m-1">
        <div class="card-header">
        ${listedItems.package_name}
        </div>
        <div class="card-body">
            <table class="table table-hover">
              <thead>
                <tr>
                    <th>Types</th>
                    <th>Available</th>
                    <th>Duration</th>
                    <th>Total Photographers</th>
                </tr>
              </thead>
              <tbody>
              <tr>
              <td>Candid Photo</td>
              <td>${listedItems.candid_photo}</td>
              <td>${listedItems.candid_photo_dur}</td>
              <td>${listedItems.candid_person}</td>
              </tr>
              <tr>
              <td>Event Photo</td>
              <td>${listedItems.event_photo}</td>
              <td>${listedItems.event_photo_dur}</td>
              <td>${listedItems.event_photo_dur}</td>
              </tr>
              <tr>
              <td>Videography</td>
              <td>${listedItems.videography}</td>
              <td>${listedItems.video_dur}</td>
              <td>${listedItems.video_person}</td>
              </tr>
              </tbody>
            </table>
        </div>
      </div>
      `
  var span = document.getElementsByClassName("close")[0];
  span.onclick = function() {
      modal.style.display = "none";
  }
  window.onclick = function(event) {
  if (event.target == modal) {
      modal.style.display = "none";
  }
  }
}
xhttp.send()
}

function service_deletion(pointer){
  var modal = document.getElementById("package_model");
  var modal_body = document.getElementById("package_model_check");
  modal.style.display = "block"; var formattedMode="";
  
var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
  modal.style.display = "none";
}
window.onclick = function(event) {
if (event.target == modal) {
  modal.style.display = "none";
}
}
}
