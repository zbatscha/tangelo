setInterval(displayclock, 500)
function displayclock() {

    var now = new Date();
    var month = now.getMonth();
    var day = now.getDate();
    var year = now.getFullYear();

    month = month + 1

    if (month < 10) month = '0' + month;
    if (day < 10) day = '0' + day;

    year = year + ""
    year = year.substring(2)

    document.getElementById('date').innerHTML = month + " &nbsp/&nbsp " + day + " &nbsp/&nbsp " + year
}
