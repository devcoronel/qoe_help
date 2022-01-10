let table = document.getElementById("table_sampling")

function build(data) {

    if(typeof(data.msg) === 'object') {
        let elements = data.msg[0]
		let dates = data.msg[1]

		let tablehtml = `<table class="table table-hover" id="mytable">
		<thead class="table-dark">
		<td onclick="sortTable(0, 'mytable')" class="header"><strong>CMTS</strong></td>
		<td onclick="sortTable(1, 'mytable')" class="header"><strong>Plano</strong></td>`
					
		for (let i in dates) {
			let a = parseInt(i)+2
			tablehtml += `<td onclick="sortTable(`+ a +`, 'mytable')" class="header"><strong>`+ dates[i] +`</strong></td>`
		}
		tablehtml += '</thead><tbody>'
		
		for(let i in elements){
			tablehtml += `<td>`+ elements[i][0] +`</td>
			<td><a href="/detail/`+ elements[i][1] +`" target= "_blank">`+ elements[i][1] +`</a></td>`
			
			for (j in elements[i]) {
				if (!(j == 0 || j == 1)) {
					tablehtml += '<td>'+ elements[i][j] +'</td>'
				}
			}
			
			tablehtml += '</tr>'
				
		}
		tablehtml += '</tbody></table>'
		table.innerHTML = tablehtml
    } else{
        table.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>`+data.msg+`</strong>
        </div>
        `
    }
}