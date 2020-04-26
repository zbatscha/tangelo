
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
} else {
    let x = document.getElementById("demo");
    x.innerHTML = "Geolocation is not supported by this browser.";
}

function showPosition(position) {

    let coordinates = {
          lat: position.coords.latitude,
          long: position.coords.longitude,
    };
    $.ajax({
      type : 'POST',
      url : '/updateWeather',
      data : JSON.stringify({"coordinates": coordinates}),
      dataType: "json",
      contentType: "application/json",
      success: function (response) {
        response = JSON.parse(response);
        if response.success {
          document.getElementById('temperature').innerHTML = response.temperature;
          document.getElementById('sky').innerHTML = response.description;
        }
      },
    });
};
