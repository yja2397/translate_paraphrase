// const pusher2 = new Pusher("777da506507b1625a6b2", {
//     cluster: "ap3",
// 	encrypted: true
// });

// // Subscribe to translate-searcher channel
// const channel = pusher2.subscribe('translate-searcher');

function translate(message) {
    
    console.log('번역기.');

    $.post("/translate", {
        message: message,
    }, handle_response);

    function handle_response(data) {
    
        console.log('응답.');

        // append the bot repsonse to the div
        $('.conversation-view').empty(); // 안의 내용 지우기
        
		if(`${data.result}` == "null"){ // 내용이 없어도 일단 입력내용 송출
			console.log(`${data.result}`); // 에러코드 보여주기
			$('.conversation-view').append(`
                <div class="input">
                    ${data.message}
                </div>
			`);
		} else{ // 결과 송출
			$('.conversation-view').append(`
                <div class="input">
                    ${data.message}
                </div>
                ${data.result}
			`);
        }
        // remove the loading indicator
        $( "#loading" ).remove();
	}
}

i = 0;
setInterval(function() {
    i = ++i % 4;
    $(".loading").text("Loading sentences " + Array(i+1).join("."));
}, 800);


$('#target').on('submit', function(e){
    e.preventDefault();
    var $input_message = $('#input_message');
    var $conversation_view = $('.conversation-view');

    const input_message = $input_message.val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $conversation_view.empty();

    $conversation_view.append(`
        <div class="chat-bubble me">
            <span class="chat-content">
                ${input_message}
            </span>
        </div>
	`);
    // loading
    $conversation_view.append(`
        <div class="chat-bubble" id="loading">
            <span class="chat-content">
                <b class="loading">Loading sentences</b>
            </span>
        </div>
	`);

        // clear the text input 
    $input_message.val('');

    var div = document.getElementsByClassName("conversation-view")[0];
    div.scrollTop = div.scrollHeight;

    console.log(input_message);
    
    // send the message
    translate(input_message);
});

function copy(){
    if ($("#writeInput").length){
        var copyText = document.getElementById("writeInput");
    
        copyText.select();
        copyText.setSelectionRange(0,99999);
    
        document.execCommand("copy");
    
        alert("복사되었습니다.");
    
        console.log(copyText.value);

    }else{
        alert("복사할 내용이 없습니다.")
    }
}

function goPara(message){
    var para = $('.paragraph')
    if ($("#write span").length){
        $("#write span").remove();
        $("#write").append(`
            <textarea id="writeInput" cols="40" rows="8" >
                ${message}
            </textarea>
        `)
    }else{
        text = $("#writeInput")
        $('#writeInput').append(`
            ${message}
        `)
    }
}