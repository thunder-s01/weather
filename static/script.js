function getLocation() {
    // check browser support
    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(

            // ✅ SUCCESS
            function(position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;

                console.log("Lat:", lat, "Lon:", lon);

                // redirect to Flask route
                window.location.href = `/location?lat=${lat}&lon=${lon}`;
            },

            // ❌ ERROR
            function(error) {
                console.log(error);

                if (error.code === 1) {
                    alert("❌ Location permission denied. Please allow location.");
                } 
                else if (error.code === 2) {
                    alert("❌ Location unavailable.");
                } 
                else if (error.code === 3) {
                    alert("❌ Request timed out.");
                } 
                else {
                    alert("❌ Unknown error occurred.");
                }
            }

        );

    } else {
        alert("❌ Geolocation is not supported by this browser.");
    }
}