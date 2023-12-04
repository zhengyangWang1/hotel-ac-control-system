var temperatureSlider = document.getElementById("temperature-slider");
var temperatureValue = document.getElementById("temperature");
var fanSpeedSlider = document.getElementById("fan-speed-slider");
var fanSpeedValue = document.getElementById("fan-speed");
var modeSelector = document.getElementById("mode-selector");
var acToggleBtn = document.getElementById("ac-toggle");
var acStatusText = document.getElementById("ac-status-text");
var isACOn = true;
var room_id = 101;

// 禁用控件
// function disableControls() {
//     temperatureSlider.disabled = true;
//     fanSpeedSlider.disabled = true;
//     modeSelector.disabled = true;
// }
//
// // 启用控件
// function enableControls() {
//     temperatureSlider.disabled = false;
//     fanSpeedSlider.disabled = false;
//     modeSelector.disabled = false;
// }
//
// // 初始化禁用控件
// // disableControls();
// enableControls()

temperatureSlider.addEventListener("input", function() {
    if (isACOn) {
        temperatureValue.innerText = temperatureSlider.value + "°C";
    } else {
        this.value = temperatureValue.innerText.slice(0, -2); // 重置滑块
        alert('空调未开启！');
    }
});

fanSpeedSlider.addEventListener("input", function() {
    if (isACOn) {
        var fanSpeed = fanSpeedSlider.value;
        fanSpeedValue.innerText = fanSpeed === "1" ? "低风" : fanSpeed === "2" ? "中风" : "高风";
    } else {
        this.value = fanSpeedValue.innerText === "低风" ? "1" : fanSpeedValue.innerText === "中风" ? "2" : "3"; // 重置滑块
        alert('空调未开启！');
    }
});

modeSelector.addEventListener("change", function() {
    if (!isACOn) {
        this.value = this.getAttribute('data-prev');
        alert('空调未开启！');
    } else {
        this.setAttribute('data-prev', this.value);
    }
});

// 初始化时设置模式选择器的data-prev属性
modeSelector.setAttribute('data-prev', modeSelector.value);


function toggleAC() {
    var room_id = document.querySelector('input[name="room_id"]').value;
    var newState = isACOn ? 'off' : 'on'; // 根据当前状态决定新状态

    // 发送AJAX请求
    $.ajax({
        type: "POST",
        url: newState === 'on' ? '/open_ac' : '/close_ac', // 根据状态选择URL
        data: { room_id: room_id },
        success: function(response) {
            // 根据响应更新状态
            isACOn = newState === 'on';
            acToggleBtn.textContent = isACOn ? "关闭" : "开启";
            acStatusText.textContent = isACOn ? "空调已开启" : "空调已关闭";

            // 根据空调状态启用或禁用控件
            if (isACOn) {
                enableControls();
            } else {
                disableControls();
            }
        },
        error: function(error) {
            console.error("Error:", error);
            alert('无法更改空调状态！');
        }
    });
}


 //退房函数
 document.getElementById('checkout').addEventListener('click', function(event) {
    event.preventDefault(); // 阻止链接默认行为
    if (confirm('确定要退房吗？')) {
        // 用户确认退房
        fetch('/path-to-your-backend-endpoint', {
            method: 'POST', // 或者你需要的方法
            // 其他请求参数
        })
        .then(response => response.json())
        .then(data => {
            // 处理返回的数据
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});


// JavaScript函数，处理开启和关闭空调的Ajax请求
function handleAcAction_roomState(event) {
    event.preventDefault();  // 阻止表单的默认提交行为

    var form = event.target; // 获取触发事件的表单
    var url = form.action;   // 表单的action属性指向后端的URL
    var formData = new FormData(form); // 创建一个FormData对象，包含表单数据
    console.log("handleAcAction被调用"); // 输出调试信息
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken() // 获取CSRF Token
        }
    })
    .then(response => response.json())
    .then(data => {
        // 假设后端返回的数据包含room_state字段
        document.getElementById('room_state').textContent = data.room_state;
    })
    .catch(error => console.error('Error:', error));
}

// 从cookie中获取CSRF Token
function getCsrfToken() {
    var name = 'csrftoken';
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 添加事件监听器到表单
document.getElementById('ac_open_panel').addEventListener('submit', handleAcAction_roomState);
document.getElementById('ac_close_panel').addEventListener('submit', handleAcAction_roomState);



// 处理空调设置表单的提交
function AcSettingsAlert(event) {
    event.preventDefault();  // 阻止表单的默认提交行为

    var form = event.target;
    var formData = new FormData(form);
    var actionUrl = form.action; // 获取表单的action URL

    fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken() // 使用CSRF Token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // 根据返回的数据判断操作是否成功，并给出提示
        if (data.status === 'success') {
            alert('空调设置成功！');
        } else {
            alert('空调设置失败：' + (data.message || '未知错误'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('请求过程中发生错误！');
    });
}

// 绑定事件监听器到空调设置表单
document.getElementById('ac_temperature_control').addEventListener('submit',  AcSettingsAlert);




function updateStatus() {
    console.log('updateStatus() 函数被调用了！'); // 添加日志

    // var room_id = document.getElementById('displayRoomNumber').textContent; // 假设这个元素中存储了 room_id
    console.log('room_id:', room_id);
    var requestData = {
        room_id: room_id // 将 room_id 加入请求数据中
        // 可以添加其他需要的数据...
    };
    console.log('requestData:', requestData);
    // 使用fetch或其他AJAX方法发送请求
    fetch('/change_ac_state/', {
        method: 'POST',
        body: JSON.stringify(requestData), // 将请求数据转换为 JSON 字符串放入请求 body 中
        headers: {
            'Content-Type': 'application/json', // 指定请求 body 中的数据类型为 JSON
            'X-CSRFToken': getCsrfToken()
            // 可以添加其他请求头...
        }
    })
        .then(response => response.json())
        .then(data => {
            // 假设服务器返回的数据格式是 { cur_tem: '...', cur_wind: '...', cost: '...', sum_cost: '...', ac_status: '...' }
            document.getElementById('cur_tem').textContent = data.cur_tem;
            document.getElementById('cur_wind').textContent = data.cur_wind;
            document.getElementById('cost').textContent = data.cost;
            document.getElementById('sum_cost').textContent = data.sum_cost;

            // 更新空调状态
            document.getElementById('room_state').textContent = data.ac_status;

            // 其他更新逻辑...
        })
        .catch(error => console.error('Error:', error));
}

// 设置定时器，每秒调用一次updateStatus函数
setInterval(updateStatus, 1000);


