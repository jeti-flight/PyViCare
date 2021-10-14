

# slider

## 效果演示

![slider](https://github.com/mklls/slider/raw/master/screenshot/slider.gif)

## 快速开始 

### 安装

#### 手动下载

你可以点击[这里](https://github.com/mklls/slider/archive/master.zip)下载
然后解压到你的html所在目录
#### 直接下载

```bash
#克隆仓库
git clone git@github.com:mklls/slider.git
#切换目录
cd slider
#编写代码
```

### 如何使用

```HTML
<head>
  <!-- 引入jquery -->
  <script src="./jQuery3.1.1.js"></script>
  <!-- 引入Slider -->
  <script src="./Slider.js"></script>
  <!-- 将 body 撑满浏览器的可视区域-->
  <style>
      body {
        width: 100%;
        height: 100%;
      }
  </style>
</head>
<body>
  <main class="container">
    <!-- 在此处编写你的Html -->
    <div id="slider1" class="silder-wrap"></div>
    <div class="status"></div>
  </main>
  <!-- 在最底部引入你的javascript -->
  <script src="./tutorial.js"></script>
</body>
```

```javascript
/* 你的javascript文件 tutorial.js*/
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
//添加回调函数
slider.valueChanged = function(value) {
  status.innerHTML = "你松开了鼠标当前值: " + slider.Duration*value;
}
slider.valueChanging = function(value) {
  status.innerHTML = "你正在拖动进度条，当前值: " + slider.Duration*value;
}

```

## API

#### `new Slider({object})`

- `Duration` Number (必填参数) - 滑动条滑到最右侧时所代表的值(最大值)

- `width` String (可选参数) - 滑动条的宽度 ，需要填写css单位，可以是 `vw px % em` 诸如此类。缺省值 `600px`
- `height` String (可选参数) - 滑动条的高度，需要填写css单位，可以是 `vw px % em` 诸如此类。缺省值 `3px`
- `backgroundColor` String (可选参数) - 未滑过的的背景色。缺省值 ![#D3D3D3](https://placehold.it/15/D3D3D3/000000?text=+) lightgrey
- `barColor` String (可选参数) - 已滑过的背景色。缺省值 ![#FF1493](https://placehold.it/15/FF1493/000000?text=+) deeppink
- `hasBall` Boolean (可选参数) - 是否在已经滑过部分右侧添加圆形滑块。缺省值 `true`
- `ballColor` String (可选参数) - 滑块的颜色。缺省值 ![#29AFFF](https://placehold.it/15/29AFFF/000000?text=+) #29AFFF
- `ballRadius ` String (可选参数) - 滑块的直径(反正没人用，我就不改名称了)。 缺省值 `1.5 * height`
- `scale` Number (可选参数) - 滑动时滑块的缩放倍数。 缺省值 `2`
- `alwayShowBall` Boolean  (可选参数)  - 总是显示滑块。缺省XD值 `false`
- `formatProgress` Boolean (可选参数) - 是否在滑动条两侧分别显示当前值和最大值。缺省值 `false`
- `hasIndicator` Boolean (可选参数) - 是否在滑动条上方显示当前值指示器。缺省值 `true`
- `indicatorColor` String (可选参数) - 指示器颜色。缺省值 ![#778899](https://placehold.it/15/778899/000000?text=+) #778899
- `indicatorTextColor` String (可选参数) - 指示器文本颜色。缺省值 ![#000000](https://placehold.it/15/000000/000000?text=+) black
- ` format` Number(可选参数) - 指示器和两侧数值的格式。 缺省值 `0`
  - `0` -  `m:ss`
  - `1` - `纯数字`

#### `setCurrent(progress)`

- `progress` Number 大小为 `0~1` 设置当前滑块指向的值。



#### `setDuration(duration)`

- `duratoin ` Number 设置滑块滑倒最右侧时的值。



#### `getSlider()`

- 返回滑动条的 DOM 对象



#### `valueChanging(value)`

- `value` Number  介于 0 ~ 1 的小数

> 用鼠标拖动滑动条时执行的回调函数 



#### `valueChanged(progress)`

- progresss Number  介于 0 ~ 1 的小数

> 鼠标结束拖动过程松开时执行的回调函数
