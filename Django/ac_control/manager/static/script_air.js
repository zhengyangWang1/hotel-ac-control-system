function hideAllTabs() {
    var tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
}

// 在页面加载时隐藏所有选项卡内容
window.onload = hideAllTabs;


function openCity(evt, cityName) {
    // 声明所有变量
    var i, tabcontent, tablinks;
  
    // 使用 class="tabcontent" 获取所有元素并隐藏它们
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
     // 获取所有带有 class="tablinks" 的元素并删除类 "active"
   tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // 显示当前选项卡，并将 "active" 类添加到打开选项卡的链接
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }


  function viewDetails(roomId) {
    var button = document.querySelector(`button[onclick="viewDetails('${roomId}')"]`);
    var detailsRow = button.parentNode.parentNode.nextElementSibling;
    if (detailsRow && detailsRow.classList.contains('details')) {
        // 如果已经存在详情行，则移除它
        detailsRow.remove();
    } else {
        // 创建一个包含详情的新行
        var newDetailsRow = document.createElement('tr');
        newDetailsRow.classList.add('details');
        newDetailsRow.innerHTML = `
        <td colspan="6">
        <div>空调操作记录 #${roomId}</div>
        <table class="table">
            <thead>
                <tr>
                    <th>时间</th>
                    <th>操作</th>
                    <th>费用</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>2023-11-20</td>
                    <td>开启</td>
                    <td>¥5</td>
                </tr>
                <tr>
                    <td>2023-11-21</td>
                    <td>调节温度</td>
                    <td>¥3</td>
                </tr>
                <!-- 更多记录 -->
            </tbody>
        </table>
    </td>
    
        `;
        // 将新行插入表格
        button.parentNode.parentNode.parentNode.insertBefore(newDetailsRow, button.parentNode.parentNode.nextSibling);
    }
}

setInterval(function() {
    location.reload();
  }, 3000); // 1000 毫秒，即每隔1秒
  

// function updateRoomStatus() {
//     fetch('/monitor-api')  // 替换为您的API端点
//         .then(response => response.json())
//         .then(data => {
//             const status = data.status;
//             let tbodyHTML = '';
//             for (const room_id in status) {
//                 const s = status[room_id];
//                 tbodyHTML += `<tr>
//                                 <td>${room_id}</td>
//                                 <td>${s.air_condition}</td>
//                                 <td>${s.cur_tem}</td>
//                                 <td>${s.target_tem}</td>
//                                 <td>${s.cur_wind}</td>
//                                 <td>制热</td> <!-- 假设模式也是状态的一部分 -->
//                                 <td>
//                                     <button class="button-primary">维修</button>
//                                     <!-- 可以添加其他按钮或操作 -->
//                                 </td>
//                               </tr>`;
//             }
//             document.querySelector('tbody').innerHTML = tbodyHTML;
//         })
//         .catch(error => console.error('Error:', error));
// }

// // 每隔一定时间（比如每秒）更新房间状态
// setInterval(updateRoomStatus, 1000); // 每1000毫秒（1秒）执行一次