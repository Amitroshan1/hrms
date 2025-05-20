function sendPunch(action) {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by your browser.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;

      fetch("/punch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          action: action,
          latitude: latitude,
          longitude: longitude
        })
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
      })
      .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong.");
      });
    },
    (error) => {
      alert("Error getting location: " + error.message);
    }
  );
}

document.getElementById("punchInBtn").addEventListener("click", () => {
  sendPunch("punch_in");
});

document.getElementById("punchOutBtn").addEventListener("click", () => {
  sendPunch("punch_out");
});
