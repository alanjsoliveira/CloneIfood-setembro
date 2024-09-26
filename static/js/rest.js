/*Interação ver mais informações do restaurante*/
document.getElementById("verMaisBtn").addEventListener("click", function() {
    var maisInfo = document.getElementById("maisInfo");
    if (maisInfo.style.display === "none") {
        maisInfo.style.display = "block";
        document.getElementById("verMaisBtn").textContent = "Ver menos";
    } else {
        maisInfo.style.display = "none";
        document.getElementById("verMaisBtn").textContent = "Ver mais";
    }
});

