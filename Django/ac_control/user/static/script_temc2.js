//  // 获取温度控制滑块元素
//  var temperatureSlider = document.getElementById("temperature-slider");
//  var temperatureValue = document.getElementById("temperature");

//  // 获取风度控制滑块元素
//  var fanSpeedSlider = document.getElementById("fan-speed-slider");
//  var fanSpeedValue = document.getElementById("fan-speed");

//  // 获取空调模式选择器元素
//  var modeSelector = document.getElementById("mode-selector");


//  // 获取耗电量和费用元素
//  var powerConsumptionValue = document.getElementById("power-consumption");
//  var costValue = document.getElementById("cost");
//  var acToggleBtn = document.getElementById("ac-toggle");
//  var acStatusText = document.getElementById("ac-status-text");
//  var isACOn = false;


//  temperatureSlider.addEventListener("input", function() {
//     if (isACOn) {
//         temperatureValue.innerText = temperatureSlider.value + "°C";
//     }
//     else{
//         alert('空调未开启！')
//     }
// });

// // 初始化时设置模式选择器的data-prev属性
// modeSelector.setAttribute('data-prev', modeSelector.value);

// // 监听模式选择器的变化
// modeSelector.addEventListener("change", function() {
//     if (isACOn) {
//          // 记录当前选择的模式
//         this.setAttribute('data-prev', this.value);
//     } else {

//         alert('空调未开启！');
//     }
// });


//  fanSpeedSlider.addEventListener("input", function() {
//      var fanSpeed = fanSpeedSlider.value;    
//      if (isACOn) {
//         if (fanSpeed === "1") {
//             fanSpeedValue.innerText = "低风";
//         } else if (fanSpeed === "2") {
//             fanSpeedValue.innerText = "中风";
//         } else if (fanSpeed === "3") {
//             fanSpeedValue.innerText = "高风";
//         }
//     }
//     else{
//         alert('空调未开启！')
//     }
//  });

//  function toggleAC() {
//      isACOn = !isACOn;
//      if (isACOn) {
//          acToggleBtn.textContent = "关闭";
//          acStatusText.textContent = "空调已开启";
//      } else {
//          acToggleBtn.textContent = "开启";
//          acStatusText.textContent = "空调已关闭";
//      }
//  }


//  function submitForm() {
//     alert('空调状态已设置!');
//     return true;
// }

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
disableControls();

temperatureSlider.addEventListener("input", function () {
    if (isACOn) {
        temperatureValue.innerText = temperatureSlider.value + "°C";
    } else {
        this.value = temperatureValue.innerText.slice(0, -2); // 重置滑块
        alert('空调未开启！');
    }
});

fanSpeedSlider.addEventListener("input", function () {
    if (isACOn) {
        var fanSpeed = fanSpeedSlider.value;
        fanSpeedValue.innerText = fanSpeed === "1" ? "低风" : fanSpeed === "2" ? "中风" : "高风";
    } else {
        this.value = fanSpeedValue.innerText === "低风" ? "1" : fanSpeedValue.innerText === "中风" ? "2" : "3"; // 重置滑块
        alert('空调未开启！');
    }
});

modeSelector.addEventListener("change", function () {
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
    isACOn = !isACOn;
    if (isACOn) {
        acToggleBtn.textContent = "关闭";
        acStatusText.textContent = "空调已开启";
        enableControls();

    } else {
        acToggleBtn.textContent = "开启";
        acStatusText.textContent = "空调已关闭";
        disableControls();
    }
}

function submitForm() {
    if (isACOn) {
        alert('空调状态已设置!');
        return true;
    } else {
        alert('请先开启空调!');
        return false;
    }
}


//退房函数
document.getElementById('checkout').addEventListener('click', function (event) {
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
