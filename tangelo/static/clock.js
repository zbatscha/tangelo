setInterval(displayclock, 500)
function displayclock() {

    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    var month = now.getMonth();
    var day = now.getDate();
    var year = now.getFullYear();

    if (hour > 12) {
        hour = hour - 12
    }

    if (hour == 0) {
        hour = 12
    }

    month = month + 1

    if (hour < 10) hour = '0' + hour;
    if (minute < 10) minute = '0' + minute;
    if (second < 10) second = '0' + second;
    if (month < 10) month = '0' + month;
    if (day < 10) day = '0' + day;

    year = year + ""
    year = year.substring(2)

    document.getElementById('time').innerHTML = hour + "&nbsp&nbsp" + minute + "&nbsp&nbsp" + second
    document.getElementById('date').innerHTML = month + " &nbsp/&nbsp " + day + " &nbsp/&nbsp " + year
}