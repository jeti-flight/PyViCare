/*
 * @Author: mkll
 * @Date: 2019-11-03 11:19:29
 * @LastEditors: mkll
 * @LastEditTime: 2019-11-03 17:06:41
 * @Description: 昨晚居然没有失眠，蛤蛤，通宵了:(
 * @See: 
 */
// 创建 slider 对象
let slider1 = new Slider({
  Duration: 410,
  hasIndicator: false,
  ballRadius: '20px'
});

let slider2 = new Slider({
  Duration: 322,
  backgroundColor: 'rgb(203, 255, 251)',
  barColor: 'blueviolet',
  height:'6px',
  hasBall: true,
  hasIndicator: true,
  ballRadius: '15px',
  scale:'2',
  formatProgress: true,
});

let slider3 = new Slider({
  Duration: 123,
  backgroundColor: 'rgb(203, 25, 251)',
  barColor: 'blueviolet',
  height: '2px',
  hasBall: true,
  hasIndicator: true,
  ballRadius: '20px',
  scale: '2',
  formatProgress: true,
  alwayShowBall: true,
  format: 1
});


$('#slider1').append(slider1.getSlider());
$('#slider2').append(slider2.getSlider());
$('#slider3').append(slider3.getSlider());