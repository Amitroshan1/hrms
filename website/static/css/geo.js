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
        .then(response => {
          if (!response.ok) {
            return response.json().then(err =>
              Promise.reject(new Error(err.message || "Server error"))
            );
          }
          return response.json();
        })
        .then(data => {
          alert(data.message);
        })
        .catch(error => {
          console.error("🔴 Fetch Error:", error);
          alert("❌ Something went wrong: " + error.message);
        });
    },
    (error) => {
      console.error("🛑 Geolocation Error:", error.message);
      alert("📍 Location access denied. Please allow location access to punch in/out.");
    }
  );
}

document.getElementById("punchInBtn").addEventListener("click", (event) => {
  event.preventDefault(); // 🛑 Prevent form submission or reload
  sendPunch("punch_in");
});

document.getElementById("punchOutBtn").addEventListener("click", (event) => {
  event.preventDefault(); // 🛑 Prevent form submission or reload
  sendPunch("punch_out");
});