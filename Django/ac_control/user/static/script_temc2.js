 // 获取温度控制滑块元素
 var temperatureSlider = document.getElementById("temperature-slider");
 var temperatureValue = document.getElementById("temperature");

 // 获取风度控制滑块元素
 var fanSpeedSlider = document.getElementById("fan-speed-slider");
 var fanSpeedValue = document.getElementById("fan-speed");

 // 获取空调模式选择器元素
 var modeSelector = document.getElementById("mode-selector");

 // 获取耗电量和费用元素
 var powerConsumptionValue = document.getElementById("power-consumption");
 var costValue = document.getElementById("cost");

 // 添加事件监听器来响应滑块和选择器的变化
 temperatureSlider.addEventListener("input", function() {
     temperatureValue.innerText = temperatureSlider.value + "°C";
     // 更新耗电量和费用
     updatePowerConsumptionAndCost();
 });

 fanSpeedSlider.addEventListener("input", function() {
     var fanSpeed = fanSpeedSlider.value;
     if (fanSpeed === "1") {
         fanSpeedValue.innerText = "低风";
     } else if (fanSpeed === "2") {
         fanSpeedValue.innerText = "中风";
     } else if (fanSpeed === "3") {
         fanSpeedValue.innerText = "高风";
     }
     // 更新耗电量和费用
     //updatePowerConsumptionAndCost();
 });

 // modeSelector.addEventListener("change", function() {
 //     // 更新耗电量和费用
 //     updatePowerConsumptionAndCost();
 // });

 // // 更新耗电量和费用
 // function updatePowerConsumptionAndCost() {
 //     var temperature = parseInt(temperatureSlider.value);
 //     var fanSpeed = parseInt(fanSpeedSlider.value);
 //     var mode = modeSelector.value;

 //     // 假设简单的计算模型
 //     var powerConsumption = (temperature - 20) * 0.05 * fanSpeed;
 //     var cost = powerConsumption * 0.2; // 假设每度电费用为0.2元

 //     powerConsumptionValue.innerText = powerConsumption.toFixed(2) + " kWh";
 //     costValue.innerText = "$" + cost.toFixed(2);
 // }

 // 初始化
 //updatePowerConsumptionAndCost();

 var acToggleBtn = document.getElementById("ac-toggle");
 var acStatusText = document.getElementById("ac-status-text");
 var isACOn = false;

 function toggleAC() {
     isACOn = !isACOn;
     if (isACOn) {
         acToggleBtn.textContent = "关闭";
         acStatusText.textContent = "空调已开启";
     } else {
         acToggleBtn.textContent = "开启";
         acStatusText.textContent = "空调已关闭";
     }
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
