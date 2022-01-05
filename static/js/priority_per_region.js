let region = document.getElementById("region")

region.addEventListener('change', function(e){
    e.preventDefault();
    console.log("cambio")
    console.log(region.value)

    fetch('/priority' , {
		method: 'POST',
		body: JSON.stringify({
            region: region.value
        })
	})

})