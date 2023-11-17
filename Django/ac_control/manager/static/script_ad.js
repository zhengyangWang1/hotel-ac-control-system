function showRegisterForm() {
    document.getElementById('registerForm').style.display = 'block';
}
  
function closeRegisterForm() {
    document.getElementById('registerForm').style.display = 'none';
    }

function showloginForm(){
    document.getElementById('loginFrom').style.display = 'block';
}

function closeloginForm() {
    document.getElementById('loginFrom').style.display = 'none';
    }

function login() {

    var identity = document.getElementById('identity1').value;
    var username = document.getElementById('username1').value;
    var password = document.getElementById('password1').value;

    if (!identity) {
        alert('请选择身份。');
        return false;
    }
    if (!username) {
        alert('请输入用户名。');
        return false;
    }
    if (!password) {
        alert('请输入密码。');
        return false;
    }
    //在这里进行后台验证

    //在这里执行跳转，但是因为纯前端， window.location方法无法跳转
    window.location = 'tem_c2.html';
    
    return true;
}


function submitForm() {
    var identity = document.getElementById('identity').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;

    // 检查是否选择了房间
    if (!identity) {
        alert('请选择身份');
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
    alert('注册信息已提交！');
    // 这里应该是发送数据到服务器的代码
    // 例如使用 AJAX 或者将表单数据提交到一个服务器端脚本

    return true;
}

