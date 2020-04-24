var x = document.getElementById("demo");
var long
var lat

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
} else {
    x.innerHTML = "Geolocation is not supported by this browser.";
}

function showPosition(position) {

    let coordinates = {
          lat: position.coords.latitude,
          long: position.coords.longitude,
    };
    $.ajax({
      type : 'POST',
      url : "{{ url_for('updateWeather') }}",
      data : JSON.stringify({"coordinates": coordinates}),
      dataType: "json",
      contentType: "application/json",
      success: function (response) {
          alert(response);
          document.getElementById('temperature').innerHTML = response.temperature;
          document.getElementById('sky').innerHTML = response.description;
       },
    });
};
