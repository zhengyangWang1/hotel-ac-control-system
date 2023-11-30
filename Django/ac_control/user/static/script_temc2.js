var temperatureSlider = document.getElementById("temperature-slider");
var temperatureValue = document.getElementById("temperature");
var fanSpeedSlider = document.getElementById("fan-speed-slider");
var fanSpeedValue = document.getElementById("fan-speed");
var modeSelector = document.getElementById("mode-selector");
var acToggleBtn = document.getElementById("ac-toggle");
var acStatusText = document.getElementById("ac-status-text");
var isACOn = false;

// 禁用控件
function disableControls() {
    temperatureSlider.disabled = true;
    fanSpeedSlider.disabled = true;
    modeSelector.disabled = true;
}

// 启用控件
function enableControls() {
    temperatureSlider.disabled = false;
    fanSpeedSlider.disabled = false;
    modeSelector.disabled = false;
}

// 初始化禁用控件
// disableControls();

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

// function toggleAC() {
//     isACOn = !isACOn;
//     if (isACOn) {
//         acToggleBtn.textContent = "关闭";
//         acStatusText.textContent = "空调已开启";
//         enableControls();
//     } else {
//         acToggleBtn.textContent = "开启";
//         acStatusText.textContent = "空调已关闭";
//         disableControls();
//     }
// }

// function submitForm() {
//     if (isACOn) {
//         alert('空调状态已设置!');
//         return true;
//     } else {
//         alert('请先开启空调!');
//         return false;
//     }
// }



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
