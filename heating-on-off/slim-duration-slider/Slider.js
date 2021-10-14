/*
 * @Author: mkll
 * @Date: 2019-10-28 16:15:02
 * @LastEditors: mkll
 * @LastEditTime: 2019-11-14 20:46:38
 * @Description: 昨晚居然没有失眠，蛤蛤，通宵了:(
 * @See: 
 */
'use strict'

/**
 * @description
 * @author mkll
 * @date 2019-11-01
 * @class DraggableProgressbar
 * @param 
 */
class Slider {
  constructor({
    width, height, backgroundColor, barColor, scale, Duration, 
    formatProgress=false, alwayShowBall=false, hasBall=true, hasIndicator=true,
    ballColor, ballRadius, format, indicatorColor, indicatorTextColor
  }) {
    if(typeof Duration !== 'number') throw 'error : expected Duration';
    this.type = format || 0;
    this.formatProgress = formatProgress;
    this.width = width || '600px';
    this.height = height || '3px';
    this.alwayShowBall = alwayShowBall;
    this.hasIndicator = hasIndicator;
    this.indicatorColor = indicatorColor || '#778899';
    this.indicatorTextColor = indicatorTextColor || 'black';
    this.hasBall = hasBall;
    this.valueChanging = function(){};
    this.valueChanged = function(){};
    this.backgroundColor = backgroundColor || 'lightgrey';
    this.barColor = barColor || 'deeppink';
    if (this.hasBall) {
      this.ballColor = ballColor ||'#29AFFF';
      this.ballRadius = ballRadius || parseFloat(this.height)*1.5;
      this.scale = scale || 2;
    } else {
      this.ballColor = 'transparent';
      this.ballRadius = 0;
      this.scale = 0;
    }
    this.Duration = Duration;
    this.pressDown = false;
  };

  initSlider() {
    this.progressbar = $(`<div class='progressbar'></div>`);
    this.bar = $(`<div class='bar'></div>`);
    this.slider = $(`<div class="slider"></div>`);
    this.slider.css('userSelect','none');
    this.progressbar.css({
      width: '100%',
      height: this.height,
      background: this.backgroundColor,
      position: 'relative',
      '-moz-user-select': 'none',
      '-ms-user-select': 'none',
      '-webkit-user-select': 'none',
      userSelect: 'none',
      borderTop:'10px solid transparent',
      borderBottom: '10px solid transparent',
      backgroundClip: 'padding-box',
      transition: '0.1s',
      display: 'inline-block',
    });

    this.bar.css({
      width: '50px',
      height: 'inherit',
      background: this.barColor,
      transition: '0.1s',
    });
    
    this.slider.css({
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      flexFlow: 'row nowrap'
    });
    this.bar.appendTo(this.progressbar);

    if (this.formatProgress) {
      this.currentTime = $(`<div class="current-time"></div>`);
      this.duration = $(`<div class="duration"></div>`);

      this.currentTime
        .css({
          paddingRight: '8px',
        });

      this.duration
        .css({
          paddingLeft: '8px',
        });
      
      this.currentTime.text(this.format(0));
      this.duration.text(this.format(this.Duration));
      this.slider.append(this.currentTime);
      this.slider.append(this.duration);
    }

    this.slider.css('width', this.width);

    this.formatProgress 
      ? this.progressbar.insertAfter(this.currentTime)
      : this.slider.append(this.progressbar);
    
  }

  initBall() {
    this.ball =  $(`<div class="ball"></div>`);
    this.ball.css({
      width: this.ballRadius,
      height: this.ballRadius,
      background: this.ballColor,
      borderRadius: '50%',
      position: 'relative',
      left: `calc(100% - ${parseFloat(this.ballRadius) / 2}px)`,
      top: `-${(parseFloat(this.ballRadius) - parseFloat(this.height)) / 2}px`,
      transform: 'scale(1)',
      transition:'all 0.1s',
      zIndex: 3
    });
    this.alwayShowBall
      ? this.ball.css('opacity', 1)
      : this.ball.css('opacity', 0);
    this.ball.appendTo(this.bar);
  }

  initIndicator() {
    let offset = parseFloat(this.ballRadius)*(this.scale-0.5);
    this.indicatorValue = $('<span><span>');
    this.valueIndicator = $(`<div class="value-indicator"></div>`);
    this.valueIndicator.css({
      width: '30px',
      height: '30px',
      borderRadius: '50% 50% 0 50%',
      transform: 'rotate(45deg) scale(0)',
      background: this.indicatorColor,
      position: 'relative',
      left: `calc(100% - 30px)`,
      top: `-${40 + offset}px`,
      transformOrigin: 'bottom right',
      transition: 'all 0.3s',
      zIndex: 999,
    });
    this.indicatorValue.css({
      transform: 'rotate(-45deg)',
      position: 'absolute',
      color: this.indicatorTextColor,
      width: '100%',
      height: '100%',
      lineHeight: '30px',
      textAlign: 'center',
      fontSize: '13px',
    });
    this.indicatorValue.appendTo(this.valueIndicator);
    this.valueIndicator.appendTo(this.bar);
  }

