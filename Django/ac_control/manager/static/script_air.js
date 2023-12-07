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
    // 这里是您的刷新逻辑
    // 例如，重新请求数据并更新页面元素
  }, 1000); // 5000毫秒，即5秒
