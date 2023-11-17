function showRegisterForm() {
    document.getElementById('registerForm').style.display = 'block';
}
  
function closeRegisterForm() {
    document.getElementById('registerForm').style.display = 'none';
    }

function showEnterRoomForm(){
    document.getElementById('enterRoomFrom').style.display = 'block';
}

function closeEnterRoomForm() {
    document.getElementById('enterRoomFrom').style.display = 'none';
    }

function enterRoom() {
//      // 获取选择的房间号
//   var roomNumber = document.getElementById('roomNumber').value;

//   // 保存到localStorage
//   localStorage.setItem('chosenRoomNumber', roomNumber);

//   // 现在你可以重定向到第二个页面，或者做其他事情
//    window.location.href = 'D:\workspace\web\tem_c2.html'; // 如果你想立即重定向

    alert('进入房间的功能尚未实现！');
}



function submitForm() {
    var roomNumber = document.getElementById('roomNumber').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;

    // 检查是否选择了房间
    if (!roomNumber) {
        alert('请选择房间号。');
        return false;
    }

    // 检查用户名是否已填写
    if (!username.trim()) {
        alert('请填写用户名。');
        return false;
    }

    // 检查密码是否已填写
    if (!password) {
        alert('请填写密码。');
        return false;
    }

    // 检查确认密码是否已填写
    if (!confirmPassword) {
        alert('请填写确认密码。');
        return false;
    }

    // 检查密码和确认密码是否一致
    if (password !== confirmPassword) {
        alert('密码和确认密码不一致，请重新输入。');
        return false;
    }
    
    // 所有检查通过后
    alert('入住信息已提交！');
    // 这里应该是发送数据到服务器的代码
    // 例如使用 AJAX 或者将表单数据提交到一个服务器端脚本

    return true;
}

