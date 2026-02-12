const form = document.getElementById("aqiForm");
const output = document.getElementById("aqiOutput");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    output.innerText = "Predicting AQI... ⏳";

    const data = {
        date: document.getElementById("date").value,
        city: document.getElementById("city").value,
        pm25: parseFloat(document.getElementById("pm25").value),
        pm10: parseFloat(document.getElementById("pm10").value),
        no2: parseFloat(document.getElementById("no2").value),
        co: parseFloat(document.getElementById("co").value),
        temp: parseFloat(document.getElementById("temp").value),
        humidity: parseFloat(document.getElementById("humidity").value),
        retail_mobility: parseFloat(document.getElementById("retail_mobility").value),
        workplace_mobility: parseFloat(document.getElementById("workplace_mobility").value),
        transit_mobility: parseFloat(document.getElementById("transit_mobility").value),
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            output.innerText = "❌ " + result.error;
        } else {
            output.innerText =
                `Predicted AQI: ${result.predicted_aqi.toFixed(2)} (${result.category})`;
        }

    } catch (err) {
        output.innerText = "❌ Cannot connect to backend server";
    }
});
