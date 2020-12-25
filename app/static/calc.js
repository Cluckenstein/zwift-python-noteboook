function post(){
    var text = document.getElementById('workout').value;
    /** 
    var responsee = 'a'
    $.ajax({ type: "GET",   
         url: "http://localhost:5000/tester",   
         async: false,
         success : function(text)
         {
             response = text;
         }
    });

    console.log('a')*/
    $.ajax({
        type : 'POST',
        cache : false,
        //url : "{{url_for('tester')}}",
        url: "http://localhost:5000/tester/",  
        data : {'key': text,
                'ftp':document.getElementById('ftp').value},
        dataType: 'json',
        success : function(response)
        {
            console.log(response)
            //fig = JSON.parse(response);
            plot = document.getElementById('plot')
            Plotly.newPlot(plot, response,{})
        }
    });
}

window.onload = function() {
	// setup the button click
	document.getElementById("button_show").onclick = function() {
        console.log('posting  box')
		post()
	};
}