  registerEvent() {
    this.pressDown = false;
    if (this.formatProgress) {
      this.currentTime.on('mouseup mousedown mouseover', event => event.stopPropagation());
      this.duration.on('mouseup mousedown mouseover', event => event.stopPropagation());
    }
    this.ball && this.ball.on({
      mouseover: event => event.stopPropagation(),
      mouseup: event => {
        event.stopPropagation();
        this.pressDown = false;
        this.ball.css('transform', `scale(1)`);
        this.hasIndicator && this.valueIndicator.css('transform', 'rotate(45deg) scale(0)');
        let progress = this.getPercent(event);
        this.valueChanged && this.valueChanged(progress);
      },
      mousedown: event => {
        event.stopPropagation();
        this.pressDown = true;
        let progress = this.getPercent(event);
        this.bar.css({width:`${progress*100}%`});
        this.ball && this.ball.css('transform', `scale(${this.scale})`);
        this.hasIndicator && this.valueIndicator.css('transform', 'rotate(45deg) scale(1)');
        this.hasIndicator && this.indicatorValue.text(this.format(this.Duration*progress));
        this.hasIndicator && this.indicatorValue.text(this.format(this.Duration*progress));
      },
      mouseleave: () => {
        !this.pressDown && this.ball.css('transform', `scale(1)`);
      }
    });
    this.progressbar.on({
      mouseover: () => {
        event.stopPropagation();
        this.ball && this.ball.css('opacity', 1);
      },
      mouseleave: () => {
        this.ball && this.alwayShowBall || !this.pressDown && this.ball.css('opacity', 0);
      },
      mouseup: () => {
        this.pressDown = false;
        let current = parseFloat(this.bar.css('width'));
        let total = parseFloat(this.progressbar.css('width'));
        let progress = current/total;
        this.bar.css('width', `${progress*100}%`);
        this.ball && this.ball.css('transform', `scale(1)`);
        this.ball && !this.alwayShowBall && this.ball.css('opacity', '0');
        this.formatProgress && this.currentTime.text(this.format(this.Duration*progress));
        this.hasIndicator && this.indicatorValue.text(this.format(this.Duration*progress));
        this.hasIndicator && this.valueIndicator.css('transform', 'rotate(45deg) scale(0)');
        this.valueChanged && this.valueChanged(progress);
      },
      mousedown: (event) => {
        event.stopPropagation();
        this.pressDown = true;
        this.bar.css('width', `${event.offsetX}px`);
        this.ball && this.ball.css('transform', `scale(${this.scale})`);
        this.hasIndicator && this.valueIndicator.css('transform', 'rotate(45deg) scale(1)');
        
        !this.alwayShowBall && this.ball && this.ball.css('opacity', 1);
      },
      mousemove: (event) => {
        event.stopPropagation();
        if (!this.pressDown) return;
        let progress = this.getPercent(event);
        this.bar.css({width:`${progress*100}%`});
        this.formatProgress && this.currentTime.text(this.format(this.Duration*progress));
        this.hasIndicator && this.indicatorValue.text(this.format(this.Duration*progress));
        this.valueChanging && this.valueChanging(progress);
      }
    });
    $('body').on({
      mouseup: () => {
        if (!this.pressDown) return;
        this.pressDown = false;
        let current = parseFloat(this.bar.css('width'));
        let total = parseFloat(this.progressbar.css('width'));
        let progress = current/total;
        this.bar.css('width', `${progress*100}%`);
        this.ball && this.ball.css('transform', `scale(1)`);
        this.ball && !this.alwayShowBall && this.ball.css('opacity', 0);
        this.hasIndicator && this.valueIndicator.css('transform', 'rotate(45deg) scale(0)');
        this.valueChanged && this.valueChanged(progress);
      },
      mousemove: event => {
        if(!this.pressDown) return;
        let progress = this.getPercent(event);
        this.bar.css({width:`${progress*100}%`});
        this.formatProgress && this.currentTime.text(this.format(this.Duration*progress));
        this.hasIndicator && this.indicatorValue.text(this.format(this.Duration*progress));
        this.valueChanging && this.valueChanging(progress);
      }
    });
  }
  format(duration) {
    let hour = Math.floor(duration / 3600);
    let min = Math.floor(duration / 60);
    let sec = Math.round(duration % 60);
    let ret = "";
    if (hour >= 1) {
      min -= 60;
      ret += hour + ":";
    }
  
    hour >= 1 && min < 10 ?
      ret += '0' + min + ":" :
      ret += min + ":";

    sec < 10 ? ret += "0" + sec
             : ret += sec;
    
    return ret;
  }
  setCurrent(progress) {
    if (typeof progress !== 'number') 
      throw 'expected a number';
    if (progress > 1 || progress < 0) 
      throw 'parameter should range from 0 to 1';
    this.bar.css('width', `${progress*100}%`);
  }
  setDuration(duration) {
    if (typeof duration !== 'number') 
      throw 'expected a number';
    this.duration = duration;
  }
  getPercent(event) {
    let offsetX = this.progressbar.offset().left;
    let total = parseFloat(this.progressbar.css('width'));
    let progress = (event.pageX-offsetX)/total;
    progress < 0 && (progress = 0);
    progress > 1 && (progress = 1);
    return progress;
  }
  getSlider() {
    this.initSlider();
    this.setCurrent(0);
    this.hasBall && this.initBall();
    this.hasIndicator && this.initIndicator();
    this.registerEvent();
    return this.slider;
  }
}
// LIST TO DO
// 修复指示器bug
// commit push、
