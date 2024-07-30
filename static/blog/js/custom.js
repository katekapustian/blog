function updateClock() {
    var now = new Date();
    var days = ['Sunday 🌞', 'Monday 🌞', 'Tuesday 🌞', 'Wednesday 🌞', 'Thursday 🌞', 'Friday 🌞', 'Saturday 🌞'];
    var day = days[now.getDay()];
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    var strTime = hours + ':' + minutes + ':' + seconds;
    document.getElementById('day').innerHTML = day;
    document.getElementById('clock').innerHTML = strTime;
}

function showRandomQuote() {
    var quotes = [
        "Code is like humor. When you have to explain it, it’s bad.",
        "Experience is the name everyone gives to their mistakes.",
        "In order to be irreplaceable, one must always be different.",
        "Java is to JavaScript what car is to Carpet.",
        "Knowledge is power.",
        "Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday’s code.",
        "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away."
    ];
    var randomIndex = Math.floor(Math.random() * quotes.length);
    document.getElementById('quote').innerHTML = quotes[randomIndex];
}

document.addEventListener('DOMContentLoaded', function() {
    updateClock();
    showRandomQuote();
    setInterval(updateClock, 1000);
});
