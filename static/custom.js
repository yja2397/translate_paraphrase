function translate(message) {
    $.post("/translate", {
        message: message,
    }, handle_response);

    function handle_response(data) {

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

$('#login').on('submit', function(e){
    e.preventDefault();

    console.log("HO");

    $.post("/login", {
        userid: $('#userid').val(),
        pswd: $('#pswd').val(),
    }, handle_response);

    console.log("NO?");

    function handle_response(data) {
        console.log("ON?");

        if(`${data.connect}` == "0"){
            location.href="index.html";
        }else{
            if(`${data.connect}` == "1"){
                alert("존재하지 않는 아이디입니다.");
            }else{
                alert("비밀번호가 틀렸습니다.");
            }
            location.href="login.html";
        }
    }
});

$('#join').on('submit', function(e){
    e.preventDefault();

    $.post("/join", {
        userid: $('#userid').val(),
        pswd: $('#pswd').val(),
    }, handle_response);

    function handle_response(data) {
        if(`${data.connect}` == "0"){
            alert("회원가입을 축하합니다. 자동 로그인됩니다.");
            location.href="index.html";
        }else{
            alert("이미 존재하는 아이디입니다.")
            location.href="join.html";
        }
    }

});


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

function save(){    
    if ($("#writeInput").length){
        text = $.trim($("#writeInput").text());

        $.post("/save", {
            text: text,
        }); // db 삽입
    
        function handle_response(data) {
            alert(`${data.message}`);
        }

    }else{
        alert("저장할 내용이 없습니다.")
    }


}

function logout(){
    if(confirm('정말 로그아웃하시겠습니까?')){
        $.post("/logout");
        location.href="index.html";
    }
}

function speakPara(order){
    message = $.trim($('.order' + order).text());

    $.post("/speak", {
        message: message,
    }); // 말하기
    
}

function load(order){
    time = $.trim($('.order' + order).text());

    $.post("/load", {
        message : message,
    }) // 글 불러오기

    var para = $('.paragraph')
    if ($("#write span").length){
        $("#write span").remove();
        $("#write").append(`
            <textarea id="writeInput" cols="40" rows="8" >
                ${message}
            </textarea>
        `)
    }else{
        $("#writeInput").remove();

        $("#write").append(`
            <textarea id="writeInput" cols="40" rows="8" >
                ${message}
            </textarea>
        `)

    }
}

function goPara(order){
    message = $.trim($('.order' + order).text());

    $.post("/insert", {
        message: message,
    }); // db 삽입

    var para = $('.paragraph')
    if ($("#write span").length){
        $("#write span").remove();
        $("#write").append(`
            <textarea id="writeInput" cols="40" rows="8" >
                ${message}
            </textarea>
        `)
    }else{
        text = $.trim($("#writeInput").text() + " " + message);
        
        $("#writeInput").remove();

        $("#write").append(`
            <textarea id="writeInput" cols="40" rows="8" >
                ${text}
            </textarea>
        `)

    }
}