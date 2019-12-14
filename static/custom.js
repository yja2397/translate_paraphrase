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
        $( "#myProgress" ).remove();
	}
}

i = 0;
setInterval(function() {
    i = ++i % 4;
    $(".loading").text("Loading sentences " + Array(i+1).join("."));
}, 800);

$('#login').on('submit', function(e){
    e.preventDefault();

    $.post("/login", {
        userid: $('#userid').val(),
        pswd: $('#pswd').val(),
    }, handle_response);

    function handle_response(data) {
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

    /* 회원가입 자바스크립트 */
    if(invalidItem()){

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
    }
});

    //유효성 체크할 함수
function invalidItem() {
    // 아이디 체크
    if($("input[name=userid]").val() == '') {
        alert("아이디를 입력하세요.");
        $("input[name=userid]").focus();

        return false;
    }

    // 비밀번호 체크
    if($("input[name=pswd]").val() == ''){
        alert("비밀번호를 입력하세요");
        $("input[name=pswd]").focus();

        return false;
    }

    return true;
}


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
        <div id="myProgress">
            <div id="myBar">
            </div>
        </div>
        <script>
            $(document).ready(function(){ move(); });
        </script>
    `);


        // clear the text input 
    $input_message.val('');

    var div = document.getElementsByClassName("conversation-view")[0];
    div.scrollTop = div.scrollHeight;
    
    // send the message
    translate(input_message);
});

function move() {
    var i = 0;
    if (i == 0) {
        i = 1;
        var elem = $("#myBar");
        var width = 1;
        var id = setInterval(frame, 130);
        function frame() {
            if (width >= 99) {
                clearInterval(id);
                i = 0;
            } else {
                width++;
                if (width < 50 && width % 4 == 0){
                    elem.width(width + "%");
                }else if(width > 50 && width % 2 == 0){
                    elem.width(width + "%");
                }
            }
        }
    }
}

function copy(){
    if ($("#writeInput").length){
        var copyText = document.getElementById("writeInput");
    
        copyText.select();
        copyText.setSelectionRange(0,99999);
    
        document.execCommand("copy");
    
        alert("복사되었습니다.");
    }else{
        alert("복사할 내용이 없습니다.")
    }
}

function save(){    
    if ($("#writeInput").length){
        text = $.trim($("#writeInput").text());

        title = prompt("글 제목");

        $.post("/save", {
            text: text,
            title: title,
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
        setTimeout(function(){
            location.href="index.html";
        }, 1000);
    }
}

function speakPara(order){
    message = $.trim($('.order' + order).text());

    $.post("/speak", {
        message: message,
    }); // 말하기
    
}

$(".subj").click(function() {
    time = $.trim($('.order' + String($(".subj").index(this))).text());
    
    $.post("/load", {
        time : time,
    }, handle_response); // 글 불러오기

    function handle_response(data) {
        if ($("#write span").length){
            $("#write span").remove();
            $("#view span").remove();

            $("#write").append(`
                <textarea id="writeInput" cols="40" rows="8" >
                    ${data.message}
                </textarea>
            `);
            $("#view").append(`
                <textarea id="viewInput" cols="40" rows="8" >
                    ${data.translated}
                </textarea>
            `);
        }else{
            $("#writeInput").remove();
            $("#viewInput").remove();

            $("#write").append(`
                <textarea id="writeInput" cols="40" rows="8" >
                    ${data.message}
                </textarea>
            `);
            $("#view").append(`
                <textarea id="viewInput" cols="40" rows="8" >
                    ${data.translated}
                </textarea>
            `);
        }
    }
});

function goPara(order){
    message = $.trim($('.order' + order).text());

    if ($("#write span").length){
        text = message;

        $.post("/insert", {
            message: message,
            text: text
        }, handle_response); // db 삽입
        
        function handle_response(data) {
            $("#write span").remove();
            $("#view span").remove();

            $("#write").append(`
                <textarea id="writeInput" cols="40" rows="8" >
                    ${message}
                </textarea>
            `);
            $("#view").append(`
                <textarea id="viewInput" cols="40" rows="8" >
                    ${data.translated}
                </textarea>
            `);
        }
    }else{
        text = $.trim($("#writeInput").val() + " " + message);

        $.post("/insert", {
            message: message,
            text: text
        }, handle_response); // db 삽입

        function handle_response(data) {
            $("#writeInput").remove();
            $("#viewInput").remove();

            $("#write").append(`
                <textarea id="writeInput" cols="40" rows="8" >
                    ${text}
                </textarea>
            `);
            $("#view").append(`
                <textarea id="viewInput" cols="40" rows="8" >
                    ${data.translated}
                </textarea>
            `);
        }

    }
}

function deleteSen(){
    if($(".checkbox").css("display") == "none"){
        $(".checkbox").show();
    }else{
        var checkedSen = "";

        $("input[name=chk]:checked").each(function(i){
            checkedSen += $(this).val();
            checkedSen += ", "
        });

        $.post("/deleteSen", {
            deleteSen: checkedSen,
        });
        // 삭제 sentence들.

        $(".checkbox").hide();
        setTimeout(function(){
            location.reload();
        }, 1000);
    }
}

function deletePara(){
    if($(".checkbox").css("display") == "none"){
        $(".checkbox").show();
    }else{
        var checkedPara = "";

        $("input[name=chk]:checked").each(function(i){
            checkedPara += $(this).val();
            checkedPara += ", ";
        });

        $.post("/deletePara", {
            deletePara: checkedPara,
        });
        // 삭제 글들.

        $(".checkbox").hide();
        setTimeout(function(){
            location.reload();
        }, 1000);
    }
}

function gogogo(){

	// 클릭한 체크박스의 table 에서 (바로위 부모요소를 대상)
	// 이름이 chk 인것을 찾고
	// 현재 요소의 체크 상태를 찾은 대상에 적용
    if($("#allCheck").prop("checked")) { //해당화면에 전체 checkbox들을 체크해준다 
        $("input[type=checkbox]").prop("checked",true); // 전체선택 체크박스가 해제된 경우 
    } else { //해당화면에 모든 checkbox들의 체크를해제시킨다. 
        $("input[type=checkbox]").prop("checked",false); }
}