const ctx = document.getElementById('pulseChart').getContext('2d');

let signalData = [];

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Pulse Signal',
            data: [],
            borderWidth: 2,
            tension: 0.3
        }]
    },
    options: {
        animation: false,
        responsive: true,
        scales: {
            x: {
                display: false
            }
        }
    }
});

function updateChart() {

    fetch('/signal')
        .then(res => res.json())
        .then(data => {

            document.getElementById("bpm").innerHTML =
                "Heart Rate: " + data.bpm + " BPM";

            document.getElementById("freq").innerHTML =
                "Frequency: " + data.frequency + " Hz";

            chart.data.labels = data.signal.map((_, i) => i);
            chart.data.datasets[0].data = data.signal;

            chart.update();
        });
}

setInterval(updateChart, 1000);