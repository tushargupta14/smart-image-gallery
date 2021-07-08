

function upLoadPhoto(){

    let file = document.getElementById('inputFile').files[0];
    let file_name = file.name;
    let file_type = file.type;
    let reader = new FileReader();
	
    reader.onload = function() {
		 
        let arrayBuffer = this.result;
        let blob = new Blob([new Int8Array(arrayBuffer)], {
            type: file_type
        });
        let blobUrl = URL.createObjectURL(blob);

        $("#addPic").attr('src', blobUrl);
        $("#addContain").removeClass('hide');
        document.getElementById('addName').innerText = "Add File: " +file_name;
		
        let data = document.getElementById('inputFile').files[0];
		
		let xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.addEventListener("readystatechange", function () {
            if (this.readyState === 4) {
                console.log(this.responseText);
            }
        });
        xhr.withCredentials = false;
        let label = prompt("Please enter Image Label", "Mountain");
		if(label !== undefined && label !== null)
		{
			xhr.open("PUT", "https://rm5xe4tzk7.execute-api.us-east-1.amazonaws.com/dev/upload");
			xhr.setRequestHeader("filename", file_name);
			xhr.setRequestHeader("labels", label);
			xhr.setRequestHeader("Content-Type", data.type);
			xhr.send(data);
		}
		
	}
	 
		
    reader.readAsArrayBuffer(file);

}

function diaplayItem(src, file_name) {
    let $template = $(
       ` <div class="card col-md-4">
            <img class="card-img-top" src=${src}>
            <p class="card-text">${file_name}</p>
        </div>
        <br>`
    );
    $('#picContain').append($template);
    if ($('#albumContain').hasClass('hide')) {
        $('#albumContain').removeClass('hide');
    }
}

function searchPhoto() {
    $('#albumContain').addClass('hide');
    $('#addContain').addClass('hide');
    $('#picContain').empty();

    let value_input = $('#searchValue');
    let search_sentence = value_input.val();
    value_input.val('');

    let params ={
        q: search_sentence,
    };
    apigClient.searchGet(params, {}, {}).then((res)=>{
            console.log(res);
    // todo use display item function here to create new pictures
    let body = res['data']['body'];
    if(JSON.stringify(body) === '{}'){
        alert(`There is not image matches your search!`)
    }
    for(let key in body) {
      let test_src = body[key];
      let test_name = key;
      console.log(key);
      diaplayItem(test_src, test_name);
    }

  }
    ).catch((e)=>{
        console.log('Error');
    })

}