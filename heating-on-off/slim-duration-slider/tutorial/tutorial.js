/*
 * @Author: mkll
 * @Date: 2019-11-03 16:29:10
 * @LastEditors: mkll
 * @LastEditTime: 2019-11-03 18:26:22
 * @Description: 昨晚居然没有失眠，蛤蛤，通宵了:(
 * @See: 
 */
/* 你的javascript文件 */
// 创建 slider 对象
let slider = new Slider({
  Duration: 410,
  hasIndicator: false,
  ballRadius: '20px'
});
// 获取要添加 Slider 的标签
let wrap = document.getElementById('slider1');
// 获取 Slider DOM 对象
let s = slider.getSlider().get(0);
// 添加 Slider DOM 对象
wrap.appendChild(s);

let status = document.getElementsByClassName('status')[0];
slider.valueChanged = function(value) {
  status.innerHTML = "你松开了鼠标当前值: " + slider.Duration*value;
}
slider.valueChanging = function(value) {
  status.innerHTML = "你正在拖动进度条，当前值: " + slider.Duration*value;
}
