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
        widget_id: "weather",
        coordinates: {
          lat: position.coords.latitude,
          long: position.coords.longitude,
        }
      };
      $.ajax({
        type : 'POST',
        url : "{{url_for('updateWeather')}}",
        data : JSON.stringify({"coordinates": coordinates}),
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            var temp = ((response.main.temp - 273.15) * 9/5 + 32).toFixed(1)
            temp += " °F"
            document.getElementById('temperature').innerHTML = temp;
            document.getElementById('sky').innerHTML = response.weather[0].description;
            console.log(data.weather[0].description);
           },
      });
}

// function serverrequest() {
//     if (long != null) {
//         fetch("https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + long +"&appid=ff9101a1b97b3e7617260a4da9012daa")
//         .then((response) => {
//             return response.json();
//         })
//         .then((data) => {
//             var temp = ((data.main.temp - 273.15) * 9/5 + 32).toFixed(1)
//             temp += " °F"
//             document.getElementById('temperature').innerHTML = temp;
//             document.getElementById('sky').innerHTML = data.weather[0].description;
//             console.log(data.weather[0].description);
//         });
//     } else {
//         setTimeout(serverrequest, 300)
//     }
// };

