let region = document.getElementById("region")

region.addEventListener('change', function(e){
  e.preventDefault();

  fetch('/sampling' , {
	method: 'POST',
	body: JSON.stringify(
            region.value
        )
	})
    .then(response => response.json())
	.then(data => {
        if(typeof(data.msg) === 'object') {
            build(data)
        } else{
            mytable.innerHTML = data.msg
        }
    })
    .catch(err => {
        console.log(err)
        mytable.innerHTML =
        `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>Se detectó excesivas peticiones a la Base de Datos en un tiempo corto. Intentar de nuevo</strong>
        </div>
        `
    })
})